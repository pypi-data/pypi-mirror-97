import os

from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict

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


class Asset(baseflow.lib.Asset):
    _asset_family = flow.Parent(2)
    _asset_type = flow.Parent(4)
    departments = flow.Child(AssetDepartments).ui(expanded=True)

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


class AssetLib(flow.Object):

    asset_types = flow.Child(AssetTypes).ui(expanded=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(file_category="LIB")
