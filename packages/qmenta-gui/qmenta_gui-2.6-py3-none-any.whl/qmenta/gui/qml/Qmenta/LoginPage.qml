import QtQuick 2.6
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2

Page {
    id: loginPage
    property bool loginSuccessful: false
    onLoginSuccessfulChanged: {
        if (loginSuccessful) {
            errorLabel.text = " ";
        } else {
            // logout
            passwordTextField.text = "";
        }
    }

    BrainBanner {
        id: banner
        anchors {
            left: parent.left
            top: parent.top
            bottom: copyrightItem.top
        }
        width: parent.width / 2
    }

    Item {
        id: loginForm
        anchors {
            left: banner.right
            top: parent.top
            bottom: copyrightItem.top
            right: parent.right
        }

        Column {
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Math.max(50, parent.width/5)
                rightMargin: Math.max(50, parent.width/5)
                verticalCenter: parent.verticalCenter
            }
            spacing: 15
            height: childrenRect.height
            Image {
                id: qmentaImage
                anchors {
                    left: parent.left
                    right: parent.right
                    margins: 10
                }
                height: 200
                asynchronous: true
                fillMode: Image.PreserveAspectFit
                source: "images/qmenta-logo-small-crop.png"
            }
            Label {
                id: errorLabel
                color: Material.color(Material.red)
                text: " "
            }
            TextField {
                id: usernameTextField
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width
                placeholderText: "Username"
                focus: true
            }
            TextField {
                id: passwordTextField
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width
                placeholderText: "Password"
                echoMode: TextInput.Password
                Keys.onEnterPressed: loginButton.clicked()
                Keys.onReturnPressed: loginButton.clicked()
            }
            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width
                height: childrenRect.height
                padding: 10
                spacing: 10
                Button {
                    id: loginButton
                    text: "login"
                    width: parent.width / 2 - 15
                    onClicked: {
                        loginPage.loginSuccessful = account.login(
                            usernameTextField.text, passwordTextField.text);

                        if (!loginPage.loginSuccessful) {
                            passwordTextField.text = "";
                            errorLabel.text = "Invalid login. Please try again.";
                        }
                    }
                    Material.background: qmentaColors.green
                    Material.foreground: "white"
                }
                Button {
                    id: signupButton
                    enabled: false
                    width: parent.width / 2 - 15
                    text: "sign up"
                    onClicked: {
                        print("not implemented yet")
                    }
                    Material.background: qmentaColors.green
                    Material.foreground: "white"
                }
            }
        }
    }

    Item {
        id: copyrightItem
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        height: 100

        Label {
            anchors.centerIn: parent
            textFormat: Text.StyledText
            text: "<b>QMENTA Uploader v" + appVersion + 
                  "</b><br><br>Copyright (C) 2021 QMENTA (R). All rights reserved."
            horizontalAlignment: Text.AlignHCenter
        }
    }
}
