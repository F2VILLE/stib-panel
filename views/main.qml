import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visibility: Window.FullScreen
    title: "STIB Panel"
    color: "#111214"

    function setText() {
        var i = Math.round(Math.random() * 3);
        text.text = texts[i];
    }

    ColumnLayout {
        anchors.fill: parent

        Text {
            id: text
            text: "Arrêt ULB"
            color: "#f0f0f0"
            font.pixelSize: 22
            Layout.alignment: Qt.AlignVTop | Qt.AlignHCenter
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
                    text: "Updated at --:--"
                    color: "#999999"
                    font.pixelSize: 12
                    Layout.alignment: Qt.AlignVTop | Qt.AlignHCenter
                }
            }

            delegate: RowLayout {
                width: parent.width
                height: 40
                spacing: 12

                Rectangle {
                    width: 40
                    height: 32
                    radius: 6
                    color: {
                        if (modelData.line === "8")
                            return "#3578e5";
                        if (modelData.line === "71")
                            return "#1e981e";
                        if (modelData.line === "72")
                            return "#e454cc";
                        if (modelData.line === "25")
                            return "#bd3836";
                        return "#3a3d40";
                    }
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
