from PyQt5 import QtCore, QtWidgets
from dataaccesfacility.datamodel import Configuration

class ConnectDialog(QtWidgets.QDialog):

    def __init__(self,configuration=None, parent=None):
        super().__init__(parent)
        self.setupUi(configuration)

    def setupUi(self,configuration=None):

        self.setObjectName("Dialog")
        self.resize(459, 160)
        self.setWindowTitle("Configuración Base de Datos")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Congiguración:")

        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")

        self.passwordLabel = QtWidgets.QLabel(self.groupBox)
        self.passwordLabel.setObjectName("passwordLabel")
        self.passwordLabel.setText("Contraseña:")
        self.gridLayout.addWidget(self.passwordLabel, 1, 2, 1, 1)

        self.userNameLabel = QtWidgets.QLabel(self.groupBox)
        self.userNameLabel.setObjectName("userNameLabel")
        self.userNameLabel.setText("Usuario:")
        self.gridLayout.addWidget(self.userNameLabel, 1, 0, 1, 1)

        self.passwordEdit = QtWidgets.QLineEdit(self.groupBox)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setClearButtonEnabled(False)
        self.passwordEdit.setObjectName("passwordEdit")
        self.gridLayout.addWidget(self.passwordEdit, 1, 3, 1, 1)

        self.portLabel = QtWidgets.QLabel(self.groupBox)
        self.portLabel.setObjectName("portLabel")
        self.portLabel.setText("Port:")
        self.gridLayout.addWidget(self.portLabel, 0, 2, 1, 1)

        self.hostEdit = QtWidgets.QLineEdit(self.groupBox)
        self.hostEdit.setObjectName("hostEdit")
        self.gridLayout.addWidget(self.hostEdit, 0, 1, 1, 1)

        self.userEdit = QtWidgets.QLineEdit(self.groupBox)
        self.userEdit.setObjectName("userEdit")
        self.gridLayout.addWidget(self.userEdit, 1, 1, 1, 1)

        self.hostLabel = QtWidgets.QLabel(self.groupBox)
        self.hostLabel.setObjectName("hostLabel")
        self.hostLabel.setText("Host:")
        self.gridLayout.addWidget(self.hostLabel, 0, 0, 1, 1)

        self.portEdit = QtWidgets.QLineEdit(self.groupBox)
        self.portEdit.setObjectName("portEdit")
        self.gridLayout.addWidget(self.portEdit, 0, 3, 1, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.acceptButton = QtWidgets.QPushButton(self)
        self.acceptButton.setObjectName("acceptButton")
        self.acceptButton.setText("Connectar")
        self.acceptButton.clicked.connect(self.acceptButtonAction)
        self.horizontalLayout.addWidget(self.acceptButton)

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Cancelar")
        self.cancelButton.clicked.connect(self.cancelButtonAction)
        self.horizontalLayout.addWidget(self.cancelButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.setConfiguration(configuration)

        QtCore.QMetaObject.connectSlotsByName(self)

    def getConfiguration(self):

        configuration = Configuration()

        configuration.port = self.portEdit.text()
        configuration.user_name = self.userEdit.text()
        configuration.host = self.hostEdit.text()
        return configuration

    def getPassWord(self):
        return self.passwordEdit.text()

    def setConfiguration(self, configuration):
        if configuration is not None:
            self.portEdit.setText(configuration.port)
            self.userEdit.setText(configuration.user_name)
            self.hostEdit.setText(configuration.host)

    def acceptButtonAction(self):
        self.accept()

    def cancelButtonAction(self):
        self.close()