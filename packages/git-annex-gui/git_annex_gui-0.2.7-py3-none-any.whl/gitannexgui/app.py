import sys

import pkg_resources

from PySide2.QtCore import Qt
from PySide2.QtCore import QResource
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from gitannexgui.gitannex import GitAnnex


def main():
    
    qml_filepath = pkg_resources.resource_filename('gitannexgui', 'main.qml')
    rcc_filepath = pkg_resources.resource_filename('gitannexgui', 'qml.rcc')
    
    # prepare gui
    QResource.registerResource(rcc_filepath)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine(qml_filepath)

    # setup gitannex handler and make available in QML
    git_annex = GitAnnex()
    engine.rootContext().setContextProperty("gitannex", git_annex)

    # start the app
    sys.exit(app.exec_())
