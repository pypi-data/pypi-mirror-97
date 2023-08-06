from libreflow import baseflow
from kabaret import flow

from .user import User
from .file import CreateTrackedFileAction, CreateTrackedFolderAction, Revision, FileSystemMap
from .lib import AssetLib
from .runners import DefaultRunners
from .film import Films


class Project(baseflow.Project,  flow.InjectionProvider):
    films = flow.Child(Films).ui(expanded=True)
    asset_lib = flow.Child(AssetLib).ui(label="Asset Library")
    admin = flow.Child(baseflow.Admin)

    # BOUHHHHHHHH :
    sequences = flow.Child(baseflow.film.Sequences).ui(hidden=True)

    @classmethod
    def _injection_provider(cls, slot_name, default_type):
        if slot_name == "libreflow.baseflow.file.CreateTrackedFileAction":
            return CreateTrackedFileAction
        elif slot_name == "libreflow.baseflow.file.CreateTrackedFolderAction":
            return CreateTrackedFolderAction
        elif slot_name == "libreflow.baseflow.file.Revision":
            return Revision
        elif slot_name == "libreflow.baseflow.file.FileSystemMap":
            return FileSystemMap
        elif slot_name == "libreflow.baseflow.runners.DefaultRunners":
            return DefaultRunners