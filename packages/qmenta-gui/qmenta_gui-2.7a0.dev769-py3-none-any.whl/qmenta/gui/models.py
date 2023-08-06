# mypy does not play nice with PySide2 objects
# type: ignore

from typing import Optional, Dict, List, Mapping, Any

from PySide2.QtCore import (  # type: ignore
    Qt, QAbstractListModel, QModelIndex, QByteArray, QObject
)
import blinker  # type: ignore

from qmenta.core.upload.single import UploadStatus, SingleUpload
from qmenta.core.upload.multi import MultipleThreadedUploads

ProjectList = List[Dict[str, str]]


class ProjectListModel(QAbstractListModel):
    NameRole: int = Qt.UserRole + 1
    IdRole: int = Qt.UserRole + 2

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """
        A ListModel containing the project list as returned by the platform.
        """
        super(ProjectListModel, self).__init__(parent)
        self._projects: ProjectList = []

    def roleNames(self) -> Mapping[int, QByteArray]:
        roles: Mapping[int, QByteArray] = {
            ProjectListModel.NameRole: QByteArray(b'name'),
            ProjectListModel.IdRole: QByteArray(b'id')
        }
        return roles

    @property
    def projects(self) -> ProjectList:
        """
        ProjectList: The input of this model, a list of dictionaries containing
        'name' and 'id' keys for each project.
        """
        return self._projects

    @projects.setter
    def projects(self, projects: ProjectList) -> None:
        self.beginResetModel()
        self._projects = projects
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex) -> int:
        return len(self._projects)

    def data(self, index: QModelIndex, role: int) -> Optional[str]:
        """
        Parameters
        ----------
        index : QModelIndex
        role : PySide2.QtCore.int
        """
        if not index.isValid():
            return None

        row: int = index.row()
        if row >= len(self._projects):
            return None

        project_data: Dict[str, str] = self._projects[row]

        if role == ProjectListModel.NameRole:
            return project_data["name"]
        elif role == ProjectListModel.IdRole:
            return project_data["id"]
        return None


class UploadListModel(QAbstractListModel):
    # Continuing the indices after the roles in ProjectListModel
    FilenameRole: int = Qt.UserRole + 3
    SubjectNameRole: int = Qt.UserRole + 4
    SessionIdRole: int = Qt.UserRole + 5
    StatusRole: int = Qt.UserRole + 6
    StatusMessageRole: int = Qt.UserRole + 7
    BytesUploadedRole: int = Qt.UserRole + 8
    FileSizeRole: int = Qt.UserRole + 9
    FailureDetailsRole: int = Qt.UserRole + 10

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """
        A ListModel containing uploads to the platform
        """
        super(UploadListModel, self).__init__(parent)

        self._uploads: Optional[MultipleThreadedUploads] = None
        on_progress: blinker.Signal = blinker.signal('upload-progress')
        on_progress.connect(self._progressChanged)
        on_status: blinker.Signal = blinker.signal('upload-status')
        on_status.connect(self._statusChanged)
        on_upload_appended: blinker.Signal = blinker.signal('upload-appended')
        on_upload_appended.connect(self._uploadAppended)

    def _progressChanged(self, caller: Any, upload_index: int) -> None:
        self.dataChanged.emit(
            self.index(upload_index), self.index(upload_index)
            # TODO: IF-1193, add the list of roles that were updated.
        )

    def _statusChanged(self, caller: Any, upload_index: int) -> None:
        self.dataChanged.emit(
            self.index(upload_index), self.index(upload_index),
            # TODO: IF-1193, add the list of roles that were updated.
        )

    def _uploadAppended(self, caller: Any, upload_index: int) -> None:
        self.beginInsertRows(QModelIndex(), upload_index, upload_index)
        self.endInsertRows()

    def roleNames(self) -> Dict[int, QByteArray]:
        roles: Dict[int, QByteArray] = {
            UploadListModel.FilenameRole: QByteArray(b'filename'),
            UploadListModel.SubjectNameRole: QByteArray(b'subject_name'),
            UploadListModel.SessionIdRole: QByteArray(b'session_id'),
            UploadListModel.StatusRole: QByteArray(b'status'),
            UploadListModel.StatusMessageRole: QByteArray(b'status_message'),
            UploadListModel.BytesUploadedRole: QByteArray(b'bytes_uploaded'),
            UploadListModel.FileSizeRole: QByteArray(b'file_size'),
            UploadListModel.FailureDetailsRole: QByteArray(b'failure_details')
        }
        return roles

    @property
    def uploads(self) -> Optional[MultipleThreadedUploads]:
        """
        The input of this model.
        """
        return self._uploads

    @uploads.setter
    def uploads(self, uploads: Optional[MultipleThreadedUploads]) -> None:
        self.beginResetModel()
        self._uploads = uploads
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex) -> int:
        if self._uploads:
            return len(self._uploads.upload_list)
        return 0

    statusMessages: Dict[UploadStatus, str] = {
        UploadStatus.TO_ZIP:
            'Waiting to create zip archive of {path}',
        UploadStatus.TO_ZIP_AND_ANONYMISE:
            'Waiting to create zip archive of {path}',
        UploadStatus.ZIPPING:
            'Archiving (zip) {path}',
        UploadStatus.TO_ANONYMISE:
            'Pending anonymisation of {input_filename}',
        UploadStatus.ANONYMISING:
            'Anonymising {input_filename}',
        UploadStatus.TO_UPLOAD:
            'Pending upload of {upload_filename}',
        UploadStatus.UPLOADING:
            'Uploading {upload_filename}',
        UploadStatus.TO_CLEAN:
            'Pending removal of temporary files',
        UploadStatus.DELETING_TMP_FILES:
            'Removing temporary files',
        UploadStatus.DONE:
            'Finished upload of {upload_filename}',
        UploadStatus.FAILED:
            'Warning: Upload failed (click for details)'
    }

    @staticmethod
    def _statusMessage(single_upload: SingleUpload) -> str:
        status: UploadStatus = single_upload.status

        msg: str
        try:
            msg = UploadListModel.statusMessages[status].format(
                path=single_upload.path,
                input_filename=single_upload.input_filename,
                upload_filename=single_upload.upload_filename
            )
        except KeyError:
            msg = 'Unknown status'

        return msg

    def data(self, index: QModelIndex, role: int) -> Any:
        """
        Parameters
        ----------
        index : QModelIndex
        role : PySide2.QtCore.int
        """
        if not self._uploads:
            return None

        if not index.isValid():
            return None

        row: int = index.row()
        if row >= len(self._uploads.upload_list):
            return None

        single_upload: SingleUpload = self._uploads.upload_list[row]

        if role == UploadListModel.FilenameRole:
            return single_upload.path
        elif role == UploadListModel.SubjectNameRole:
            return single_upload.file_info.subject_name
        elif role == UploadListModel.SessionIdRole:
            return single_upload.file_info.session_id
        elif role == UploadListModel.StatusRole:
            return single_upload.status.name
        elif role == UploadListModel.StatusMessageRole:
            return UploadListModel._statusMessage(single_upload)
        elif role == UploadListModel.BytesUploadedRole:
            return single_upload.bytes_uploaded
        elif role == UploadListModel.FileSizeRole:
            return single_upload.file_size
        elif role == UploadListModel.FailureDetailsRole:
            return single_upload.status_message
        return None
