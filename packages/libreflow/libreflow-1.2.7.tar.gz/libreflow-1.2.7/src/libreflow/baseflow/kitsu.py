import gazu

from kabaret import flow

from .maputils import ClearMapAction
from kabaret.subprocess_manager.flow import RunAction


class KitsuAPIWrapper(flow.Object):

    _server_url = flow.Param("")
    _config = flow.Parent()

    def set_host(self, url):
        gazu.client.set_host(url)

    def get_host(self):
        return gazu.client.get_host()

    def set_server_url(self, url):
        self._server_url.set(url)

    def get_server_url(self):
        return self._server_url.get()

    def log_in(self, username, password):
        try:
            gazu.log_in(username, password)
        except (
            gazu.exception.AuthFailedException,
            gazu.exception.ServerErrorException,
        ):
            return False

        return True
    
    def log_out(self):
        gazu.log_out()

    def get_tokens(self):
        return gazu.client.default_client.tokens

    def set_tokens(self, tokens):
        gazu.client.set_tokens(tokens)

    def host_is_valid(self):
        if not gazu.client.host_is_up(gazu.client.default_client):
            return False
        try:
            gazu.client.post("auth/login", {"email": "", "password": ""})
        except Exception as exc:
            return (
                type(exc) == gazu.exception.ParameterException
                or type(exc) == gazu.exception.ServerErrorException
            )

    def current_user_logged_in(self):
        """
        Checks if the current user is logged in.

        This method assumes Kitsu client's host is valid.
        """
        try:
            gazu.client.get_current_user()
        except gazu.exception.NotAuthenticatedException:
            return False

        return True
    
    def get_project_data(self):
        return gazu.project.get_project_by_name(
            self._config.project_name.get()
        )
    
    def get_shot_data(self, shot_name, sequence_name):
        sequence = self.get_sequence_data(sequence_name)
        if not sequence:
            return None
        
        return gazu.shot.get_shot_by_name(
            sequence,
            shot_name
        )
    
    def get_shot_casting(self, shot):
        return gazu.casting.get_shot_casting(shot)
    
    def get_sequence_data(self, name):
        return gazu.shot.get_sequence_by_name(
            self._config.project_id.get(),
            name
        )
    
    def get_asset_data(self, name):
        return gazu.asset.get_asset_by_name(
            self._config.project_id.get(),
            name
        )
    
    def get_asset_type(self, name):
        asset = self.get_asset_data(name)
        if not asset:
            return None

        return gazu.asset.get_asset_type(asset["entity_type_id"])


class UpdateKitsuSettings(flow.Action):

    _kitsu_object = flow.Parent(2)

    def needs_dialog(self):
        return False

    def run(self, button):
        self._kitsu_object.update_kitsu_settings()


class UpdateItemsKitsuSettings(flow.Action):

    _kitsu_map = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        for item in self._kitsu_map.mapped_items():
            item.update_kitsu_settings()

        self._kitsu_map.touch()


class KitsuSetting(flow.values.Value):
    pass


class KitsuSettings(flow.Map):

    clear_settings = flow.Child(ClearMapAction)
    update_settings = flow.Child(UpdateKitsuSettings)

    @classmethod
    def mapped_type(cls):
        return KitsuSetting

    def columns(self):
        return ["Name", "Value"]

    def _fill_row_cells(self, row, item):
        row["Name"] = item.name()
        row["Value"] = item.get()

    def update(self, settings):
        try:
            settings["kitsu_name"] = settings.pop("name")
        except KeyError:
            pass

        for name, value in settings.items():
            try:
                kitsu_setting = self.get_mapped(name)
            except flow.exceptions.MappedNameError:
                kitsu_setting = self.add(name)

            kitsu_setting.set(value)

        self.touch()


class OpenInBrowser(RunAction):

    ICON = ("icons.libreflow", "firefox")

    _url = flow.Parent()

    def runner_name_and_tags(self):
        return "Firefox", ["Browser"]

    def extra_argv(self):
        return [self._url.get()]

    def allow_context(self, context):
        return context and context.endswith(".inline")

    def needs_dialog(self):
        return False


class Url(flow.values.ComputedValue):

    open_in_browser = flow.Child(OpenInBrowser)


class KitsuObject(flow.Object):
    """
    Abstract class representing a Kitsu entity.

    Subclasses must implement the *kitsu_dict* and *compute_child_value* methods.
    """

    kitsu_settings = flow.Child(KitsuSettings).ui(hidden=True)
    kitsu_url = flow.Computed(computed_value_type=Url).ui(hidden=True)
    kitsu_id = flow.Param().ui(editable=False).ui(hidden=True)

    def kitsu_setting_names(self):
        """
        Returns the list of object's settings names, as a subset of the keys
        of the dictionary returned by *kitsu_dict*.

        Returning None will skip name filtering on *kitsu_dict* result
        in *get_kitsu_settings*.
        """
        return None

    def kitsu_dict(self):
        """
        Must be implemented to return a dictionary of parameters related
        to the Kitsu entity.

        It should simply consists in calling the appropriate Gazu
        function given the object's *kitsu_id*.
        """
        raise NotImplementedError()

    def get_kitsu_settings(self):
        settings = self.kitsu_dict()
        names = self.kitsu_setting_names()

        if names is None:
            return settings

        return {name: settings[name] for name in names}

    def update_kitsu_settings(self):
        self.kitsu_settings.update(self.get_kitsu_settings())


class KitsuMap(flow.Map):
    @classmethod
    def mapped_type(cls):
        return KitsuObject


class EntityType(flow.values.ChoiceValue):

    CHOICES = ["Assets", "Shots"]


class SyncFromKitsu(flow.Action):

    ICON = ("icons.libreflow", "sync_arrow")

    entity_type = flow.Param("Assets", EntityType)
    from_index = flow.IntParam(0).ui(label="From")
    to_index = flow.IntParam(10).ui(label="To")

    def get_buttons(self):
        self.message.set("<h3>Synchronize entities from Kitsu</h3>")

        return ["Synchronize", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return

        project = self.root().project()
        project_kitsu_id = project.kitsu_id.get()

        import time

        start_time = time.time()
        i = 0

        if self.entity_type.get() == "Shots":
            kitsu_sequences = gazu.shot.all_sequences_for_project(project_kitsu_id)[
                self.from_index.get() : self.to_index.get()
            ]
            sequences = project.sequences

            # Pull sequences
            for kitsu_sequence in kitsu_sequences:
                try:
                    sequence = sequences.add(kitsu_sequence["name"])
                except flow.exceptions.MappedNameError:
                    # Ignore sequence already mapped
                    continue

                sequence_id = kitsu_sequence["id"]
                sequence.kitsu_id.set(sequence_id)
                sequence.description.set(kitsu_sequence["description"])
                sequence.update_kitsu_settings()

                # Pull shots
                kitsu_shots = gazu.shot.all_shots_for_sequence(sequence_id)
                shots = sequence.shots

                for kitsu_shot in kitsu_shots:
                    try:
                        shot = shots.add(kitsu_shot["name"])
                    except flow.exceptions.MappedNameError:
                        # Ignore shot already mapped
                        continue

                    shot.kitsu_id.set(kitsu_shot["id"])
                    shot.description.set(kitsu_shot["description"])
                    shot.update_kitsu_settings()

                    i += 1

                shots.touch()

            sequences.touch()

            elapsed_time = float(time.time() - start_time)
            self.root().session().log_debug(
                "Elapsed time: {:.4f} min. ({:.4f} min. per shot) ({} shots)".format(
                    elapsed_time / 60.0, elapsed_time / (60.0 * float(i)), i
                )
            )

        elif self.entity_type.get() == "Assets":
            kitsu_assets = gazu.asset.all_assets_for_project(project_kitsu_id)[
                self.from_index.get() : self.to_index.get()
            ]
            assets = project.asset_lib
            i = 0

            for kitsu_asset in kitsu_assets:
                try:
                    asset = assets.add(kitsu_asset["name"])
                except (flow.exceptions.MappedNameError, TypeError) as e:
                    if isinstance(e, flow.exceptions.MappedNameError):
                        # Asset is already mapped
                        i += 1
                        continue

                    try:
                        asset = assets.add("asset{:04d}".format(i))
                    except flow.exceptions.MappedNameError:
                        i += 1
                        continue

                asset.kitsu_id.set(kitsu_asset["id"])
                asset.description.set(kitsu_asset["description"])
                asset.update_kitsu_settings()

                i += 1

            assets.touch()


class KitsuProject(KitsuObject):

    kitsu_name = flow.Param("").watched().ui(hidden=True)
    kitsu_url = flow.Computed().ui(hidden=True)
    kitsu_id = flow.Computed().ui(hidden=True)

    kitsu_api = flow.Child(KitsuAPIWrapper).ui(hidden=True)
    sync_from_kitsu = flow.Child(SyncFromKitsu).injectable().ui(label="Synchronize", hidden=True)

    def kitsu_dict(self):
        project_name = self.kitsu_name.get()
        if not project_name:
            project_name = self.name()

        return gazu.project.get_project_by_name(project_name)

    def child_value_changed(self, child_value):
        if child_value is self.kitsu_name:
            self.kitsu_id.touch()
            self.kitsu_url.touch()

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_id:
            project_dict = self.kitsu_dict()
            child_value.set(project_dict["id"])
        elif child_value is self.kitsu_url:
            child_value.set(
                "%s/productions/%s"
                % (self.kitsu_api.get_server_url(), self.kitsu_id.get())
            )


class KitsuShot(KitsuObject):

    # def kitsu_setting_names(self):
    #     return ['name', 'description', 'nb_frames', 'data']

    def kitsu_dict(self):
        return gazu.shot.get_shot(self.kitsu_id.get())

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/shots/%s"
                % (self.root().project().kitsu_url.get(), self.kitsu_id.get())
            )


class KitsuSequence(KitsuObject):
    def kitsu_dict(self):
        return gazu.shot.get_sequence(self.kitsu_id.get())

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/shots?search=%s"
                % (self.root().project().kitsu_url.get(), self.name())
            )


class KitsuAsset(KitsuObject):
    def kitsu_dict(self):
        return gazu.asset.get_asset(self.kitsu_id.get())

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/assets/%s"
                % (self.root().project().kitsu_url.get(), self.kitsu_id.get())
            )
