from PyQt5 import QtCore, QtGui, QtWidgets

class ProductDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Add New Product")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(255, 255, 255);
            }
            QLineEdit {
                width: 247px;
                height: 29px;
                border-radius: 8px;
                border: 1px solid #404040;
                background: #FFF;
                padding: 5px;
            }
            QPushButton {
                color: #FFF;
                font-family: Roboto;
                font-size: 12px;
                font-weight: 500;
                border-radius: 8px;
                background: #9747FF;
                padding: 10px;
            }
            QLabel {
                color: #404040;
                font-family: Roboto;
                font-size: 12px;
                font-weight: 500;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        # Product Name
        name_layout = QtWidgets.QHBoxLayout()
        self.name_label = QtWidgets.QLabel("Product Name:")
        self.name_input = QtWidgets.QLineEdit()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Description
        desc_layout = QtWidgets.QHBoxLayout()
        self.desc_label = QtWidgets.QLabel("Description:")
        self.desc_input = QtWidgets.QLineEdit()
        desc_layout.addWidget(self.desc_label)
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)

        # Price
        price_layout = QtWidgets.QHBoxLayout()
        self.price_label = QtWidgets.QLabel("Price:")
        self.price_input = QtWidgets.QLineEdit()
        price_layout.addWidget(self.price_label)
        price_layout.addWidget(self.price_input)
        layout.addLayout(price_layout)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("Save")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setStyleSheet("background: #404040;")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Connect buttons
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

class CustomerDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Add New Customer")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(255, 255, 255);
            }
            QLineEdit {
                width: 247px;
                height: 29px;
                border-radius: 8px;
                border: 1px solid #404040;
                background: #FFF;
                padding: 5px;
            }
            QPushButton {
                color: #FFF;
                font-family: Roboto;
                font-size: 12px;
                font-weight: 500;
                border-radius: 8px;
                background: #9747FF;
                padding: 10px;
            }
            QLabel {
                color: #404040;
                font-family: Roboto;
                font-size: 12px;
                font-weight: 500;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        # Customer Name
        name_layout = QtWidgets.QHBoxLayout()
        self.name_label = QtWidgets.QLabel("Customer Name:")
        self.name_input = QtWidgets.QLineEdit()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Address
        address_layout = QtWidgets.QHBoxLayout()
        self.address_label = QtWidgets.QLabel("Address:")
        self.address_input = QtWidgets.QLineEdit()
        address_layout.addWidget(self.address_label)
        address_layout.addWidget(self.address_input)
        layout.addLayout(address_layout)

        # Phone
        phone_layout = QtWidgets.QHBoxLayout()
        self.phone_label = QtWidgets.QLabel("Phone:")
        self.phone_input = QtWidgets.QLineEdit()
        phone_layout.addWidget(self.phone_label)
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("Save")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setStyleSheet("background: #404040;")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Connect buttons
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)