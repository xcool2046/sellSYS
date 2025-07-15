import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableView, QHeaderView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ..api.orders import get_orders

class OrderView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("订单管理")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addWidget(QPushButton("新建订单"))
        action_layout.addStretch()
        main_layout.addLayout(action_layout)
        
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
        
        self.load_order_data()
        
    def setup_model(self):
        headers = ["订单ID", "客户名称", "总金额", "销售人", "状态", "创建日期"]
        self.model.setHorizontalHeaderLabels(headers)

    def load_order_data(self):
        self.model.removeRows(0, self.model.rowCount())
        
        orders = get_orders()
        if not orders:
            print("Failed to load order data or no orders found.")
            return

        for order in orders:
            # Note: The actual fields depend on the API response.
            # Customer/Employee names might need extra lookups if the API returns IDs.
            row = [
                QStandardItem(str(order.get("id"))),
                QStandardItem(str(order.get("customer_id"))), # Placeholder, needs name
                QStandardItem(str(order.get("total_amount"))),
                QStandardItem(str(order.get("employee_id"))), # Placeholder, needs name
                QStandardItem(order.get("status")),
                QStandardItem(order.get("created_at", "").split("T")[0])
            ]
            self.model.appendRow(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = OrderView()
    view.show()
    sys.exit(app.exec())