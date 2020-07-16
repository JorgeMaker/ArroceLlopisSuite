#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
from datamodel import Customer, Address
from restfullapifacility import RestFullAPIFacility

class SearchCustomerDialog(QtWidgets.QDialog):
    """This class creates a base dialog to be able to input information
        to search customers
    """
    def __init__(self, parent=None):
        """Constructor for SearchCustomerDialog"""
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):

        self.setObjectName("Dialog")
        self.resize(537, 260)
        self.setWindowTitle("Buscar Clientes")

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setCheckable(False)
        self.groupBox.setTitle("Descripción de Clientes:")
        self.groupBox.setObjectName("groupBox")

        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")

        self.emailLabel = QtWidgets.QLabel(self.groupBox)
        self.emailLabel.setObjectName("emailLabel")
        self.emailLabel.setText("Email")
        self.gridLayout.addWidget(self.emailLabel, 1, 2, 1, 1)

        self.nameLabel = QtWidgets.QLabel(self.groupBox)
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Nombre")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.surmamesLabel = QtWidgets.QLabel(self.groupBox)
        self.surmamesLabel.setObjectName("surmamesLabel")
        self.surmamesLabel.setText("Apellidos")
        self.gridLayout.addWidget(self.surmamesLabel, 0, 2, 1, 1)

        self.customerIDLabel = QtWidgets.QLabel(self.groupBox)
        self.customerIDLabel.setObjectName("customerIDLabel")
        self.customerIDLabel.setText("Customer ID")
        self.gridLayout.addWidget(self.customerIDLabel, 2, 0, 1, 1)

        self.dateLabel = QtWidgets.QLabel(self.groupBox)
        self.dateLabel.setObjectName("dateLabel")
        self.dateLabel.setText("Fecha")
        self.gridLayout.addWidget(self.dateLabel, 2, 2, 1, 1)

        self.emailEdit = QtWidgets.QLineEdit(self.groupBox)
        self.emailEdit.setObjectName("emailEdit")
        self.emailEdit.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp('[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.([a-zA-Z]{2,4})+$/')))
        self.gridLayout.addWidget(self.emailEdit, 1, 4, 1, 1)

        self.telEdit = QtWidgets.QLineEdit(self.groupBox)
        self.telEdit.setObjectName("telEdit")
        self.telEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[6|7|8|9][0-9]{8}$')))
        self.gridLayout.addWidget(self.telEdit, 1, 1, 1, 1)

        self.telLabel = QtWidgets.QLabel(self.groupBox)
        self.telLabel.setObjectName("telLabel")
        self.telLabel.setText("Teléfono")
        self.gridLayout.addWidget(self.telLabel, 1, 0, 1, 1)

        self.nameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)

        self.surnamesEdit = QtWidgets.QLineEdit(self.groupBox)
        self.surnamesEdit.setObjectName("surnamesEdit")
        self.gridLayout.addWidget(self.surnamesEdit, 0, 4, 1, 1)

        self.dateEdit = QtWidgets.QLineEdit(self.groupBox)
        self.dateEdit.setObjectName("dateBEdit")
        self.gridLayout.addWidget(self.dateEdit, 2, 4, 1, 1)

        self.cityEdit = QtWidgets.QLineEdit(self.groupBox)
        self.cityEdit.setObjectName("cityEdit")
        self.gridLayout.addWidget(self.cityEdit, 4, 4, 1, 1)

        self.cityLabel = QtWidgets.QLabel(self.groupBox)
        self.cityLabel.setObjectName("cityLabel")
        self.cityLabel.setText("Ciudad")
        self.gridLayout.addWidget(self.cityLabel, 4, 2, 1, 1)

        self.customerIDEdit = QtWidgets.QLineEdit(self.groupBox)
        self.customerIDEdit.setObjectName("customerIDEdit")
        self.gridLayout.addWidget(self.customerIDEdit, 2, 1, 1, 1)

        self.genderLabel = QtWidgets.QLabel(self.groupBox)
        self.genderLabel.setObjectName("genderLabel")
        self.genderLabel.setText("Género")
        self.gridLayout.addWidget(self.genderLabel, 4, 0, 1, 1)

        self.genderComboBox = QtWidgets.QComboBox(self.groupBox)
        self.genderComboBox.setObjectName("genderComboBox")
        self.genderComboBox.addItems(['','Hombre','Mujer', 'Empresa'])
        self.gridLayout.addWidget(self.genderComboBox, 4, 1, 1, 1)

        self.postalCodeLabel = QtWidgets.QLabel(self.groupBox)
        self.postalCodeLabel.setObjectName("postalCodeLabel")
        self.postalCodeLabel.setText("Codigo Postal")
        self.gridLayout.addWidget(self.postalCodeLabel, 5, 0, 1, 1)

        self.channelComboBox = QtWidgets.QComboBox(self.groupBox)
        self.channelComboBox.setObjectName("channelComboBox")
        self.channelComboBox.addItems(['', 'Directo', 'RedSocial', 'Búsqueda', 'Recomendado'])
        self.gridLayout.addWidget(self.channelComboBox, 5, 4, 1, 1)

        self.marketingChannelLabel = QtWidgets.QLabel(self.groupBox)
        self.marketingChannelLabel.setObjectName("marketingChannelLabel")
        self.marketingChannelLabel.setText("Canal")
        self.gridLayout.addWidget(self.marketingChannelLabel, 5, 2, 1, 1)

        self.postalCodeEdit = QtWidgets.QLineEdit(self.groupBox)
        self.postalCodeEdit.setObjectName("postalCodeEdit")
        self.postalCodeEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^(5[0-2]|[0-4][0-9])[0-9]{3}$')))
        self.gridLayout.addWidget(self.postalCodeEdit, 5, 1, 1, 1)

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
        self.accept()

    def getSearchQuery(self):

        customerQuery = Customer()

        customerQuery.email = self.emailEdit.text()
        customerQuery.telNumbers = self.telEdit.text()
        customerQuery.name = self.nameEdit.text()
        customerQuery.surnames = self.surnamesEdit.text()
        customerQuery.customerID = self.customerIDEdit.text()
        dateText = self.dateEdit.text()
        if dateText != '':
            try:
                customerQuery.registrationDate = datetime.datetime.strptime(dateText, '%d/%m/%Y')
            except ValueError as error:
                QtWidgets.QMessageBox.critical(self, "Buscar Clintes ",
                                               "Formato de la fecha incorrecto",
                                               QtWidgets.QMessageBox.Ok)
        customerQuery.gender = self.genderComboBox.currentText()
        customerQuery.marketingChannel = self.channelComboBox.currentText()

        city = self.cityEdit.text()
        postalCode = self.postalCodeEdit.text()

        if city != '' or postalCode != '':
            adress = Address(city=city, postalCode=postalCode)
            customerQuery.address = adress

        return customerQuery


if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    searchCustomerDialog = SearchCustomerDialog()
    searchCustomerDialog.show()
    if searchCustomerDialog.exec_():
        searchQuery = searchCustomerDialog.getSearchQuery()
        persistanceFacility = RestFullAPIFacility.getInstance()
        persistanceFacility.connect()
        listOfCustomers = persistanceFacility.searchCustomers(searchQuery)
        for customer in listOfCustomers:
            print(customer.customerID)

    sys.exit(app.exec_())

