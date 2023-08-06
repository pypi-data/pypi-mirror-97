import QtQuick 2.6
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.4
import QtQuick.Layouts 1.3

Dialog {
    id: uploadDialog
    modal: true
    Material.accent: qmentaColors.green
    x: (parent.width - width) / 2
    y: (parent.height - height) / 3
    width: Math.min(700, parent.width - 50)
    height: Math.min(1000, parent.height - 50)
    padding: 0
    title: "Enter the data that will be stored in QMENTA platform."

    /*!
        The input filenames for which the metadata can be specified.
    */
    property var fileUrls: []
    
    /*!
        Return a list with a dictionary of "name", "subjectId", "sessionId"
        for each of the files in fileUrls.
    */
    function fileInfo() {
        var infoList = [];
        for (var i=0; i < repeater.count; i++) {
            var item = repeater.itemAt(i)
            infoList.push({
                "name": item.nameText,
                "subjectId": item.subjectIdText,
                "sessionId": item.sessionIdText
            });
        }
        return infoList;
    }

    QtObject {
        id: internal
        /*!
            Compute the default value for the "name" metadata.
        */
        function basename(str) {
            return (str.slice(str.lastIndexOf("/")+1));
        }
    }

    Item {
        anchors {
            fill: parent
            margins: 0
        }

        Flickable {
            id: flickable
            anchors.fill: parent
            contentHeight: column.implicitHeight
            clip: true

            leftMargin: 25
            rightMargin: 25
            topMargin: 25
            bottomMargin: 25

            ScrollBar.vertical: ScrollBar {
                // prevent the scrollbar to fade and hide when not in use
                policy: flickable.height > flickable.contentHeight ?
                            ScrollBar.AlwaysOff : ScrollBar.AlwaysOn
            }

            Column {
                id: column
                spacing: 50
                height: childrenRect.height
                Repeater {
                    id: repeater
                    model: uploadDialog.fileUrls.length
                    GridLayout {
                        columns: 2
                        columnSpacing: 25

                        // these are used by fileInfo()
                        property alias nameText: nameTextField.text
                        property alias subjectIdText: subjectIdTextField.text
                        property alias sessionIdText: sessionIdTextField.text

                        Label {
                            text: "Local file"
                        }
                        Label {
                            text: uploadDialog.fileUrls[index]
                        }
                        Label {
                            text: "Anonymise"
                        }
                        CheckBox {
                            // TODO IF-1194 Make anonymisation optional
                            enabled: false
                            checked: true
                            text: "(Enclosed DICOM/NIFTI data will be anonymised)"
                        }
                        Label {
                            text: "Name"
                        }
                        TextField {
                            id: nameTextField
                            Layout.preferredWidth: 400
                            text: internal.basename(uploadDialog.fileUrls[index])
                            placeholderText: "Name in platform"
                        }
                        Label {
                            text: "Subject ID"
                        }
                        TextField {
                            id: subjectIdTextField
                            Layout.preferredWidth: 400
                            placeholderText: "Subject ID (optional)"
                        }
                        Label {
                            text: "Session ID"
                        }
                        TextField {
                            id: sessionIdTextField
                            Layout.preferredWidth: 400
                            placeholderText: "Session ID (optional)"
                        }
                    }
                }
            }
        }
        Rectangle {
            id: bottomSeperator
            height: 1
            color: Material.color(Material.Grey, Material.Shade300)
            anchors {
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }
        }
        Rectangle {
            id: topSeperator
            height: 1
            color: Material.color(Material.Grey, Material.Shade300)
            anchors {
                left: parent.left
                right: parent.right
                top: parent.top
            }
        }
    }

    footer: DialogButtonBox {
        Button {
            flat: true
            text: "Cancel"
            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
        }
        Button {
            flat: true
            text: "Upload all"
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
        }
    }
}