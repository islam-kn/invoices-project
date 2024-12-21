from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QTableView
from invoiciz import Ui_MainWindow
from dialogs import ProductDialog, CustomerDialog
from database import Database
from invoice_pdf import InvoicePDFGenerator
import sys , os
from datetime import datetime

class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.invoice_items = []
        self.setup_create_invoice()
        
        # Initialize database
        self.db = Database()
        
        # Connect menu buttons to page changes
        self.setup_menu_connections()
        
        # Set up tables
        self.setup_tables()
        
        # Load initial data
        self.load_products()
        self.load_customers()

    def setup_menu_connections(self):
        # Connect each menu button to its corresponding page
        self.ui.pushButton.clicked.connect(lambda: self.ui.stacked.setCurrentIndex(0))  # Dashboard
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stacked.setCurrentIndex(1))  # Create Invoice
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stacked.setCurrentIndex(2))  # History
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stacked.setCurrentIndex(3))  # Products
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stacked.setCurrentIndex(4))  # Customers
        
        # Set button styles for current page
        self.ui.stacked.currentChanged.connect(self.update_button_styles)

    def update_button_styles(self, index):
        # Reset all button styles
        default_style = """
            .QPushButton{
                padding: 10px;
                color: #404040;
                font-family: Roboto;
                font-size: 12px;
                font-style: normal;
                font-weight: 500;
                line-height: normal;
            }
            .QPushButton::hover{
                color : #000;
                border-bottom : 1px solid #000;
                border-radius : 0px;
            }
        """
        
        active_style = """
            .QPushButton{
                color: #FFF;
                font-family: Roboto;
                font-size: 12px;
                font-style: normal;
                font-weight: 500;
                line-height: normal;
                border-radius: 8px;
                background: #9747FF;
                padding: 10px;
            }
            .QPushButton::hover {
                background-color: rgb(94, 44, 159);
            }
        """
        
        # Reset all buttons to default style
        buttons = [self.ui.pushButton, self.ui.pushButton_2, self.ui.pushButton_3, 
                  self.ui.pushButton_4, self.ui.pushButton_5]
        for button in buttons:
            button.setStyleSheet(default_style)
        
        # Set active style for current page button
        buttons[index].setStyleSheet(active_style)

    def setup_connections(self):
        # Connect product management buttons
        self.ui.addProduct_button.clicked.connect(self.show_add_product_dialog)
        self.ui.deleteProduct_button.clicked.connect(self.delete_product)
        self.ui.editProduct_button.clicked.connect(self.edit_product)
        
        # Connect customer management buttons
        self.ui.addCustomer_button.clicked.connect(self.show_add_customer_dialog)
        self.ui.deleteCustomer_button.clicked.connect(self.delete_customer)
        self.ui.editCustomer_button.clicked.connect(self.edit_customer)
        
        # Connect search buttons
        self.ui.historySearch_Button.clicked.connect(self.search_history)
        self.ui.productSearch_Button.clicked.connect(self.search_products)
        self.ui.customersSearch_Button.clicked.connect(self.search_customers)
        
        # Connect edit buttons
        self.ui.editProduct_button.clicked.connect(self.edit_product)
        self.ui.editCustomer_button.clicked.connect(self.edit_customer)

    def setup_tables(self):
        table_style = """
            QTableView {
                background-color: #FFFFFF;
                border: 1px solid #EEEEEE;
                border-radius: 8px;
                gridline-color: #EEEEEE;
            }
            QTableView::item {
                border-bottom: 1px solid #EEEEEE;
            }
            QTableView::item:selected {
                background-color: #F5EBFF;
                color: #404040;
            }
            QHeaderView::section {
                background-color: #FAFAFA;  /* Lighter grey for headers */
                padding: 15px 12px;
                border: none;
                border-bottom: 1px solid #EEEEEE;
                border-right: 1px solid #EEEEEE;
                color: #404040;
                font-family: Roboto;
                font-size: 13px;
                font-weight: 500;
            }
        """

        # Products table
        self.products_model = TableModel([], ['ID', 'Name', 'Description', 'Price'])
        self.ui.tableView_3.setModel(self.products_model)
        self.ui.tableView_3.setStyleSheet(table_style)
        self.ui.tableView_3.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView_3.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableView_3.verticalHeader().setVisible(False)
        self.ui.tableView_3.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tableView_3.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.tableView_3.setShowGrid(False)
        
        # Customers table
        self.customers_model = TableModel([], ['ID', 'Name', 'Address', 'Phone'])
        self.ui.tableView_4.setModel(self.customers_model)
        self.ui.tableView_4.setStyleSheet(table_style)
        self.ui.tableView_4.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView_4.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableView_4.verticalHeader().setVisible(False)
        self.ui.tableView_4.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tableView_4.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.tableView_4.setShowGrid(False)

        # Invoice create table
        self.ui.create_tableView.setStyleSheet(table_style)
        self.ui.create_tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.create_tableView.verticalHeader().setVisible(False)
        self.ui.create_tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.create_tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.create_tableView.setShowGrid(False)

        # History table
        self.ui.history_tableView.setStyleSheet(table_style)
        self.ui.history_tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.history_tableView.verticalHeader().setVisible(False)
        self.ui.history_tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.history_tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection) 
        self.ui.history_tableView.setShowGrid(False)

    def load_products(self):
        products = self.db.get_products()
        self.products_model = TableModel(products, ['ID', 'Name', 'Description', 'Price'])
        self.ui.tableView_3.setModel(self.products_model)

    def load_customers(self):
        customers = self.db.get_customers()
        self.customers_model = TableModel(customers, ['ID', 'Name', 'Address', 'Phone'])
        self.ui.tableView_4.setModel(self.customers_model)

    def get_selected_row_id(self, table_view):
        index = table_view.currentIndex()
        if index.isValid():
            return int(table_view.model().data(table_view.model().index(index.row(), 0), Qt.DisplayRole))
        return None

    def show_add_product_dialog(self):
        dialog = ProductDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            name = dialog.name_input.text()
            description = dialog.desc_input.text()
            price = float(dialog.price_input.text())
            self.db.add_product(name, description, price)
            self.load_products()  # Refresh table

    def show_add_customer_dialog(self):
        dialog = CustomerDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            name = dialog.name_input.text()
            address = dialog.address_input.text()
            phone = dialog.phone_input.text()
            self.db.add_customer(name, address, phone)
            self.load_customers()  # Refresh table

    def add_product_to_invoice(self):
        # Add product to current invoice
        pass

    def save_invoice(self):
        if not self.validate_invoice():
            return
            
        try:
            # Save customer
            customer_id = self.db.add_customer(
                self.ui.companyName_input.text(),
                self.ui.companyAddress_input.text(),
                self.ui.companyPhone_input.text()
            )
            
            # Save invoice with type
            invoice_id = self.db.add_invoice(
                None,  # owner_id
                customer_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                float(self.ui.totalPrice_input.text()),
                self.ui.type_comboBox.currentText()
            )
            
            # Save items
            for item in self.invoice_items:
                self.db.add_invoice_item(
                    invoice_id,
                    None,  # product_id
                    item['quantity'],
                    item['price']
                )
                
            self.show_success("Invoice saved successfully!")
            self.clear_invoice_form()
            
        except Exception as e:
            self.show_error(f"Error saving invoice: {str(e)}")

    def print_invoice(self):
        invoice_data = {
            'type': self.ui.type_comboBox.currentText(),
            'customer': {
                'name': self.ui.companyName_input.text(),
                'address': self.ui.companyAddress_input.text(),
                'phone': self.ui.companyPhone_input.text()
            },
            'items': self.invoice_items,
            'net_total': float(self.ui.netPrice_input.text()),
            'discount': float(self.ui.discount_input.text() or 0),
            'total': float(self.ui.totalPrice_input.text())
        }
        
        pdf_generator = InvoicePDFGenerator(invoice_data)
        filename = pdf_generator.generate()
        
        # Open PDF
        os.startfile(filename)

    def cancel_invoice(self):
        # Cancel current invoice
        pass

    def delete_product(self):
        product_id = self.get_selected_row_id(self.ui.tableView_3)
        if product_id is not None:
            self.db.delete_product(product_id)
            self.load_products()

    def edit_product(self):
        selected_row = self.ui.tableView_3.currentIndex().row()
        if selected_row >= 0:
            product_data = self.products_model._data[selected_row]
            result = self.show_edit_product_dialog(product_data)
            if result:  # Only refresh if edit was successful
                self.load_products()

    def show_edit_product_dialog(self, product_data):
        dialog = ProductDialog()
        dialog.name_input.setText(str(product_data[1]))
        dialog.desc_input.setText(str(product_data[2]))
        dialog.price_input.setText(str(product_data[3]))
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            product_id = product_data[0]
            name = dialog.name_input.text()
            description = dialog.desc_input.text()
            price = float(dialog.price_input.text())
            
            self.db.update_product(product_id, name, description, price)
            return True
        return False

    def edit_customer(self):
        selected_row = self.ui.tableView_4.currentIndex().row()
        if selected_row >= 0:
            customer_data = self.customers_model._data[selected_row]
            result = self.show_edit_customer_dialog(customer_data)
            if result:  # Only refresh if edit was successful
                self.load_customers()

    def show_edit_customer_dialog(self, customer_data):
        dialog = CustomerDialog()
        dialog.name_input.setText(str(customer_data[1]))
        dialog.address_input.setText(str(customer_data[2]))
        dialog.phone_input.setText(str(customer_data[3]))
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            customer_id = customer_data[0]
            name = dialog.name_input.text()
            address = dialog.address_input.text()
            phone = dialog.phone_input.text()
            
            self.db.update_customer(customer_id, name, address, phone)
            return True
        return False

    def delete_customer(self):
        customer_id = self.get_selected_row_id(self.ui.tableView_4)
        if customer_id is not None:
            self.db.delete_customer(customer_id)
            self.load_customers()

    def search_history(self):
        # Search invoices history
        pass

    def search_products(self):
        # Search products
        pass

    def search_customers(self):
        # Search customers
        pass

    def setup_create_invoice(self):
        # Setup invoice table
        self.invoice_model = TableModel([], ['Product', 'Quantity', 'Unit Price', 'Total'])
        self.ui.create_tableView.setModel(self.invoice_model)
        self.ui.create_tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # Connect buttons
        self.ui.addButton.clicked.connect(self.add_invoice_item)
        self.ui.cancelInvoice_button.clicked.connect(self.clear_invoice_form)  # Using cancel button to remove items
        self.ui.saveInvoice_button.clicked.connect(self.save_invoice)
        self.ui.printInvoice_button.clicked.connect(self.print_invoice)
        
        # Connect inputs
        self.ui.discount_input.textChanged.connect(self.calculate_totals)
        self.ui.productQuantity_input.textChanged.connect(self.validate_numbers)
        self.ui.productPrice_input.textChanged.connect(self.validate_numbers)
        
        # Setup validators
        self.ui.productQuantity_input.setValidator(QtGui.QIntValidator(1, 999999))
        self.ui.productPrice_input.setValidator(QtGui.QDoubleValidator(0.00, 999999.99, 2))
        self.ui.discount_input.setValidator(QtGui.QDoubleValidator(0.00, 100.00, 2))

        # Setup invoice types
        invoice_types = ["Bon de commande", "Bon d'achat", "Bon de vente", "Bon de livraison"]
        self.ui.type_comboBox.addItems(invoice_types)

    def add_invoice_item(self):
        if not self.validate_item_inputs():
            return
            
        name = self.ui.productName_input.text()
        quantity = int(self.ui.productQuantity_input.text())
        price = float(self.ui.productPrice_input.text())
        total = quantity * price
        
        self.invoice_items.append({
            'name': name,
            'quantity': quantity,
            'price': price,
            'total': total
        })
        
        self.refresh_invoice_table()
        self.calculate_totals()
        self.clear_item_inputs()

    def validate_item_inputs(self):
        if not self.ui.productName_input.text():
            self.show_error("Product name is required")
            return False
            
        if not self.ui.productQuantity_input.text():
            self.show_error("Quantity is required")
            return False
            
        if not self.ui.productPrice_input.text():
            self.show_error("Price is required")
            return False
            
        return True

    def validate_numbers(self):
        sender = self.sender()
        if sender.text() and not sender.hasAcceptableInput():
            sender.setText("")

    def calculate_totals(self):
        net_total = sum(item['total'] for item in self.invoice_items)
        self.ui.netPrice_input.setText(f"{net_total:.2f}")
        
        try:
            discount = float(self.ui.discount_input.text() or 0)
            discount_amount = net_total * (discount / 100)
            total = net_total - discount_amount
            self.ui.totalPrice_input.setText(f"{total:.2f}")
        except ValueError:
            self.ui.totalPrice_input.setText(f"{net_total:.2f}")

    def refresh_invoice_table(self):
        data = [[
            item['name'],
            str(item['quantity']),
            f"{item['price']:.2f}",
            f"{item['total']:.2f}"
        ] for item in self.invoice_items]
        
        self.invoice_model = TableModel(data, ['Product', 'Quantity', 'Unit Price', 'Total'])
        self.ui.create_tableView.setModel(self.invoice_model)

    def clear_item_inputs(self):
        self.ui.productName_input.clear()
        self.ui.productQuantity_input.clear()
        self.ui.productPrice_input.clear()

    def clear_invoice_form(self):
        self.clear_item_inputs()
        self.ui.companyName_input.clear()
        self.ui.companyPhone_input.clear()
        self.ui.companyAddress_input.clear()
        self.ui.discount_input.clear()
        self.ui.netPrice_input.clear()
        self.ui.totalPrice_input.clear()
        self.invoice_items.clear()
        self.refresh_invoice_table()

    def validate_invoice(self):
        if not self.ui.companyName_input.text():
            self.show_error("Company name is required")
            return False
            
        if not self.ui.companyAddress_input.text():
            self.show_error("Company address is required")
            return False
            
        if not self.ui.companyPhone_input.text():
            self.show_error("Company phone is required")
            return False
            
        if not self.invoice_items:
            self.show_error("Add at least one product")
            return False
            
        return True

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self, "Error", message)

    def show_success(self, message):
        QtWidgets.QMessageBox.information(self, "Success", message)

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())