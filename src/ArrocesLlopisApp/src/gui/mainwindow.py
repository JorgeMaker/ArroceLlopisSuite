#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets

from toolbar import ArrocesLlopisToolBar
from toolswidget import ToolsWidget


class UserInteractionMainWindow(object):
    """This class creates athe main window for the application  """
    def setupUi(self, main_window):

        main_window.setObjectName("MainWindow")
        main_window.resize(595, 458)
        main_window.setWindowTitle("Gestión Arroces Llopis  ")


        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # Add layout de to the main window
        self.horizontalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("verticalLayout")

        # Add tabebd tools widget to the main  window
        self.tabbedToolsWidget = ToolsWidget(self.centralwidget)
        self.horizontalLayout.addWidget(self.tabbedToolsWidget)

        # Add toolbar to the main window
        self.toolBar = ArrocesLlopisToolBar(main_window,self.tabbedToolsWidget, main_window)
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        # Add status bar to the main window
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        # Add central Widget to the main window
        main_window.setCentralWidget(self.centralwidget)
