#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets
from dataaccesfacility.datamodel import Product
from restfullapifacility import RestFullAPIFacility ,DataPersistancesError

class AbstractProductDialog(QtWidgets.QDialog):
    """This class creates a base dialog to be able to input information
        to manage products
    """
    def __init__(self,product=None, parent=None):
        """Constructor for AbstractOrderDialog"""
        super().__init__(parent)
        self.setupUi(product)

    def setupUi(self, order = None):

        self.setWindowTitle("Añadir Producto")
        self.setObjectName("productDialog")
        self.resize(459, 191)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Descripcion del Producto:")

        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")

        self.productIDEdit = QtWidgets.QLineEdit(self.groupBox)
        self.productIDEdit.setObjectName("productIDEdit")
        self.gridLayout.addWidget(self.productIDEdit, 0, 1, 1, 1)

        self.typeLabel = QtWidgets.QLabel(self.groupBox)
        self.typeLabel.setObjectName("typeLabel")
        self.typeLabel.setText('Tipo')
        self.gridLayout.addWidget(self.typeLabel, 0, 2, 1, 1)

        self.productIDLabel = QtWidgets.QLabel(self.groupBox)
        self.productIDLabel.setObjectName("productIDLabel")
        self.productIDLabel.setText('ID Producto')
        self.gridLayout.addWidget(self.productIDLabel, 0, 0, 1, 1)

        self.nameLabel = QtWidgets.QLabel(self.groupBox)
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText('Nombre')
        self.gridLayout.addWidget(self.nameLabel, 1, 0, 1, 1)

        self.nameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)

        self.priceEdit = QtWidgets.QLineEdit(self.groupBox)
        self.priceEdit.setObjectName("priceEdit")
        self.priceEdit.setValidator(QtGui.QDoubleValidator(0, 100, 2))
        self.gridLayout.addWidget(self.priceEdit, 1, 3, 1, 1)

        self.priceLabel = QtWidgets.QLabel(self.groupBox)
        self.priceLabel.setObjectName("emailLabel")
        self.priceLabel.setText('Precio')
        self.gridLayout.addWidget(self.priceLabel, 1, 2, 1, 1)

        self.versionLabel = QtWidgets.QLabel(self.groupBox)
        self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setText('Versión')
        self.gridLayout.addWidget(self.versionLabel, 2, 0, 1, 1)

        self.versionEdit = QtWidgets.QLineEdit(self.groupBox)
        self.versionEdit.setObjectName("versionEdit")
        self.gridLayout.addWidget(self.versionEdit, 2, 1, 1, 1)

        self.statusLabel = QtWidgets.QLabel(self.groupBox)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setText('Estado')
        self.gridLayout.addWidget(self.statusLabel, 2, 2, 1, 1)

        self.typeComboBox = QtWidgets.QComboBox(self.groupBox)
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItems(["Arroz", "Otro"])
        self.gridLayout.addWidget(self.typeComboBox, 0, 3, 1, 1)


        self.statusComboBox = QtWidgets.QComboBox(self.groupBox)
        self.statusComboBox.setObjectName("statusComboBox")
        self.statusComboBox.addItems(["Disponible", "Retirado", "Indisponible"])
        self.gridLayout.addWidget(self.statusComboBox, 2, 3, 1, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.acceptButton = QtWidgets.QPushButton(self)
        self.acceptButton.setObjectName("acceptButton")
        self.acceptButton.clicked.connect(self.acceptButtonAction)
        self.horizontalLayout.addWidget(self.acceptButton)

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Cancelar")
        self.cancelButton.clicked.connect(self.cancelButtonAction)

        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def setProduct(self, product):

        self.priceEdit.setText(str(product.price))
        self.versionEdit.setText(str(product.version))
        self.nameEdit.setText(product.name)
        self.productIDEdit.setText(product.productID)

        self.typeComboBox.setCurrentText(product.pType)
        self.statusComboBox.setCurrentText(str(product.isAvailable))

    def getProduct(self):

        product = Product()

        product.productID = self.productIDEdit.text()
        product.name = self.nameEdit.text()
        product.pType = self.typeComboBox.currentText()
        product.price = self.priceEdit.text()
        product.version = self.versionEdit.text()
        product.isAvailable = self.statusComboBox.currentText()

        return product

    def cancelButtonAction(self):
        self.close()


class EditProductDialog(AbstractProductDialog):

    def __init__(self, product=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Producto")
        self.acceptButton.setText("Modificar")
        self.productIDEdit.setEnabled(False)
        if product is not None:
            self.setProduct(product)

    def acceptButtonAction(self):

        product = self.getProduct()
        if product.name is "":
            QtWidgets.QMessageBox.critical(self, "Editar Producto", "El nombre no puede ser vacío",
                                           QtWidgets.QMessageBox.Ok)
            return
        try:
            product.price = float(product.price)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Editar Producto", "Valor del precio incorrecto",
                                           QtWidgets.QMessageBox.Ok)
            return
        self.accept()


class AddProductDialog(AbstractProductDialog):

    def __init__(self, customer=None, parent=None):
        super().__init__(None, parent)
        self.setWindowTitle("Añadir Producto")
        self.acceptButton.setText("Añadir")

        self.persistanceFacility = RestFullAPIFacility.getInstance()

    def acceptButtonAction(self):
        product = self.getProduct()

        if product.productID is "":
            QtWidgets.QMessageBox.critical(self, "Editar Producto", "El ID no puede ser vacío",
                                           QtWidgets.QMessageBox.Ok)
            return

        # Vefificar que no existe otro producto con el mismo ID
        try:
            self.persistanceFacility.retrieve_product(product.productID)
        except DataPersistancesError as e:
                if e.responseCode != 404:
                    QtWidgets.QMessageBox.critical(self, "Añadir Producto", "Producto ID ya existente",
                                                   QtWidgets.QMessageBox.Ok)
                    return

        if product.name is "":
            QtWidgets.QMessageBox.critical(self, "Editar Producto", "El nombre no puede ser vacío",
                                           QtWidgets.QMessageBox.Ok)
            return

        if product.price is "":
            QtWidgets.QMessageBox.critical(self, "Editar Producto", "El precio no puede ser vacío",
                                           QtWidgets.QMessageBox.Ok)
            return

        self.accept()

