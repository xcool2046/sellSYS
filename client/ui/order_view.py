from PySide6.QtCore import Qt, QDateTime, QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QLineEdit, QPushButton, QTableView,
                             QHeaderView, QMessageBox, QSplitter)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from ..api import orders, customers, products, employees
from datetime import datetime
from ..schemas.product import Product
from .order_creation_dialog import OrderCreationDialog

class OrderView(QWidget):
    def __init__(self):
        super().__init__()
        self.customers = []
        self.products = []
        self.employees = []
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 顶部筛选栏
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        # 输入客户名称
        filter_layout.addWidget(QLabel("输入客户名称"))
        self.customer_search = QLineEdit()
        self.customer_search.setPlaceholderText("输入客户名称")
        self.customer_search.setFixedWidth(150)
        filter_layout.addWidget(self.customer_search)
        
        # 产品名称
        filter_layout.addWidget(QLabel("产品名称"))
        self.product_combo = QComboBox()
        self.product_combo.setFixedWidth(120)
        self.product_combo.addItem("全部")
        filter_layout.addWidget(self.product_combo)
        
        # 生效日期
        filter_layout.addWidget(QLabel("生效日期"))
        self.effective_date_combo = QComboBox()
        self.effective_date_combo.setFixedWidth(120)
        self.effective_date_combo.addItem("全部")
        filter_layout.addWidget(self.effective_date_combo)
        
        # 到期日期
        filter_layout.addWidget(QLabel("到期日期"))
        self.expiry_date_combo = QComboBox()
        self.expiry_date_combo.setFixedWidth(120)
        self.expiry_date_combo.addItem("全部")
        filter_layout.addWidget(self.expiry_date_combo)
        
        # 签单日期
        filter_layout.addWidget(QLabel("签单日期"))
        self.sign_date_combo = QComboBox()
        self.sign_date_combo.setFixedWidth(120)
        self.sign_date_combo.addItem("全部")
        filter_layout.addWidget(self.sign_date_combo)
        
        # 订单状态
        filter_layout.addWidget(QLabel("订单状态"))
        self.status_combo = QComboBox()
        self.status_combo.setFixedWidth(120)
        self.status_combo.addItems(["全部", "待收款", "已收款", "已到期"])
        filter_layout.addWidget(self.status_combo)
        
        # 销售人
        filter_layout.addWidget(QLabel("销售人"))
        self.sales_combo = QComboBox()
        self.sales_combo.setFixedWidth(120)
        self.sales_combo.addItem("全部")
        filter_layout.addWidget(self.sales_combo)
        
        # 查询按钮
        self.search_btn = QPushButton("查询")
        self.search_btn.setFixedSize(80, 28)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        filter_layout.addWidget(self.search_btn)
        
        # 重置按钮
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setFixedSize(80, 28)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        filter_layout.addWidget(self.reset_btn)
        
        filter_layout.addStretch()
        
        self.add_order_btn = QPushButton("➕ 创建订单")
        self.add_order_btn.setFixedSize(100, 28)
        self.add_order_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green */
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        filter_layout.addWidget(self.add_order_btn)
        
        layout.addLayout(filter_layout)
        
        # 使用分割器来创建上下两个表格
        splitter = QSplitter(Qt.Vertical)
        
        # 上表格
        self.upper_table = QTableView()
        self.upper_model = QStandardItemModel()
        self.upper_table.setModel(self.upper_model)
        self.setup_table_headers(self.upper_model)
        self.setup_table_style(self.upper_table)
        splitter.addWidget(self.upper_table)
        
        # 下表格  
        self.lower_table = QTableView()
        self.lower_model = QStandardItemModel()
        self.lower_table.setModel(self.lower_model)
        self.setup_table_headers(self.lower_model)
        self.setup_table_style(self.lower_table)
        splitter.addWidget(self.lower_table)
        
        # 设置分割器初始比例
        splitter.setSizes([300, 400])
        
        layout.addWidget(splitter)
        
        # 合计行
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("合计"))
        total_layout.addStretch()
        layout.addLayout(total_layout)
        
        self.setLayout(layout)
        
        # 连接信号
        self.search_btn.clicked.connect(self.search_orders)
        self.reset_btn.clicked.connect(self.reset_filters)
        self.add_order_btn.clicked.connect(self.open_create_order_dialog)
        
    def setup_table_headers(self, model):
        """设置表格列头 - 两个表格使用相同的列"""
        headers = [
            "序号", "客户单位", "产品名称", "型号规格", 
            "产品定价", "实际售价", "数量", "单位", 
            "订单金额", "生效日期", "到期日期", "签单时间"
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
        
    def load_data(self):
        """加载数据"""
        try:
            # 加载客户列表
            self.customers = customers.get_customers() or []
            
            # 加载产品列表
            product_list = products.get_products() or []
            self.products = [Product(**p) for p in product_list]
            for product in self.products:
                self.product_combo.addItem(product.name)
                
            # 加载员工列表
            self.employees = employees.get_employees() or []
            for employee in self.employees:
                self.sales_combo.addItem(employee['name'])
                
            # 加载订单数据
            self.load_orders()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据失败: {str(e)}")
            
    def load_orders(self, params=None):
        """加载订单数据到两个表格"""
        try:
            order_list = orders.get_orders(params=params) or []
            
            # 清空表格
            self.upper_model.setRowCount(0)
            self.lower_model.setRowCount(0)
            
            # 用于统计的变量
            total_quantity = 0
            total_amount = 0.0
            
            # 添加数据到两个表格
            for idx, order in enumerate(order_list):
                # 获取关联数据
                customer_name = self.get_customer_name(order.get('customer_id'))
                product = self.get_product(order.get('product_id'))
                employee_name = self.get_employee_name(order.get('sales_person_id'))
                
                # 计算订单金额
                actual_price = order.get('actual_price', 0)
                quantity = order.get('quantity', 0)
                order_amount = actual_price * quantity
                total_quantity += quantity
                total_amount += order_amount
                
                # 格式化日期
                effective_date = order.get('effective_date', '')
                if effective_date and effective_date != '':
                    try:
                        effective_date = datetime.fromisoformat(effective_date.replace('Z', '+00:00')).strftime("%Y-%m-%d")
                    except:
                        pass
                        
                expiry_date = order.get('expiry_date', '')
                if expiry_date and expiry_date != '':
                    try:
                        expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00')).strftime("%Y-%m-%d")
                    except:
                        pass
                        
                sign_time = order.get('sign_time', '')
                if sign_time and sign_time != '':
                    try:
                        sign_time = datetime.fromisoformat(sign_time.replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                
                # 创建行数据
                row_data = [
                    str(idx + 1),  # 序号
                    customer_name,  # 客户单位
                    product.name if product else "",  # 产品名称
                    product.specifications if product else "",  # 型号规格
                    f"{product.list_price:.2f}" if product else "0.00",  # 产品定价
                    f"{actual_price:.2f}",  # 实际售价
                    str(quantity),  # 数量
                    order.get('unit', ''),  # 单位
                    f"{order_amount:.2f}",  # 订单金额
                    effective_date,  # 生效日期
                    expiry_date,  # 到期日期
                    sign_time  # 签单时间
                ]
                
                # 添加到上表格
                upper_row = []
                for i, value in enumerate(row_data):
                    item = QStandardItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    # 数字列右对齐
                    if i in [4, 5, 6, 8]:  # 产品定价、实际售价、数量、订单金额
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    upper_row.append(item)
                self.upper_model.appendRow(upper_row)
                
                # 添加到下表格
                lower_row = []
                for i, value in enumerate(row_data):
                    item = QStandardItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    # 数字列右对齐
                    if i in [4, 5, 6, 8]:  # 产品定价、实际售价、数量、订单金额
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    lower_row.append(item)
                self.lower_model.appendRow(lower_row)
            
            # 在下表格添加合计行
            total_row = []
            for i in range(12):
                if i == 0:
                    item = QStandardItem("合计")
                elif i == 6:  # 数量列
                    item = QStandardItem(str(total_quantity))
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif i == 8:  # 订单金额列
                    item = QStandardItem(f"{total_amount:.2f}")
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item = QStandardItem("")
                
                item.setTextAlignment(Qt.AlignCenter)
                # 设置合计行背景色
                item.setBackground(QColor("#f5f5f5"))
                total_row.append(item)
                
            self.lower_model.appendRow(total_row)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载订单数据失败: {str(e)}")
            
    def get_customer_name(self, customer_id):
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
        """搜索订单"""
        params = {}
        customer_name = self.customer_search.text().strip()
        if customer_name:
            params['customer_name'] = customer_name
            
        product_name = self.product_combo.currentText()
        if self.product_combo.currentIndex() > 0:
            params['product_name'] = product_name
            
        status = self.status_combo.currentText()
        if self.status_combo.currentIndex() > 0:
            params['status'] = status
            
        sales_name = self.sales_combo.currentText()
        if self.sales_combo.currentIndex() > 0:
            selected_employee = next((emp for emp in self.employees if emp['name'] == sales_name), None)
            if selected_employee:
                params['sales_id'] = selected_employee['id']
                
        self.load_orders(params)
        
    def reset_filters(self):
        """重置筛选条件"""
        self.customer_search.clear()
        self.product_combo.setCurrentIndex(0)
        self.effective_date_combo.setCurrentIndex(0)
        self.expiry_date_combo.setCurrentIndex(0)
        self.sign_date_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        self.sales_combo.setCurrentIndex(0)
        self.load_orders()

    def open_create_order_dialog(self):
        """打开创建订单对话框"""
        dialog = OrderCreationDialog(self)
        if dialog.exec():
            self.load_orders() # 刷新订单列表