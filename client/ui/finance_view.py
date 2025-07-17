import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableView, QTabWidget,
    QHeaderView, QAbstractItemView, QSizePolicy, QFrame, QSpacerItem, QApplication
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDateEdit
from datetime import datetime, date
from decimal import Decimal
from ..api.orders import get_orders
from ..api.customers import get_customers
from ..api.products import get_products
from ..api.employees import get_employees

class FinanceView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.orders_data = []
        self.customers_data = []
        self.products_data = []
        self.employees_data = []
        self.setup_ui()
        self.load_basic_data()
        self.load_orders_data()
        
    def setup_ui(self):
        """设置UI布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("financeTabWidget")
        
        # 打单列表标签页
        self.orders_tab = QWidget()
        self.setup_orders_tab()
        self.tab_widget.addTab(self.orders_tab, "打单列表")
        
        # 订单统计标签页（暂时空白）
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        stats_label = QLabel("订单统计")
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_label.setStyleSheet("color: #666; font-size: 16px;")
        stats_layout.addWidget(stats_label)
        self.tab_widget.addTab(stats_tab, "订单统计")
        
        main_layout.addWidget(self.tab_widget)
        
    def setup_orders_tab(self):
        """设置打单列表标签页"""
        layout = QVBoxLayout(self.orders_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 工具栏
        self.setup_toolbar(layout)
        
        # 表格
        self.setup_table(layout)
        
        # 合计行
        self.setup_summary(layout)
        
    def setup_toolbar(self, parent_layout):
        """设置工具栏"""
        toolbar_container = QWidget()
        toolbar_container.setObjectName("toolbarContainer")
        
        # 主要水平布局
        main_toolbar_layout = QHBoxLayout(toolbar_container)
        main_toolbar_layout.setContentsMargins(0, 0, 0, 0)
        main_toolbar_layout.setSpacing(15)
        
        # 左侧筛选区域
        filters_widget = QWidget()
        filters_layout = QVBoxLayout(filters_widget)
        filters_layout.setContentsMargins(0,0,0,0)
        filters_layout.setSpacing(10)
        
        # 第一行筛选
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)

        # 客户名称
        row1_layout.addWidget(QLabel("客户名称:"))
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("请输入客户单位名称")
        self.customer_name_input.setFixedWidth(180)
        row1_layout.addWidget(self.customer_name_input)

        # 订单状态
        row1_layout.addWidget(QLabel("订单状态:"))
        self.status_combo = QComboBox()
        self.status_combo.addItem("全部", None)
        self.status_combo.addItem("待付款", "待付款")
        self.status_combo.addItem("已付款", "已付款")
        self.status_combo.addItem("已完成", "已完成")
        self.status_combo.addItem("已取消", "已取消")
        self.status_combo.setFixedWidth(120)
        row1_layout.addWidget(self.status_combo)
        row1_layout.addStretch()

        # 第二行筛选
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(5)

        # 签单日期
        self.sign_date_start_edit, self.sign_date_end_edit = self._create_date_range_picker(row2_layout, "签单日期:")
        # 生效日期
        self.effective_date_start_edit, self.effective_date_end_edit = self._create_date_range_picker(row2_layout, "生效日期:")
        # 到期日期
        self.expiry_date_start_edit, self.expiry_date_end_edit = self._create_date_range_picker(row2_layout, "到期日期:")
        row2_layout.addStretch()

        filters_layout.addLayout(row1_layout)
        filters_layout.addLayout(row2_layout)
        
        main_toolbar_layout.addWidget(filters_widget)

        # 右侧按钮区域
        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.search_btn = QPushButton("查询")
        self.search_btn.setObjectName("searchButton")
        self.search_btn.setFixedSize(80, 32)
        
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setObjectName("resetButton")
        self.reset_btn.setFixedSize(80, 32)
        
        buttons_layout.addWidget(self.search_btn)
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addStretch()
        
        main_toolbar_layout.addLayout(buttons_layout)
        main_toolbar_layout.addStretch()
        
        parent_layout.addWidget(toolbar_container)
        
        # 连接信号
        self.search_btn.clicked.connect(self.search_orders)
        self.reset_btn.clicked.connect(self.reset_filters)

    def _create_date_range_picker(self, layout, label_text):
        """辅助函数，用于创建带标签的日期范围选择器"""
        layout.addWidget(QLabel(label_text))
        start_date_edit = QDateEdit()
        start_date_edit.setCalendarPopup(True)
        start_date_edit.clear()
        start_date_edit.setSpecialValueText("开始日期")
        start_date_edit.setFixedWidth(120)
        layout.addWidget(start_date_edit)
        
        layout.addWidget(QLabel("至"))
        
        end_date_edit = QDateEdit()
        end_date_edit.setCalendarPopup(True)
        end_date_edit.clear()
        end_date_edit.setSpecialValueText("结束日期")
        end_date_edit.setFixedWidth(120)
        layout.addWidget(end_date_edit)
        
        # 添加间隔
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer)
        
        return start_date_edit, end_date_edit
        
    def setup_table(self, parent_layout):
        """使用QTableView设置表格"""
        self.table = QTableView()
        self.table.setObjectName("financeTable")
        self.model = QStandardItemModel(self)
        self.table.setModel(self.model)

        # 表格设置
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.setup_table_headers()
        
        parent_layout.addWidget(self.table)

    def setup_table_headers(self):
        """设置表头和列宽"""
        headers = [
            "序号", "客户单位", "产品名称", "型号规格", "产品定价", "实际售价",
            "数量", "单位", "订单金额", "销售提成", "主管提成", "经理提成",
            "签单日期", "销售人", "订单状态", "到账日期", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # 固定宽度
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        
        # 可伸展列
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        # 其他列使用交互式调整，并设置初始宽度
        self.table.setColumnWidth(3, 100) # 型号规格
        self.table.setColumnWidth(4, 90)  # 产品定价
        self.table.setColumnWidth(5, 90)  # 实际售价
        self.table.setColumnWidth(6, 60)  # 数量
        self.table.setColumnWidth(7, 60)  # 单位
        self.table.setColumnWidth(8, 90)  # 订单金额
        self.table.setColumnWidth(9, 90)  # 销售提成
        self.table.setColumnWidth(10, 90) # 主管提成
        self.table.setColumnWidth(11, 90) # 经理提成
        self.table.setColumnWidth(12, 110) # 签单日期
        self.table.setColumnWidth(13, 80) # 销售人
        self.table.setColumnWidth(14, 90) # 订单状态
        self.table.setColumnWidth(15, 110) # 到账日期
        self.table.setColumnWidth(16, 100) # 操作
        
    def setup_summary(self, parent_layout):
        """设置底部合计行"""
        summary_frame = QFrame()
        summary_frame.setObjectName("summaryFrame")
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setContentsMargins(10, 10, 10, 10)
        summary_layout.setSpacing(20)
        
        # 合计标签
        summary_layout.addWidget(QLabel("合计"))
        
        # 添加空白填充到订单金额列位置
        summary_layout.addSpacerItem(QSpacerItem(600, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        
        # 订单金额合计
        self.total_amount_label = QLabel("0.00")
        self.total_amount_label.setObjectName("summaryValue")
        self.total_amount_label.setFixedWidth(90)
        self.total_amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.total_amount_label)
        
        # 销售提成合计
        self.sales_commission_label = QLabel("0.00")
        self.sales_commission_label.setObjectName("summaryValue")
        self.sales_commission_label.setFixedWidth(90)
        self.sales_commission_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.sales_commission_label)
        
        # 主管提成合计
        self.manager_commission_label = QLabel("0.00")
        self.manager_commission_label.setObjectName("summaryValue")
        self.manager_commission_label.setFixedWidth(90)
        self.manager_commission_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.manager_commission_label)
        
        # 经理提成合计
        self.director_commission_label = QLabel("0.00")
        self.director_commission_label.setObjectName("summaryValue")
        self.director_commission_label.setFixedWidth(90)
        self.director_commission_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.director_commission_label)
        
        # 添加右侧空白填充
        summary_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        parent_layout.addWidget(summary_frame)
        
    def load_basic_data(self):
        """加载基础数据（客户、产品、员工）"""
        try:
            self.customers_data = get_customers() or []
            self.products_data = get_products() or []
            self.employees_data = get_employees() or []
        except Exception as e:
            print(f"加载基础数据错误: {e}")
            
    def load_orders_data(self):
        """加载订单数据"""
        try:
            self.orders_data = get_orders() or []
            self.populate_table()
            self.update_summary()
        except Exception as e:
            print(f"加载订单数据错误: {e}")
            
    def populate_table(self):
        pass
        """使用QStandardItemModel填充表格数据"""
        self.model.removeRows(0, self.model.rowCount())

        for row_index, order in enumerate(self.orders_data):
            # 订单项信息（假设一个订单只有一个产品）
            order_item_data = order.get("order_items", [{}])[0]
            product_info = self.get_product_info(order_item_data.get("product_id"))
            
            def format_decimal(value, default=0):
                return f"{Decimal(value or default):.2f}"
            
            def format_date(date_str):
                if not date_str: return ""
                return date_str.split("T")[0]

            # 准备数据项
            items = [
                QStandardItem(str(row_index + 1)),
                QStandardItem(self.get_customer_name(order.get("customer_id"))),
                QStandardItem(product_info.get("name", "")),
                QStandardItem(product_info.get("spec", "")),
                QStandardItem(format_decimal(product_info.get('price'))), # 'price' is the base price
                QStandardItem(format_decimal(order_item_data.get('unit_price'))),
                QStandardItem(str(order_item_data.get("quantity", 0))),
                QStandardItem(product_info.get("unit", "")),
                QStandardItem(format_decimal(order.get('total_amount'))),
                QStandardItem(format_decimal(product_info.get('sales_commission'))),
                QStandardItem(format_decimal(product_info.get('manager_commission'))),
                QStandardItem(format_decimal(product_info.get('director_commission'))),
                QStandardItem(format_date(order.get("created_at"))),
                QStandardItem(self.get_employee_name(order.get("sales_id"))),
                QStandardItem(order.get("status", "")),
                QStandardItem(format_date(order.get("payment_date"))),
                QStandardItem() # Placeholder for button
            ]
            
            # 设置文本居中
            for i in [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
                items[i].setTextAlignment(Qt.AlignCenter)
                
            self.model.appendRow(items)

            # 操作按钮
            is_paid = order.get("status") in ["已付款", "已完成", "已发货", "部分付款"]
            action_btn = QPushButton("确认收款")
            action_btn.setObjectName("actionButton")
            action_btn.setEnabled(not is_paid)
            if is_paid:
                action_btn.setText("已收款")

            action_btn.clicked.connect(lambda checked, o=order: self.confirm_payment(o.get("id")))
            self.table.setIndexWidget(self.model.index(row_index, 16), action_btn)
            
    def get_customer_name(self, customer_id):
        """根据客户ID获取客户名称"""
        for customer in self.customers_data:
            if customer.get("id") == customer_id:
                return customer.get("company", "")
        return ""
        
    def get_product_info(self, product_id):
        """根据产品ID获取产品信息"""
        for product in self.products_data:
            if product.get("id") == product_id:
                return product
        return {}
        
    def get_employee_name(self, employee_id):
        """根据员工ID获取员工姓名"""
        for employee in self.employees_data:
            if employee.get("id") == employee_id:
                return employee.get("name", "")
        return ""
        
    def update_summary(self):
        """更新合计行"""
        total_amount = Decimal('0')
        total_sales_commission = Decimal('0')
        total_manager_commission = Decimal('0')
        total_director_commission = Decimal('0')
        
        for order in self.orders_data:
            total_amount += Decimal(str(order.get("total_amount", 0)))
            
            # 计算提成
            for item in order.get("order_items", []):
                product = self.get_product_info(item.get("product_id"))
                quantity = int(item.get("quantity", 0))
                
                total_sales_commission += Decimal(str(product.get('sales_commission', 0))) * quantity
                total_manager_commission += Decimal(str(product.get('manager_commission', 0))) * quantity
                total_director_commission += Decimal(str(product.get('director_commission', 0))) * quantity
        
        self.total_amount_label.setText(f"{total_amount:.2f}")
        self.sales_commission_label.setText(f"{total_sales_commission:.2f}")
        self.manager_commission_label.setText(f"{total_manager_commission:.2f}")
        self.director_commission_label.setText(f"{total_director_commission:.2f}")
        
    def search_orders(self):
        """搜索订单"""
        try:
            params = {}
            
            customer_name = self.customer_name_input.text().strip()
            if customer_name:
                params['customer_name'] = customer_name
                
            if self.status_combo.currentIndex() > 0:
                params['status'] = self.status_combo.currentText()

            # 日期范围筛选
            if self.sign_date_start_edit.date().isValid():
                params['sign_date_start'] = self.sign_date_start_edit.date().toString(Qt.ISODate)
            if self.sign_date_end_edit.date().isValid():
                params['sign_date_end'] = self.sign_date_end_edit.date().toString(Qt.ISODate)

            if self.effective_date_start_edit.date().isValid():
                params['effective_date_start'] = self.effective_date_start_edit.date().toString(Qt.ISODate)
            if self.effective_date_end_edit.date().isValid():
                params['effective_date_end'] = self.effective_date_end_edit.date().toString(Qt.ISODate)

            if self.expiry_date_start_edit.date().isValid():
                params['expiry_date_start'] = self.expiry_date_start_edit.date().toString(Qt.ISODate)
            if self.expiry_date_end_edit.date().isValid():
                params['expiry_date_end'] = self.expiry_date_end_edit.date().toString(Qt.ISODate)

            self.orders_data = get_orders(params) or []
            self.populate_table()
            self.update_summary()
            
        except Exception as e:
            print(f"搜索订单时发生错误: {e}")
            self.load_orders_data()
        
    def reset_filters(self):
        """重置筛选条件"""
        self.customer_name_input.clear()
        self.status_combo.setCurrentIndex(0)
        
        self.sign_date_start_edit.clear()
        self.sign_date_end_edit.clear()
        self.effective_date_start_edit.clear()
        self.effective_date_end_edit.clear()
        self.expiry_date_start_edit.clear()
        self.expiry_date_end_edit.clear()
        
        self.load_orders_data()
        
    def confirm_payment(self, order_id):
        """确认收款"""
        try:
            from PySide6.QtWidgets import QMessageBox
            from ..api.orders import update_order_financials
            
            # 弹出确认对话框
            reply = QMessageBox.question(
                self, 
                '确认收款', 
                f'确定要标记订单 {order_id} 为已收款吗？',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # 找到对应的订单
                order_to_update = None
                for order in self.orders_data:
                    if order.get("id") == order_id:
                        order_to_update = order
                        break
                
                if order_to_update:
                    # 准备财务更新数据
                    financial_data = {
                        "status": "已付款",
                        "paid_amount": float(order_to_update.get("total_amount", 0)),
                        "payment_date": datetime.now().isoformat()
                    }
                    
                    # 调用API更新
                    result = update_order_financials(order_id, financial_data)
                    
                    if result:
                        QMessageBox.information(self, "成功", "订单收款状态已更新！")
                        # 刷新数据
                        self.load_orders_data()
                    else:
                        QMessageBox.warning(self, "错误", "更新订单状态失败，请重试。")
                else:
                    QMessageBox.warning(self, "错误", "未找到指定的订单。")
                    
        except Exception as e:
            print(f"确认收款时发生错误: {e}")
            QMessageBox.critical(self, "错误", f"操作失败: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = FinanceView()
    view.show()
    sys.exit(app.exec())