# !/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets

from configurationdialog import ConfigurationDialog
from restfullapifacility import RestFullAPIFacility, DataPersistancesError
from sharedcomponets import IconProvider


class ArrocesLlopisToolBar(QtWidgets.QToolBar):
    """ This class is used to create a tool bar to launch a tool to manage each
        available endpoint
    """
    def __init__(self,main_window, workAreaTabWidget,  parent=None):

        super(QtWidgets.QToolBar, self).__init__(parent)
        self.customersAction = QtWidgets.QAction(main_window)
        self.customersAction.setIcon(IconProvider.getIconByName("customers"))
        self.customersAction.setObjectName("customersAction")
        self.customersAction.triggered.connect(
            workAreaTabWidget.addCustomersTool)

        self.ordersAction = QtWidgets.QAction(main_window)
        self.ordersAction.setIcon(IconProvider.getIconByName("orders"))
        self.ordersAction.setObjectName("ordersAction")
        self.ordersAction.triggered.connect(workAreaTabWidget.addOrdersTool)

        self.productsAction = QtWidgets.QAction(main_window)
        self.productsAction.setIcon(IconProvider.getIconByName("products"))
        self.productsAction.setObjectName("productsAction")
        self.productsAction.triggered.connect(workAreaTabWidget.addProductsTool)

        self.connectToolButton = QtWidgets.QToolButton(main_window)
        self.connectToolButton.setCheckable(True)
        self.connectToolButton.setIcon(IconProvider.getIconByName("disconnect"))
        self.connectToolButton.setObjectName("connectToolButton")
        self.connectToolButton.toggled.connect(self.connectAction)

        self.configureAction = QtWidgets.QAction(main_window)
        self.configureAction.setIcon(IconProvider.getIconByName("configure"))
        self.configureAction.setObjectName("configureAction")
        self.configureAction.triggered.connect(self.configuretAction)

        self.addAction(self.customersAction)
        self.addAction(self.ordersAction)
        self.addAction(self.productsAction)
        self.addSeparator()
        self.addWidget(self.connectToolButton)
        self.addSeparator()
        self.addAction(self.configureAction)

    def createAction(self, main_window, workAreaTabWidget, iconName, objName):

        action = QtWidgets.QAction(main_window)
        action.setIcon(IconProvider.getIconByName(iconName))
        action.setObjectName(objName)
        action.triggered.connect(workAreaTabWidget.addCustomersTool)

        return action

    def connectAction(self):
        if self.connectToolButton.isChecked():
            faciliy = RestFullAPIFacility.getInstance()
            try:
                faciliy.otainNewToken()
            except DataPersistancesError as error:
                if error.responseCode == DataPersistancesError.CONN_ERROR:
                    QtWidgets.QMessageBox.critical(self,
                                                   "Autenticación con el servidor",
                                                   "No se pudo conectar con el servidor",
                                                   QtWidgets.QMessageBox.Ok)
                    self.connectToolButton.setIcon(
                        IconProvider.getIconByName("disconnect"))
                    return

            if not faciliy.isAuthenticated():
                self.connectToolButton.setChecked(False)
                QtWidgets.QMessageBox.critical(self,
                                               "Autenticación con el servidor",
                                               "Fallo conectando a la atentificando revise la configuración ",
                                               QtWidgets.QMessageBox.Ok)
            else:
                self.connectToolButton.setIcon(IconProvider.getIconByName("connect"))
        else:
            self.connectToolButton.setIcon(IconProvider.getIconByName("disconnect"))

    def configuretAction(self):

        configuration = RestFullAPIFacility.getInstance().parseConfigurationFile()
        configurationDialog = ConfigurationDialog(configuration)
        configurationDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        if configurationDialog.exec_():
            modifiedConfiguration = configurationDialog.getConfiguration()
            RestFullAPIFacility.getInstance().saveConfigurationToFile(modifiedConfiguration)