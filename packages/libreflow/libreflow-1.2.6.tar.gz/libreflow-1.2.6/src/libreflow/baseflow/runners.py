import os
import sys
import platform
import subprocess
from pathlib import Path
import time

from kabaret import flow
from kabaret.subprocess_manager.runner_factory import Runner, logger
from kabaret.subprocess_manager.flow import RunAction


CHOICES = ["blend", "kra", "png", "jpg", "txt", "abc", "mov", "psd", "aep", "zip", "mp4", "fbx", "ai"]
CHOICES_ICONS = {
            "blend": ("icons.libreflow", "blender"),
            "kra": ("icons.libreflow", "krita"),
            "png": ("icons.gui", "picture"),
            "jpg": ("icons.gui", "picture"),
            "txt": ("icons.flow", "notepad"),
            "abc": ("icons.flow", "alembic"),
            "aep": ("icons.libreflow", "afterfx"),
            "psd": ("icons.flow", "photoshop"),
            "mov": ("icons.flow", "quicktime"),
            "ai":  ("icons.libreflow", "illustrator"),
            "zip": ("icons.flow", "file"),
            "mp4": ("icons.gui", "youtube-logo"),
            "fbx": ("icons.libreflow", "fbx"),
        }



# Runners
# -----------------

class BaseRunner(Runner):

    def run(self):
        cmd = [self.executable()]
        cmd.extend(self.argv())

        env = self.env()

        os_flags = {}

        # Disowning processes in linux/mac
        if hasattr(os, "setsid"):
            os_flags["preexec_fn"] = os.setsid

        # Disowning processes in windows
        if hasattr(subprocess, "STARTUPINFO"):
            # Detach the process
            os_flags["creationflags"] = subprocess.CREATE_NEW_CONSOLE

            # Hide the process console
            startupinfo = subprocess.STARTUPINFO()
            if self.show_terminal():
                flag = "/C"
                if self.keep_terminal():
                    flag = "/K"
                cmd = ["cmd", flag] + cmd
            else:
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            os_flags["startupinfo"] = startupinfo

        logger.info("Running Subprocess: %r", cmd)
        
        if not os.path.exists(self.get_log_path()):
            os.mkdir(self.get_log_path())

        log_out_path = "%s/%s_%s.log" % (
            self.get_log_path(),
            self.runner_name(),
            time.time(),
        )
        log_err_path = "%s/%s_%s_error.log" % (
            self.get_log_path(),
            self.runner_name(),
            time.time(),
        )

        with open(log_out_path, "w+") as out, open(log_err_path, "w+") as err:
            popen = subprocess.Popen(cmd, env=env, stdout=out, stderr=err, **os_flags)
            self._popen = popen

    def get_log_path(self):
        return "%s/.libreflow/log" % Path.home()


class DefaultEditor(BaseRunner):
    @classmethod
    def can_edit(cls, filename):
        return True

    def executable(self):
        if platform.system() == "Darwin":
            return "open"
        elif platform.system() == "Linux":
            return "xdg-open"
        return None

    def run(self):
        if platform.system() == "Windows":
            os.startfile(self.argv()[0])
        else:
            super(DefaultEditor, self).run()


class EditFileRunner(BaseRunner):

    ICON = ("icons.flow", "action")

    @classmethod
    def can_edit(cls, filename):
        ext = os.path.splitext(filename)[1]
        supported_exts = cls.supported_extensions()

        return not bool(supported_exts) or ext in supported_exts

    @classmethod
    def supported_extensions(cls):
        """
        Supported file extensions.

        Return None by default to allow any extension.
        """
        return None

    def show_terminal(self):
        return False

    def exec_env_var(self):
        return "%s_EXEC_PATH" % self.__class__.__name__.upper()

    def executable(self):
        exec_var = self.exec_env_var()
        if self.version:
            exec_var += "_%s" % self.version.replace(".", "_")

        try:
            return os.environ[exec_var]
        except KeyError:
            return os.environ[self.exec_env_var()]


class Blender(EditFileRunner):

    ICON = ("icons.libreflow", "blender")
    TAGS = [
        "Modeling",
        "Sculpting",
        "Animation",
        "Rigging",
        "3D Drawing",
        "Rendering",
        "Simulation",
        "Video Editing",
        "VFX",
    ]

    @classmethod
    def supported_versions(cls):
        return ["2.83", "2.90", "2.91"]

    @classmethod
    def supported_extensions(cls):
        return [".blend"]


class Krita(EditFileRunner):

    ICON = ("icons.libreflow", "krita")
    TAGS = ["2D Drawing", "Image Editing"]

    @classmethod
    def supported_versions(cls):
        return ["4.3.0"]

    @classmethod
    def supported_extensions(cls):
        return [".kra", ".png", ".jpg"]


class VSCodium(EditFileRunner):

    ICON = ("icons.libreflow", "vscodium")
    TAGS = ["Text editing", "IDE"]

    @classmethod
    def supported_extensions(cls):
        return [".txt"]


class NotepadPP(EditFileRunner):

    ICON = ("icons.flow", "notepad")
    TAGS = ["Text editing"]

    @classmethod
    def supported_extensions(cls):
        return [".txt"]


class Firefox(EditFileRunner):

    ICON = ("icons.flow", "notepad")
    TAGS = ["Browser"]

    @classmethod
    def can_edit(cls, filename):
        return True


class PythonRunner(BaseRunner):

    def executable(self):
        return sys.executable
    
    def show_terminal(self):
        return False

    def keep_terminal(self):
        return False


class SessionWorker(PythonRunner):

    def argv(self):
        args = [
            "%s/../scripts/session_worker.py" % (
                os.path.dirname(__file__)
            ),
            self.runner_name()
        ]
        args += self.extra_argv
        return args


class LaunchSessionWorker(RunAction):

    def runner_name_and_tags(self):
        return "SessionWorker", []
    
    def launcher_oid(self):
        raise NotImplementedError()

    def launcher_exec_func_name(self):
        raise NotImplementedError()
    
    def extra_argv(self):
        return [
            self.launcher_oid(),
            self.launcher_exec_func_name()
        ]


class RunnerChoiceValue(flow.values.ChoiceValue):

    _extension = flow.Parent(2)

    def choices(self):
        factory = self.root().project().get_factory()

        runner_names = [
            nat[0]
            for nat in factory.find_runners("*.{}".format(self._extension.name()))
        ]

        return runner_names


class RunnerVersionChoiceValue(flow.values.ChoiceValue):

    STRICT_CHOICES = False

    _action = flow.Parent()

    def choices(self):
        factory = self.root().project().get_factory()
        runner_name = self._action.application.get()
        runner_versions = factory.get_runner_versions(runner_name)

        if not runner_versions:
            runner_versions = []

        return runner_versions


class ChangeDefaultRunner(flow.Action):

    _extension = flow.Parent()

    application = flow.Param(None, RunnerChoiceValue).watched()
    version = flow.Param(None, RunnerVersionChoiceValue)

    def get_buttons(self):
        return ["Validate", "Cancel"]

    def child_value_changed(self, child_value):
        if child_value is self.application:
            version_choices = self.version.choices()
            if not version_choices:
                self.version.set("")
            else:
                self.version.set(version_choices[0])

            self.version.touch()

    def run(self, button):
        if button == "Cancel":
            return

        factory = self.root().project().get_factory()
        runner_names = [nat[0] for nat in factory.find_runners()]

        if not self.application.get() in runner_names:
            self.root().session().log_debug("Application not recognized")
            return self.get_result(close=False)

        runner_versions = factory.get_runner_versions(self.application.get())

        if (
            self.version.get()
            and runner_versions
            and not str(self.version.get()) in runner_versions
        ):
            self.root().session().log_debug(
                "Version {version} of {app} unknown".format(
                    version=self.version.get(), app=self.application.get()
                )
            )
            return self.get_result(close=False)

        self._extension.runner_name.set(self.application.get())
        self._extension.runner_version.set(self.version.get())
        self._extension.touch()


class DefaultRunner(flow.Object):

    runner_name = flow.Param("").ui(editable=False)
    runner_version = flow.Param("").ui(editable=False)

    change_default_application = flow.Child(ChangeDefaultRunner)

    def get_runner(self):
        factory = self.root().project().get_factory()

        if not self.runner_name.get():
            runners = factory.find_runners(
                edited_filename="*.{ext}".format(ext=self.name())
            )

            if runners:
                runner_name = runners[0][0]
                runner_version = factory.get_runner_versions(runner_name)[0] or ""
                self.runner_name.set(runner_name)
                self.runner_version.set(runner_version)

        return factory.get_runner(
            runner_name=self.runner_name.get(),
            tags=[],
            version=self.runner_version.get(),
        )


class DefaultRunners(flow.DynamicMap):
    @classmethod
    def mapped_type(cls):
        return DefaultRunner

    def mapped_names(self, page_num=0, page_size=None):
        return CHOICES

    def columns(self):
        return ["Extension", "Default application", "Version"]

    def _fill_row_cells(self, row, item):
        row["Extension"] = item.name()
        row["Default application"] = item.runner_name.get()
        row["Version"] = item.runner_version.get()

    def _fill_row_style(self, style, item, row):
        style["activate_oid"] = item.change_default_application.oid()

        runner = item.get_runner()
        if runner:
            style["icon"] = runner.runner_icon()
            return

        style["icon"] = ("icons.gui", "cog-wheel-silhouette")
