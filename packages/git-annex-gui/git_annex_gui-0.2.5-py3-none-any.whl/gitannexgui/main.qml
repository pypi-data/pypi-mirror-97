import QtQuick 2.6
import QtQuick.Window 2.2
import Qt.labs.platform 1.0
import QtWebEngine 1.8


Window {
    id: app
    visible: true
    width: 1024
    height: 680
    title: qsTr("git-annex gui")
    
    WebEngineView {
        id: webview
        anchors.fill: parent
        url: ""
    }
    
    SystemTrayIcon {
        visible: true
        iconSource: "qrc:/git.svg"
        menu: Menu {
            MenuItem {
                text: qsTr("Start")
                onTriggered: {
                    gitannex.start()
                    webview.url = gitannex.url()
                    webview.reload()
                }
            }
            MenuItem {
                text: qsTr('Stop')
                onTriggered: gitannex.stop()
            }
            MenuItem {
                text: qsTr('Quit')
                onTriggered: Qt.quit()
            }
        }
        onActivated: {
            app.visible = !app.visible
        }
    }

}
