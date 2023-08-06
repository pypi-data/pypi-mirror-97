#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mypy does not play nice with PySide2 objects
# type: ignore

import sys
from os import path
from typing import Optional, List, Dict, Any

from PySide2.QtCore import QObject, Signal, Slot, Property  # type: ignore
import blinker  # type: ignore

from qmenta.core import platform, upload
from qmenta.gui.models import ProjectListModel, UploadListModel
from qmenta.core.platform import Auth


class QAccount(QObject):
    """
    This glues the Python and QML code together

    Parameters
    ----------
    baseUrl : str
        The base URL of the platform to connect to.
        Default value: ```https://platform.qmenta.com```

    Attributes
    ----------
    auth : Auth
        The authentication object for communicating with the platform.
        Initial value: None. Will be set by the login() function
    projectsModel : ProjectListModel
        The list of projects in the platform
    uploadListModel : UploadListModel
        The list of uploads that were added
    keepTmpFiles: bool
        If set, temporary files will not be deleted when an upload is finished.
        Default value: False
    """
    def __init__(self, baseUrl: str = 'https://platform.qmenta.com') -> None:
        QObject.__init__(self)
        self.auth: Optional[Auth] = None
        self.baseUrl: str = baseUrl
        self.projectsModel: ProjectListModel = ProjectListModel()
        self.uploadListModel: UploadListModel = UploadListModel()
        self.keepTmpFiles: bool = False

        onStatus: blinker.Signal = blinker.signal('upload-status')
        onStatus.connect(self._statusChanged)

        # These properties are used to determine if uploads are inprogress
        #   or pending, and to prevent the user from switching projects or
        #   logging out.
        self._uploadsAdded: int = 0
        self._uploadsFinished: int = 0
        self._uploading: bool = False

    @Slot()
    def logout(self) -> None:
        self.projectsModel.projects = []
        self.uploadListModel.uploads = None

    @Slot(str, str, result=bool)
    def login(self, username: str, password: str) -> bool:
        try:
            self.auth = platform.Auth.login(
                username, password, base_url=self.baseUrl
            )
        except platform.PlatformError:
            self.auth = None
            return False

        self.updateProjects()
        self.clearUploads()

        return True

    def updateProjects(self) -> None:
        # TODO IF-1114 Error handling. Show popups when something goes wrong.
        assert self.auth
        try:
            data = platform.parse_response(platform.post(
                self.auth, 'projectset_manager/get_projectset_list'
            ))
        except platform.PlatformError as e:
            print('Failed to get project list: {}'.format(e))
            raise

        titles: List[Dict[str, str]] = []
        for project in data:
            titles.append({"name": project["name"], "id": project["_id"]})
        self.projectsModel.projects = titles

    @staticmethod
    def _parsePath(filename: str) -> str:
        """
        Removes trailing file:// path based on the OS for the API call to
        detect the filename path correctly
        """
        fname: str = filename
        if fname.startswith("file://"):
            fname = fname[7:]
            # In addition, on Windows there is a third '/' to strip
            # Don't just check for 'win' in sys.platform because it will fail
            # for macOS, for which sys.platform == 'darwin'
            if sys.platform == 'win32' and fname.startswith("/"):
                fname = fname[1:]

        return fname

    @Slot(str, str, str, int, str, bool)
    def addUpload(
        self, filename: str, subjectName: str, sessionId: str, projectId: int,
        name: str = '', anonymise: bool = True
    ) -> None:
        """
        Upload the file after optional anonymisation

        Parameters
        ----------
        filename : str
            The file containing the data to be uploaded (after optional
            anonymisation)
        subject_id : str
            The ID of the subject to create or add the data to
        session_id : str
            The ID of the session to create
        project_id : int
            The ID of the project to upload the data to
        name : str
            The name of the file in the platform. If left unset, the basename
            of filename will be used. Default value: ''
        anonymise : bool
            If set, a new zip file will be created with the same name but
            '-anon' appended to the filename before the extension, which
            contains the anonymised version of the data of the original
            zip file. The new zip file will be uploaded instead of the original
            one. Default value: True
        """
        assert self.uploadListModel.uploads
        self._uploadsAdded = self._uploadsAdded + 1
        self.setUploading(True)

        fname: str = QAccount._parsePath(filename)
        name_in_platform: str
        if name:
            name_in_platform = name
        else:
            name_in_platform = path.split(fname)[1]

        self.uploadListModel.uploads.add_upload(
            fname,
            upload.FileInfo(
                project_id=projectId,
                name=name_in_platform,
                subject_name=subjectName,
                session_id=sessionId
            ),
            anonymise=anonymise,
            keep_created_files=self.keepTmpFiles
        )

    @Slot()
    def clearUploads(self) -> None:
        """
        Clear the list of uploads. Call this function when switching
        projects. Do not call this if any uploads are pending or in progress.
        """
        # In the near future we will add functionality to cancel/remove uploads
        #   from the list. IF-1177. This function will then be replaced.
        assert self.auth
        assert not self._uploading
        if (self.uploadListModel.uploads):
            assert self.uploadListModel.uploads.uploads_in_progress == 0
        self.uploadListModel.uploads = upload.MultipleThreadedUploads(
            self.auth)

    def _statusChanged(self, caller: Any, upload_index: int) -> None:
        # Here, we assume that after an upload has been added using
        # addUpload(), there will be exactly ONE status change where the
        # new status becomes DONE or FAILED.
        if caller.status in [
            upload.UploadStatus.DONE, upload.UploadStatus.FAILED
        ]:
            self._uploadsFinished = self._uploadsFinished + 1
            self.setUploading(self._uploadsFinished < self._uploadsAdded)

    def getUploading(self) -> bool:
        return self._uploading

    def setUploading(self, uploading: bool) -> None:
        if uploading != self._uploading:
            self._uploading = uploading
            self.uploadingChanged.emit()

    @Signal
    def uploadingChanged(self) -> None:
        pass

    uploading = Property(bool, getUploading, setUploading,
                         notify=uploadingChanged)
