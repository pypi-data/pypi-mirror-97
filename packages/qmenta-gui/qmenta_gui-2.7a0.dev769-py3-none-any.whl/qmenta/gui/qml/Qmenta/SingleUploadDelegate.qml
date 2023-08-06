import QtQuick 2.6
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.2

/*!
    \qmltype SingleUploadDelegate
    \brief Item delegate for visualizing a single upload
*/
ItemDelegate {
    id: singleUploadDelegate
    width: parent.width
    height: 100

    /*!
        The upload to visualize
    */
    property var singleUpload

    GridLayout {
        anchors {
            fill: parent
            margins: 25
            verticalCenter: parent.verticalCenter
        }
        columns: 2

        Label {
            Layout.fillWidth: true
            Layout.columnSpan: 2
            font {
                weight: Font.DemiBold
                pointSize: 12
            }
            text: singleUpload.filename
        }

        Label {
            text: singleUpload.status_message
            Layout.fillWidth: true
        }

        Label {
            property real kb_uploaded: (singleUpload.bytes_uploaded / 1024).toFixed(1)
            property real kb_total: (singleUpload.file_size / 1024).toFixed(1)
            text: kb_uploaded + " / " + kb_total + " KB"
            visible: singleUpload.file_size > 0
        }

        ProgressBar {
            id: progressBar
            Layout.columnSpan: 2
            Layout.fillWidth: true

            Material.accent: singleUpload.status == 'FAILED' ?
                    Material.color(Material.red) : qmentaColors.green

            from: 0
            to: singleUpload.file_size
            value: singleUpload.bytes_uploaded
            indeterminate: singleUpload.status == 'ANONYMISING'
        }
    }
}