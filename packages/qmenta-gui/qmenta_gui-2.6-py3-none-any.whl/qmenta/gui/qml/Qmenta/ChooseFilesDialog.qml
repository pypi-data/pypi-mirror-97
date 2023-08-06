import QtQuick 2.6
import QtQuick.Dialogs 1.3 as D

D.FileDialog {
    title: "Please choose ZIP file(s) containing one session each"
    // folder: shortcuts.home   // You don't want this inside a snap
    selectExisting: true
    selectMultiple: true
    selectFolder: false
    nameFilters: ["ZIP files (*.zip)"]
    selectedNameFilter: "ZIP files (*.zip)"
    sidebarVisible: true
}