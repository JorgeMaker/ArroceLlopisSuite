#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets

from customersdialog import EditCustomerDialog, AddCustomerDialog
from orderdialogs import EditOrderDialog, AddOrderDialog
from productdialogs import EditProductDialog, AddProductDialog
from searchcustomerdialog import SearchCustomerDialog
from searchorderdialog import SearchOrderDialog
from sharedcomponets import IconProvider, EditDataTable

from dataaccesfacility.datamodel import Product, Customer, Order

from restfullapifacility import RestFullAPIFacility, DataPersistancesError


class AbstractManagementTool(QtWidgets.QWidget):
    """This class is the base calla used to create all different tools used to
        manage each API Rest endpoint
    """
    def __init__(self, hedlabels, hedprops,parent=None):
        """Constructor for ToolsWidget"""
        super(QtWidgets.QWidget, self).__init__(parent)
        self.setObjectName("AbstractManagementTool")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = EditDataTable(self)
        self.tableWidget.setHeaderContent(hedlabels,hedprops)
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.loadButton = QtWidgets.QPushButton(self)
        self.loadButton.setIcon(IconProvider.getIconByName("load"))
        self.loadButton.setObjectName("loadButton")
        self.loadButton.setText("Cargar")
        self.loadButton.clicked.connect(self.loadButtonAction)
        self.horizontalLayout.addWidget(self.loadButton)

        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.setIcon(IconProvider.getIconByName("add"))
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Añadir")
        self.addButton.clicked.connect(self.addButtonAction)
        self.horizontalLayout.addWidget(self.addButton)

        self.editButton = QtWidgets.QPushButton(self)
        self.editButton.setIcon(IconProvider.getIconByName("edit"))
        self.editButton.setObjectName("editButton")
        self.editButton.setText("Editar")
        self.editButton.clicked.connect(self.editButtonAction)
        self.horizontalLayout.addWidget(self.editButton)

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.setIcon(IconProvider.getIconByName('delete'))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setText("Eliminar")
        self.deleteButton.clicked.connect(self.deleteButtonAction)
        self.horizontalLayout.addWidget(self.deleteButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

    def loadButtonAction(self):
        raise NotImplementedError

    def addButtonAction(self):
        raise NotImplementedError

    def editButtonAction(self):
        raise NotImplementedError

    def deleteButtonAction(self):
        raise NotImplementedError


class OrdersManagementTool(AbstractManagementTool):
    """  """
    def __init__(self, hedlabels, hedprops,parent=None):
        """Constructor for ToolsWidget"""
        super().__init__(hedlabels, hedprops,parent)
        self.setObjectName("ordersTab")
        self.tableWidget.doubleClicked.connect(self.doubleClickedTable)

        self.searchButton = QtWidgets.QPushButton(self)
        self.searchButton.setIcon(IconProvider.getIconByName("search"))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Buscar")
        self.searchButton.clicked.connect(self.searchButtonAction)
        self.horizontalLayout.addWidget(self.searchButton)

    def doubleClickedTable(self):
        index = self.tableWidget.selectedIndexes()[0]
        orderID = self.tableWidget.item(index.row(), 0).text()

        persistanceFacility = RestFullAPIFacility.getInstance()

        if persistanceFacility.isAuthenticated():
            try:
                order = persistanceFacility.retrieve_order(orderID)
            except DataPersistancesError as error:
                if error.responseCode == 401:
                    message = "Error cargando pedidos el token de acceso " \
                              "ha caducado, renuevalo"
                else:
                    message = "Error cargando Pedidos: Código[{}] Mensaje :{}".format(
                    error.responseCode, error.message)
                QtWidgets.QMessageBox.critical(self, "Cargar  pedidos",
                                               message,
                                               QtWidgets.QMessageBox.Ok)
                return

            orderDialog = EditOrderDialog(order)
            orderDialog.setWindowModality(QtCore.Qt.ApplicationModal)
            if orderDialog.exec_():
                modifiedOrded = orderDialog.getOrder()
                if persistanceFacility.isAuthenticated():
                    persistanceFacility.update_order(modifiedOrded)
                    self.updateOrderAtTable(modifiedOrded)

    def loadButtonAction(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        persistanceFacility = RestFullAPIFacility.getInstance()

        if persistanceFacility.isAuthenticated():
            persistanceFacility = RestFullAPIFacility.getInstance()

            try:
                ordersList = persistanceFacility.retrieve_all_orders()

            except DataPersistancesError as error:
                if error.responseCode == 401:
                    message = "Error cargando pedidos el token de acceso " \
                              "ha caducado, renuevalo"
                else:
                    message = "Error cargando Pedidos: Código[{}] Mensaje :{}".format(
                        error.responseCode, error.message)
                QtWidgets.QMessageBox.critical(self, "Cargar  pedidos",
                                               message,
                                               QtWidgets.QMessageBox.Ok)
                return

            if ordersList is not None:
                for order in ordersList:
                    self.addOrderToTable(order)
        else:
            QtWidgets.QMessageBox.critical(self, "Cargar  Pedidos", "Autetifique con el servidor",
                                           QtWidgets.QMessageBox.Ok)

    def addButtonAction(self):

        orderDialog = AddOrderDialog()
        orderDialog.setWindowModality(QtCore.Qt.ApplicationModal)

        if orderDialog.exec_():
            order = orderDialog.getOrder()
            self.addOrder(order)

    def editButtonAction(self):

        selectedRows = self.tableWidget.selectedItems()

        if selectedRows:
            index = self.tableWidget.selectedIndexes()[0]
            orderID = self.tableWidget.item(index.row(), 0).text()
            persistanceFacility = RestFullAPIFacility.getInstance()
            if persistanceFacility.isAuthenticated():
                try:
                    order = persistanceFacility.retrieve_order(orderID)
                except DataPersistancesError as error:
                    if error.responseCode == 401:
                        message = "Error cargando pedidos el token de acceso " \
                                  "ha caducado, renuevalo"
                    else:
                        message = "Error cargando Pedidos: Código[{}] Mensaje :{}".format(
                            error.responseCode, error.message)
                    QtWidgets.QMessageBox.critical(self, "Cargar  pedidos",
                                                   message,
                                                   QtWidgets.QMessageBox.Ok)
                    return
                orderDialog = EditOrderDialog(order)
                orderDialog.setWindowModality(QtCore.Qt.ApplicationModal)
                if orderDialog.exec_():
                    modifiedOrder = orderDialog.getOrder()

                    if persistanceFacility.isAuthenticated():
                        persistanceFacility.update_order(modifiedOrder)
                        self.updateOrderAtTable(order)
            else:
                QtWidgets.QMessageBox.critical(self, "Editar  Pedido", "Autentifique con el servidor",
                                               QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.critical(self, "Editar pedido", "Seleccione un pedido a editar",
                                               QtWidgets.QMessageBox.Ok)

    def deleteButtonAction(self):
        selectedRows = self.tableWidget.selectedItems()
        if selectedRows:
            row = selectedRows[0].row()
            orderID = self.tableWidget.item(row, 0).text()

            if self.deleteOrder(orderID):
                self.tableWidget.removeRow(row)
                self.tableWidget.clearSelection()
        else:
            QtWidgets.QMessageBox.critical(self, "Eliminar Pedido", "Seleccione un pedido a eliminar ",

                                           QtWidgets.QMessageBox.Ok)
    def searchButtonAction(self):
        searchOrderDialog = SearchOrderDialog()
        searchOrderDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        if searchOrderDialog.exec_():
            query = searchOrderDialog.getSearchQuery()
            persistanceFacility = RestFullAPIFacility.getInstance()
            if persistanceFacility.isAuthenticated():
                try:
                    listOfOrders = persistanceFacility.searchOrders(query)
                except DataPersistancesError as error:
                    if error.responseCode == 401:
                        message = "Error cargando pedidos el token de acceso " \
                                  "ha caducado, renuevalo"
                    else:
                        message = "Error cargando Pedidos: Código[{}] Mensaje :{}".format(
                            error.responseCode, error.message)
                    QtWidgets.QMessageBox.critical(self, "Cargar pedidos",
                                                   message,
                                                   QtWidgets.QMessageBox.Ok)
                    return

                if listOfOrders is None:
                    self.tableWidget.clearContents()
                    self.tableWidget.setRowCount(0)
                elif type(listOfOrders) is Order:
                    self.tableWidget.clearContents()
                    self.tableWidget.setRowCount(0)
                    self.addOrderToTable(listOfOrders)
                else:
                    self.tableWidget.clearContents()
                    self.tableWidget.setRowCount(0)
                    for order in listOfOrders:
                        self.addOrderToTable(order)

    def addOrder(self, order):
        persistanceFacility = RestFullAPIFacility.getInstance()
        if persistanceFacility.isAuthenticated():
            try:
                persistanceFacility.add_order(order)
            except DataPersistancesError as error:
                if error.responseCode == 401:
                    message = "Error añadiendo pedidos el token de acceso " \
                              "ha caducado, renuevalo"
                else:
                    message = "Error añadiendo Pedidos: Código[{}] Mensaje :{}".format(
                        error.responseCode, error.message)
                QtWidgets.QMessageBox.critical(self, "Cargar  pedidos",
                                               message,
                                               QtWidgets.QMessageBox.Ok)
                return
            self.addOrderToTable(order)

    def addOrderToTable(self, order):

        insertRow = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

        self.tableWidget.setItem(insertRow, 0, QtWidgets.QTableWidgetItem(order.orderID))
        persistanceFacility = RestFullAPIFacility.getInstance()
        try:
            customer = persistanceFacility.retrieve_customer(order.customer)
        except DataPersistancesError as error:
            if error.responseCode == 401:
                message = "Error añadiendo pedidos el token de acceso " \
                          "ha caducado, renuevalo"
            else:
                message = "Error añadiendo Pedidos: Código[{}] Mensaje :{}".format(
                    error.responseCode, error.message)
            QtWidgets.QMessageBox.critical(self, "Cargar  pedidos",
                                           message,
                                           QtWidgets.QMessageBox.Ok)
            return

        self.tableWidget.setItem(insertRow, 1, QtWidgets.QTableWidgetItem(customer.name + ' '+ customer.surnames))
        self.tableWidget.setItem(insertRow, 2, QtWidgets.QTableWidgetItem(order.customer))
        self.tableWidget.setItem(insertRow, 3, QtWidgets.QTableWidgetItem(order.requestDate.strftime("%d-%m-%Y")))
        self.tableWidget.setItem(insertRow, 4, QtWidgets.QTableWidgetItem(order.deliveryTime))
        self.tableWidget.setItem(insertRow, 5, QtWidgets.QTableWidgetItem(order.status))
        self.tableWidget.setItem(insertRow, 6, QtWidgets.QTableWidgetItem(str(order.price) + ' €'))

    def updateOrderAtTable(self, order):

        orderID = order.orderID
        orderIndex = self.getRowByOrderID(orderID)

        self.tableWidget.setItem(orderIndex, 0, QtWidgets.QTableWidgetItem(order.orderID))
        persistanceFacility = RestFullAPIFacility.getInstance()
        try:
            customer = persistanceFacility.retrieve_customer(order.customer)
        except DataPersistancesError as error:
            if error.responseCode == 401:
                message = "Error cargando pedidos el token de acceso " \
                          "ha caducado, renuevalo"
            else:
                message = "Error cargando Pedidos: Código[{}] Mensaje :{}".format(
                    error.responseCode, error.message)
            QtWidgets.QMessageBox.critical(self, "Cargar  pedidos",
                                           message,
                                           QtWidgets.QMessageBox.Ok)
            return

        self.tableWidget.setItem(orderIndex, 1, QtWidgets.QTableWidgetItem(customer.name + ' ' + customer.surnames))
        self.tableWidget.setItem(orderIndex, 2, QtWidgets.QTableWidgetItem(order.customer))
        self.tableWidget.setItem(orderIndex, 3, QtWidgets.QTableWidgetItem(order.requestDate.strftime("%d-%m-%Y")))
        self.tableWidget.setItem(orderIndex, 4, QtWidgets.QTableWidgetItem(order.deliveryTime))
        self.tableWidget.setItem(orderIndex, 5, QtWidgets.QTableWidgetItem(order.status))
        self.tableWidget.setItem(orderIndex, 6, QtWidgets.QTableWidgetItem(str(order.price) + ' €'))

    def getListOfProductsString(self, list_of_products):

        productListString = ''

        for procuctOrdered in list_of_products:
            productName = procuctOrdered[0]
            productQuantity = procuctOrdered[1]
            productListString = productListString + productName + 'x' + str(productQuantity)+ '  '

        return productListString

    def deleteOrder(self, orderID):

        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("Eliminación del Pedido definitiva")
        msgBox.setInformativeText('Desea realmente eliminar la orden con ID '+ orderID + ' ?')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)

        if msgBox.exec_() == QtWidgets.QMessageBox.Yes:
            persistanceFacility = RestFullAPIFacility.getInstance()
            if persistanceFacility.isAuthenticated():
                try:
                    persistanceFacility.delete_order(orderID)
                except DataPersistancesError as error:
                    if error.responseCode == 401:
                        message = "Error cargando pedidos el token de acceso " \
                                  "ha caducado, renuevalo"
                    else:
                        message = "Error cargando Pedidos: Código[{}] Mensaje :{}".format(
                            error.responseCode, error.message)
                        QtWidgets.QMessageBox.critical(self, "Cargar  pedidos",
                                                       message,
                                                       QtWidgets.QMessageBox.Ok)
                        return
                return True
            else:
                return False
        else:
            return False

    def getRowByOrderID(self, orderID):

        for index in range(self.tableWidget.rowCount()):
            searcheadID = self.tableWidget.item(index, 0).text()
            if searcheadID == orderID:
                return index


class CustomerManagementTool(AbstractManagementTool):
    """  """

    def __init__(self, hedlabels, hedprops,parent=None):
        """Constructor for ToolsWidget"""
        super().__init__(hedlabels, hedprops,parent)
        self.setObjectName("customersTab")
        self.tableWidget.doubleClicked.connect(self.doubleClickedTable)

        self.searchButton = QtWidgets.QPushButton(self)
        self.searchButton.setIcon(IconProvider.getIconByName("search"))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Buscar")
        self.searchButton.clicked.connect(self.searchButtonAction)
        self.horizontalLayout.addWidget(self.searchButton)

    def doubleClickedTable(self):

        index = self.tableWidget.selectedIndexes()[0]
        customerID = self.tableWidget.item(index.row(), 6).text()
        persistanceFacility = RestFullAPIFacility.getInstance()
        if persistanceFacility.isAuthenticated():
            customer = persistanceFacility.retrieve_customer(customerID)
            customerDialog = EditCustomerDialog(customer)
            customerDialog.setWindowModality(QtCore.Qt.ApplicationModal)
            if customerDialog.exec_():
                customer = customerDialog.getCustomer()
                persistanceFacility = RestFullAPIFacility.getInstance()
                if persistanceFacility.isAuthenticated():
                    persistanceFacility.update_customer(customer)
                    self.updateCustomerAttable(customer)

    def loadButtonAction(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        persistanceFacility = RestFullAPIFacility.getInstance()
        if persistanceFacility.isAuthenticated():
            customerList = None
            try:
                customerList = persistanceFacility.retrieve_all_customers()
            except DataPersistancesError as error:
                message = "Error cargando clientes Código[{}] Mensaje :{}".format(error.responseCode, error.message)
                QtWidgets.QMessageBox.critical(self, "Cargar  clientes",
                                               message,
                                               QtWidgets.QMessageBox.Ok)
            if customerList is None:
                pass
            else:
                if type(customerList) is Customer:
                    self.addCustomerToTable(customerList)
                else:
                    for customer in customerList:
                        self.addCustomerToTable(customer)
        else:
            QtWidgets.QMessageBox.critical(self, "Cargar  clientes", "Autetifique con el servidor",
                                           QtWidgets.QMessageBox.Ok)

    def addButtonAction(self):
        customerDialog = AddCustomerDialog()
        customerDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        if customerDialog.exec_():
            customer = customerDialog.getCustomer()
            self.addCustomer(customer)

    def editButtonAction(self):
        selectedRows = self.tableWidget.selectedItems()

        if selectedRows:
            index = self.tableWidget.selectedIndexes()[0]
            customerID = self.tableWidget.item(index.row(), 6).text()
            persistanceFacility = RestFullAPIFacility.getInstance()
            if persistanceFacility.isAuthenticated():
                customer = persistanceFacility.retrieve_customer(customerID)
                customerDialog = EditCustomerDialog(customer)
                customerDialog.setWindowModality(QtCore.Qt.ApplicationModal)
                if customerDialog.exec_():
                    customer = customerDialog.getCustomer()
                    persistanceFacility = RestFullAPIFacility.getInstance()
                    if persistanceFacility.isAuthenticated():
                        persistanceFacility.update_customer(customer)
                        self.updateCustomerAttable(customer)
            else:
                QtWidgets.QMessageBox.critical(self, "Editar  Cliente", "Autetifique con el servidor",
                                               QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.critical(self, "Editar  Cliente", "Seleccione un cliente a editar ",
                                               QtWidgets.QMessageBox.Ok)

    def deleteButtonAction(self):

        selectedRowsItems = self.tableWidget.selectedItems()

        if selectedRowsItems:
            row = selectedRowsItems[0].row()
            customerID = self.tableWidget.item(row, 6).text()

            if self.deleteCustomer(customerID):
                self.tableWidget.removeRow(row)
                self.tableWidget.clearSelection()
        else:
            QtWidgets.QMessageBox.critical(self, "Eliminar Cliente", "Seleccione un cliente a eliminar ",
                                           QtWidgets.QMessageBox.Ok)

    def searchButtonAction(self):

        searchCustomerDialog = SearchCustomerDialog()
        searchCustomerDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        if searchCustomerDialog.exec_():
            query = searchCustomerDialog.getSearchQuery()
            persistanceFacility = RestFullAPIFacility.getInstance()
            if persistanceFacility.isAuthenticated():
                listOfCustomers = persistanceFacility.searchCustomers(query)

                if listOfCustomers is None:
                    self.tableWidget.clearContents()
                    self.tableWidget.setRowCount(0)
                elif type(listOfCustomers) is Customer:
                    self.tableWidget.clearContents()
                    self.tableWidget.setRowCount(0)
                    self.addCustomerToTable(listOfCustomers)
                else:
                    self.tableWidget.clearContents()
                    self.tableWidget.setRowCount(0)
                    for customer in listOfCustomers:
                        self.addCustomerToTable(customer)

    def addCustomer(self, customer):
        persistanceFacility = RestFullAPIFacility.getInstance()
        if persistanceFacility.isAuthenticated():
            try:
                persistanceFacility.add_customer(customer)
            except DataPersistancesError as error:
                QtWidgets.QMessageBox.critical(self, "Añadir cliente",
                                               "Error al añadir un clinete\n"+
                                               error.message,
                                               QtWidgets.QMessageBox.Ok)
            self.addCustomerToTable(customer)

    def addCustomerToTable(self, customer):

        insertRow = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

        self.tableWidget.setItem(insertRow, 0, QtWidgets.QTableWidgetItem(customer.name))
        self.tableWidget.setItem(insertRow, 1, QtWidgets.QTableWidgetItem(customer.surnames))
        self.tableWidget.setItem(insertRow, 2, QtWidgets.QTableWidgetItem(customer.telNumbers))
        self.tableWidget.setItem(insertRow, 3, QtWidgets.QTableWidgetItem(customer.email))
        self.tableWidget.setItem(insertRow, 4,
                                 QtWidgets.QTableWidgetItem(customer.address.street + '  ' + customer.address.flat))
        self.tableWidget.setItem(insertRow, 5, QtWidgets.QTableWidgetItem(customer.registrationDate.strftime("%d-%m-%Y")))
        self.tableWidget.setItem(insertRow, 6,
                             QtWidgets.QTableWidgetItem(customer.customerID))

    def updateCustomerAttable(self, customer):

        customerID = customer.customerID
        customerIndex = self.getRowByCustomerID(customerID)
        self.tableWidget.setItem(customerIndex, 0, QtWidgets.QTableWidgetItem(customer.name))
        self.tableWidget.setItem(customerIndex, 1, QtWidgets.QTableWidgetItem(customer.surnames))
        self.tableWidget.setItem(customerIndex, 2, QtWidgets.QTableWidgetItem(customer.telNumbers))
        self.tableWidget.setItem(customerIndex, 3, QtWidgets.QTableWidgetItem(customer.email))
        self.tableWidget.setItem(customerIndex, 4,
                                 QtWidgets.QTableWidgetItem(customer.address.street + '  ' + customer.address.flat))
        self.tableWidget.setItem(customerIndex, 5, QtWidgets.QTableWidgetItem(customer.registrationDate.strftime('%d-%m-%y')))
        self.tableWidget.setItem(customerIndex, 6,
                             QtWidgets.QTableWidgetItem(customer.customerID))


    def deleteCustomer(self,customerID):

        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("Eliminación de Cliente definitiva")
        msgBox.setInformativeText('Desea realmente eliminar al clinete con ID ' + customerID + ' ?')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
        if msgBox.exec_() == QtWidgets.QMessageBox.Yes:
            persistanceFacility = RestFullAPIFacility.getInstance()
            if persistanceFacility.isAuthenticated():
                try:
                    persistanceFacility.delete_customer(customerID)
                except DataPersistancesError as error:
                    if error.responseCode == 500:
                        QtWidgets.QMessageBox.critical(self, "Eliminar Cliente",
                                                   "No puede eliminarse un cliente que está en uso",
                                                   QtWidgets.QMessageBox.Ok)
                    elif error.responseCode == 0:
                        QtWidgets.QMessageBox.critical(self, "Eliminar Cliente",
                                                   "Error al conectar con el servidor no se puede elimunar el cliente",
                                                   QtWidgets.QMessageBox.Ok)

                    else:
                        QtWidgets.QMessageBox.critical(self, "Eliminar Cliente",
                                                   "Error al eliminar un cliente [{}]".format(error.responseCode)+
                                                   error.message,
                                                   QtWidgets.QMessageBox.Ok)
                    return False
                return True
            else:
                return False
        else:
            return False

    def getRowByCustomerID(self, customerID):

        for index in range(self.tableWidget.rowCount()):
            searcheadID = self.tableWidget.item(index, 6).text()
            if searcheadID == customerID:
                return index


class ProductsManagementTool(AbstractManagementTool):
    """  """

    def __init__(self, hedlabels, hedprops,parent=None):
        """Constructor for ToolsWidget"""
        super().__init__(hedlabels, hedprops,parent)
        self.setObjectName("productsTab")
        self.tableWidget.doubleClicked.connect(self.doubleClickedTable)

    def doubleClickedTable(self):

        index = self.tableWidget.selectedIndexes()[0]
        productID = self.tableWidget.item(index.row(), 5).text()

        persistanceFacility = RestFullAPIFacility.getInstance()
        if persistanceFacility.isAuthenticated():
            product = persistanceFacility.retrieve_product(productID)
            productDialog = EditProductDialog(product)
            productDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        if productDialog.exec_():
            product = productDialog.getProduct()
            if persistanceFacility.isAuthenticated():
                persistanceFacility.update_product(product)
                self.updateProductAtTable(product)

    def updateProductAtTable(self,product):

        productID = product.productID
        productIndex = self.getRowByProductID(productID)

        self.tableWidget.setItem(productIndex, 0, QtWidgets.QTableWidgetItem(product.name))
        self.tableWidget.setItem(productIndex, 1, QtWidgets.QTableWidgetItem(product.pType))
        self.tableWidget.setItem(productIndex, 2, QtWidgets.QTableWidgetItem(str(product.price)+ ' €'))
        self.tableWidget.setItem(productIndex, 3, QtWidgets.QTableWidgetItem(product.isAvailable))
        self.tableWidget.setItem(productIndex, 4, QtWidgets.QTableWidgetItem(product.version))
        self.tableWidget.setItem(productIndex, 5, QtWidgets.QTableWidgetItem(product.productID))

    def loadButtonAction(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        persistanceFacility = RestFullAPIFacility.getInstance()

        if persistanceFacility.isAuthenticated():
            productsList = persistanceFacility.retrieve_all_products()

            if productsList is None:
                pass
            else:
                if type(productsList) is Product:
                    self.addProductToTable(productsList)
                else:
                    for product in productsList:
                        self.addProductToTable(product)
        else:
            QtWidgets.QMessageBox.critical(self, "Cargar  Productos", "Autetifique con el servidor",
                                           QtWidgets.QMessageBox.Ok)

    def addProductToTable(self, product):

        insertRow = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

        self.tableWidget.setItem(insertRow, 0, QtWidgets.QTableWidgetItem(product.name))
        self.tableWidget.setItem(insertRow, 1, QtWidgets.QTableWidgetItem(product.pType))
        self.tableWidget.setItem(insertRow, 2, QtWidgets.QTableWidgetItem(str(product.price) + ' €'))
        self.tableWidget.setItem(insertRow, 3, QtWidgets.QTableWidgetItem(product.isAvailable))
        self.tableWidget.setItem(insertRow, 4, QtWidgets.QTableWidgetItem(str(product.version)))
        self.tableWidget.setItem(insertRow, 5, QtWidgets.QTableWidgetItem(product.productID))


    def addButtonAction(self):
        productDialog = AddProductDialog()
        productDialog.setWindowModality(QtCore.Qt.ApplicationModal)

        if productDialog.exec_():
            product = productDialog.getProduct()
            self.addProduct(product)

    def editButtonAction(self):

        selectedRows = self.tableWidget.selectedItems()

        if selectedRows:
            index = self.tableWidget.selectedIndexes()[0]
            productID = self.tableWidget.item(index.row(), 5).text()
            persistanceFacility = RestFullAPIFacility.getInstance()
            if persistanceFacility.isAuthenticated():
                product = persistanceFacility.retrieve_product(productID)
                productDialog = EditProductDialog(product)
                productDialog.setWindowModality(QtCore.Qt.ApplicationModal)
                if productDialog.exec_():
                    editedProduct = productDialog.getProduct()
                    persistanceFacility = RestFullAPIFacility.getInstance()
                    if persistanceFacility.isAuthenticated():
                        persistanceFacility.update_product(editedProduct)
                        self.updateProductAtTable(editedProduct)
            else:
                QtWidgets.QMessageBox.critical(self, "Editar  Producto", "Autetifique con el servidor",
                                               QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.critical(self, "Editar  Producto", "Seleccione un producto a editar",
                                           QtWidgets.QMessageBox.Ok)

    def deleteButtonAction(self):

        selectedRows = self.tableWidget.selectedItems()
        if selectedRows:
            row = selectedRows[0].row()
            productID = self.tableWidget.item(row, 5).text()

            if self.deleteProduct(productID):
                self.tableWidget.removeRow(row)
                self.tableWidget.clearSelection()
        else:
            QtWidgets.QMessageBox.critical(self, "Eliminar Producto", "Seleccione un producto a eliminar ",
                                           QtWidgets.QMessageBox.Ok)

    def addProduct(self, product):

        persistanceFacility = RestFullAPIFacility.getInstance()
        if persistanceFacility.isAuthenticated():
            persistanceFacility.add_product(product)
            self.addProductToTable(product)

    def updateProduct(self, product):

        productID = product.productID

        self.productsTableModel.update({productID: product})

        productIndex = self.getRowByProductID(productID)

        self.tableWidget.setItem(productIndex, 0, QtWidgets.QTableWidgetItem(product.name))
        self.tableWidget.setItem(productIndex, 1, QtWidgets.QTableWidgetItem(product.pType))
        self.tableWidget.setItem(productIndex, 2, QtWidgets.QTableWidgetItem(product.price))
        self.tableWidget.setItem(productIndex, 3, QtWidgets.QTableWidgetItem(product.isAvailable))
        self.tableWidget.setItem(productIndex, 4, QtWidgets.QTableWidgetItem(product.version))
        self.tableWidget.setItem(productIndex, 5, QtWidgets.QTableWidgetItem(product.productID))

    def deleteProduct(self, productID):

        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("Eliminación de Producto definitiva")
        msgBox.setInformativeText('Desea realmente eliminar al producto con ID '+ productID + ' ?')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
        if msgBox.exec_() == QtWidgets.QMessageBox.Yes:
            persistanceFacility = RestFullAPIFacility.getInstance()
            if persistanceFacility.isAuthenticated():
                try:
                    persistanceFacility.delete_product(productID)
                    return True
                except DataPersistancesError as error:
                    QtWidgets.QMessageBox.critical(self, "Eliminar Producto", "Producto en uso, mejoer cambiar a estado INDISPONIBLE ",
                                                   QtWidgets.QMessageBox.Ok)
                    return False
            else:
                return False
        else:
            return False

    def getRowByProductID(self, customerID):

        for index in range(self.tableWidget.rowCount()):
            searcheadID = self.tableWidget.item(index, 5).text()
            if searcheadID == customerID:
                return index
