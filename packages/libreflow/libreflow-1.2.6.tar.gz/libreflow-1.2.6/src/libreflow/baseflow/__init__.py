import os
import json
import gazu
import getpass
import pathlib

from kabaret import flow
from kabaret.app.ui.gui.widgets.flow.flow_view import (
    CustomPageWidget,
    QtWidgets,
    QtCore,
)
from kabaret.app.ui.gui.widgets.editors import editor_factory
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict
from kabaret.subprocess_manager.runners import Explorer

from .users import Users, UserEnvironment, UserBookmarks, UserProfile
from .film import Sequences
from .lib import Assets
from .runners import (
    Krita,
    Blender,
    VSCodium,
    NotepadPP,
    Firefox,
    SessionWorker,
    DefaultEditor,
    DefaultRunners,
)
from .site import Sites, Site, Synchronize, MinioFileUploader, MinioFileDownloader
from .kitsu import KitsuAPIWrapper


class LoginPageWidget(CustomPageWidget):
    def build(self):
        # Get project root oid
        self.project_oid = self.session.cmds.Flow.split_oid(self.oid)[0][1]

        # Build UI
        self.label = QtWidgets.QLabel(self)
        self.label.setText("<h2>Connexion page</h2>")
        self.error_label = QtWidgets.QLabel(self)
        self.error_label.setText("")

        self.lineedit_kitsu_id = QtWidgets.QLineEdit()
        self.lineedit_kitsu_password = QtWidgets.QLineEdit()
        self.button_login = QtWidgets.QPushButton("Log in")
        self.button_login.setMinimumWidth(100)

        # Set kitsu_password field input mode
        self.lineedit_kitsu_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineedit_kitsu_password.setInputMethodHints(
            QtCore.Qt.ImhHiddenText
            | QtCore.Qt.ImhNoPredictiveText
            | QtCore.Qt.ImhNoAutoUppercase
        )

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.label, 0, 0)
        grid_layout.addWidget(self.lineedit_kitsu_id, 1, 0, 1, 2)
        grid_layout.addWidget(self.lineedit_kitsu_password, 2, 0, 1, 2)
        grid_layout.addWidget(self.error_label, 3, 0)
        grid_layout.addWidget(self.button_login, 3, 1)
        grid_layout.setColumnStretch(0, 1)

        self.setLayout(grid_layout)

        self.button_login.clicked.connect(self.on_button_login_clicked)

    def on_button_login_clicked(self):
        kitsu_id = self.lineedit_kitsu_id.text()
        kitsu_password = self.lineedit_kitsu_password.text()
        logged_in = self.session.cmds.Flow.call(
            self.project_oid,
            "log_in",
            args={},
            kwargs={"kitsu_id": kitsu_id, "kitsu_password": kitsu_password},
        )

        if not logged_in:
            self.error_label.setText(
                "<font color=#C71B1F>Login failed... \
                Check credentials !</font>"
            )
            return

        self.error_label.setText("")
        self.page.refresh()


class LoginPage(flow.Object):

    kitsu_server_url = flow.Param("")



class SynchronizeFilesResult(flow.Action):

    def allow_context(self, context):
        return False

    def get_buttons(self):
        return ["Close"]
    
    def run(self, button):
        return


class SynchronizeFiles(Synchronize):
    ICON = ("icons.libreflow", "sync_arrow")

    result = flow.Child(SynchronizeFilesResult)

    def needs_dialog(self):
        return True
    
    def get_buttons(self):
        self.message.set((
            "<h3><font color=#D66700>"
            "Synchronizing all requested files may freeze your session for a while."
            "</font></h3>"
        ))
        return ["Confirm", "Cancel"]

    def allow_context(self, context):
        return context and context.endswith(".details")
    
    def run(self, button):
        if button == "Cancel":
            return
        
        current_site = self.root().project().get_current_site()
        nb_waiting_jobs = len(current_site.queue.jobs(status="WAITING"))

        super(SynchronizeFiles, self).run(button)

        nb_processed_jobs = nb_waiting_jobs - len(current_site.queue.jobs(status="WAITING"))

        if nb_processed_jobs == nb_waiting_jobs:
            self.result.message.set((
                "<h3><font color=#029600>"
                "Synchronization successful !"
                "</font></h3>"
            ))
        else:
            self.result.message.set((
                "<h3><font color=#D66700>"
                f"Warning: {nb_processed_jobs}/{nb_waiting_jobs} files synchronized"
                "</font></h3>"
            ))
        return self.get_result(next_action=self.result.oid())


class GotoBookmarks(flow.Action):
    ICON = ("icons.gui", "star")

    def needs_dialog(self):
        return False
    
    def run(self, button):
        return self.get_result(
            goto=self.root().project().admin.bookmarks.oid()
        )


class SiteChoiceValue(flow.values.ChoiceValue):

    _parent = flow.Parent()

    def choices(self):
        return self.root().project().admin.sites.mapped_names()


class RequestRevisionsAs(flow.Action):

    path = flow.SessionParam("").ui(
        placeholder="Revision oid pattern (e.g., /siren/films/siren/sequences/sq27/shots/*/departments/misc/files/*/history/revisions/v001)"
    )
    requesting_site_name = flow.Param("default", SiteChoiceValue).watched().ui(
        label="Requesting site"
    )
    requested_site_name = flow.Param("default", SiteChoiceValue).watched().ui(
        label="Site to query"
    )

    def allow_context(self, context):
        current_site = self.root().project().get_current_site()
        return context and current_site.request_files_from_anywhere.get()
    
    def child_value_changed(self, child_value):
        if child_value in (self.requesting_site_name, self.requested_site_name):
            msg = "<h2>Request revisions</h2>"
            if self.requested_site_name.get() == self.requesting_site_name.get():
                msg += (
                    "<font color=#D5000D>"
                    "Requested and requesting sites can't be the same."
                    "</font>"
                )

            self.message.set(msg)

    def get_buttons(self):
        self.requested_site_name.set(self.requested_site_name.choices()[0])
        return ["Request", "Close"]
    
    def run(self, button):
        if button == "Close":
            return
        
        requested_site_name = self.requested_site_name.get()
        requesting_site_name = self.requesting_site_name.get()
        
        if requested_site_name == requesting_site_name:
            return self.get_result(close=False)
        
        self.message.set("<h2>Request revisions</h2>")
        
        splitted_oids = self.path.get().split('*')
        lvl = len(splitted_oids)
        oids = []

        def ls(oid):
            if self.root().session().cmds.Flow.is_map(oid):
                return self.root().session().cmds.Flow.get_mapped_oids(oid)

            return list(map(
                lambda rel: rel[0],
                self.root().session().cmds.Flow.ls(oid)[0]
            ))
        
        oids = [splitted_oids[0]]

        for splitted_oid in splitted_oids[1:]:
            updated_oids = []
            if splitted_oid.startswith("/"):
                splitted_oid = splitted_oid[1:]
            
            for oid in oids:
                if oid.endswith("/"):
                    oid = oid[:-1]
                if not self.root().session().cmds.Flow.exists(oid):
                    msg = self.message.get()
                    msg += (
                        "<font color=#D5000D>"
                        f"Oid <b>{oid}</b> does not exist"
                        "</font>"
                    )
                    self.message.set(msg)
                    return self.get_result(close=False)

                children = ls(oid)
                
                for child in children:
                    updated_oids.append(child + "/" + splitted_oid)
            
            oids = updated_oids

        processed_revisions = 0

        for revision_oid in oids:
            if not self.root().session().cmds.Flow.exists(revision_oid):
                self.root().session().log_error(f"Revision {revision_oid} does not exist")
                continue

            request_action_oid = revision_oid + "/request_as"
            self.root().session().cmds.Flow.set_value(
                request_action_oid + "/requesting_site_name",
                requesting_site_name
            )
            self.root().session().cmds.Flow.set_value(
                request_action_oid + "/requested_site_name",
                requested_site_name
            )
            processed_revisions += 1
            self.root().session().cmds.Flow.run_action(request_action_oid, None)
        
        msg = "<h3>Request revisions</h3>"
        msg += f"<b>{processed_revisions}</b> revision(s) processed."
        self.message.set(msg)

        return self.get_result(close=False)


class Synchronization(flow.Object):
    ICON = ("icons.libreflow", "sync_arrow")
    
    _project = flow.Parent()
    synchronize_files = flow.Child(SynchronizeFiles)
    request_revisions_as = flow.Child(RequestRevisionsAs)

    def summary(self):
        current_site = self._project.get_current_site()
        nb_waiting_jobs = len(current_site.queue.jobs(status="WAITING"))
        
        if nb_waiting_jobs > 0:
            return (
                "<font color=#D5000D><b>"
                f"{nb_waiting_jobs} job(s) waiting"
                "</b></font>"
            )


class LogOut(flow.Action):

    ICON = ("icons.libreflow", "log_out")

    def needs_dialog(self):
        return False
    
    def allow_context(self, context):
        return context and context.endswith(".details")
    
    def run(self, button):
        project = self.root().project()
        kitsu_config = "%s/kitsu_config.json" % project.user_settings_folder()

        if os.path.exists(kitsu_config):
            os.remove(kitsu_config)

        project.log_out()
        
        return self.get_result(
            goto=project.oid(),
            refresh=True
        )


class KitsuConfig(flow.Object):

    ICON = ('icons.libreflow', 'kitsu')

    server_url = flow.Param().watched()
    project_name = flow.Param().watched()
    project_id = flow.Computed(
        cached=True
    )
    gazu_api = flow.Child(KitsuAPIWrapper).ui(
        hidden=True
    )

    def child_value_changed(self, child_value):
        self.project_id.touch()

    def compute_child_value(self, child_value):
        if child_value is self.project_id:
            data = self.gazu_api.get_project_data()
            child_value.set(data["id"])


class ProjectSettings(flow.Object):
    project_nice_name = flow.Param()
    project_thumbnail = flow.Param().ui(editor='textarea')


class Admin(flow.Object):

    ICON = ("icons.gui", "team-admin")

    _project = flow.Parent()

    current_site_name = flow.Computed(cached=True)
    root_dir = flow.Computed(cached=True)
    # kitsu_server_url = flow.Param("").watched()

    project_settings = flow.Child(ProjectSettings)
    settings = flow.Child(ContextualView)
    users = flow.Child(Users)
    kitsu = flow.Child(KitsuConfig)
    
    user_environment = flow.Child(UserEnvironment).ui(expanded=False)
    default_applications = flow.Child(DefaultRunners).ui(expanded=False).injectable()

    sites = flow.Child(Sites)
    process_jobs = flow.Child(Synchronize)
    login_page = flow.Child(LoginPage).ui(hidden=True)

    def child_value_changed(self, child_value):
        if child_value is self.kitsu_server_url:
            self._project.update_kitsu_host(child_value.get())
            self._project.kitsu_id.touch()
            self._project.kitsu_url.touch()

    def compute_child_value(self, child_value):
        if child_value == self.root_dir:
            '''
            TODO : Override by site on multisite !
            '''
            root_dir = None
            if "ROOT_DIR" in os.environ:
                print("WARNING: ROOT_DIR was defined by the environement !")
                root_dir = os.environ["ROOT_DIR"]
            else:
                # Otherwise, get current site's root dir
                root_dir = self.sites[self.current_site_name.get()].root_folder.get()
            child_value.set(root_dir)
        elif child_value is self.current_site_name:
            site_name = None
            site_name_var = "KABARET_SITE_NAME"

            if site_name_var in os.environ:
                site_name = os.environ[site_name_var]
            else:
                cluster_name = os.environ["KABARET_CLUSTER_NAME"]

                if cluster_name in self.sites.mapped_names():
                    site_name = cluster_name
                else:
                    site_name = "default"
            child_value.set(site_name)
        # elif child_value is self.current_user_id:
        #     # Check env
        #     if "USER_NAME" in os.environ:
        #         child_value.set(os.environ["USER_NAME"])
        #         return
            
        #     # Check user file
        #     user_file = os.path.join(self._project.user_settings_folder(), "user.json")
        #     if os.path.exists(user_file):
        #         with open(user_file, "r") as f:
        #             user_config = json.load(f)
        #             child_value.set(user_config["username"])
        #             return

        #     # Return local user name otherwise
        #     child_value.set(getpass.getuser())


class Project(flow.Object):

    log_out_action = flow.Child(LogOut).ui(label="Log out")

    user = flow.Child(UserProfile)
    asset_lib = flow.Child(Assets).ui(expanded=True)
    sequences = flow.Child(Sequences).ui(expanded=True)
    admin = flow.Child(Admin)
    synchronization = flow.Child(Synchronization).ui(expanded=True)

    _show_login_page = flow.Computed().ui(editor="bool")

    _RUNNERS_FACTORY = None

    def get_root(self, alternative=None):
        '''
        alternative can be used if root_dir.get() returns None
        '''
        root_dir = self.admin.root_dir.get()
        if root_dir is None and alternative != None:
            root_dir = alternative
        return root_dir

    def set_user(self, username):
        project_settings_folder = self.project_settings_folder()

        if not os.path.exists(project_settings_folder):
            os.makedirs(project_settings_folder)

        user_file = os.path.join(project_settings_folder, "current_user.json")

        with open(user_file, "w+") as f:
            user_config = dict(username=username)
            json.dump(user_config, f)
        
        self.user.current_user_id.touch()

    def get_user(self):
        return self.user.current_user_id.get()

    def get_current_site(self):
        """
        Returns the site within which the current
        session is beeing run.
        """
        return self.admin.sites[
            self.admin.current_site_name.get()
        ]
    
    def get_exchange_site(self):
        """
        Returns the first exchange site found in
        project's registered site list.
        """
        for site in self.admin.sites.mapped_items():
            if site.site_type.get() == "Exchange":
                return site

        return None

    def is_admin(self, username):
        try:
            return self.admin.users.is_admin(username)
        except flow.exceptions.MappedNameError:
            # Unregistered user not admin by default
            return False

    def compute_child_value(self, child_value):
        if child_value is self._show_login_page:
            kitsu_api = self.kitsu_api()
            valid_host = kitsu_api.host_is_valid()

            if not valid_host:
                logged_in = False
            else:
                logged_in = kitsu_api.current_user_logged_in()

            if not logged_in:
                try:
                    f = open("%s/kitsu_config.json" % self.user_settings_folder(), "r")
                except IOError:
                    logged_in = False
                else:
                    kitsu_config = json.load(f)
                    kitsu_api.set_host(kitsu_config["kitsu_host"])
                    kitsu_api.set_tokens(kitsu_config["tokens"])

                    logged_in = kitsu_api.current_user_logged_in()

            child_value.set(not kitsu_api.host_is_valid() or not logged_in)
        else:
            super(Project, self).compute_child_value(child_value)

    def update_kitsu_host(self, server_url):
        kitsu_api = self.kitsu_api()
        kitsu_api.set_server_url(server_url)
        kitsu_api.set_host(server_url + "/api")

        return kitsu_api.host_is_valid()

    def log_in(self, kitsu_id, kitsu_password):
        kitsu_api = self.kitsu_api()

        self.update_kitsu_host(self.admin.kitsu.server_url.get())
        success = kitsu_api.log_in(kitsu_id, kitsu_password)

        if success:            
            # Set current user
            user_name = self.admin.users.get_user_name(kitsu_id)
            
            if not user_name:
                # Create user profile if not registered
                self.admin.users.add_user(kitsu_id)
            
            self.set_user(user_name)

            # Create user folder at first login
            user_settings_folder = self.user_settings_folder()
            if not os.path.exists(user_settings_folder):
                os.makedirs(user_settings_folder)

            # Save authentification tokens
            tokens = kitsu_api.get_tokens()
            kitsu_config = {}
            kitsu_config["tokens"] = tokens
            kitsu_config["kitsu_host"] = kitsu_api.get_host()

            if user_settings_folder is not None:
                with open("%s/kitsu_config.json" % user_settings_folder, "w+") as f:
                    json.dump(kitsu_config, f)

        return success
    
    def log_out(self):
        self.kitsu_api.log_out()()
    
    def kitsu_id(self):
        return self.admin.kitsu.project_id.get()

    def kitsu_name(self):
        return self.admin.kitsu.project_name.get()
    
    def kitsu_api(self):
        return self.admin.kitsu.gazu_api

    def get_contextual_view(self, context_name):
        if context_name == "settings":
            return self.admin.settings

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(
                PROJECT=self.name(),
                default_shot_layout_files="{sequence}_{shot}_layout.blend, {sequence}_{shot}_layout-movie.mov",
                default_shot_animation_files="{sequence}_{shot}_animation.blend, {sequence}_{shot}_animation-movie.mov, {sequence}_{shot}_animation-export.abc",
                default_asset_model_files="{asset_name}_model.blend, {asset_name}_model-movie.mov, {asset_name}_model-export.abc",
                default_asset_rig_files="{asset_name}_rig.blend, {asset_name}_rig-turnaround.mov",
                project_thumbnail="{ROOT_DIR}TECH/{PROJECT}_thumbnail.png",
            )

    def get_user_bookmarks(self):
        user = self.get_user()
        if user in self.admin.users.mapped_names():
            return self.admin.users[user].bookmarks
        else:
            return None

    def project_settings_folder(self):
        return os.path.join(
            pathlib.Path.home(),
            ".libreflow",
            self.name()
        )

    def user_settings_folder(self):
        '''
        DEPRECATED ! TO DELETE ? 
        '''
        return os.path.join(
            self.project_settings_folder(),
            self.get_user()
        )

    def get_project_thumbnail2(self):
        image = self.admin.project_settings.project_thumbnail.get()
        return image
    def get_project_thumbnail(self):
        contextual_dict = get_contextual_dict(self, "settings")
        contextual_dict["ROOT_DIR"] = self.get_root()
        if "project_thumbnail" not in contextual_dict:
            return None
        path = None

        try:
            path = contextual_dict["project_thumbnail"].format(**contextual_dict)
        except KeyError:
            return None

        if path and os.path.exists(path):
            return path
        else:
            return None

    def update_user_environment(self):
        self.admin.user_environment.update()

    def _register_runners(self):
        self._RUNNERS_FACTORY.ensure_runner_type(Blender)
        self._RUNNERS_FACTORY.ensure_runner_type(Krita)
        self._RUNNERS_FACTORY.ensure_runner_type(VSCodium)
        self._RUNNERS_FACTORY.ensure_runner_type(NotepadPP)
        self._RUNNERS_FACTORY.ensure_runner_type(Firefox)
        self._RUNNERS_FACTORY.ensure_runner_type(Explorer)
        self._RUNNERS_FACTORY.ensure_runner_type(MinioFileUploader)
        self._RUNNERS_FACTORY.ensure_runner_type(MinioFileDownloader)
        self._RUNNERS_FACTORY.ensure_runner_type(SessionWorker)
        self._RUNNERS_FACTORY.ensure_runner_type(DefaultEditor)

    def ensure_runners_loaded(self):
        session = self.root().session()
        subprocess_manager = session.get_actor("SubprocessManager")

        if self._RUNNERS_FACTORY is None:
            self._RUNNERS_FACTORY = subprocess_manager.create_new_factory(
                "Libre Flow Tools"
            )
            self._register_runners()

        subprocess_manager.ensure_factory(self._RUNNERS_FACTORY)

    def get_factory(self):
        self.ensure_runners_loaded()
        return self._RUNNERS_FACTORY
    
    def touch(self):
        super(Project, self).touch()
        self.update_user_environment()

    def _fill_ui(self, ui):
        if self._RUNNERS_FACTORY is None:
            self.ensure_runners_loaded()

        self.touch()

        if self._show_login_page.get():
            ui["custom_page"] = "libreflow.baseflow.LoginPageWidget"
