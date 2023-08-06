import QtQuick 2.6
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtQuick.Layouts 1.3

Page {
    id: projectsPage

    header: QmentaHeader {
        title: "Project list"
    }

    Component {
        id: uploadPage
        UploadPage { }
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
        model: projectListModel
        delegate: ItemDelegate {
            width: parent ? parent.width : 0
            text: name
            onClicked: {
                listView.currentIndex = index;
                stackView.push(
                    uploadPage,
                    {"projectId": id, "projectName": name}
                )
            }
        }
    }
}
