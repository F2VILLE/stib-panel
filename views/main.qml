import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes

ApplicationWindow {
    visibility: Window.FullScreen
    title: "STIB Panel"
    color: "#111214"

    ColumnLayout {
        anchors.fill: parent

        Text {
            id: text
            text: "Arrêt " + busStopName
            color: "#f0f0f0"
            font.pixelSize: 22
            Layout.alignment: Qt.AlignVTop | Qt.AlignHCenter
        }
        
        Text {
            text: busError
            color: "#ff9898"
            font.pixelSize: 16
            Layout.alignment: Qt.AlignHCenter
        }

        ListView {
            id: busLinesView
            objectName: "busLinesModel"
            model: busProvider.busData
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: 500
            Layout.preferredWidth: 500
            spacing: 8
            clip: true
            boundsBehavior: Flickable.StopAtBounds
            highlightMoveDuration: 200
            highlightFollowsCurrentItem: true

            header: ColumnLayout {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                Layout.fillWidth: true
                Text {
                    text: "Updated at " + busLastUpdate
                    color: "#999999"
                    font.pixelSize: 12
                    Layout.alignment: Qt.AlignVTop | Qt.AlignHCenter
                }
            }

            delegate: RowLayout {
                width: parent.width
                height: 40
                spacing: 12

                ColumnLayout {
                    Layout.alignment: Qt.AlignVCenter
                    Image {
                        Layout.preferredWidth: 32
                        Layout.preferredHeight: 32
                        source: lineTypeIcons[modelData.type]
                        fillMode: Image.PreserveAspectFit
                        Layout.alignment: Qt.AlignVCenter
                    }
                }

                Rectangle {
                    width: 40
                    height: 32
                    radius: 6
                    color: modelData.color
                    border.color: "#f0f0f0"
                    border.width: 1
                    Layout.alignment: Qt.AlignVCenter

                    Text {
                        text: modelData.line
                        color: "#f0f0f0"
                        font.pixelSize: 18
                        anchors.centerIn: parent
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 2

                    Text {
                        text: modelData.destination
                        color: "#f0f0f0"
                        font.pixelSize: 16
                        font.bold: true
                        elide: Text.ElideRight
                        Layout.fillWidth: true
                    }
                }

                ColumnLayout {
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                    Text {
                        text: modelData.waiting
                        color: "#f0f0f0"
                        font.pixelSize: 16
                        font.bold: true
                        Layout.alignment: Qt.AlignRight
                    }
                }
            }
        }
    }
}
