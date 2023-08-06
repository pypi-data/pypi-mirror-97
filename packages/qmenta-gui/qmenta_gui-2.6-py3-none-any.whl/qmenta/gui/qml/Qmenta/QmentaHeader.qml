import QtQuick 2.6
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtQuick.Layouts 1.3

ToolBar {
    id: toolBar
    property alias title: label.text
    Material.foreground: "white"
    property alias backButtonEnabled: toolButton.enabled
    signal backButtonClicked()

    RowLayout {
        anchors.fill: parent
        ToolButton {
            id: toolButton
            text: "<"
            onClicked: {
                stackView.pop();
                toolBar.backButtonClicked();
            }
        }
        Label {
            id: label
            elide: Label.ElideRight
            horizontalAlignment: Qt.AlignHCenter
            verticalAlignment: Qt.AlignVCenter
            Layout.fillWidth: true
            font.pixelSize: 22
        }
    }
}
