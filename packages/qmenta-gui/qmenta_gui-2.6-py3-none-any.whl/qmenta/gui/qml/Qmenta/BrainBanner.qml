import QtQuick 2.6
import QtGraphicalEffects 1.0

Item {
    id: brainImageItem

    Rectangle {
        id: brainImageBackground
        anchors.centerIn: parent
        color: "white"
        property real maxSize: 600
        width: Math.min(Math.min(maxSize, parent.width - 150), parent.height - 150)
        height: width
        radius: width/2

        Item {
            id: gradientItem
            anchors.fill: brainImage
            LinearGradient {
                id: qmentaGradient
                anchors.fill: parent
                start: Qt.point(0, 0)
                end: Qt.point(width, 0)
                rotation: 10
                gradient: Gradient {
                    GradientStop { position: 0.0; color: qmentaColors.green }
                    GradientStop { position: 1.0; color: qmentaColors.blue }
                }
                NumberAnimation on rotation {
                    from: 0
                    to: 360
                    duration: 6000
                    loops: Animation.Infinite
                }
            }
            visible: false
        }

        ShaderEffectSource {
            id: gradientSource
            anchors.fill: brainImage
            sourceItem: gradientItem
            visible: false
        }

        Image {
            id: brainImage
            anchors {
                fill: parent
                margins: 10
            }
            visible: false
            asynchronous: true
            fillMode: Image.PreserveAspectFit
            source: "images/brain_small.svg"
            property real size: brainImageBackground.maxSize - brainImage.anchors.margins*2
            sourceSize {
                width: size
                height: size
            }
        }

        OpacityMask {
            anchors.fill: brainImage
            source: gradientSource
            maskSource: brainImage
        }
    }
}
