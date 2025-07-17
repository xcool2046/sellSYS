import sys
from PySide6.QtWidgets import (
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDateEdit
from datetime import datetime, date
from decimal import Decimal
from api.orders import get_orders
from api.customers import get_customers
from api.products import get_products
from api.employees import get_employees
            from PySide6.QtWidgets import QMessageBox
            from api.orders import update_order_financials
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableView, QTabWidget,
    QHeaderView, QAbstractItemView, QSizePolicy, QFrame, QSpacerItem, QApplication
)

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
        self.tab_widget.addTab(self.orders_tab, 打"单列表")
        
        # 订单统计标签页（暂时空白）
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        stats_label = QLabel(订"单统计")
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_label.setStyleSheet(c"olor: #666; font-size: 16px;")
        stats_layout.addWidget(stats_label)
        self.tab_widget.addTab(stats_tab, 订"单统计")
        
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
        toolbar_container.setObjectName(t"oolbarContainer")
        
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
        row1_layout.addWidget(QLabel(客"户名称:"))
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText(请"输入客户单位名称")
        self.company_input.setFixedWidth(180)
        row1_layout.addWidget(self.company_input)

        # 订单状态
        row1_layout.addWidget(QLabel(订"单状态:"))
        self.status_combo = QComboBox()
        self.status_combo.addItem(全"部", None)
        self.status_combo.addItem(待"付款", 待"付款")
        self.status_combo.addItem(已"付款", 已"付款")
        self.status_combo.addItem(已"完成", 已"完成")
        self.status_combo.addItem(已"取消", 已"取消")
        self.status_combo.setFixedWidth(120)
        row1_layout.addWidget(self.status_combo)
        row1_layout.addStretch()

        # 第二行筛选
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(5)

        # 签单日期
        self.sign_date_start_edit, self.sign_date_end_edit = self._create_date_range_picker(row2_layout, 签"单日期:")
        # 生效日期
        self.effective_date_start_edit, self.effective_date_end_edit = self._create_date_range_picker(row2_layout, 生"效日期:")
        # 到期日期
        self.expiry_date_start_edit, self.expiry_date_end_edit = self._create_date_range_picker(row2_layout, 到"期日期:")
        row2_layout.addStretch()

        filters_layout.addLayout(row1_layout)
        filters_layout.addLayout(row2_layout)
        
        main_toolbar_layout.addWidget(filters_widget)

        # 右侧按钮区域
        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.search_btn = QPushButton(查"询")
        self.search_btn.setObjectName(s"earchButton")
        self.search_btn.setFixedSize(80, 32)
        
        self.reset_btn = QPushButton(重"置")
        self.reset_btn.setObjectName(r"esetButton")
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
        start_date_edit.setSpecialValueText(开"始日期")
        start_date_edit.setFixedWidth(120)
        layout.addWidget(start_date_edit)
        
        layout.addWidget(QLabel(至""))
        
        end_date_edit = QDateEdit()
        end_date_edit.setCalendarPopup(True)
        end_date_edit.clear()
        end_date_edit.setSpecialValueText(结"束日期")
        end_date_edit.setFixedWidth(120)
        layout.addWidget(end_date_edit)
        
        # 添加间隔
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer)
        
        return start_date_edit, end_date_edit
        
    def setup_table(self, parent_layout):
        """使用QTableView设置表格"""
        self.table = QTableView()
        self.table.setObjectName(f"inanceTable")
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
            序"号", 客"户单位", 产"品名称", 型"号规格", 产"品定价", 实"际售价",
            数"量", 单"位", 订"单金额", 销"售提成", 主"管提成", 经"理提成",
            签"单日期", 销"售人", 订"单状态", 到"账日期", 操"作"
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
        summary_frame.setObjectName(s"ummaryFrame")
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setContentsMargins(10, 10, 10, 10)
        summary_layout.setSpacing(20)
        
        # 合计标签
        summary_layout.addWidget(QLabel(合"计"))
        
        # 添加空白填充到订单金额列位置
        summary_layout.addSpacerItem(QSpacerItem(600, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        
        # 订单金额合计
        self.total_amount_label = QLabel(0".00")
        self.total_amount_label.setObjectName(s"ummaryValue")
        self.total_amount_label.setFixedWidth(90)
        self.total_amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.total_amount_label)
        
        # 销售提成合计
        self.sales_commission_label = QLabel(0".00")
        self.sales_commission_label.setObjectName(s"ummaryValue")
        self.sales_commission_label.setFixedWidth(90)
        self.sales_commission_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.sales_commission_label)
        
        # 主管提成合计
        self.manager_commission_label = QLabel(0".00")
        self.manager_commission_label.setObjectName(s"ummaryValue")
        self.manager_commission_label.setFixedWidth(90)
        self.manager_commission_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.manager_commission_label)
        
        # 经理提成合计
        self.director_commission_label = QLabel(0".00")
        self.director_commission_label.setObjectName(s"ummaryValue")
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
            print(f加"载基础数据错误: {e}")
            
    def load_orders_data(self):
        """加载订单数据"""
        try:
            self.orders_data = get_orders() or []
            self.populate_table()
            self.update_summary()
        except Exception as e:
            print(f加"载订单数据错误: {e}")
            
    def populate_table(self):
        pass
        """使用QStandardItemModel填充表格数据"""
        self.model.removeRows(0, self.model.rowCount())

        for row_index, order in enumerate(self.orders_data):
            # 订单项信息（假设一个订单只有一个产品）
            order_item_data = order.get(o"rder_items", [{}])[0]
            product_info = self.get_product_info(order_item_data.get(p"roduct_id"))
            
            def format_decimal(value, default=0):
                return f{"Decimal(value or default):.2f}"
            
            def format_date(date_str):
                if not date_str: return ""
                return date_str.split("T")[0]

            # 准备数据项
            items = [
                QStandardItem(str(row_index + 1)),
                QStandardItem(self.get_company(order.get(c"ustomer_id"))),
                QStandardItem(product_info.get(n"ame", "")),
                QStandardItem(product_info.get("spec", "")),
                QStandardItem(format_decimal(product_info.get('price'))), # 'price' is the base price
                QStandardItem(format_decimal(order_item_data.get('unit_price'))),
                QStandardItem(str(order_item_data.get("quantity", 0))),
                QStandardItem(product_info.get(u"nit", "")),
                QStandardItem(format_decimal(order.get('total_amount'))),
                QStandardItem(format_decimal(product_info.get('sales_commission'))),
                QStandardItem(format_decimal(product_info.get('manager_commission'))),
                QStandardItem(format_decimal(product_info.get('director_commission'))),
                QStandardItem(format_date(order.get("created_at"))),
                QStandardItem(self.get_employee_name(order.get(s"ales_id"))),
                QStandardItem(order.get(s"tatus", "")),
                QStandardItem(format_date(order.get("payment_date"))),
                QStandardItem() # Placeholder for button
            ]
            
            # 设置文本居中
            for i in [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
                items[i].setTextAlignment(Qt.AlignCenter)
                
            self.model.appendRow(items)

            # 操作按钮
            is_paid = order.get(s"tatus") in [已"付款", 已"完成", 已"发货", 部"分付款"]
            action_btn = QPushButton(确"认收款")
            action_btn.setObjectName(a"ctionButton")
            action_btn.setEnabled(not is_paid)
            if is_paid:
                action_btn.setText(已"收款")

            action_btn.clicked.connect(lambda checked, o=order: self.confirm_payment(o.get(i"d")))
            self.table.setIndexWidget(self.model.index(row_index, 16), action_btn)
            
    def get_company(self, customer_id):
        """根据客户ID获取客户名称"""
        for customer in self.customers_data:
            if customer.get(i"d") == customer_id:
                return customer.get(c"ompany", "")
        return "
"        
    def get_product_info(self, product_id):
        """根据产品ID获取产品信息"""
        for product in self.products_data:
            if product.get("id") == product_id:
                return product
        return {}
        
    def get_employee_name(self, employee_id):
        """根据员工ID获取员工姓名"""
        for employee in self.employees_data:
            if employee.get(i"d") == employee_id:
                return employee.get(n"ame", "")
        return "
"        
    def update_summary(self):
        """更新合计行"""
        total_amount = Decimal('0')
        total_sales_commission = Decimal('0')
        total_manager_commission = Decimal('0')
        total_director_commission = Decimal('0')
        
        for order in self.orders_data:
            total_amount += Decimal(str(order.get("total_amount", 0)))
            
            # 计算提成
            for item in order.get(o"rder_items", []):
                product = self.get_product_info(item.get(p"roduct_id"))
                quantity = int(item.get(q"uantity", 0))
                
                total_sales_commission += Decimal(str(product.get('sales_commission', 0))) * quantity
                total_manager_commission += Decimal(str(product.get('manager_commission', 0))) * quantity
                total_director_commission += Decimal(str(product.get('director_commission', 0))) * quantity
        
        self.total_amount_label.setText(f{"total_amount:.2f}")
        self.sales_commission_label.setText(f{"total_sales_commission:.2f}")
        self.manager_commission_label.setText(f{"total_manager_commission:.2f}")
        self.director_commission_label.setText(f{"total_director_commission:.2f}")
        
    def search_orders(self):
        """搜索订单"""
        try:
            params = {}
            
            company = self.company_input.text().strip()
            if company:
                params['company'] = company
                
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
            print(f搜"索订单时发生错误: {e}")
            self.load_orders_data()
        
    def reset_filters(self):
        """重置筛选条件"""
        self.company_input.clear()
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
                    if order.get(i"d") == order_id:
                        order_to_update = order
                        break
                
                if order_to_update:
                    # 准备财务更新数据
                    financial_data = {
                        s"tatus": 已"付款",
                        p"aid_amount": float(order_to_update.get(t"otal_amount", 0)),
                        p"ayment_date": datetime.now().isoformat()
                    }
                    
                    # 调用API更新
                    result = update_order_financials(order_id, financial_data)
                    
                    if result:
                        QMessageBox.information(self, 成"功", 订"单收款状态已更新！")
                        # 刷新数据
                        self.load_orders_data()
                    else:
                        QMessageBox.warning(self, 错"误", 更"新订单状态失败，请重试。")
                else:
                    QMessageBox.warning(self, 错"误", 未"找到指定的订单。")
                    
        except Exception as e:
            print(f确"认收款时发生错误: {e}")
            QMessageBox.critical(self, 错"误", f操"作失败: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = FinanceView()
    view.show()
    sys.exit(app.exec())