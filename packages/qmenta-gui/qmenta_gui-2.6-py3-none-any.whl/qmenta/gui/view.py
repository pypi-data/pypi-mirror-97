#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Optional

from PySide2.QtCore import QObject  # type: ignore
from PySide2.QtQml import QQmlApplicationEngine  # type: ignore

from qmenta.gui.client import QAccount  # type: ignore
from qmenta.gui import __version__ as gui_version


class MainView(QQmlApplicationEngine):
    """
    The main view for the QMENTA Uploader

    Parameters
    ----------
    base_url : str
        The base url of the platform to connect to.

    Attributes
    ----------
    q_account : QAccount
        The object used for communication with the platform
    """
    def __init__(self, base_url: str,
                 parent: Optional[QObject] = None) -> None:
        super(MainView, self).__init__(parent)

        self.q_account = QAccount(base_url)

        # Make these variables available as properties in QML.
        self.rootContext().setContextProperty("appVersion", gui_version)
        self.rootContext().setContextProperty("account", self.q_account)
        self.rootContext().setContextProperty("projectListModel",
                                              self.q_account.projectsModel)

        self.rootContext().setContextProperty("uploadListModel",
                                              self.q_account.uploadListModel)

        qmldir: str = os.path.join(os.path.dirname(__file__), 'qml')
        self.addImportPath(qmldir)

        # Load the main QML file
        qmlfile: str = os.path.join(qmldir, "Qmenta/app.qml")
        self.load(qmlfile)
