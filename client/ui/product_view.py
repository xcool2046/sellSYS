import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableView, QHeaderView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ..api.products import get_products

class ProductView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("产品管理")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Search/Filter area (simplified for now)
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLineEdit(placeholderText="输入产品名称..."))
        search_layout.addWidget(QPushButton("搜索"))
        main_layout.addLayout(search_layout)
        
        # Table view
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.model = QStandardItemModel()
        self.setup_model()
        self.table_view.setModel(self.model)
        
        main_layout.addWidget(self.table_view)
        
        self.load_product_data()
        
    def setup_model(self):
        headers = ["ID", "产品名称", "型号规格", "定价", "佣金"]
        self.model.setHorizontalHeaderLabels(headers)

    def load_product_data(self):
        """Fetches product data from the API and populates the table."""
        self.model.removeRows(0, self.model.rowCount()) # Clear existing data
        
        products = get_products()
        if not products:
            print("Failed to load product data or no products found.")
            return

        for product in products:
            row = [
                QStandardItem(str(product.get("id", ""))),
                QStandardItem(product.get("name", "N/A")),
                QStandardItem(product.get("specs", "N/A")),
                QStandardItem(str(product.get("price", "0.00"))),
                QStandardItem(str(product.get("commission_rate", "0%")))
            ]
            self.model.appendRow(row)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = ProductView()
    view.show()
    sys.exit(app.exec())