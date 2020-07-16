#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This module contains ans script to start the ArocesLlopis Application
    a GIU application ta manage customers, orders and products as a API Rest
    client
"""
from PyQt5 import QtWidgets
from mainwindow import UserInteractionMainWindow


if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    userInteractionMainWindow = UserInteractionMainWindow()
    userInteractionMainWindow.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())