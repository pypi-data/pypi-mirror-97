from libreflow import baseflow
from kabaret import flow

from .user import User
from .file import CreateTrackedFileAction, CreateTrackedFolderAction, Revision, FileSystemMap
from .lib import AssetLib
from .runners import DefaultRunners
from .film import Films

from libreflow import _version as libreflow_version
from libreflow.thesiren import _version as libreflowthesiren_version
from packaging import version

class ProjectSettings(baseflow.ProjectSettings,  flow.InjectionProvider):
    libreflow_version = flow.Param() # .ui(editable=False)
    libreflow_siren_version = flow.Param() # .ui(editable=False)



class Project(baseflow.Project,  flow.InjectionProvider):
    films = flow.Child(Films).ui(expanded=True)
    asset_lib = flow.Child(AssetLib).ui(label="Asset Library")
    admin = flow.Child(baseflow.Admin)

    # BOUHHHHHHHH :
    sequences = flow.Child(baseflow.film.Sequences).ui(hidden=True)

    def get_requiered_versions(self):
        '''
        return a list of dependencies
        [dependecyName, currentVersion, requieredVersion, updateNeeded(0:no|1:yes minor|2: yes major)],[]
        '''
        versions = []

        libreflow_cur_version = version.parse(libreflow_version.get_versions()["version"])
        libreflow_req_version = version.parse(self.admin.project_settings.libreflow_version.get())
        
        if libreflow_cur_version < libreflow_req_version \
                and ((libreflow_cur_version.major < libreflow_req_version.major) or \
                    (libreflow_cur_version.minor < libreflow_req_version.minor)):
            # VERY IMPORTANT UPDATE
            libreflow_needs_update = 2
        elif libreflow_cur_version < libreflow_req_version:
            # MINOR UPDATE
            libreflow_needs_update = 1
        else:
            # NO UDPATE
            libreflow_needs_update = 0

        versions.append(["libreflow", str(libreflow_cur_version), str(libreflow_req_version), libreflow_needs_update])
        
        libreflow_sir_cur_version = version.parse(libreflowthesiren_version.get_versions()["version"])
        libreflow_sir_req_version = version.parse(self.admin.project_settings.libreflow_siren_version.get())

        if libreflow_sir_cur_version < libreflow_sir_req_version \
                and ((libreflow_sir_cur_version.major < libreflow_sir_req_version.major) or \
                    (libreflow_sir_cur_version.minor < libreflow_sir_req_version.minor)):
            # VERY IMPORTANT UPDATE
            libreflow_sir_needs_update = 2
        elif libreflow_sir_cur_version < libreflow_sir_req_version:
            # MINOR UPDATE
            libreflow_sir_needs_update = 1
        else:
            # NO UDPATE
            libreflow_sir_needs_update = 0

       
        versions.append(["libreflow.thesiren", str(libreflow_sir_cur_version), str(libreflow_sir_req_version), libreflow_sir_needs_update])
    
        for v in versions:
            print(v)
        return versions

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
        elif slot_name == "libreflow.baseflow.ProjectSettings":
            return ProjectSettings