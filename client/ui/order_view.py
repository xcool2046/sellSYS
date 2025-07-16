import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableView, QHeaderView, QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Slot

from ..api.orders import get_orders
from .order_creation_dialog import OrderCreationDialog

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
        self.new_order_button = QPushButton("新建订单")
        self.new_order_button.clicked.connect(self.open_new_order_dialog)
        action_layout.addWidget(self.new_order_button)
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

        if isinstance(orders, dict) and "error" in orders:
            error_detail = orders.get("detail", "无详细信息")
            QMessageBox.critical(self, "加载错误", f"无法加载订单数据: {error_detail}")
            return

        if not isinstance(orders, list):
            QMessageBox.warning(self, "无数据", "未找到订单数据或数据格式错误。")
            return

        for order in orders:
            if not isinstance(order, dict): continue
            
            # Note: The actual fields depend on the API response.
            # Customer/Employee names might need extra lookups if the API returns IDs.
            row = [
                QStandardItem(str(order.get("id", ""))),
                QStandardItem(str(order.get("customer_id", ""))), # Placeholder, needs name
                QStandardItem(str(order.get("total_amount", "0.0"))),
                QStandardItem(str(order.get("employee_id", ""))), # Placeholder, needs name
                QStandardItem(order.get("status", "未知")),
                QStandardItem(order.get("created_at", "").split("T")[0])
            ]
            self.model.appendRow(row)

    @Slot()
    def open_new_order_dialog(self):
        """
        Opens the dialog to create a new order.
        """
        dialog = OrderCreationDialog(self)
        if dialog.exec():
            # If the dialog was accepted (OK clicked), refresh the order list
            self.load_order_data()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = OrderView()
    view.show()
    sys.exit(app.exec())