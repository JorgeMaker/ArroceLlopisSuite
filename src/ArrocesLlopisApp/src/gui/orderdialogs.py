#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from dataaccesfacility.datamodel import Order, Product
from datetime import date, datetime
from sharedcomponets import IconProvider, EditDataTable
from restfullapifacility import RestFullAPIFacility, DataPersistancesError


class AbstractOrderDialog(QtWidgets.QDialog):
    """This class creates a base dialog to be able to input information
        to search customers
    """

    def __init__(self,order=None, parent=None):
        """Constructor for AbstractOrderDialog"""
        super().__init__(parent)
        self.persistanceFacility = RestFullAPIFacility.getInstance()
        self.listOfProducts = self.persistanceFacility.retrieve_all_products()
        self.setupUi(order)

    def setupUi(self, order = None):

        self.setWindowTitle("Añadir Pedido")
        self.setObjectName("orderDialog")
        self.resize(602, 366)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.orderDataGroupBox = QtWidgets.QGroupBox(self)
        self.orderDataGroupBox.setFlat(False)
        self.orderDataGroupBox.setObjectName("orderDataGroupBox")

        self.gridLayout = QtWidgets.QGridLayout(self.orderDataGroupBox)
        self.gridLayout.setObjectName("gridLayout")

        self.customerLabel = QtWidgets.QLabel(self.orderDataGroupBox)
        self.customerLabel.setObjectName("customerLabel")
        self.customerLabel.setText("Cliente")
        self.gridLayout.addWidget(self.customerLabel, 0, 2, 1, 1)

        self.statusLabel = QtWidgets.QLabel(self.orderDataGroupBox)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setText("Estado")
        self.gridLayout.addWidget(self.statusLabel, 1, 0, 1, 1)

        self.priceLabel = QtWidgets.QLabel(self.orderDataGroupBox)
        self.priceLabel.setObjectName("emailLabel")
        self.priceLabel.setText("Precio pagado:")
        self.gridLayout.addWidget(self.priceLabel, 2, 0, 1, 1)

        self.dateEdit = QtWidgets.QDateEdit(self.orderDataGroupBox)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 1, 3, 1, 1)

        self.orderIDEdit = QtWidgets.QLineEdit(self.orderDataGroupBox)
        self.orderIDEdit.setObjectName("orderIDEdit")
        self.gridLayout.addWidget(self.orderIDEdit, 0, 1, 1, 1)

        self.paidPriceEdit = QtWidgets.QLineEdit(self.orderDataGroupBox)
        self.paidPriceEdit.setObjectName("paidPriceEdit")
        self.paidPriceEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.paidPriceEdit, 2, 1, 1, 1)

        self.deliveryDtateLabel = QtWidgets.QLabel(self.orderDataGroupBox)
        self.deliveryDtateLabel.setObjectName("deliveryDtateLabel")
        self.deliveryDtateLabel.setText("Fecha de entrega:")
        self.gridLayout.addWidget(self.deliveryDtateLabel, 1, 2, 1, 1)

        self.customerEdit = QtWidgets.QLineEdit(self.orderDataGroupBox)
        self.customerEdit.setObjectName("customerEdit")
        #self.customerEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[6|7|8|9][0-9]{8}$')))
        self.gridLayout.addWidget(self.customerEdit, 0, 3, 1, 1)

        self.orderIDLabel = QtWidgets.QLabel(self.orderDataGroupBox)
        self.orderIDLabel.setObjectName("orderIDLabel")
        self.orderIDLabel.setText("ID de Pedido:")
        self.gridLayout.addWidget(self.orderIDLabel, 0, 0, 1, 1)

        self.deliveryTimeComboBox = QtWidgets.QComboBox(self.orderDataGroupBox)
        self.deliveryTimeComboBox.setObjectName("deliveryTimeComboBox")
        self.deliveryTimeComboBox.addItems(["13:00", "13:30", "14:00", "14:30", "15:00", "15:30"])
        self.gridLayout.addWidget(self.deliveryTimeComboBox, 2, 3, 1, 1)

        self.orderEstatusComboBox = QtWidgets.QComboBox(self.orderDataGroupBox)
        self.orderEstatusComboBox.setObjectName("orderEstatusComboBox")
        self.orderEstatusComboBox.addItems(["Pendiente", "Cobrada", "Cancelada"])
        self.gridLayout.addWidget(self.orderEstatusComboBox, 1, 1, 1, 1)

        self.deliveryTimeLabel = QtWidgets.QLabel(self.orderDataGroupBox)
        self.deliveryTimeLabel.setObjectName("deliveryTimeLabel")
        self.deliveryTimeLabel.setText("Hora de entrega:")
        self.gridLayout.addWidget(self.deliveryTimeLabel, 2, 2, 1, 1)

        self.verticalLayout.addWidget(self.orderDataGroupBox)

        self.procuctListGroupBox = QtWidgets.QGroupBox(self)
        self.procuctListGroupBox.setFlat(False)
        self.procuctListGroupBox.setCheckable(False)
        self.procuctListGroupBox.setObjectName("procuctListGroupBox")

        self.downVerticalLayout = QtWidgets.QVBoxLayout(self.procuctListGroupBox)
        self.downVerticalLayout.setObjectName("downVerticalLayout")

        self.productListTable = ProductListTable()
        hedlabels = ('Producto', 'Cantidad')
        hedprops = (300, 100)
        self.productListTable.setHeaderContent(hedlabels, hedprops)

        self.productListTable.setObjectName("productListTable")
        self.downVerticalLayout.addWidget(self.productListTable)

        self.downHorizontalLayout = QtWidgets.QHBoxLayout()
        self.downHorizontalLayout.setObjectName("downHorizontalLayout")

        self.productLabel = QtWidgets.QLabel(self.procuctListGroupBox)
        self.productLabel.setObjectName("label")
        self.productLabel.setText("Producto:")
        self.downHorizontalLayout.addWidget(self.productLabel)

        self.productComboBox = QtWidgets.QComboBox(self.procuctListGroupBox)
        self.productComboBox.setObjectName("comboBox")

        self.productComboBox.addItems(self.getProductNames())
        self.downHorizontalLayout.addWidget(self.productComboBox)

        self.quantityLabel = QtWidgets.QLabel(self.procuctListGroupBox)
        self.quantityLabel.setObjectName("quantityLabel")
        self.quantityLabel.setText("Cantidad :")
        self.downHorizontalLayout.addWidget(self.quantityLabel)
        self.quantityLabel.setText("Cantidad :")

        self.spinBox = QtWidgets.QSpinBox(self.procuctListGroupBox)
        self.spinBox.setObjectName("spinBox")
        self.downHorizontalLayout.addWidget(self.spinBox)
        self.downVerticalLayout.addLayout(self.downHorizontalLayout)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.addProductButton = QtWidgets.QPushButton(self.procuctListGroupBox)
        self.addProductButton.setIcon(IconProvider.getIconByName('add'))
        self.addProductButton.setObjectName("addProductButton")
        self.addProductButton.setText('Añadir Producto')
        self.horizontalLayout.addWidget(self.addProductButton)
        self.addProductButton.clicked.connect(self.addProductAction)

        self.deleteProductButton = QtWidgets.QPushButton(self.procuctListGroupBox)
        self.deleteProductButton.setIcon(IconProvider.getIconByName('delete'))
        self.deleteProductButton.setObjectName("deleteProductButton")
        self.deleteProductButton.setText('Eliminar Producto')
        self.horizontalLayout.addWidget(self.deleteProductButton)
        self.deleteProductButton.clicked.connect(self.deleteProductAction)

        self.downVerticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.procuctListGroupBox)

        self.buttonsHorizontalLayout = QtWidgets.QHBoxLayout()
        self.buttonsHorizontalLayout.setObjectName("buttonsHorizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonsHorizontalLayout.addItem(spacerItem)

        self.acceptButton = QtWidgets.QPushButton(self)
        self.acceptButton.setObjectName("addOrerButton")
        self.acceptButton.clicked.connect(self.acceptButtonAction)
        self.buttonsHorizontalLayout.addWidget(self.acceptButton)

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText('Cancelar')
        self.buttonsHorizontalLayout.addWidget(self.cancelButton)
        self.cancelButton.clicked.connect(self.cancelButtonAction)

        self.verticalLayout.addLayout(self.buttonsHorizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(self)

    def getOrder(self):

        order = Order()

        order.requestDate = datetime.strptime(self.dateEdit.text(), '%d/%m/%Y')
        order.orderID = self.orderIDEdit.text()
        order.price = self.calculatePaidPrice()
        order.customer = self.customerEdit.text()
        order.status = self.orderEstatusComboBox.currentText()
        order.deliveryTime = self.deliveryTimeComboBox.currentText()
        list_of_products = []
        amountOfProducts = []
        for product, quatity in self.productListTable.getProductList():
            list_of_products.append(product.productID)
            amountOfProducts.append(quatity)
        order.amountOfProducts = amountOfProducts
        order.listOfProducts = list_of_products
        return order

    def setOrder(self,order):

        self.dateEdit.setDate(QtCore.QDate.fromString(order.requestDate.strftime("%d-%m-%Y"), "dd-MM-yyyy"))
        self.orderIDEdit.setText(order.orderID)
        self.customerEdit.setText(order.customer)
        self.paidPriceEdit.setText(str(order.price) + ' ' + '€')

        self.orderEstatusComboBox.setCurrentText(order.status)
        self.deliveryTimeComboBox.setCurrentText(order.deliveryTime)

        self.productListTable.setProductList(order.listOfProducts,order.amountOfProducts)

    def addProductAction(self):
        product = self.listOfProducts[self.productComboBox.currentIndex()]
        quantity = self.spinBox.value()
        if quantity == 0:
            return
        self.productListTable.addProduct(product, quantity)
        self.displayPaidPrice()
        self.spinBox.setValue(0)
        self.spinBox.repaint()

    def deleteProductAction(self):
        self.productListTable.deleteProduct()
        self.displayPaidPrice()

    def displayPaidPrice(self):

        self.paidPriceEdit.setText(str(self.calculatePaidPrice()) + ' ' + '€')
        self.paidPriceEdit.repaint()

    def calculatePaidPrice(self):
        totalPaid = 0
        for product, quantity in self.productListTable.productListAtTable:
            totalPaid = totalPaid + float(product.price) * quantity
        return totalPaid

    def cancelButtonAction(self):
        self.close()

    def accetButtonAction(self):
        raise NotImplementedError

    def getProductNames(self):
        productNames = []

        if self.listOfProducts is not None:
            for product in self.listOfProducts:
                productNames.append(product.name)
        else:
            QtWidgets.QMessageBox.critical(self, "Eliminar Cliente", "No hay productos en la base de datos ",
                                           QtWidgets.QMessageBox.Ok)
        return productNames


class ProductListTable(EditDataTable):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.productListAtTable = []
        self.persistanceFacility = RestFullAPIFacility.getInstance()

    def setProductList(self, listOfProdutIDs, amountOfProductsList):

        for productID in listOfProdutIDs:
            product = self.persistanceFacility.retrieve_product(productID)
            index = listOfProdutIDs.index(productID)
            self.productListAtTable.append((product, amountOfProductsList[index]))
            self.addProductToTable(product.name,  amountOfProductsList[index])

    def addProductToTable(self,product, quantity):
        insertRow = self.rowCount()
        self.setRowCount(self.rowCount() + 1)

        if type(product).__name__ == 'Product':
            self.setItem(insertRow, 0, QtWidgets.QTableWidgetItem(product.name))
        else:
            self.setItem(insertRow, 0, QtWidgets.QTableWidgetItem(product))

        self.setItem(insertRow, 1, QtWidgets.QTableWidgetItem(str(quantity)))

    def getProductList(self):
        productList = []
        for product, quantity in self.productListAtTable:
            productList.append((product, quantity))

        return productList

    def deleteProduct(self):
        selectedRows = self.selectedItems()

        if selectedRows:
            row = selectedRows[0].row()
            self.removeRow(row)
            self.clearSelection()
            self.productListAtTable.pop(row)

        else:
            QtWidgets.QMessageBox.critical(self, "Eliminar Cliente", "Seleccione un cliente a eliminar ",
                                           QtWidgets.QMessageBox.Ok)


    def addProduct(self, product, quantity):

        if type(product) is Product:
            self.addProductToTable(product.anme, quantity)
            self.productListAtTable.append((product, quantity))

        else:
            self.addProductToTable(product, quantity)
            retrievedProduct = self.persistanceFacility.retrieve_product(product.productID)
            self.productListAtTable.append((retrievedProduct, quantity))


class EditOrderDialog(AbstractOrderDialog):

    def __init__(self, order=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Pedido")
        self.acceptButton.setText("Modificar")
        self.orderIDEdit.setEnabled(False)
        if order is not None:
            self.setOrder(order)

    def acceptButtonAction(self):
        order = self.getOrder()
        try:
            self.persistanceFacility.retrieve_customer(order.customer)
        except DataPersistancesError as error:
            QtWidgets.QMessageBox.critical(self, "Lista de Productos", "El Cliente NO existe",
                                           QtWidgets.QMessageBox.Ok)
            return
        # Verificar que tenemos algun producto
        if order.price == 0:
            QtWidgets.QMessageBox.critical(self, "Lista de Productos", "Debes añadir algún producto al pedido",
                                           QtWidgets.QMessageBox.Ok)
            return

        self.accept()


class AddOrderDialog(AbstractOrderDialog):

    def __init__(self, customer = None, parent=None):
        super().__init__(None, parent)
        self.setWindowTitle("Añadir Pedido")
        self.acceptButton.setText("Añadir")
        # self.orderIDEdit.setText()
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.persistanceFacility = RestFullAPIFacility.getInstance()

    # def calculateOrderIDSeed(self):
    #     day = date.today().isoweekday()
    #     weekNumber = date.today().isocalendar()[1]
    #     year = date.today().year
    #     return str(year) + '/' + str(weekNumber) + '/' + str(day) + '/'

    def acceptButtonAction(self):
        order = self.getOrder()
        if order.orderID != '':
            # Vefificar que no existe otra orden con el mismo ID
            try:
                self.persistanceFacility.retrieve_order(order.orderID)
            except DataPersistancesError as error:
                if error.responseCode != 404:
                    QtWidgets.QMessageBox.critical(self, "Lista de Productos",
                                                   "Pedido ID ya existente",
                                                   QtWidgets.QMessageBox.Ok)
                    return
        try:
            self.persistanceFacility.retrieve_customer(order.customer)

        except DataPersistancesError as error:
            QtWidgets.QMessageBox.critical(self, "Lista de Productos", "El Cliente NO existe",
                                           QtWidgets.QMessageBox.Ok)
            return
        # Verificar que tenemos algun producto
        if order.price == 0:
            QtWidgets.QMessageBox.critical(self, "Lista de Productos", "Debes añadir algún producto al pedido",
                                           QtWidgets.QMessageBox.Ok)
            return
        self.accept()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    order = Order("01/6/25/2019", "621457412", "Pagado", "10/12/2020",
                   [("ARRO_AB", 3), ("ARRO_NE", 5), ("ARRO_VE", 10)], "50.50", "15:30")

    orderDialog = EditOrderDialog(order)
    orderDialog.show()
    if orderDialog.exec_():
        retreivedOrder = orderDialog.getOrder()
        print(retreivedOrder)

    sys.exit(app.exec_())
