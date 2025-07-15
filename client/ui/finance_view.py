import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableView, QHeaderView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ..api.orders import get_orders, update_order_financials
from datetime import datetime

class FinanceView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("财务管理 - 订单收款")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Table view to display orders
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        # Add double click signal to handle payment confirmation
        self.table_view.doubleClicked.connect(self.confirm_payment_dialog)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.model = QStandardItemModel()
        self.setup_model()
        self.table_view.setModel(self.model)
        
        main_layout.addWidget(self.table_view)
        
        self.load_data()
        
    def setup_model(self):
        headers = ["ID", "客户ID", "总金额", "已付金额", "状态", "付款日期"]
        self.model.setHorizontalHeaderLabels(headers)

    def load_data(self):
        self.model.removeRows(0, self.model.rowCount())
        orders = get_orders()
        if not orders:
            return
        for order in orders:
            row = [
                QStandardItem(str(order.get("id"))),
                QStandardItem(str(order.get("customer_id"))),
                QStandardItem(str(order.get("total_amount"))),
                QStandardItem(str(order.get("paid_amount", "0.00"))),
                QStandardItem(order.get("status")),
                QStandardItem(order.get("payment_date", "").split("T")[0]),
            ]
            self.model.appendRow(row)

    def confirm_payment_dialog(self, index):
        # Simplified confirmation: mark as fully paid on double click
        order_id = self.model.item(index.row(), 0).text()
        total_amount = self.model.item(index.row(), 2).text()
        
        financial_data = {
            "status": "已付款",
            "paid_amount": total_amount,
            "payment_date": datetime.now().isoformat()
        }
        
        response = update_order_financials(int(order_id), financial_data)
        if response:
            self.load_data() # Refresh the view
        else:
            # Here you would show an error dialog
            print(f"Failed to update order {order_id}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = FinanceView()
    view.show()
    sys.exit(app.exec())