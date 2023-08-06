import os
import shutil

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
                "lib",
                settings["asset_type"],
                settings["asset_family"],
                settings["asset_name"],
                settings["department"],
            )
            child_value.set(path)
        elif child_value is self._file_prefix:
            settings = get_contextual_dict(self, "settings")
            child_value.set("lib_{asset_type}_{asset_family}_{asset_name}_{dept}_".format(**settings))
    
    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(
                department=self.name(),
                dept=self._short_name.get() if self._short_name.get() else self.name(),
                context=self._parent.__class__.__name__.lower(),
            )

class DesignDepartment(Department):
    _short_name = flow.Param("dsn")

class ModelingDepartment(Department):
    _short_name = flow.Param("mod")

class ShadingDepartment(Department):
    _short_name = flow.Param("sha")

class RiggingDepartment(Department):
    _short_name = flow.Param("rig")


class AssetDepartments(flow.Object):
    design = flow.Child(DesignDepartment)
    modeling = flow.Child(ModelingDepartment)
    rigging = flow.Child(RiggingDepartment)
    shading = flow.Child(ShadingDepartment)


class RevisionType(flow.values.ChoiceValue):
    
    CHOICES = ["working copy", "new publication"]


class SetAssetFilePublishComment(flow.Action):

    _file = flow.Parent()
    _files = flow.Parent(2)
    comment = flow.SessionParam("")

    def get_buttons(self):
        src_path = self._file.source_path.get()
        self.comment.set(
            "Created from %s" % os.path.basename(src_path)
        )

        return ["Confirm", "Cancel"]
    
    def run(self, button):
        if button == "Cancel":
            return self.get_result(next_action=self._file.configure.oid())
        
        self._file.publish_comment.set(self.comment.get())
        self._file.ready.set(True)
        self._files.touch()


class ConfigureAssetFileAction(flow.Action):

    _file = flow.Parent()
    _files = flow.Parent(2)

    path = flow.Param("").ui(
        label="Source path",
        placeholder="Drop here a valid file/folder"
    )
    create_as = flow.Param("working copy", RevisionType).ui(
        label="Create as"
    )

    def get_buttons(self):
        self.message.set("")
        return ["Confirm", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return
        
        path = self.path.get()
        ext = self._file.file_extension.get()

        if not os.path.exists(path):
            self.message.set(f"<font color=#D5000D>Invalid source path.</font>")
            return self.get_result(close=False)
        
        source_ext = os.path.splitext(path)[1][1:]

        if not ext and source_ext:
            self.message.set(f"<font color=#D5000D>Source must be a <b>folder</b>.</font>")
            return self.get_result(close=False)
        
        if source_ext != ext:
            self.message.set(f"<font color=#D5000D>File extension must be <b>{ext}</b>.</font>")
            return self.get_result(close=False)
        
        revision_type = self.create_as.get()
        self._file.create_as.set(revision_type)
        self._file.source_path.set(path)

        if revision_type == "new publication":
            return self.get_result(next_action=self._file.set_publish_comment.oid())

        self._file.ready.set(True)
        self._files.touch()


class AssetFile(flow.Object):

    _files = flow.Parent()
    _asset = flow.Parent(3)

    file_name = flow.Computed()
    file_extension = flow.Computed()
    file_department = flow.Computed()
    # file_oid = flow.SessionParam("").ui(editable=False)
    ready = flow.SessionParam(False).ui(editor="bool")
    
    source_path = flow.SessionParam("").ui(editable=False)
    create_as = flow.SessionParam("").ui(editable=False)
    publish_comment = flow.SessionParam("").ui(editable=False)

    configure = flow.Child(ConfigureAssetFileAction)
    set_publish_comment = flow.Child(SetAssetFilePublishComment)

    def department_from_short_name(self, short_name):
        dept_name = self._files.department_names(short_name)
        dept_oid = self._asset.oid() + "/departments/" + dept_name
        
        return self.root().get_object(dept_oid)

    def create(self):
        if not self.ready.get():
            return

        department = self.department_from_short_name(self.file_department.get())
        files = department.files
        file_name = self.file_name.get()
        file_extension = self.file_extension.get()

        # Get file's mapped name
        mapped_name = file_name
        if file_extension:
            mapped_name += "_" + file_extension

        if files.has_mapped_name(mapped_name):
            file = files[mapped_name]
        else:
            if file_extension:
                file = self._create_file(file_name, file_extension, department)
            else:
                file = self._create_folder(file_name, department)
        
        working_copy = self._create_working_copy(file, self.source_path.get(), is_folder=not bool(file_extension))

        if self.create_as.get() == "new publication":
            self._publish_file(file, self.publish_comment.get())
    
    def _create_file(self, name, format, department):
        files = department.files
        files.create_file.file_name.set(name)
        files.create_file.file_format.set(format)
        files.create_file.run(None)
        
        return files["%s_%s" % (name, format)]
    
    def _create_folder(self, name, department):
        files = department.files
        files.create_folder.folder_name.set(name)
        files.create_folder.run(None)
        
        return files[name]

    def _create_working_copy(self, file, source_path=None, is_folder=False):
        file.create_working_copy_action.from_revision.set("")
        file.create_working_copy_action.run(None)
        working_copy = file.get_working_copy()

        if source_path:
            if is_folder:
                working_copy_path = working_copy.path.get()
                # print(file.name(), source_path, working_copy_path)
                shutil.rmtree(working_copy_path)
                shutil.copytree(source_path, working_copy_path)
            else:
                working_copy_path = working_copy.get_path()
                os.remove(working_copy_path)
                shutil.copy2(source_path, working_copy_path)

        return working_copy
    
    def _publish_file(self, file, comment):
        file.publish_action.comment.set(comment)
        file.publish_action.upload_after_publish.set(True)
        file.publish_action.run("Unlock")
        
        return file.get_head_revision()
    
    def head_revision(self):
        if not self.exists():
            return None
        
        file = self.root().get_object(self.file_oid.get())
        return file.get_head_revision()
    
    def compute_child_value(self, child_value):
        file_data = self._files._files_data[self.name()]
        
        if child_value is self.file_name:
            self.file_name.set(file_data["name"])
        elif child_value is self.file_extension:
            self.file_extension.set(file_data["extension"])
        elif child_value is self.file_department:
            self.file_department.set(file_data["department"])


class AssetFiles(flow.DynamicMap):

    _asset = flow.Parent(2)

    def mapped_names(self, page_num=0, page_size=None):
        names = []
        self._files_data = {}

        for dept_files in self.asset_file_names().items():
            dept_name = dept_files[0]

            for name in dept_files[1]:
                file_name, file_ext = os.path.splitext(name)
                key = dept_name + "_" + name.replace(".", "_")

                self._files_data[key] = {
                    "name": file_name,
                    "extension": file_ext[1:],
                    "department": dept_name,
                }
                names.append(key)
        
        return names    
    
    def department_names(self, short_name):
        return {
            "dsn": "design",
            "mod": "modeling",
            "rig": "rigging",
            "sha": "shading",
        }[short_name]
    
    def asset_file_names(self):
        asset_type = self._asset._asset_type.name()
        if asset_type == "sets":
            return {
                "dsn": ["design.ai", "layers"],
            }
        else:
            return {
                "mod": ["modelisation_export.fbx"],
                "rig": ["rig.blend", "rig_ok.blend"],
                "sha": ["textures"],
            }
    
    def file_data(self, mapped_name):
        return self._files_data[mapped_name]
    
    @classmethod
    def mapped_type(cls):
        return AssetFile
    
    def columns(self):
        return ["File/folder", "Department"]
    
    def _fill_row_cells(self, row, item):
        name = item.file_name.get()
        ext = item.file_extension.get()
        if ext:
            name += "." + ext

        row["File/folder"] = name
        row["Department"] = self.department_names(item.file_department.get())
    
    def _fill_row_style(self, style, item, row):
        style["icon"] = ('icons.gui', 'check' if item.ready.get() else 'check-box-empty')
        style["activate_oid"] = item.configure.oid()


class ConfigureAssetAction(flow.Action):

    _asset = flow.Parent()
    files = flow.Child(AssetFiles)

    def get_buttons(self):
        self.message.set("<h2>Configure asset files</h2>")
        return ["Confirm", "Reset", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return
        
        if button == "Reset":
            for file in self.files.mapped_items():
                file.ready.set(False)
            
            self.files.touch()
            return self.get_result(close=False)
        
        for file in self.files.mapped_items():
            file.create()
        
        return self.get_result(goto=self._asset.oid())


class Asset(baseflow.lib.Asset):
    _asset_family = flow.Parent(2)
    _asset_type = flow.Parent(4)
    departments = flow.Child(AssetDepartments).ui(expanded=True)
    configure_action = flow.Child(ConfigureAssetAction)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/episodes/all/assets/%s"
                % (self.root().project().kitsu_url.get(), self.kitsu_id.get())
            )


class Assets(flow.Map):
    _asset_family = flow.Parent()
    _asset_type = flow.Parent(3)
    create_asset = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Asset

class AssetFamily(flow.Object):
    assets = flow.Child(Assets).ui(expanded=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(asset_family=self.name())

class AssetFamilies(flow.Map):
    create_asset_family = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return AssetFamily

class AssetType(flow.Object):

    asset_families = flow.Child(AssetFamilies).ui(expanded=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(asset_type=self.name())


class AssetTypes(flow.Map):

    create_asset_type = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return AssetType


class RevisionType(flow.values.ChoiceValue):

    CHOICES = ["working copy", "first publication"]


class CreateAssetAction(flow.Action):

    ICON = ("icons.gui", "plus-sign-in-a-black-circle")

    asset_name = flow.SessionParam("").watched().ui(
        label="Name",
        placeholder="Kitsu asset name"
    )
    type = flow.Computed()
    family = flow.Computed()
    
    _asset_oid = flow.Computed()

    def asset_type_short_name(self, name):
        return {
            "Characters": "chars",
            "Props": "props",
            "Sets": "sets",
        }[name]
    
    def asset_family_short_name(self, name):
        return name
    
    def revert_to_defaults(self):
        self.type.revert_to_default()
        self.family.revert_to_default()

    def child_value_changed(self, child_value):
        if child_value is self.asset_name:
            self.type.touch()
            self.family.touch()
    
    def compute_child_value(self, child_value):
        kitsu_api = self.root().project().kitsu_api()
        asset_name = self.asset_name.get()
        asset_data = kitsu_api.get_asset_data(asset_name)
        asset_type = kitsu_api.get_asset_type(asset_name)

        if child_value is self.type:                                                                                           
            self.type.set(self.asset_type_short_name(asset_type["name"]) if asset_type else "")
        elif child_value is self.family:
            self.family.set(self.asset_family_short_name(asset_data["data"]["family"]) if asset_data else "")
    
    def _asset_oid(self):
        return self.root().project().oid() + "/asset_lib/asset_types/%s/asset_families/%s/assets/%s" % (
            self.type.get(),
            self.family.get(),
            self.asset_name.get()
        )
    
    def get_buttons(self):
        self.message.set("<h2>Create an asset</h2>")
        return ["Create", "Cancel"]
    
    def run(self, button):
        if button == "Cancel":
            return

        # Asset already exists, next step is configuration
        asset_oid = self._asset_oid()

        if self.root().session().cmds.Flow.exists(asset_oid):
            asset = self.root().get_object(asset_oid)
            return self.get_result(next_action=asset.configure_action.oid())

        asset_name = self.asset_name.get()
        asset_type_name = self.type.get()
        asset_family_name = self.family.get()

        # Warn if asset isn't registered in Kitsu
        if not asset_type_name or not asset_family_name:
            if not asset_name:
                msg = "Asset name must not be empty"
            else:
                msg = f"No asset named <b>{asset_name}</b> in Kitsu."

            self.message.set((
                "<h3>Configure asset</h3>"                
                f"<font color=#D5000D>{msg}</font>"
            ))
            return self.get_result(close=False)

        # Get/create asset type and family
        asset_lib = self.root().project().asset_lib

        if not asset_lib.asset_types.has_mapped_name(asset_type_name):
            asset_type = asset_lib.asset_types.add(asset_type_name)
        else:
            asset_type = asset_lib.asset_types[asset_type_name]

        if not asset_type.asset_families.has_mapped_name(asset_family_name):
            asset_family = asset_type.asset_families.add(asset_family_name)
        else:
            asset_family = asset_type.asset_families[asset_family_name]

        asset = asset_family.assets.add(asset_name)
        asset_family.assets.touch()

        return self.get_result(next_action=asset.configure_action.oid())


class AssetLib(flow.Object):

    asset_types = flow.Child(AssetTypes).ui(expanded=True)
    add_asset = flow.Child(CreateAssetAction).ui(
        label="Add asset"
    )

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(file_category="LIB")
