#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from managementtools import OrdersManagementTool, ProductsManagementTool, CustomerManagementTool
from sharedcomponets import IconProvider

class ToolsWidget(QtWidgets.QTabWidget):
    """ This class is used to host each tool used to manage each available
        endpoint
    """
    def __init__(self, parent=None):
        """Constructor for ToolsWidget"""
        super(QtWidgets.QTabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setObjectName("toolsTabWidget")

        self.ordersManagementTool = None
        self.customerManagementTool = None
        self.productsManagementTool = None

        self.tabCloseRequested.connect(self.removeTabHandler)

        self.setStyleSheet("QTabBar::close - button { image: url(close.png) subcontrol - position: left; }")
        self.setStyleSheet("QTabBar::tab { height: 30px; width: 150px;}")

    def removeTabHandler(self, index):

        supressedTab = self.widget(index)
        if type(supressedTab) is OrdersManagementTool:
            self.ordersManagementTool = None
        elif type(supressedTab) is CustomerManagementTool:
            self.customerManagementTool = None
        elif type(supressedTab) is ProductsManagementTool:
            self.productsManagementTool = None

        self.removeTab(index)

    def addCustomersTool(self):
        if self.customerManagementTool is None:

            hedlabels = ('Nombre', 'Apellidos', 'Télefono', 'Email', 'Dirección','Fecha', 'ID Cliente')
            hedprops = (100, 100, 100, 100, 100, 100, 100)
            self.customerManagementTool = CustomerManagementTool(hedlabels, hedprops)
            self.addTab(self.customerManagementTool, IconProvider.getIconByName("customers"), "Clientes")

    def addOrdersTool(self):
        if self.ordersManagementTool is None:
            hedlabels = ('Pedido ID','Nombre Cliente', 'Teléfono','Fecha','Hora Entrega', 'Estado', 'Precio')
            hedprops = (100, 100, 100, 100, 100, 100,100)
            self.ordersManagementTool = OrdersManagementTool(hedlabels, hedprops)
            self.addTab(self.ordersManagementTool, IconProvider.getIconByName("orders"), "Pedidos")

    def addProductsTool(self):
        if self.productsManagementTool is None:
            hedlabels = ('Nombre', 'Tipo', 'Precio', 'Estatus', 'Versión', 'Product ID')
            hedprops = (200, 100, 100, 100, 100, 100)
            self.productsManagementTool = ProductsManagementTool(hedlabels, hedprops)
            self.addTab(self.productsManagementTool, IconProvider.getIconByName("products"), "Productos")