import QtQuick 2.6
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import Qmenta 0.1

import QtQuick.Window 2.2

Window {
    width: 800
    height: 600
    visible: true

    QtObject {
        id: qmentaColors
        readonly property color blue: "#3C73B8"
        readonly property color green: "#2CA895"
        readonly property color grey: "#8f9194"
    }

    Material.theme: Material.Light
    Material.accent: qmentaColors.green
    Material.primary: qmentaColors.blue

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: LoginPage {
            id: loginPage
            onLoginSuccessfulChanged: {
                if (loginPage.loginSuccessful) {
                    stackView.push(projectsPage)
                } else {
                    print("Logged out")
                }
            }
        }
        onDepthChanged: {
            if (depth == 1) {
                account.logout()
                loginPage.loginSuccessful = false
            }
        }
    }

    Component {
        id: projectsPage
        ProjectsPage { }
    }
}