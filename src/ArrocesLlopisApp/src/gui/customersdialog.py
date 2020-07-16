#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from dataaccesfacility.datamodel import Customer, Address
from sharedcomponets import provincias

from datetime import datetime


class AbstractCustomerDialog(QtWidgets.QDialog):
    """This class creates a base dialog to manage the customers and is extended
        to create  create, edit customers
    """
    def __init__(self,customer=None, parent=None):
        super().__init__(parent)
        self.setupUi( customer)

    def setupUi(self,customer=None):

        self.setWindowTitle("Añadir Cliente")
        self.setObjectName("customerDialog")
        self.resize(662, 371)

        self.gridLayoutUp = QtWidgets.QGridLayout(self)
        self.gridLayoutUp.setObjectName("gridLayoutUp")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout.addItem(spacerItem)

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setText("Cancelar")
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(self.cancelButtonAction)

        self.horizontalLayout.addWidget(self.cancelButton)

        self.acceptButton = QtWidgets.QPushButton(self)
        self.acceptButton.setText("Añadir")
        self.acceptButton.setObjectName("acceptButton")
        self.horizontalLayout.addWidget(self.acceptButton)
        self.acceptButton.clicked.connect(self.acceptButtonAction)

        self.gridLayoutUp.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.addressGroupBox = QtWidgets.QGroupBox(self)
        self.addressGroupBox.setObjectName("addressGroupBox")
        self.addressGroupBox.setTitle("Dirección:")

        self.addressGridLayout = QtWidgets.QGridLayout(self.addressGroupBox)
        self.addressGridLayout.setObjectName("addressGridLayout")

        self.provinceLabel = QtWidgets.QLabel(self.addressGroupBox)
        self.provinceLabel.setObjectName("provinceLabel")
        self.provinceLabel.setText("Provincia:")
        self.addressGridLayout.addWidget(self.provinceLabel, 2, 3, 1, 1)

        self.cityLabel = QtWidgets.QLabel(self.addressGroupBox)
        self.cityLabel.setObjectName("cityLabel")
        self.cityLabel.setText("Ciudad:")
        self.addressGridLayout.addWidget(self.cityLabel, 2, 0, 1, 1)

        self.postalCodeLineEdit = QtWidgets.QLineEdit(self.addressGroupBox)
        self.postalCodeLineEdit.setObjectName("postalCodeLineEdit")
        self.postalCodeLineEdit.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp('^(5[0-2]|[0-4][0-9])[0-9]{3}$')))
        self.addressGridLayout.addWidget(self.postalCodeLineEdit, 3, 2, 1, 1)

        self.cityLineEdit = QtWidgets.QLineEdit(self.addressGroupBox)
        self.cityLineEdit.setObjectName("cityLineEdit")
        self.cityLineEdit.setText('Madrid')
        self.addressGridLayout.addWidget(self.cityLineEdit, 2, 2, 1, 1)

        self.provinceComboBox = QtWidgets.QComboBox(self.addressGroupBox)
        self.provinceComboBox.setObjectName("channelComboBox")
        self.provinceComboBox.addItems(provincias)

        self.addressGridLayout.addWidget(self.provinceComboBox, 2, 4, 1, 1)

        self.flatLineEdit = QtWidgets.QLineEdit(self.addressGroupBox)
        self.flatLineEdit.setObjectName("flatLineEdit")
        self.addressGridLayout.addWidget(self.flatLineEdit, 0, 4, 1, 1)

        self.flatLabel = QtWidgets.QLabel(self.addressGroupBox)
        self.flatLabel.setObjectName("flatLabel")
        self.flatLabel.setText("Piso:")
        self.addressGridLayout.addWidget(self.flatLabel, 0, 3, 1, 1)

        self.postalCodeLabel = QtWidgets.QLabel(self.addressGroupBox)
        self.postalCodeLabel.setObjectName("postalCodeLabel")
        self.postalCodeLabel.setText("Código Postal:")
        self.addressGridLayout.addWidget(self.postalCodeLabel, 3, 0, 1, 1)

        self.adressLabel = QtWidgets.QLabel(self.addressGroupBox)
        self.adressLabel.setObjectName("adressLabel")
        self.adressLabel.setText("Dirección:")
        self.addressGridLayout.addWidget(self.adressLabel, 0, 0, 1, 1)

        self.adressLineEdit = QtWidgets.QLineEdit(self.addressGroupBox)
        self.adressLineEdit.setObjectName("adressLineEdit")
        self.addressGridLayout.addWidget(self.adressLineEdit, 0, 2, 1, 1)

        self.gridLayoutUp.addWidget(self.addressGroupBox, 1, 1, 1, 1)

        self.personalDataGroupBox = QtWidgets.QGroupBox(self)
        self.personalDataGroupBox.setEnabled(True)
        self.personalDataGroupBox.setObjectName("personalDataGroupBox")
        self.personalDataGroupBox.setTitle("Datos Personales:")

        self.gridLayoutDown = QtWidgets.QGridLayout(self.personalDataGroupBox)
        self.gridLayoutDown.setObjectName("gridLayoutDown")

        self.dateLabel = QtWidgets.QLabel(self.personalDataGroupBox)
        self.dateLabel.setObjectName("dateLabel")
        self.gridLayoutDown.addWidget(self.dateLabel, 2, 0, 1, 1)

        self.emailLlineLineEdit = QtWidgets.QLineEdit(self.personalDataGroupBox)
        self.emailLlineLineEdit.setObjectName("emailLlineLineEdit")
        self.emailLlineLineEdit.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp('[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.([a-zA-Z]{2,4})+$/')))
        self.gridLayoutDown.addWidget(self.emailLlineLineEdit, 1, 3, 1, 1)

        self.customerIDLineEdit = QtWidgets.QLineEdit(self.personalDataGroupBox)
        self.customerIDLineEdit.setObjectName("customerIDLineEdit")
        self.gridLayoutDown.addWidget(self.customerIDLineEdit, 3, 3, 1, 1)

        self.telLabel = QtWidgets.QLabel(self.personalDataGroupBox)
        self.telLabel.setObjectName("telLabel")
        self.telLabel.setText("Teléfono:")
        self.gridLayoutDown.addWidget(self.telLabel, 1, 0, 1, 1)

        self.nameLabel = QtWidgets.QLabel(self.personalDataGroupBox)
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Nombre:")
        self.gridLayoutDown.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.dateEdit = QtWidgets.QDateEdit(self.personalDataGroupBox)
        self.dateEdit.setObjectName("dateEdit")
        self.dateLabel.setText("Fecha de Alta:")
        self.gridLayoutDown.addWidget(self.dateEdit, 2, 1, 1, 1)

        self.emailLabel = QtWidgets.QLabel(self.personalDataGroupBox)
        self.emailLabel.setObjectName("emailLabel")
        self.emailLabel.setText("Email:")
        self.gridLayoutDown.addWidget(self.emailLabel, 1, 2, 1, 1)

        self.surnameLineEdit = QtWidgets.QLineEdit(self.personalDataGroupBox)
        self.surnameLineEdit.setObjectName("surnameLineEdit")
        self.gridLayoutDown.addWidget(self.surnameLineEdit, 0, 3, 1, 1)

        self.genderComboBox = QtWidgets.QComboBox(self.personalDataGroupBox)
        self.genderComboBox.setObjectName("genderComboBox")
        self.genderComboBox.addItems(['Hombre','Mujer'])
        self.gridLayoutDown.addWidget(self.genderComboBox, 3, 1, 1, 1)

        self.customerIDLabel = QtWidgets.QLabel(self.personalDataGroupBox)
        self.customerIDLabel.setObjectName("customerIDLabel")
        self.customerIDLabel.setText("Cliente ID:")
        self.gridLayoutDown.addWidget(self.customerIDLabel, 3, 2, 1, 1)

        self.telLineEdit = QtWidgets.QLineEdit(self.personalDataGroupBox)
        self.telLineEdit.setObjectName("telLineEdit")
        self.telLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[6|7|8|9][0-9]{8}$')))
        self.gridLayoutDown.addWidget(self.telLineEdit, 1, 1, 1, 1)

        self.channelComboBox = QtWidgets.QComboBox(self.personalDataGroupBox)
        self.channelComboBox.setObjectName("channelComboBox")
        self.channelComboBox.addItems(["Directo", "RedSocial", "Búsqueda", "Recomendado"])
        self.gridLayoutDown.addWidget(self.channelComboBox, 2, 3, 1, 1)

        self.nameLineEdit = QtWidgets.QLineEdit(self.personalDataGroupBox)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayoutDown.addWidget(self.nameLineEdit, 0, 1, 1, 1)

        self.surnamenesLabel = QtWidgets.QLabel(self.personalDataGroupBox)
        self.surnamenesLabel.setObjectName("surnamenesLabel")
        self.surnamenesLabel.setText("Apellidos")
        self.gridLayoutDown.addWidget(self.surnamenesLabel, 0, 2, 1, 1)

        self.genderLabel = QtWidgets.QLabel(self.personalDataGroupBox)
        self.genderLabel.setObjectName("genderLabel")
        self.genderLabel.setText("Género")
        self.gridLayoutDown.addWidget(self.genderLabel, 3, 0, 1, 1)

        self.channelLabel = QtWidgets.QLabel(self.personalDataGroupBox)
        self.channelLabel.setObjectName("channelLabel")
        self.channelLabel.setText("Canal")
        self.gridLayoutDown.addWidget(self.channelLabel, 2, 2, 1, 1)

        self.gridLayoutUp.addWidget(self.personalDataGroupBox, 0, 1, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(self)

        if customer is not None:
            self.fillForm(customer)

    def cancelButtonAction(self):
        self.close()

    def acceptButtonAction(self):
        raise NotImplementedError

    def fillForm(self, customer):

        self.adressLineEdit.setText(customer.address.street)
        self.cityLineEdit.setText(customer.address.city)
        self.customerIDLineEdit.setText(customer.customerID)
        self.emailLlineLineEdit.setText(customer.email)
        self.nameLineEdit.setText(customer.name)
        self.flatLineEdit.setText(customer.address.flat)
        self.postalCodeLineEdit.setText(str(customer.address.postalCode))
        self.surnameLineEdit.setText(customer.surnames)
        self.telLineEdit.setText(customer.telNumbers)
        self.genderComboBox.setCurrentText(customer.gender)
        self.channelComboBox.setCurrentText(customer.marketingChannel)
        self.provinceComboBox.setCurrentText(customer.address.province)
        self.dateEdit.setDate(QtCore.QDate.fromString(customer.registrationDate.strftime("%d-%m-%Y"), "dd-MM-yyyy"))

    def getCustomer(self):

        customer = Customer()
        customer.address = Address()
        customer.address.street = self.adressLineEdit.text()
        customer.address.city = self.cityLineEdit.text()
        customer.customerID = self.customerIDLineEdit.text()
        customer.email = self.emailLlineLineEdit.text()
        customer.name = self.nameLineEdit.text()
        customer.address.flat = self.flatLineEdit.text()
        customer.address.postalCode = self.postalCodeLineEdit.text()
        customer.surnames = self.surnameLineEdit.text()
        customer.telNumbers = self.telLineEdit.text()
        customer.gender = self.genderComboBox.currentText()
        customer.marketingChannel = self.channelComboBox.currentText()
        customer.address.province = self.provinceComboBox.currentText()
        customer.registrationDate = datetime.strptime(QtCore.QDate.toString(self.dateEdit.date(), "dd/MM/yyyy"), '%d/%m/%Y')
        return customer

class EditCustomerDialog(AbstractCustomerDialog):
    """This class creates a dialog to modify all information of a given
        customer
    """
    def __init__(self, customer = None, parent=None):
        super().__init__(parent)
        self.customerIDLineEdit.setEnabled(False)
        self.setWindowTitle("Editar Cliente")
        self.acceptButton.setText("Modificar")
        if customer is not None:
           self.fillForm(customer)

    def acceptButtonAction(self):
        customer = self.getCustomer()
        self.accept()

class AddCustomerDialog(AbstractCustomerDialog):
    """This class creates a dialog to enter all information neded to
        create a new customer
    """
    def __init__(self, customer=None, parent=None):
        super(AddCustomerDialog, self).__init__(customer,parent)
        self.setWindowTitle("Añadir Cliente")
        self.acceptButton.setText("Añadir")

    def acceptButtonAction(self):
        customer = self.getCustomer()
        if customer.customerID == '':
            QtWidgets.QMessageBox.critical(self, "Añadir Cliente", "Debes poner un identificador de cliente",
                                           QtWidgets.QMessageBox.Ok)
            return
        if customer.email == '':
            QtWidgets.QMessageBox.critical(self, "Añadir Cliente", "Debes poner un email para el cliente",
                                           QtWidgets.QMessageBox.Ok)
            return
        if customer.telNumbers == '':
            QtWidgets.QMessageBox.critical(self, "Añadir Cliente", "Debes poner un telefono para el cliente",
                                           QtWidgets.QMessageBox.Ok)
            return
        if customer.name == '':
            QtWidgets.QMessageBox.critical(self, "Añadir Cliente", "Debes poner un nombre para el cliente",
                                           QtWidgets.QMessageBox.Ok)
            return
        if customer.surnames == '':
            QtWidgets.QMessageBox.critical(self, "Añadir Cliente", "Debes poner appellidos para el cliente",
                                           QtWidgets.QMessageBox.Ok)
            return
        self.accept()
