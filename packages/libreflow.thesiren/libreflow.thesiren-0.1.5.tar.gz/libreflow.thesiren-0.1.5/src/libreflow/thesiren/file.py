from kabaret import flow

import os

from libreflow.baseflow.file import (
    FileFormat,
    Revision,
    TrackedFile,
    FileSystemMap,
    CreateTrackedFileAction, CreateFileAction,
    CreateTrackedFolderAction, CreateFolderAction,
    AddFilesFromExisting,
)

from kabaret.flow_contextual_dict import get_contextual_dict

from .runners import (CHOICES, CHOICES_ICONS)


class FileFormat(flow.values.ChoiceValue):
    CHOICES = CHOICES





class CreateTrackedFileAction(CreateTrackedFileAction):

    ICON = ("icons.gui", "plus-sign-in-a-black-circle")

    _files = flow.Parent()
    _department = flow.Parent(2)

    file_name = flow.Param("")
    file_format = flow.Param("blend", FileFormat).ui(
        choice_icons=CHOICES_ICONS
    )

    def run(self, button):
        if button == "Cancel":
            return

        settings = get_contextual_dict(self, "settings")
        name = self.file_name.get()
        prefix = self._department._file_prefix.get()

        self.root().session().log_debug(
            "Creating file %s.%s" % (name, self.file_format.get())
        )

        self._files.add_tracked_file(name, self.file_format.get(), prefix + name)
        self._files.touch()

class CreateTrackedFolderAction(CreateTrackedFolderAction):
    ICON = ("icons.gui", "plus-sign-in-a-black-circle")

    _files = flow.Parent()
    _department = flow.Parent(2)


    folder_name = flow.Param("")


    def run(self, button):
        if button == "Cancel":
            return

        settings = get_contextual_dict(self, "settings")
        
        name = self.folder_name.get()
        prefix = self._department._file_prefix.get()

        self.root().session().log_debug(
            "Creating folder %s" % name
        )

        self._files.add_tracked_folder(name, prefix + name)
        self._files.touch()


class Revision(Revision):
    def compute_child_value(self, child_value):
        if child_value is self.file_name:
            name = "{filename}.{ext}".format(
                filename=self._file.complete_name.get(),
                ext=self._file.format.get(),
            )
            child_value.set(name)
        else:
            super(Revision, self).compute_child_value(child_value)


class TrackedFile(TrackedFile):

    def get_name(self):
        return self.name()


class CreateFolderAction(CreateFolderAction):

    def allow_context(self, context):
        return False


class CreateFileAction(CreateFileAction):

    def allow_context(self, context):
        return False


class AddFilesFromExisting(AddFilesFromExisting):

    def allow_context(self, context):
        return False


class FileSystemMap(FileSystemMap):
    
    create_untracked_folder = flow.Child(CreateFolderAction)
    create_untracked_file = flow.Child(CreateFileAction)
    add_files_from_existing = flow.Child(AddFilesFromExisting)

    def add_tracked_file(self, name, extension, complete_name):
        key = "%s_%s" % (name, extension)
        file = self.add(key, object_type=TrackedFile)
        file.format.set(extension)
        file.complete_name.set(complete_name)

        # Create file folder
        try:
            self.root().session().log_debug(
                "Create file folder '{}'".format(file.get_path())
            )
            os.makedirs(file.get_path())
        except OSError:
            self.root().session().log_error(
                "Creation of file folder '{}' failed.".format(file.get_path())
            )
            pass

        # Create current revision folder
        current_revision_folder = os.path.join(file.get_path(), "current")

        try:
            self.root().session().log_debug(
                "Create current revision folder '{}'".format(
                    current_revision_folder
                )
            )
            os.mkdir(current_revision_folder)
        except OSError:
            self.root().session().log_error(
                "Creation of current revision folder '{}' failed".format(
                    current_revision_folder
                )
            )
            pass

        return file
