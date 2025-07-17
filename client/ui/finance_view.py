import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, 
    QHeaderView, QAbstractItemView, QSizePolicy, QFrame, QSpacerItem
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
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
        stats_label = QLabel("订单统计（本期不做）")
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
        
        # 筛选栏
        self.setup_filters(layout)
        
        # 表格
        self.setup_table(layout)
        
        # 合计行
        self.setup_summary(layout)
        
    def setup_filters(self, parent_layout):
        """设置筛选栏"""
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setSpacing(10)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        
        # 输入客户名称
        filter_layout.addWidget(QLabel("输入客户名称"))
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("输入客户名称")
        self.customer_name_input.setFixedWidth(150)
        filter_layout.addWidget(self.customer_name_input)
        
        # 产品名称下拉
        filter_layout.addWidget(QLabel("产品名称"))
        self.product_combo = QComboBox()
        self.product_combo.setFixedWidth(120)
        self.product_combo.addItem("全部", None)
        filter_layout.addWidget(self.product_combo)
        
        # 生效日期下拉
        filter_layout.addWidget(QLabel("生效日期"))
        self.effective_date_combo = QComboBox()
        self.effective_date_combo.setFixedWidth(120)
        self.effective_date_combo.addItem("全部", None)
        filter_layout.addWidget(self.effective_date_combo)
        
        # 到期日期下拉
        filter_layout.addWidget(QLabel("到期日期"))
        self.expire_date_combo = QComboBox()
        self.expire_date_combo.setFixedWidth(120)
        self.expire_date_combo.addItem("全部", None)
        filter_layout.addWidget(self.expire_date_combo)
        
        # 签单日期下拉
        filter_layout.addWidget(QLabel("签单日期"))
        self.sign_date_combo = QComboBox()
        self.sign_date_combo.setFixedWidth(120)
        self.sign_date_combo.addItem("全部", None)
        filter_layout.addWidget(self.sign_date_combo)
        
        # 订单状态下拉
        filter_layout.addWidget(QLabel("订单状态"))
        self.status_combo = QComboBox()
        self.status_combo.setFixedWidth(100)
        self.status_combo.addItem("全部", None)
        self.status_combo.addItem("待付款", "待付款")
        self.status_combo.addItem("已付款", "已付款")
        self.status_combo.addItem("已完成", "已完成")
        self.status_combo.addItem("已取消", "已取消")
        filter_layout.addWidget(self.status_combo)
        
        # 销售人下拉
        filter_layout.addWidget(QLabel("销售人"))
        self.sales_combo = QComboBox()
        self.sales_combo.setFixedWidth(100)
        self.sales_combo.addItem("全部", None)
        filter_layout.addWidget(self.sales_combo)
        
        # 查询和重置按钮
        self.search_btn = QPushButton("查询")
        self.search_btn.setObjectName("searchButton")
        self.search_btn.setFixedWidth(80)
        filter_layout.addWidget(self.search_btn)
        
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setObjectName("resetButton")
        self.reset_btn.setFixedWidth(80)
        filter_layout.addWidget(self.reset_btn)
        
        # 添加弹性空间
        filter_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        parent_layout.addWidget(filter_frame)
        
        # 连接信号
        self.search_btn.clicked.connect(self.search_orders)
        self.reset_btn.clicked.connect(self.reset_filters)
        
    def setup_table(self, parent_layout):
        """设置表格"""
        self.table = QTableWidget()
        self.table.setObjectName("financeTable")
        
        # 设置列
        headers = [
            "序号", "客户单位", "产品名称", "型号规格", "产品定价", "实际售价", 
            "数量", "单位", "订单金额", "销售提成", "主管提成", "经理提成",
            "签单日期", "销售人", "订单状态", "到期日期", "操作"
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # 表格设置
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # 设置列宽策略
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 序号
        header.resizeSection(0, 60)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # 客户单位
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # 产品名称
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # 型号规格
        header.resizeSection(3, 100)
        for i in range(4, 12):  # 价格和提成列
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            header.resizeSection(i, 90)
        header.setSectionResizeMode(12, QHeaderView.ResizeMode.Fixed)  # 签单日期
        header.resizeSection(12, 100)
        header.setSectionResizeMode(13, QHeaderView.ResizeMode.Fixed)  # 销售人
        header.resizeSection(13, 80)
        header.setSectionResizeMode(14, QHeaderView.ResizeMode.Fixed)  # 订单状态
        header.resizeSection(14, 80)
        header.setSectionResizeMode(15, QHeaderView.ResizeMode.Fixed)  # 到期日期
        header.resizeSection(15, 100)
        header.setSectionResizeMode(16, QHeaderView.ResizeMode.Fixed)  # 操作
        header.resizeSection(16, 120)
        
        parent_layout.addWidget(self.table)
        
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
            
            # 填充产品下拉框
            self.product_combo.clear()
            self.product_combo.addItem("全部", None)
            for product in self.products_data:
                self.product_combo.addItem(product.get("name", ""), product.get("id"))
                
            # 填充销售人员下拉框
            self.sales_combo.clear()
            self.sales_combo.addItem("全部", None)
            for employee in self.employees_data:
                if employee.get("role") == "sales":
                    self.sales_combo.addItem(employee.get("name", ""), employee.get("id"))
                    
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
        """填充表格数据"""
        self.table.setRowCount(len(self.orders_data))
        
        for row, order in enumerate(self.orders_data):
            # 序号
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            
            # 客户单位
            customer_name = self.get_customer_name(order.get("customer_id"))
            self.table.setItem(row, 1, QTableWidgetItem(customer_name))
            
            # 订单项信息（假设一个订单只有一个产品，如果有多个需要特殊处理）
            order_items = order.get("order_items", [])
            if order_items:
                item = order_items[0]  # 取第一个产品
                product = self.get_product_info(item.get("product_id"))
                
                # 产品名称
                self.table.setItem(row, 2, QTableWidgetItem(product.get("name", "")))
                # 型号规格
                self.table.setItem(row, 3, QTableWidgetItem(product.get("spec", "")))
                # 产品定价
                self.table.setItem(row, 4, QTableWidgetItem(f"{float(product.get('base_price', 0)):.2f}"))
                # 实际售价
                self.table.setItem(row, 5, QTableWidgetItem(f"{float(item.get('unit_price', 0)):.2f}"))
                # 数量
                self.table.setItem(row, 6, QTableWidgetItem(str(item.get("quantity", 0))))
                # 单位
                self.table.setItem(row, 7, QTableWidgetItem(product.get("unit", "")))
                # 订单金额
                self.table.setItem(row, 8, QTableWidgetItem(f"{float(order.get('total_amount', 0)):.2f}"))
                # 销售提成
                sales_commission = float(product.get('sales_commission', 0)) * int(item.get("quantity", 0))
                self.table.setItem(row, 9, QTableWidgetItem(f"{sales_commission:.2f}"))
                # 主管提成
                manager_commission = float(product.get('manager_commission', 0)) * int(item.get("quantity", 0))
                self.table.setItem(row, 10, QTableWidgetItem(f"{manager_commission:.2f}"))
                # 经理提成
                director_commission = float(product.get('director_commission', 0)) * int(item.get("quantity", 0))
                self.table.setItem(row, 11, QTableWidgetItem(f"{director_commission:.2f}"))
            else:
                # 如果没有订单项，填充空值
                for col in range(2, 12):
                    self.table.setItem(row, col, QTableWidgetItem(""))
            
            # 签单日期
            created_at = order.get("created_at", "")
            if created_at:
                date_str = created_at.split("T")[0] if "T" in created_at else created_at
                self.table.setItem(row, 12, QTableWidgetItem(date_str))
            else:
                self.table.setItem(row, 12, QTableWidgetItem(""))
                
            # 销售人
            sales_name = self.get_employee_name(order.get("sales_id"))
            self.table.setItem(row, 13, QTableWidgetItem(sales_name))
            
            # 订单状态
            self.table.setItem(row, 14, QTableWidgetItem(order.get("status", "")))
            
            # 到期日期
            end_date = order.get("end_date", "")
            if end_date:
                date_str = end_date.split("T")[0] if "T" in end_date else end_date
                self.table.setItem(row, 15, QTableWidgetItem(date_str))
            else:
                self.table.setItem(row, 15, QTableWidgetItem(""))
                
            # 操作按钮
            action_btn = QPushButton("确认收款")
            action_btn.setObjectName("actionButton")
            action_btn.clicked.connect(lambda checked, order_id=order.get("id"): self.confirm_payment(order_id))
            self.table.setCellWidget(row, 16, action_btn)
            
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
            # 获取筛选条件
            params = {}
            
            # 客户名称筛选
            customer_name = self.customer_name_input.text().strip()
            if customer_name:
                params['customer_name'] = customer_name
                
            # 产品名称筛选
            product_id = self.product_combo.currentData()
            if product_id:
                product_name = self.product_combo.currentText()
                params['product_name'] = product_name
                
            # 订单状态筛选
            status = self.status_combo.currentData()
            if status:
                params['status'] = status
                
            # 销售人员筛选
            sales_id = self.sales_combo.currentData()
            if sales_id:
                params['sales_id'] = sales_id
            
            # 调用API获取筛选后的数据
            self.orders_data = get_orders(params) or []
            self.populate_table()
            self.update_summary()
            
        except Exception as e:
            print(f"搜索订单时发生错误: {e}")
            # 如果搜索失败，加载所有数据
            self.load_orders_data()
        
    def reset_filters(self):
        """重置筛选条件"""
        self.customer_name_input.clear()
        self.product_combo.setCurrentIndex(0)
        self.effective_date_combo.setCurrentIndex(0)
        self.expire_date_combo.setCurrentIndex(0)
        self.sign_date_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        self.sales_combo.setCurrentIndex(0)
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