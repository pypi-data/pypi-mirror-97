import QtQuick 2.6
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.4
import QtQuick.Layouts 1.3

Page {
    id: projectsPage
    property string projectName: "(no project name set)"
    property int projectId: -1

    header: QmentaHeader {
        title: "Upload new sessions to " + projectName
        // Disable back button when any upload is in progress.
        backButtonEnabled: !account.uploading
        onBackButtonClicked: {
            account.clearUploads();
        }
    }

    ChooseFilesDialog {
        id: fileDialog
        onAccepted: {
            fileDialog.close();
            uploadDialog.fileUrls = fileDialog.fileUrls;
            uploadDialog.open();
        }
    }

    ChooseDirDialog {
        id: dirDialog
        onAccepted: {
            dirDialog.close();
            uploadDialog.fileUrls = dirDialog.fileUrls;
            uploadDialog.open();
        }
    }

    FileMetaDataDialog {
        id: uploadDialog
        onAccepted: {
            var infoList = uploadDialog.fileInfo();
            for (var i=0; i < infoList.length; i++) {
                var info = infoList[i];
                account.addUpload(
                    uploadDialog.fileUrls[i],
                    info["subjectId"],
                    info["sessionId"],
                    projectId,
                    info["name"],
                    // TODO IF-1194 Make anonymisation optional
                    true    // always anonymise
                )
            }
        }
    }

    Dialog {
        id: statusMessageDialog
        modal: true
        x: (parent.width - width) / 2
        y: (parent.height - height) / 3
        property alias text: label.text
        Label {
            id: label
        }
        standardButtons: Dialog.Ok
        Material.accent: qmentaColors.green
    }

    ListView {
        id: listView
        anchors.fill: parent
        ScrollBar.vertical: ScrollBar {
            id: scrollBar
            // prevent the scrollbar to fade and hide when not in use
            policy: listView.height > listView.contentHeight ?
                        ScrollBar.AlwaysOff : ScrollBar.AlwaysOn
        }

        model: uploadListModel
        delegate: SingleUploadDelegate {
            singleUpload: model
            onClicked: {
                if (singleUpload.status == 'FAILED') {
                    statusMessageDialog.title = singleUpload.filename;
                    statusMessageDialog.text = singleUpload.failure_details;
                    statusMessageDialog.open();
                }
            }
        }
        header: RowLayout {
            anchors {
                left: parent.left
                right: parent.right
            }
            z: 2    // Draw the header over the list items

            Button {
                id: uploadButton
                Layout.fillWidth: true
                text: "Choose ZIP file(s) to upload"
                onClicked: {
                    fileDialog.open();
                }
            }
            Button {
                Layout.fillWidth: true
                text: "Choose directory to upload"
                onClicked: {
                    dirDialog.open();
                }
            }
        }
        headerPositioning: ListView.PullBackHeader
    }
}