import os
import gazu
import shutil
import glob

import kabaret.app.resources as resources
from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict
from kabaret.subprocess_manager.flow import RunAction

from libreflow import baseflow

class Department(baseflow.departments.Department):
    _short_name = flow.Param(None)
    _file_prefix = flow.Computed(cached=True)
    
    def compute_child_value(self, child_value):
        if child_value is self.path:
            settings = get_contextual_dict(self, "settings")
            path = os.path.join(
                settings["film"],
                settings["sequence"],
                settings["shot"],
                settings["department"],
            )
            child_value.set(path)
        elif child_value is self._file_prefix:
            settings = get_contextual_dict(self, "settings")
            child_value.set("{film}_{sequence}_{shot}_{dept}_".format(**settings))
    
    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(
                department=self.name(),
                dept=self._short_name.get() if self._short_name.get() else self.name(),
                context=self._parent.__class__.__name__.lower(),
            )


class AssetStatus(flow.values.ChoiceValue):

    CHOICES = ["NotAvailable", "Downloadable", "Available"]


class LayoutDependency(flow.Object):

    _parent = flow.Parent()
    
    asset_name = flow.Computed()
    asset_type = flow.Computed()
    asset_family = flow.Computed()
    asset_path = flow.Computed()
    asset_file_oid = flow.Computed()
    asset_revision_oid = flow.Computed()
    available = flow.Computed()

    def compute_child_value(self, child_value):
        if child_value is self.asset_name:
            child_value.set(self.name())
        elif child_value is self.asset_type:
            if self.name() in ["audio", "board"]:
                child_value.set(self.name())
                return

            child_value.set(
                self._parent.asset_type_short_name(
                    self._parent.asset_data(self.name())["asset_type_name"]
                )
            )
        elif child_value is self.asset_family:
            if self.name() in ["audio", "board"]:
                child_value.set(self.name())
                return

            kitsu_api = self.root().project().kitsu_api()
            child_value.set(self._parent.asset_family_short_name(
                kitsu_api.get_asset_data(self.name())["data"]["family"]
            ))
        elif child_value is self.asset_file_oid:
            asset = None

            if self.name() in ["audio", "board"]:
                asset_type = self.name()
                asset = self._parent._shot
            else:
                asset_type = self.asset_type.get()
                asset_family = self.asset_family.get()
                asset_name = self.asset_name.get()
                asset_oid = self.root().project().oid() + f"/asset_lib/asset_types/{asset_type}/asset_families/{asset_family}/assets/{asset_name}"

                if self.root().session().cmds.Flow.exists(asset_oid):
                    asset = self.root().get_object(asset_oid)
            
            if not asset:
                child_value.set(None)
                return

            file_name = self._parent.asset_type_file_name(asset_type)
            files = self._parent.files_from_asset_type(asset, asset_type)
            
            if not files.has_mapped_name(file_name):
                child_value.set(None)
            else:
                child_value.set(files[file_name].oid())
        elif child_value is self.asset_revision_oid:
            asset_file_oid = self.asset_file_oid.get()
            
            if asset_file_oid:
                file = self.root().get_object(asset_file_oid)
                rev = file.get_head_revision()

                if rev and rev.exists():
                    child_value.set(rev.oid())
                else:
                    child_value.set(None)
            else:
                child_value.set(None)
        elif child_value is self.asset_path:
            asset_revision_oid = self.asset_revision_oid.get()
            asset_type = self.asset_type.get()

            if not asset_revision_oid:
                child_value.set(None)
            else:
                rev = self.root().get_object(asset_revision_oid)
                if not rev.exists():
                    child_value.set(None)
                else:
                    if asset_type == "sets":
                        child_value.set(rev.path.get())
                    else:
                        child_value.set(rev.get_path())
        elif child_value is self.available:
            asset_path = self.asset_path.get()

            if self.asset_revision_oid.get():
                child_value.set("Available")
            elif self.asset_file_oid.get():
                child_value.set("Downloadable")
            else:
                child_value.set("NotAvailable")


class LayoutDependencies(flow.DynamicMap):

    _shot = flow.Parent(4)
    _sequence = flow.Parent(6)
    _updated = flow.BoolParam(False)

    def mapped_names(self, page_num=0, page_size=None):
        kitsu_api = self.root().project().kitsu_api()
        shot_name = self._shot.name()
        sequence_name = self._sequence.name()

        # Get shot data
        kitsu_api = self.root().project().kitsu_api()
        shot_data = kitsu_api.get_shot_data(shot_name, sequence_name)
        self._assets_data = {}

        if not shot_data:
            self.message.set((
                "<h2>Configure layout shot</h2>"
                "<font color=#D5000D>"
                f'No shot named <b>{shot_name}</b> in sequence <b>{sequence_name}</b>.'
                "</font>"
            ))
            return []
        
        shot_casting = kitsu_api.get_shot_casting(shot_data)
        self._assets_data = {asset["asset_name"]: asset for asset in shot_casting}
        return list(self._assets_data.keys()) + ["audio", "board"]
    
    def asset_data(self, asset_name):
        return self._assets_data[asset_name]

    @classmethod
    def mapped_type(cls):
        return LayoutDependency

    def columns(self):
        return ["Name", "Type", "Family", "Revision"]
    
    def asset_type_file_name(self, asset_type):
        return {
            "sets": "layers",
            "chars": "rig_ok_blend",
            "props": "rig_ok_blend",
            "audio": "audio_wav",
            "board": "board_mp4",
        }[asset_type]
    
    def files_from_asset_type(self, asset, asset_type):
        if asset_type == "sets":
            return asset.departments.design.files
        elif asset_type in ["audio", "board"]:
            return asset.departments.misc.files
        else:
            return asset.departments.rigging.files
    
    def asset_type_short_name(self, name):
        return {
            "Characters": "chars",
            "Props": "props",
            "Sets": "sets",
        }[name]
    
    def asset_family_short_name(self, name):
        if name == "3d":
            return "secondary"
        
        return name
    
    def _fill_row_cells(self, row, item):
        row["Name"] = item.asset_name.get()
        row["Type"] = item.asset_type.get()
        row["Family"] = item.asset_family.get()
        
        rev_oid = item.asset_revision_oid.get()
        rev_name = rev_oid.split("/")[-1] if rev_oid else ""
        row["Revision"] = rev_name
    
    def _fill_row_style(self, style, item, row):
        icon_by_status = {
            "NotAvailable": ("icons.libreflow", "cross-mark-on-a-black-circle-background-colored"),
            "Downloadable": ("icons.libreflow", "exclamation-sign-colored"),
            "Available": ("icons.libreflow", "checked-symbol-colored"),
        }
        style["icon"] = icon_by_status[item.available.get()]


class BuildLayoutScene(RunAction):

    _department = flow.Parent()
    _shot = flow.Parent(3)
    _sequence = flow.Parent(5)

    dependencies = flow.Child(LayoutDependencies)

    def runner_name_and_tags(self):
        return "Blender", []
    
    def allow_context(self, context):
        return context and context.endswith(".inline")

    def extra_argv(self):
        # Declare Blender operator call generators
        blender_operators = {
            "setup": lambda **kwargs: 'bpy.ops.pipeline.scene_builder_setup(frame_start={frame_start}, frame_end={frame_end}, resolution_x={resolution_x}, resolution_y={resolution_y}, fps={fps})\n'.format(**kwargs),
            "add_asset": lambda filepath, asset_name: f'bpy.ops.pipeline.scene_builder_import_asset(filepath="{filepath}", asset_name="{asset_name}")\n',
            "add_set": lambda set_dir, set_dicts: f'bpy.ops.pipeline.scene_builder_import_set(directory="{set_dir}", files={set_dicts})\n',
            "add_audio": lambda filepath: f'bpy.ops.pipeline.scene_builder_import_audio(filepath="{filepath}")\n',
            "add_board": lambda filepath: f'bpy.ops.pipeline.scene_builder_import_storyboard(filepath="{filepath}")\n',
            "save": lambda filepath: f'bpy.ops.wm.save_as_mainfile(filepath="{filepath}", compress=True)\n',
        }
        
        # Get scene builder arguments
        frame_start = 101
        frame_end = 101 + self._shot_data.get("nb_frames", 0)
        resolution_x = 2048
        resolution_y = 858
        fps = 24

        assets = self._shot_data.get("assets_data", [])
        sets = self._shot_data.get("sets_data", [])
        audio_path = self._shot_data.get("audio_path", None)
        board_path = self._shot_data.get("board_path", None)
        layout_path = self._shot_data["layout_path"] # Mandatory
        template_path = resources.get("file_templates", "template.blend")

        # Build Blender Python expression
        python_expr = "import bpy\n"
        python_expr += blender_operators["setup"](frame_start=frame_start, frame_end=frame_end, resolution_x=resolution_x, resolution_y=resolution_y, fps=fps)
        
        for name, path in assets:
            python_expr += blender_operators["add_asset"](path, name)
        for set_dir, set_dicts in sets:
            python_expr += blender_operators["add_set"](set_dir, set_dicts)

        if audio_path: python_expr += blender_operators["add_audio"](audio_path)
        if board_path: python_expr += blender_operators["add_board"](board_path)

        python_expr += blender_operators["save"](layout_path)

        return [
            "-b", template_path,
            "--addons", "io_import_images_as_planes,camera_plane,lfs_scene_builder,add_camera_rigs",
            "--python-expr", python_expr
        ]
    
    def extra_env(self):
        return {
            "ROOT_PATH": self.root().project().get_root()
        }

    def get_buttons(self):
        msg = "<h2>Configure layout shot</h2>"

        for dep in self.dependencies.mapped_items():
            if dep.available.get() in ["Downloadable", "NotAvailable"]:
                msg += (
                    "<h3><font color=#D66700>"
                    "Some dependencies are still missing, either because they do not already exists or need to be downloaded on your site.\n"
                    "You can build the scene anyway, but you will have to manually update it when missing dependencies will be available."
                    "</font></h3>"
                )
                break
        
        self.message.set(msg)

        return ["Build and edit", "Build and publish", "Cancel"]
    
    def _create_file(self, name, format, department):
        files = department.files
        files.create_file.file_name.set(name)
        files.create_file.file_format.set(format)
        files.create_file.run(None)
        
        return files["%s_%s" % (name, format)]

    def _create_working_copy(self, file, original_path=None):
        file.create_working_copy_action.from_revision.set("")
        file.create_working_copy_action.run(None)
        working_copy = file.get_working_copy()

        if original_path:
            working_copy_path = working_copy.get_path()
            os.remove(working_copy_path)
            shutil.copy2(original_path, working_copy_path)

        return working_copy
    
    def _publish_file(self, file, comment):
        file.publish_action.comment.set(comment)
        file.publish_action.upload_after_publish.set(True)
        file.publish_action.run("Unlock")
        
        return file.get_head_revision()
    
    def run(self, button):
        if button == "Cancel":
            return
        
        if button == "Refresh":
            self.dependencies.touch()
            return self.get_result(refresh=True, close=False)

        shot_name = self._shot.name()
        sequence_name = self._sequence.name()

        # Get shot data
        kitsu_api = self.root().project().kitsu_api()
        shot_data = kitsu_api.get_shot_data(shot_name, sequence_name)

        # Store dependencies file paths for Blender script building
        self._shot_data = {}
        self._shot_data["nb_frames"] = shot_data["nb_frames"]
        self._shot_data["assets_data"] = []
        self._shot_data["sets_data"] = []

        for dep in self.dependencies.mapped_items():
            if dep.available.get() != "Available":
                continue

            asset_type = dep.asset_type.get()
            path = dep.asset_path.get().replace("\\", "/")
            
            if asset_type in ["chars", "props"]:
                self._shot_data["assets_data"].append((dep.asset_name.get(), path))
            elif asset_type == "sets":
                set_names = list(map(os.path.basename, glob.glob("%s/*.png" % path)))

                self._shot_data["sets_data"].append(
                    (path, [{"name": name} for name in set_names])
                )
            else:
                self._shot_data["%s_path" % asset_type] = path

        # Configure layout file
        if not self._shot.departments.layout.files.has_mapped_name("layout_blend"):
            layout_file = self._create_file("layout", "blend", self._department)
        else:
            layout_file = self._shot.departments.layout.files["layout_blend"]
    
        layout_revision = self._create_working_copy(layout_file)
        if button == "Build and publish":
            layout_revision = self._publish_file(layout_file, "Created with scene builder")

        self._shot_data["layout_path"] = layout_revision.get_path().replace("\\", "/")

        super(BuildLayoutScene, self).run(button)


class LayoutDepartment(Department):
    _short_name = flow.Param("lay")

    build_layout_scene = flow.Child(BuildLayoutScene).ui(
        label="Build layout scene"
    )

class AnimationDepartment(Department):
    _short_name = flow.Param("ani")

class MiscDepartment(Department):
    _short_name = flow.Param("misc")

class ShotDepartments(flow.Object):
    layout = flow.Child(LayoutDepartment).ui(expanded=False)
    animation = flow.Child(AnimationDepartment).ui(expanded=False)
    misc = flow.Child(MiscDepartment).ui(expanded=False)


class Shot(baseflow.film.Shot):

    _film = flow.Parent(4)
    departments = flow.Child(ShotDepartments).ui(expanded=True)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/%s" % (self._film.kitsu_url.get(), self.kitsu_id.get())
            )


class Shots(baseflow.film.Shots):

    create_shot = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Shot


class Sequence(baseflow.film.Sequence):

    _film = flow.Parent(2)
    shots = flow.Child(Shots).ui(default_height=420, expanded=True)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/shots?search=%s" % (self._film.kitsu_url.get(), self.name())
            )


class Sequences(baseflow.film.Sequences):

    ICON = ("icons.flow", "sequence")

    _film = flow.Parent()

    create_sequence = flow.Child(baseflow.maputils.SimpleCreateAction)
    update_kitsu_settings = flow.Child(baseflow.film.UpdateItemsKitsuSettings)

    @classmethod
    def mapped_type(cls):
        return Sequence

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return self._film.get_default_contextual_edits(context_name)



class Film(flow.Object):

    ICON = ("icons.flow", "film")

    sequences = flow.Child(Sequences).ui(default_height=420, expanded=True)
    
    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(film=self.name())


class Films(flow.Map):

    ICON = ("icons.flow", "film")

    create_film = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Film

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(file_category="PROD")


# TODO

# file_category a corriger