#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import datamodel

import datetime


class SearchOrderDialog(QtWidgets.QDialog):
    """This class creates a  dialog to be able to input information
        to search orders
    """
    def __init__(self, parent=None):
        """Constructor for AbstractOrderDialog"""
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):

        self.setWindowTitle("Buscar Pedido")
        self.setObjectName("Dialog")
        self.resize(537, 225)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Descripcion de Pedidos:")

        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")

        self.dateLabel = QtWidgets.QLabel(self.groupBox)
        self.dateLabel.setObjectName("priceBLabel")
        self.dateLabel.setText("Fecha")
        self.gridLayout.addWidget(self.dateLabel, 1, 2, 1, 1)

        self.orderiDLabel = QtWidgets.QLabel(self.groupBox)
        self.orderiDLabel.setObjectName("orderiDLabel")
        self.orderiDLabel.setText("ID Pedido")
        self.gridLayout.addWidget(self.orderiDLabel, 0, 0, 1, 1)

        self.statusLabel = QtWidgets.QLabel(self.groupBox)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setText("Estado")
        self.gridLayout.addWidget(self.statusLabel, 0, 2, 1, 1)

        self.customnerLabel = QtWidgets.QLabel(self.groupBox)
        self.customnerLabel.setObjectName("customnerLabel")
        self.customnerLabel.setText('Cliente ID')
        self.gridLayout.addWidget(self.customnerLabel, 2, 0, 1, 1)

        self.deliveryTimeLabel = QtWidgets.QLabel(self.groupBox)
        self.deliveryTimeLabel.setObjectName("deliveryTimeLabel")
        self.deliveryTimeLabel.setText("Hora Entrega")
        self.gridLayout.addWidget(self.deliveryTimeLabel, 2, 2, 1, 1)

        self.dateEdit = QtWidgets.QLineEdit(self.groupBox)
        self.dateEdit.setObjectName("priceBEdit")
        # self.dateEdit.setValidator(QtGui.QDoubleValidator(0, 100, 2))
        self.gridLayout.addWidget(self.dateEdit, 1, 4, 1, 1)

        self.priceLabel = QtWidgets.QLabel(self.groupBox)
        self.priceLabel.setObjectName("priceALabel")
        self.priceLabel.setText("Precio")
        self.gridLayout.addWidget(self.priceLabel, 1, 0, 1, 1)

        self.orderIDEdit = QtWidgets.QLineEdit(self.groupBox)
        self.orderIDEdit.setObjectName("orderIDEdit")
        self.gridLayout.addWidget(self.orderIDEdit, 0, 1, 1, 1)

        # self.dateBLabel = QtWidgets.QLabel(self.groupBox)
        # self.dateBLabel.setObjectName("dateBLabel")
        # self.dateBLabel.setText("Fecha B")
        # self.gridLayout.addWidget(self.dateBLabel, 4, 2, 1, 1)
        #
        # self.dateALabel = QtWidgets.QLabel(self.groupBox)
        # self.dateALabel.setObjectName("dateALabel")
        # self.dateALabel.setText("Fecha A")
        # self.gridLayout.addWidget(self.dateALabel, 4, 0, 1, 1)

        self.customerIDEdit = QtWidgets.QLineEdit(self.groupBox)
        self.customerIDEdit.setObjectName("customerIDEdit")
        self.gridLayout.addWidget(self.customerIDEdit, 2, 1, 1, 1)

        self.deliveryTimeComboBox = QtWidgets.QComboBox(self.groupBox)
        self.deliveryTimeComboBox.setObjectName("deliveryTimeComboBox")
        self.deliveryTimeComboBox.addItems(
            ["","13:00", "13:30", "14:00", "14:30", "15:00", "15:30"])
        self.gridLayout.addWidget(self.deliveryTimeComboBox, 2, 4, 1, 1)

        # self.dateAEdit = QtWidgets.QDateEdit(self.groupBox)
        # self.dateAEdit.setObjectName("dateAEdit")
        # self.gridLayout.addWidget(self.dateAEdit, 4, 1, 1, 1)
        #
        # self.dateBEdit = QtWidgets.QDateEdit(self.groupBox)
        # self.dateBEdit.setObjectName("dateBEdit")
        # self.gridLayout.addWidget(self.dateBEdit, 4, 4, 1, 1)

        self.statusComboBox = QtWidgets.QComboBox(self.groupBox)
        self.statusComboBox.setObjectName("statusComboBox")
        self.statusComboBox.addItems(["","Pendiente", "Cobrada", "Cancelada"])
        self.gridLayout.addWidget(self.statusComboBox, 0, 4, 1, 1)

        self.priceEdit = QtWidgets.QLineEdit(self.groupBox)
        self.priceEdit.setObjectName("priceEdit")
        self.priceEdit.setValidator(QtGui.QDoubleValidator(0, 100, 2))
        self.gridLayout.addWidget(self.priceEdit, 1, 1, 1, 1)

        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.searchButton = QtWidgets.QPushButton(self)
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Buscar")
        self.searchButton.clicked.connect(self.searchButtonAction)
        self.horizontalLayout.addWidget(self.searchButton)

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Cancelar")
        self.cancelButton.clicked.connect(self.cancelButtonAction)
        self.horizontalLayout.addWidget(self.cancelButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

    def cancelButtonAction(self):
        self.close()

    def searchButtonAction(self):
        try:
            self.getSearchQuery()
        except ValueError as error:
            QtWidgets.QMessageBox.critical(self, "Buscar pedidos ",
                                           "Formato de fecha o precio incorrecto",
                                           QtWidgets.QMessageBox.Ok)
            return
        self.accept()

    def getSearchQuery(self):

        orderQuery = datamodel.Order()

        orderQuery.orderID = self.orderIDEdit.text()
        orderQuery.customer = self.customerIDEdit.text()
        orderQuery.status = self.statusComboBox.currentText()
        if self.dateEdit.text() != '':
            orderQuery.requestDate = datetime.datetime.strptime(self.dateEdit.text(), '%d/%m/%Y')
        if self.priceEdit.text() != '':
            orderQuery.price = float(self.priceEdit.text())
        if self.deliveryTimeComboBox.currentText() != '':
            orderQuery.deliveryTime = self.deliveryTimeComboBox.currentText()
        return orderQuery


if __name__ == "__main__":

    import sys
    from dataaccesfacility.persistancefacility import MongoDataPersistenceFacility

    app = QtWidgets.QApplication(sys.argv)
    searchOrderDialog = SearchOrderDialog()
    searchOrderDialog.show()
    if searchOrderDialog.exec_():
        searchQuery = searchOrderDialog.getSearchQuery()
        persistanceFacility = MongoDataPersistenceFacility.getInstance()
        persistanceFacility.connect()
        listOfOrders = persistanceFacility.searchOrders(searchQuery)
        print(listOfOrders)

    sys.exit(app.exec_())
