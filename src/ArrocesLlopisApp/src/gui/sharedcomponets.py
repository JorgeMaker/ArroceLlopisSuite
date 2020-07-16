#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets
import os

class IconProvider(object):
    """ This class is used to provide icons for the rest of the application
        hiding the location of the resources
    """
    @staticmethod
    def getIconByName(icoName):

        file_index = {
            "customers": "user.png",
            "orders": "order.png",
            "products": "products.png",
            "load": "load.png",
            "add": "add.png",
            "edit": "edit.png",
            "delete": "delete.png",
            "search": "search.png",
            "connect": "connect.png",
            "disconnect": "disconnect.png",
            "configure": "configure.png"
        }
        currentDir = os.path.dirname(__file__)
        icon_path = os.path.join(currentDir, "resources", file_index[icoName])
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal,
                      QtGui.QIcon.Off)
        return icon

class EditDataTable(QtWidgets.QTableWidget):
    """This class is used to display endpoint information in a listed view  """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hedprops = None
        self.hedlabels = None
        self.horizontalHeader().setVisible(True)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(self.NoSelection)
        self.setAlternatingRowColors(True)
        self.verticalHeader().hide()

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setDragDropOverwriteMode(False)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSortingEnabled(False)
        self.setWordWrap(False)
        self.verticalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setStretchLastSection(True)

    def setHeaderContent(self, hedlabels, hedprops):
        self.hedprops = hedprops
        self.hedlabels = hedlabels
        self.setColumnCount(len(hedlabels))
        self.setHorizontalHeaderLabels(hedlabels)
        for i, sz in enumerate(self.hedprops):
            self.horizontalHeader().resizeSection(i, sz)
        self.setSelectionBehavior(self.SelectRows)

    def resizeEvent(self, event):
        selfsz = event.size().width()
        totalprops = sum(self.hedprops)
        newszs = [sz * selfsz / totalprops for sz in self.hedprops]
        for i, sz in enumerate(newszs):
            self.horizontalHeader().resizeSection(i, sz)


provincias = [  'Madrid',
                'A Coruña',
                'Álava',
                'Albacete',
                'Alicante',
                'Almería',
                'Asturias',
                'Ávila',
                'Badajoz',
                'Islas Baleares',
                'Barcelona',
                'Burgos',
                'Cáceres',
                'Cádiz',
                'Cantabria',
                'Castellón',
                'Ciudad Real',
                'Córdoba',
                'Cuenca',
                'Girona',
                'Granada',
                'Guadalajara',
                'Guipúzcoa',
                'Huelva',
                'Huesca',
                'Jaén',
                'La Rioja',
                'Las Palmas',
                'León',
                'Lleida',
                'Lugo',
                'Málaga',
                'Murcia',
                'Navarra',
                'Orense',
                'Palencia',
                'Pontevedra',
                'Salamanca',
                'Segovia',
                'Sevilla',
                'Soria',
                'Tarragona',
                'Santa Cruz de Tenerife',
                'Teruel',
                'Toledo',
                'Valencia',
                'Valladolid',
                'Vizcaya',
                'Zamora',
                'Zaragoza']
