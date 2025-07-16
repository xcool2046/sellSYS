import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableView, QHeaderView, QMessageBox, QComboBox, QDateEdit,
    QGridLayout
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide6.QtCore import Slot, QDate

from api.orders import get_orders
from api.employees import get_employees
from .order_creation_dialog import OrderCreationDialog
from schemas.order import OrderStatus

class OrderView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("订单管理")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Filters
        self.create_filter_widgets()
        main_layout.addLayout(self.filter_layout)

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

        # Summary Row
        self.summary_layout = QHBoxLayout()
        self.total_amount_label = QLabel("订单总金额: 0.00")
        font = self.total_amount_label.font()
        font.setBold(True)
        self.total_amount_label.setFont(font)
        self.summary_layout.addStretch()
        self.summary_layout.addWidget(self.total_amount_label)
        main_layout.addLayout(self.summary_layout)
        
        self.load_sales_persons()
        self.load_order_data()

    def create_filter_widgets(self):
        self.filter_layout = QGridLayout()
        self.filter_layout.setSpacing(10)

        # Row 1
        self.filter_layout.addWidget(QLabel("客户名称:"), 0, 0)
        self.customer_name_filter = QLineEdit()
        self.filter_layout.addWidget(self.customer_name_filter, 0, 1)

        self.filter_layout.addWidget(QLabel("产品名称:"), 0, 2)
        self.product_name_filter = QLineEdit()
        self.filter_layout.addWidget(self.product_name_filter, 0, 3)

        self.filter_layout.addWidget(QLabel("订单状态:"), 0, 4)
        self.status_filter = QComboBox()
        self.status_filter.addItem("所有状态", "")
        for status in OrderStatus:
            self.status_filter.addItem(status.value, status.name)
        self.filter_layout.addWidget(self.status_filter, 0, 5)
        
        # Row 2
        self.filter_layout.addWidget(QLabel("销售负责人:"), 1, 0)
        self.salesperson_filter = QComboBox()
        self.salesperson_filter.addItem("所有人", "")
        self.filter_layout.addWidget(self.salesperson_filter, 1, 1)

        self.filter_layout.addWidget(QLabel("生效日期:"), 1, 2)
        self.start_date_filter = QDateEdit(calendarPopup=True)
        self.start_date_filter.setSpecialValueText("起始日期")
        self.start_date_filter.setDate(QDate()) # Unset date
        self.filter_layout.addWidget(self.start_date_filter, 1, 3)
        
        self.end_date_filter = QDateEdit(calendarPopup=True)
        self.end_date_filter.setSpecialValueText("结束日期")
        self.end_date_filter.setDate(QDate()) # Unset date
        self.filter_layout.addWidget(self.end_date_filter, 1, 4)

        # Action Buttons
        self.search_button = QPushButton("查询")
        self.search_button.clicked.connect(self.load_order_data)
        self.filter_layout.addWidget(self.search_button, 1, 5)

        self.clear_button = QPushButton("清空")
        self.clear_button.clicked.connect(self.clear_filters)
        self.filter_layout.addWidget(self.clear_button, 1, 6)

        self.filter_layout.setColumnStretch(1, 1)
        self.filter_layout.setColumnStretch(3, 1)


    def setup_model(self):
        headers = ["订单ID", "客户名称", "总金额", "销售负责人", "订单状态", "创建日期"]
        self.model.setHorizontalHeaderLabels(headers)

    def load_sales_persons(self):
        employees = get_employees()
        if isinstance(employees, list):
            for emp in employees:
                if isinstance(emp, dict):
                    self.salesperson_filter.addItem(emp.get('name'), str(emp.get('id')))

    def load_order_data(self):
        self.model.removeRows(0, self.model.rowCount())
        
        params = {}
        if self.customer_name_filter.text():
            params['customer_name'] = self.customer_name_filter.text()
        if self.product_name_filter.text():
            params['product_name'] = self.product_name_filter.text()
        if self.status_filter.currentData():
            params['status'] = self.status_filter.currentData()
        if self.salesperson_filter.currentData():
            params['sales_id'] = self.salesperson_filter.currentData()
        if self.start_date_filter.date().isValid():
            params['start_date'] = self.start_date_filter.date().toString("yyyy-MM-dd")
        if self.end_date_filter.date().isValid():
            params['end_date'] = self.end_date_filter.date().toString("yyyy-MM-dd")

        orders = get_orders(params=params)

        if isinstance(orders, dict) and "error" in orders:
            error_detail = orders.get("detail", "无详细信息")
            QMessageBox.critical(self, "加载错误", f"无法加载订单数据: {error_detail}")
            return

        if not isinstance(orders, list):
            QMessageBox.warning(self, "无数据", "未找到订单数据或数据格式错误。")
            return

        total_amount = 0.0
        for order in orders:
            if not isinstance(order, dict): continue
            
            customer_name = order.get('customer', {}).get('company', 'N/A')
            employee_name = order.get('employee', {}).get('name', 'N/A')
            amount = float(order.get("total_amount", 0.0))
            total_amount += amount

            row = [
                QStandardItem(str(order.get("id", ""))),
                QStandardItem(customer_name),
                QStandardItem(f"{amount:.2f}"),
                QStandardItem(employee_name),
                QStandardItem(order.get("status", "未知")),
                QStandardItem(datetime.fromisoformat(order.get("created_at")).strftime('%Y-%m-%d') if order.get("created_at") else "")
            ]
            self.model.appendRow(row)
        
        self.total_amount_label.setText(f"订单总金额: {total_amount:.2f}")

    @Slot()
    def clear_filters(self):
        self.customer_name_filter.clear()
        self.product_name_filter.clear()
        self.status_filter.setCurrentIndex(0)
        self.salesperson_filter.setCurrentIndex(0)
        self.start_date_filter.setDate(QDate())
        self.end_date_filter.setDate(QDate())
        self.load_order_data()


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