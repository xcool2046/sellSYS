import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableView, QComboBox, QDateEdit, QHeaderView, QFrame,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ..api.customers import get_customers

class CustomerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Top title/tab area
        main_layout.addWidget(self._create_title_area())

        # 2. Search and filter area
        main_layout.addWidget(self._create_search_area())
        
        # 3. Table view for displaying data
        self.table_view = self._create_table_view()
        main_layout.addWidget(self.table_view)

        # Load initial data
        self.load_customer_data()

    def _create_title_area(self):
        """Creates the top area with '订单列表' and '订单统计'."""
        title_widget = QWidget()
        layout = QHBoxLayout(title_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # In a real app, these would be custom tab-like buttons
        order_list_label = QLabel("订单列表")
        order_list_label.setStyleSheet("font-weight: bold; font-size: 16px; border-bottom: 2px solid #0d6efd; padding-bottom: 5px;")
        
        order_stats_label = QLabel("订单统计 (本期不做)")
        order_stats_label.setStyleSheet("font-size: 16px; color: grey; margin-left: 20px;")
        
        layout.addWidget(order_list_label)
        layout.addWidget(order_stats_label)
        
        return title_widget

    def _create_search_area(self):
        """Creates the search filter panel."""
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        # Add some basic styling later if needed
        
        layout = QHBoxLayout(search_frame)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(QLineEdit(placeholderText="输入客户名称"))
        layout.addWidget(QComboBox()) # Placeholder for "产品名称"
        layout.addWidget(QDateEdit(calendarPopup=True)) # 生效日期
        layout.addWidget(QDateEdit(calendarPopup=True)) # 到期日期
        layout.addWidget(QComboBox()) # 订单状态
        layout.addWidget(QComboBox()) # 销售人
        
        layout.addWidget(QPushButton("查询"))
        layout.addWidget(QPushButton("重置"))

        # Initialize combo boxes, etc. in a real scenario
        # e.g., search_frame.findChild(QComboBox, "productCombo").addItems(["产品A", "产品B"])

        return search_frame

    def _create_table_view(self):
        """Creates and configures the main data table."""
        table_view = QTableView()
        table_view.setAlternatingRowColors(True)
        table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        
        self.model = QStandardItemModel()
        self._setup_table_model()
        table_view.setModel(self.model)

        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        return table_view

    def _setup_table_model(self):
        """Sets up the table headers and dummy data."""
        headers = [
            "序号", "客户单位", "产品名称", "型号规格", "产品定价", "实际售价",
            "数量", "单位", "订单金额", "销售提成", "主管提成", "经理提成",
            "签单日期", "销售人", "订单状态", "到账日期"
        ]
        self.model.setHorizontalHeaderLabels(headers)
    
    def load_customer_data(self):
        """Fetches customer data from the API and populates the table."""
        self.model.removeRows(0, self.model.rowCount()) # Clear existing data
        
        customers = get_customers() # In a real app, you'd handle pagination
        
        if isinstance(customers, dict) and "error" in customers:
            error_detail = customers.get("detail", "无详细信息")
            QMessageBox.critical(self, "加载错误", f"无法加载客户数据: {error_detail}")
            return

        if not isinstance(customers, list):
            QMessageBox.warning(self, "无数据", "未找到客户数据或数据格式错误。")
            return

        # NOTE: This is a placeholder mapping. The actual data structure from
        # the API needs to be mapped to the table columns correctly.
        for i, customer in enumerate(customers):
            if not isinstance(customer, dict): continue

            row = [
                QStandardItem(str(customer.get("id", ""))),
                QStandardItem(customer.get("company_name", "N/A")),
                QStandardItem("产品待定"), # Placeholder
                QStandardItem("规格待定"), # Placeholder
                QStandardItem("0.00"),     # Placeholder
                QStandardItem("0.00"),     # Placeholder
                QStandardItem("1"),        # Placeholder
                QStandardItem("套"),       # Placeholder
                QStandardItem("0.00"),     # Placeholder
                QStandardItem("0.00"),     # Placeholder
                QStandardItem("0.00"),     # Placeholder
                QStandardItem("0.00"),     # Placeholder
                QStandardItem(customer.get("created_at", "N/A").split("T")[0]),
                QStandardItem("销售待定"), # Placeholder
                QStandardItem(customer.get("status", "N/A")),
                QStandardItem("")          # Placeholder for 到账日期
            ]
            self.model.appendRow(row)


if __name__ == '__main__':
    # For testing the widget appearance
    app = QApplication(sys.argv)
    view = CustomerView()
    view.resize(1000, 600)
    view.show()
    sys.exit(app.exec())