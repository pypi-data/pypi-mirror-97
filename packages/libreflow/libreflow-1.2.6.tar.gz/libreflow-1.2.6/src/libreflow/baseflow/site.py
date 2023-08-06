import os
import sys
import gazu
import time
import datetime
import subprocess
import platform
from minio import Minio
import zipfile

from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict
from kabaret.subprocess_manager.flow import RunAction

from .maputils import ItemMap, CreateGenericAction, ClearMapAction, RemoveGenericAction
from libreflow.baseflow.runners import BaseRunner, PythonRunner


class StaticSiteTypeChoices(flow.values.ChoiceValue):
    CHOICES = ['Studio', 'User', 'Exchange']


class StaticSiteSyncStatusChoices(flow.values.ChoiceValue):
    CHOICES = ['NotAvailable', 'Requested', 'Available']


class StaticSiteSyncTransferStateChoices(flow.values.ChoiceValue):
    CHOICES = ['NC', 'UP_REQUESTED', 'DL_REQUESTED', 'UP_IN_PROGRESS', 'DL_IN_PROGRESS']


class LoadType(flow.values.ChoiceValue):

    CHOICES = ['Upload', 'Download']


class JobStatus(flow.values.ChoiceValue):

    CHOICES = ['WFA', 'WAITING', 'PROCESSED', 'ERROR', 'PAUSE', 'DONE']


class Job(flow.Object):

    type = flow.Param('Download', LoadType)
    status = flow.Param('WAITING', JobStatus)
    priority = flow.IntParam(50)
    emitter_oid = flow.Param()
    date = flow.Param().ui(editor='datetime')
    date_end = flow.Param("").ui(editor='datetime')
    is_archived = flow.BoolParam()
    requested_by_user = flow.Param()
    requested_by_studio = flow.Param()
    log = flow.Param().ui(editor='textarea')

    def __repr__(self):
        job_repr = "%s(type=%s, status=%s, priority=%s, emitter=%s, date=%s, date_end=%s, is_archived=%s, requested_by_user=%s, requested_by_studio=%s)" % (
                self.__class__.__name__,
                self.type.get(),
                self.status.get(),
                self.priority.get(),
                self.emitter_oid.get(),
                self.date.get(),
                self.date_end.get(),
                self.is_archived.get(),
                self.requested_by_user.get(),
                self.requested_by_studio.get()
            )

        return job_repr


class ClearQueueAction(flow.Action):

    _queue = flow.Parent()

    def needs_dialog(self):
        return False
    
    def run(self, button):
        self._queue.clear()
        self._queue.touch()


class JobQueue(flow.Map):

    @classmethod
    def mapped_type(cls):
        return Job
    
    def get_next_waiting_job(self):
        for job in reversed(self.mapped_items()):
            if job.status.get() == "WAITING":
                return job
        
        return None
    
    def jobs(self, type=None, status=None):
        jobs = self.mapped_items()

        if type:
            jobs = list(filter(lambda job: job.type.get() == type, jobs))
        if status:
            jobs = list(filter(lambda job: job.status.get() == status, jobs))
        
        return jobs
    
    def insert(self, name, priority=0):
        """
        Inserts a new job with given name and priority.
        """
        job = self.add(name)
        self._mapped_names.set_score(name, priority)

        return job
    
    def submit_job(self,
            emitter_oid,
            user,
            studio,
            date_end=None,
            job_type='Download',
            init_status='WAITING',
            priority=50
        ):
        
        name = '%s_%s_%s_%i' % (
            emitter_oid[1:].replace('/', '_'),
            studio,
            job_type,
            time.time()
        )
        job = self.insert(name, priority)

        self.root().session().log_info("Submitted job %s" % job)

        job.type.set(job_type)
        job.status.set(init_status)
        job.priority.set(priority)
        job.emitter_oid.set(emitter_oid)
        job.date.set(datetime.datetime.fromtimestamp(time.time()).ctime())
        job.date_end.set(date_end)
        job.requested_by_user.set(user)
        job.requested_by_studio.set(studio)
        job.is_archived.set(False)
        job.log.set('?')

        self.touch()

        return job
    
    def columns(self):
        return [
            "Type",
            "Status",
            "Priority",
            "Emitted on",
            "Expires on",
            "Requested by (site/user)",
        ]
    
    def _fill_row_cells(self, row, item):
        row["Type"] = item.type.get()
        row["Status"] = item.status.get()
        row["Priority"] = item.priority.get()
        row["Emitted on"] = item.date.get()
        row["Expires on"] = item.date_end.get()
        row["Requested by (site/user)"] = "%s/%s" % (
            item.requested_by_studio.get(),
            item.requested_by_user.get()
        )


class ProcessJobs(flow.Action):

    def needs_dialog(self):
        return False

    def _process(self, job):
        raise NotImplementedError(
            "Must be implemented to process the given job"
        )
    
    def _get_jobs(self):
        current_site = self.root().project().get_current_site()
        return current_site.queue.jobs()
    
    def run(self, button):
        for job in self._get_jobs():
            self.root().session().log_info("Processing job %s" % job)
            self._process(job)


class MinioFileUploader(PythonRunner):
    
    def argv(self):
        args = ["%s/../scripts/minio_file_uploader.py" % (
            os.path.dirname(__file__)
        )]
        args += self.extra_argv
        return args


class MinioFileDownloader(PythonRunner):
    
    def argv(self):
        args = ["%s/../scripts/minio_file_downloader.py" % (
            os.path.dirname(__file__)
        )]
        args += self.extra_argv
        return args


class MinioUploadFile(flow.Object):

    def upload(self, local_path, server_path):
        self.root().session().log_info(
            "Uploading file %s -> %s" % (
                local_path,
                server_path
            )
        )
        current_site = self.root().project().get_current_site()
        minioClient = Minio(
            current_site.exchange_server_url.get(),
            access_key=current_site.exchange_server_login.get(),
            secret_key=current_site.exchange_server_password.get(),
            secure=True
        )

        minioClient.fput_object(
            "testbucked",
            server_path,
            local_path
        )


class MinioDownloadFile(flow.Object):

    def download(self, server_path, local_path):
        self.root().session().log_info(
            "Downloading file %s -> %s" % (
                server_path,
                local_path
            )
        )
        current_site = self.root().project().get_current_site()
        minioClient = Minio(
            current_site.exchange_server_url.get(),
            access_key=current_site.exchange_server_login.get(),
            secret_key=current_site.exchange_server_password.get(),
            secure=True
        )

        minioClient.fget_object(
            "testbucked",
            server_path,
            local_path
        )

        if os.path.splitext(local_path)[1] == ".zip":
            # Unzip
            with zipfile.ZipFile(local_path, 'r') as zip_wc:
                zip_wc.extractall(os.path.dirname(local_path))


class Synchronize(ProcessJobs):

    uploader = flow.Child(MinioUploadFile).ui(hidden=True)
    downloader = flow.Child(MinioDownloadFile).ui(hidden=True)

    def _get_jobs(self):
        # Get current site's waiting jobs only
        current_site = self.root().project().get_current_site()
        return current_site.queue.jobs(status="WAITING")

    def _get_sync_status(self, revision_oid, site_name=None, site_type="Studio"):
        if not site_name and site_type == "Exchange":
            exchange_site = self.root().project().get_exchange_site()
            if exchange_site:
                site_name = exchange_site.name()
            else:
                return "NotAvailable"

        sync_status = self.root().session().cmds.Flow.call(
            revision_oid, "get_sync_status",
            args={}, kwargs=dict(site_name=site_name)
        )
        return sync_status

    def _set_sync_status(self, revision_oid, status, site_name=None, site_type="Studio"):
        if not site_name and site_type == "Exchange":
            exchange_site = self.root().project().get_exchange_site()
            if exchange_site:
                site_name = exchange_site.name()
            else:
                self.root().session().log_error(
                    "No registered exchange site on this project !"
                )
                return

        self.root().session().cmds.Flow.call(
            revision_oid, "set_sync_status",
            args={status}, kwargs=dict(site_name=site_name)
        )
    
    def _touch(self, oid):
        oid = self.root().session().cmds.Flow.resolve_path(oid)
        self.root().session().cmds.Flow.call(
            oid, "touch", args={}, kwargs={}
        )

    def _process(self, job):
        if job.status.get() == "PROCESSED":
            self.root().session().log_warning(
                "Job %s already processed !" % job.name()
            )
            return

        local_path = self.root().session().cmds.Flow.call(
            job.emitter_oid.get(),
            "get_path",
            args={},
            kwargs={}
        )
        server_path = self.root().session().cmds.Flow.call(
            job.emitter_oid.get(),
            "get_relative_path",
            args={},
            kwargs={}
        )
        local_path = local_path.replace("\\", "/")
        server_path = server_path.replace("\\", "/")

        if job.type.get() == "Upload":
            if not os.path.exists(local_path):
                self.root().session().log_error((
                    "Following file requested for upload but does not exist !"
                    "\n>>>>> %s" % local_path
                ))
                return

            self.uploader.upload(local_path, server_path)
            self._set_sync_status(job.emitter_oid.get(), "Available", site_type="Exchange")
        elif job.type.get() == "Download":
            sync_status = self._get_sync_status(job.emitter_oid.get(), site_type="Exchange")
            
            if sync_status != "Available":
                self.root().session().log_error((
                    "Following file requested for download "
                    "but not available on any exchange server !"
                    "\n>>>>> %s" % local_path
                ))
                return

            self.downloader.download(server_path, local_path)
            self._set_sync_status(job.emitter_oid.get(), "Available")
            self._touch(job.emitter_oid.get() + "/..")
        
        job.status.set("PROCESSED")
        
        # Refresh project's sync section UI
        self.root().project().synchronization.touch()


class RequestedSiteChoiceValue(flow.values.ChoiceValue):
    _revision = flow.Parent(2)

    def choices(self):
        site_names = []
        
        for site in self._revision.sync.mapped_items():
            if site.status.get() == "Available":
                site_names.append(site.name())
        
        return site_names


class RequestingSiteChoiceValue(flow.values.ChoiceValue):
    _revision = flow.Parent(2)

    def choices(self):
        site_names = []
        
        for site in self._revision.sync.mapped_items():
            if site.status.get() == "NotAvailable":
                site_names.append(site.name())
        
        return site_names


class RequestAs(flow.Action):

    _revision = flow.Parent()
    priority = flow.IntParam(50)
    requesting_site_name = flow.Param(None, RequestingSiteChoiceValue).ui(label="Requesting site")
    requested_site_name = flow.Param(None, RequestedSiteChoiceValue).ui(label="Site to query")

    def get_buttons(self):
        site_names = self.requested_site_name.choices()
        # Actually, an existing revision implies there is at least one
        # site on which it is available, which is the source site
        self.requested_site_name.set(site_names[0])

        return ["Request", "Cancel"]
    
    def allow_context(self, context):
        return (
            context
            and not self._revision.is_working_copy()
            and self.root().project().get_current_site().request_files_from_anywhere.get()
        )

    def run(self, button):
        if button == "Cancel":
            return
        
        requesting_site_name = self.requesting_site_name.get()

        # Get requesting and requested sites
        sites = self.root().project().admin.sites
        requested_site = sites[self.requested_site_name.get()]
        requesting_site = sites[requesting_site_name]
        
        # Add a download job for the requesting site
        requesting_site.queue.submit_job(
            job_type="Download",
            init_status="WAITING",
            emitter_oid=self._revision.oid(),
            user=self.root().project().get_user(),
            studio=requesting_site_name,
            priority=self.priority.get(),
        )
        self._revision.set_sync_status("Requested", site_name=requesting_site_name)
        self._revision._revisions.touch()
        
        # Check if the version is not available on the exchange server
        for site_name in self._revision.sync.mapped_names():
            site = sites[site_name]
            site_status = self._revision.sync[site_name]

            if site.site_type.get() == "Exchange" and site_status.status.get() == "Available":
                self.root().session().log_warning(
                    "Revision already available on exchange server"
                )
                self.root().project().synchronization.touch()
                return self.get_result()
            
        # Check if the source version upload is not already requested
        for job in requested_site.queue.jobs(type="Upload", status="WAITING"):
            if job.emitter_oid.get() == self._revision.oid():
                self.root().session().log_warning(
                    "Revision already requested for upload in source site"
                )
                self.root().project().synchronization.touch()
                return self.get_result()
        
        # Add an upload job for the requested site
        requested_site.queue.submit_job(
            job_type="Upload",
            init_status="WAITING",
            emitter_oid=self._revision.oid(),
            user=self.root().project().get_user(),
            studio=requesting_site_name,
            priority=self.priority.get(),
        )

        # Refresh project's sync section UI
        self.root().project().synchronization.touch()


class Request(RequestAs):

    _revision = flow.Parent()
    priority = flow.IntParam(50)
    requesting_site_name = flow.Param("").ui(hidden=True)

    def get_buttons(self):
        self.requesting_site_name.set(
            self.root().project().admin.current_site_name.get()
        )

        return super(Request, self).get_buttons()
    
    def allow_context(self, context):
        return (
            context
            and not self._revision.is_working_copy()
            and not self._revision.get_sync_status() == "Available"
        )


class ResetJobStatuses(flow.Action):
    _site = flow.Parent()
    status = flow.Param("WAITING", JobStatus)

    def run(self, button):
        for job in self._site.queue.mapped_items():
            job.status.set(self.status.get())
        
        self._site.queue.touch()


class ClearQueue(flow.Action):
    _site = flow.Parent()

    def needs_dialog(self):
        return False
    
    def run(self, button):
        self._site.queue.clear()
        self._site.queue.touch()


class Site(flow.Object):
    short_name = flow.Param("")
    description = flow.Param("")
    request_files_from_anywhere = flow.BoolParam(False).ui(tooltip="Allowed to request files for any site")

    site_type = flow.Param("Studio", StaticSiteTypeChoices)

    exchange_server_url = flow.Param("http://")
    exchange_server_login = flow.Param("")
    exchange_server_password = flow.Param("").ui(editor='password')

    root_folder = flow.Computed(cached=True)
    root_windows_folder = flow.Param()
    root_linux_folder = flow.Param()
    root_darwin_folder = flow.Param()
    
    sync_dl_max_connections = flow.IntParam(1)
    sync_up_max_connections = flow.IntParam(1)

    queue = flow.Child(JobQueue).ui(expanded=True)

    remove_site = flow.Child(RemoveGenericAction)
    reset_statuses = flow.Child(ResetJobStatuses)
    clear_queue = flow.Child(ClearQueue)

    def compute_child_value(self, child_value):
        if child_value is self.root_folder:
            root_dir = None
            # Get the operative system
            _os = platform.system()
            if _os == "Linux":
                root_dir = self.root_linux_folder.get()
            elif _os == "Windows":
                root_dir = self.root_windows_folder.get()
            elif _os == "Darwin":
                root_dir = self.root_darwin_folder.get()
            else:
                print("ERROR: Unrecognized operative system ?")
            
            if not root_dir or not os.path.exists(root_dir):
                print("WARNING: ROOT_DIR path DOES NOT EXISTS")

            child_value.set(root_dir)


class Sites(ItemMap):
    ICON = ('icons.gui', 'home')

    create_site = flow.Child(CreateGenericAction)

    def mapped_names(self, page_num=0, page_size=None):
        return ["default"] + super(Sites, self).mapped_names(page_num, page_size)
    
    def short_names(self):
        return [s.short_name.get() for s in self.mapped_items()]

    def _configure_child(self, child):
        if child.name() == "default":
            child.description.set("default_value")
            child.site_type.set("Studio")

    def _get_mapped_item_type(self, mapped_name):
        if mapped_name == "default":
            return self.mapped_type()

        return super(Sites, self)._get_mapped_item_type(mapped_name)

    @classmethod
    def mapped_type(cls):
        return Site

    def columns(self):
        return ['Name', 'Waiting jobs (upload)', 'Waiting jobs (download)']

    def _fill_row_cells(self, row, item):
        row['Name'] = item.name()
        row['Waiting jobs (upload)'] = len(item.queue.jobs(type="Upload", status="WAITING"))
        row['Waiting jobs (download)'] = len(item.queue.jobs(type="Download", status="WAITING"))

    def _fill_row_style(self, style, item, row):
        if item.site_type.get() == "User":
            style['icon'] = ('icons.gui', 'user')
        elif item.site_type.get() == "Studio":
            style['icon'] = ('icons.gui', 'home')
        elif item.site_type.get() == "Exchange":
            style['icon'] = ('icons.gui', 'sitemap')
        else:
            style['icon'] = ('icons.gui', 'vline')


class SyncSiteStatus(flow.Object):
    status = flow.Param("NotAvailable", StaticSiteSyncStatusChoices)

    def get_short_name(self):
        site = self.root().project().admin.sites[self.name()]
        return site.short_name.get()


class SyncMap(flow.DynamicMap):
    version = flow.Parent()

    @classmethod
    def mapped_type(cls):
        return SyncSiteStatus

    def mapped_names(self, page_num=0, page_size=None):
        project = self.root().project()
        project_sites = project.admin.sites

        sites = []

        for s in project_sites.mapped_items():
            sites.append(s.name())

        return sites

    def columns(self):
        return ['Name', 'Status']

    def _fill_row_cells(self, row, item):
        row['Status'] = item.status.get()
        row['Name'] = item.name()

        if item.name() == self.version.site.get():
            row['Name'] += " (S)"
