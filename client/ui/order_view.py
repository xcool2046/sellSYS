from PySide6.QtCore import Qt, QDateTime, QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
from PySide6.QtGui import QStandardItemModel, QStandardItem
from api import orders, customers, products, employees
from datetime import datetime
from schemas.product import Product
from .order_creation_dialog import OrderCreationDialog
                             QComboBox, QLineEdit, QPushButton, QTableView,
                             QHeaderView, QMessageBox, QDateEdit)

class OrderView(QWidget):
    def __init__(self):
        super().__init__()
        self.customers = []
        self.products = []
        self.employees = []
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Toolbar (Filters and Actions) ---
        toolbar_container = QWidget()
        toolbar_container.setObjectName("toolbarContainer")
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)

        self.customer_search = QLineEdit()
        self.customer_search.setPlaceholderText("客户名称")
        toolbar_layout.addWidget(self.customer_search)

        self.product_combo = QComboBox()
        self.product_combo.addItem("产品名称")
        toolbar_layout.addWidget(self.product_combo)
        
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setSpecialValueText("生效日期")
        self.start_date_edit.clear() # Display placeholder
        toolbar_layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setSpecialValueText("到期日期")
        self.end_date_edit.clear() # Display placeholder
        toolbar_layout.addWidget(self.end_date_edit)

        self.sign_date_edit = QDateEdit(self)
        self.sign_date_edit.setCalendarPopup(True)
        self.sign_date_edit.setSpecialValueText("签单日期")
        self.sign_date_edit.clear() # Display placeholder
        toolbar_layout.addWidget(self.sign_date_edit)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["订单状态", "待收款", "已收款", "已到期"])
        toolbar_layout.addWidget(self.status_combo)
        
        self.sales_combo = QComboBox()
        self.sales_combo.addItem("销售人")
        toolbar_layout.addWidget(self.sales_combo)
        
        self.search_btn = QPushButton("查询")
        self.search_btn.setObjectName("searchButton")
        toolbar_layout.addWidget(self.search_btn)
        
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setObjectName("resetButton")
        toolbar_layout.addWidget(self.reset_btn)

        toolbar_layout.addStretch()
        
        self.add_order_btn = QPushButton("创建订单")
        self.add_order_btn.setObjectName("addButton")
        toolbar_layout.addWidget(self.add_order_btn)
        
        main_layout.addWidget(toolbar_container)
        
        # 主表格
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.setup_table_headers(self.model)
        self.setup_table_style(self.table_view)
        main_layout.addWidget(self.table_view)
        
        # 合计栏
        summary_layout = QHBoxLayout()
        summary_layout.setContentsMargins(0, 5, 10, 5)
        
        self.total_label = QLabel("合计")
        summary_layout.addWidget(self.total_label)
        
        summary_layout.addStretch(2)
        
        self.total_actual_price_label = QLabel("实际售价: 0.00")
        summary_layout.addWidget(self.total_actual_price_label)
        
        summary_layout.addStretch(1)
        
        self.total_quantity_label = QLabel("数量: 0")
        summary_layout.addWidget(self.total_quantity_label)
        
        summary_layout.addStretch(1)
        
        self.total_amount_label = QLabel("订单金额: 0.00")
        summary_layout.addWidget(self.total_amount_label)
        
        summary_layout.addStretch(10) # Add more stretch to push to the left
        
        main_layout.addLayout(summary_layout)
        
        # 连接信号
        self.search_btn.clicked.connect(self.search_orders)
        self.reset_btn.clicked.connect(self.reset_filters)
        self.add_order_btn.clicked.connect(self.open_create_order_dialog)
        
    def setup_table_headers(self, model):
        """设置表格列头"""
        headers = [
            "序号", "客户单位", "产品名称", "型号规格",
            "产品定价", "实际售价", "数量", "单位",
            "订单金额", "生效日期", "到期日期", "签单时间",
            "销售人", "订单状态"
        ]
        model.setHorizontalHeaderLabels(headers)
        
    def setup_table_style(self, table):
        """设置表格样式"""
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableView.SelectRows)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableView.NoEditTriggers)
        
        # 设置列宽
        header = table.horizontalHeader()
        header.resizeSection(0, 50)   # 序号
        header.resizeSection(1, 200)  # 客户单位
        header.resizeSection(2, 150)  # 产品名称
        header.resizeSection(3, 120)  # 型号规格
        header.resizeSection(4, 100)  # 产品定价
        header.resizeSection(5, 100)  # 实际售价
        header.resizeSection(6, 60)   # 数量
        header.resizeSection(7, 60)   # 单位
        header.resizeSection(8, 100)  # 订单金额
        header.resizeSection(9, 100)  # 生效日期
        header.resizeSection(10, 100) # 到期日期
        header.resizeSection(11, 150) # 签单时间
        header.resizeSection(12, 100) # 销售人
        header.resizeSection(13, 100) # 订单状态
        
    def load_data(self):
        """加载数据"""
        try:
            # 加载客户列表
            self.customers = customers.get_customeromers() or []
            
            # 加载产品列表
            product_list = products.get_products() or []
            self.products = [Product(**p) for p in product_list]
            # Skip placeholder "产品名称"
            for product in self.products:
                self.product_combo.addItem(product.name)
                
            # 加载员工列表
            self.employees = employees.get_employees() or []
            # Skip placeholder "销售人"
            for employee in self.employees:
                self.sales_combo.addItem(employee['name'])
                
            # 加载订单数据
            self.load_orders()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据失败: {str(e)}")
            
    def load_orders(self, params=None):
        """加载订单数据到表格"""
        try:
            order_list = orders.get_orders(params=params) or []
            
            self.model.setRowCount(0)
            
            total_actual_price = 0.0
            total_quantity = 0
            total_amount = 0.0
            
            for idx, order in enumerate(order_list):
                company = self.get_company(order.get('customer_id'))
                product = self.get_product(order.get('product_id'))
                employee_name = self.get_employee_name(order.get('sales_person_id'))
                
                actual_price = order.get('actual_price', 0)
                quantity = order.get('quantity', 0)
                order_amount = actual_price * quantity
                
                total_actual_price += actual_price
                total_quantity += quantity
                total_amount += order_amount
                
                def format_date(date_str, fmt="%Y-%m-%d"):
                    if not date_str:
                        return ""
                    try:
                        return datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime(fmt)
                    except (ValueError, TypeError):
                        return date_str

                effective_date = format_date(order.get('effective_date'))
                expiry_date = format_date(order.get('expiry_date'))
                sign_time = format_date(order.get('sign_time'), fmt="%Y-%m-%d %H:%M:%S")

                row_data = [
                    QStandardItem(str(idx + 1)),
                    QStandardItem(company),
                    QStandardItem(product.name if product else ""),
                    QStandardItem(product.specifications if product else ""),
                    QStandardItem(f"{product.list_price:.2f}" if product else "0.00"),
                    QStandardItem(f"{actual_price:.2f}"),
                    QStandardItem(str(quantity)),
                    QStandardItem(order.get('unit', '')),
                    QStandardItem(f"{order_amount:.2f}"),
                    QStandardItem(effective_date),
                    QStandardItem(expiry_date),
                    QStandardItem(sign_time),
                    QStandardItem(employee_name),
                    QStandardItem(order.get('status', ''))
                ]
                
                for i, item in enumerate(row_data):
                    item.setTextAlignment(Qt.AlignCenter)
                    if i in [4, 5, 6, 8]:  # Numeric columns
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                self.model.appendRow(row_data)

            self.total_actual_price_label.setText(f"实际售价: {total_actual_price:.2f}")
            self.total_quantity_label.setText(f"数量: {total_quantity}")
            self.total_amount_label.setText(f"订单金额: {total_amount:.2f}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载订单数据失败: {str(e)}")
            
    def get_company(self, customer_id):
        """获取客户名称"""
        for customer in self.customers:
            if customer.get('id') == customer_id:
                return customer.get('name', '')
        return ""
        
    def get_product(self, product_id):
        """获取产品信息"""
        for product in self.products:
            if product.id == product_id:
                return product
        return None
        
    def get_employee_name(self, employee_id):
        """获取员工姓名"""
        for employee in self.employees:
            if employee.get('id') == employee_id:
                return employee.get('name', '')
        return ""
        
    def search_orders(self):
        """根据筛选条件搜索订单"""
        params = {}
        
        company = self.customer_search.text().strip()
        if company:
            params['company'] = company
            
        if self.product_combo.currentIndex() > 0:
            params['name'] = self.product_combo.currentText()

        if self.start_date_edit.date().isValid():
            params['effective_date_start'] = self.start_date_edit.date().toString(Qt.ISODate)

        if self.end_date_edit.date().isValid():
            params['expiry_date_end'] = self.end_date_edit.date().toString(Qt.ISODate)

        if self.sign_date_edit.date().isValid():
            params['sign_date'] = self.sign_date_edit.date().toString(Qt.ISODate)
            
        if self.status_combo.currentIndex() > 0:
            params['status'] = self.status_combo.currentText()
            
        if self.sales_combo.currentIndex() > 0:
            sales_name = self.sales_combo.currentText()
            selected_employee = next((emp for emp in self.employees if emp['name'] == sales_name), None)
            if selected_employee:
                params['sales_id'] = selected_employee['id']
                
        self.load_orders(params)
        
    def reset_filters(self):
        """重置筛选条件"""
        self.customer_search.clear()
        self.product_combo.setCurrentIndex(0)
        self.start_date_edit.clear()
        self.end_date_edit.clear()
        self.sign_date_edit.clear()
        self.status_combo.setCurrentIndex(0)
        self.sales_combo.setCurrentIndex(0)
        self.load_orders()

    def open_create_order_dialog(self):
        """打开创建订单对话框"""
        dialog = OrderCreationDialog(self)
        if dialog.exec():
            self.load_orders() # 刷新订单列表