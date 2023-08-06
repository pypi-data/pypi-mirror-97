import QtQuick 2.6
import QtQuick.Dialogs 1.3 as D

D.FileDialog {
    title: "Please choose a directory containing a single session to upload"
    // folder: shortcuts.home  // You don't want this inside a snap
    selectExisting: true
    // selectMultiple: true  // FIXME IF-1206: This does not work for directories
    selectFolder: true
    sidebarVisible: true
}