import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableView,
    QHeaderView, QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from api import sales_view as sales_view_api
from api import employees as employees_api
from api import contacts as contacts_api
from .sales_contact_view_dialog import SalesContactViewDialog

class SalesManagementView(QWidget):
    """
    销售管理视图
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("销售管理")
        
        # --- Layouts ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Data Storage ---
        self.table_data = []  # To store full dictionary for each row
        self.selected_customer_ids = set()

        # --- Filter Section ---
        filter_widget = QWidget()
        filter_widget.setObjectName("filterSection")
        filter_widget.setFixedHeight(70)
        filter_layout = QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(20, 15, 20, 15)
        filter_layout.setSpacing(10)

        # --- Filter Widgets ---
        self.customer_name_filter = QLineEdit()
        self.customer_name_filter.setPlaceholderText("客户名称")
        self.customer_name_filter.setObjectName("filterInput")

        self.province_filter = QComboBox()
        self.province_filter.addItem("省份", None)
        self.province_filter.setObjectName("filterCombo")
        
        self.city_filter = QComboBox()
        self.city_filter.addItem("城市", None)
        self.city_filter.setObjectName("filterCombo")

        self.status_filter = QComboBox()
        self.status_filter.addItem("联系状态", None)
        self.status_filter.setObjectName("filterCombo")
        
        self.intention_filter = QComboBox()
        self.intention_filter.addItem("客户意向", None)
        self.intention_filter.setObjectName("filterCombo")
        
        self.sales_owner_filter = QComboBox()
        self.sales_owner_filter.addItem("销售人", None)
        self.sales_owner_filter.setObjectName("filterCombo")

        self.search_button = QPushButton("查询")
        self.search_button.setObjectName("searchButton")
        
        self.reset_button = QPushButton("重置")
        self.reset_button.setObjectName("resetButton")
        
        filter_layout.addWidget(self.customer_name_filter)
        filter_layout.addWidget(self.province_filter)
        filter_layout.addWidget(self.city_filter)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(self.intention_filter)
        filter_layout.addWidget(self.sales_owner_filter)
        filter_layout.addWidget(self.search_button)
        filter_layout.addWidget(self.reset_button)
        filter_layout.addStretch()

        # --- Content Widget ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 2. 表格视图
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model = QStandardItemModel()
        self.setup_table_headers()
        self.table_view.setModel(self.model)
        
        content_layout.addWidget(self.table_view)
        
        # --- Assembly ---
        main_layout.addWidget(filter_widget)
        main_layout.addWidget(content_widget)
        
        # --- Connections ---
        self.search_button.clicked.connect(self.filter_data)
        self.reset_button.clicked.connect(self.reset_filters)
        self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        # --- Initialization ---
        self.populate_filters()
        self.load_data()

    def setup_table_headers(self):
        headers = [
            "ID", "省份", "城市", "客户单位", "联系人", "联系状态", 
            "客户意向", "联系记录", "订单", "下次预约日期", "销售人", "更新时间", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)
        self.table_view.setColumnHidden(0, True) # Hide ID

    def load_data(self):
        """加载主数据"""
        self.model.removeRows(0, self.model.rowCount())
        self.table_data.clear()

        sales_data = sales_view_api.get_sales_view()
        if not sales_data:
            return
        
        self.table_data = sales_data

        for row, record in enumerate(self.table_data):
            items = [
                QStandardItem(str(record.get('id', ''))),
                QStandardItem(record.get('province', '')),
                QStandardItem(record.get('city', '')),
                QStandardItem(record.get('company', '')),
                QStandardItem(str(record.get('contact_count', 0))),
                QStandardItem(record.get('status', '')),
                QStandardItem(record.get('intention_level', '')),
                QStandardItem(str(record.get('sales_follow_count', 0))),
                QStandardItem(str(record.get('order_count', 0))),
                QStandardItem(record.get('next_follow_date', '') or 'N/A'),
                QStandardItem(record.get('sales_owner_name', '') or '未分配'),
                QStandardItem(record.get('updated_at', '').split('.')[0] if record.get('updated_at') else ''),
            ]
            self.model.appendRow(items)
            self.add_action_buttons(row)

    def add_action_buttons(self, row):
        """为表格行添加操作按钮"""
        contact_button = QPushButton("联系记录")
        order_button = QPushButton("订单记录")
        
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.addWidget(contact_button)
        buttons_layout.addWidget(order_button)
        buttons_layout.setContentsMargins(5, 0, 5, 0)
        buttons_layout.setAlignment(Qt.AlignCenter)

        contact_button.clicked.connect(lambda: self.view_contacts(row))
        order_button.clicked.connect(lambda: self.view_orders(row))

        self.table_view.setIndexWidget(self.model.index(row, 12), buttons_widget)
        
    def populate_filters(self):
        """填充筛选器选项"""
        # 获取所有销售数据以提取唯一值
        all_data = sales_view_api.get_sales_view() or []
        
        # 提取唯一值
        provinces = set()
        cities = set()
        
        for record in all_data:
            if record.get('province'):
                provinces.add(record['province'])
            if record.get('city'):
                cities.add(record['city'])
            
        # 填充省份
        for province in sorted(provinces):
            self.province_filter.addItem(province, province)
            
        # 填充城市
        for city in sorted(cities):
            self.city_filter.addItem(city, city)
        
        # 客户状态
        self.status_filter.addItem("潜在客户", "潜在客户")
        self.status_filter.addItem("已联系", "已联系")
        self.status_filter.addItem("已报价", "已报价")
        self.status_filter.addItem("成交客户", "成交客户")
        self.status_filter.addItem("流失客户", "流失客户")
        
        # 客户意向
        self.intention_filter.addItem("高", "高")
        self.intention_filter.addItem("中", "中")
        self.intention_filter.addItem("低", "低")

        # 销售人员
        sales_people = employees_api.get_employees({'role': 'sales'}) or []
        for emp in sales_people:
            self.sales_owner_filter.addItem(emp.get('name'), emp.get('id'))

    def _on_view_contacts_clicked(self, row):
        """Handles the logic to open the contact view dialog."""
        if row >= len(self.table_data):
            return

        customer_data = self.table_data[row]
        customer_id = customer_data.get('id')

        # Fetch contacts for the customer
        contacts_data = contacts_api.get_contacts({"customer_id": customer_id})

        dialog = SalesContactViewDialog(customer_data, contacts_data, self)
        dialog.exec()

    def view_contacts(self, row):
        self._on_view_contacts_clicked(row)

    def view_orders(self, row):
        customer_id = self.model.item(row, 0).text()
        QMessageBox.information(self, "查看订单记录", f"查看客户 ID: {customer_id} 的订单记录。")

    def on_selection_changed(self, selected, deselected):
        """Update the set of selected customer IDs."""
        self.selected_customer_ids.clear()
        for index in self.table_view.selectionModel().selectedRows():
            customer_id = self.model.item(index.row(), 0).text()
            if customer_id:
                self.selected_customer_ids.add(int(customer_id))
    
    def filter_data(self):
        """根据筛选条件过滤数据"""
        # 获取筛选参数
        company_name = self.customer_name_filter.text().strip()
        province = self.province_filter.currentData()
        city = self.city_filter.currentData()
        status = self.status_filter.currentData()
        intention = self.intention_filter.currentData()
        sales_owner_id = self.sales_owner_filter.currentData()
        
        # 清空表格
        self.model.removeRows(0, self.model.rowCount())
        self.table_data.clear()
        
        # 获取所有数据
        all_data = sales_view_api.get_sales_view()
        if not all_data:
            return
            
        # 过滤数据
        filtered_data = []
        for record in all_data:
            # 客户名称筛选
            if company_name and company_name.lower() not in record.get('company', '').lower():
                continue
                
            # 省份筛选
            if province and record.get('province') != province:
                continue
                
            # 城市筛选
            if city and record.get('city') != city:
                continue
                
            # 状态筛选
            if status and record.get('status') != status:
                continue
                
            # 意向筛选
            if intention and record.get('intention_level') != intention:
                continue
                
            # 销售人筛选
            if sales_owner_id and record.get('sales_owner_id') != sales_owner_id:
                continue
                
            filtered_data.append(record)
        
        # 显示过滤后的数据
        self.table_data = filtered_data
        for row, record in enumerate(self.table_data):
            items = [
                QStandardItem(str(record.get('id', ''))),
                QStandardItem(record.get('province', '')),
                QStandardItem(record.get('city', '')),
                QStandardItem(record.get('company', '')),
                QStandardItem(str(record.get('contact_count', 0))),
                QStandardItem(record.get('status', '')),
                QStandardItem(record.get('intention_level', '')),
                QStandardItem(str(record.get('sales_follow_count', 0))),
                QStandardItem(str(record.get('order_count', 0))),
                QStandardItem(record.get('next_follow_date', '') or 'N/A'),
                QStandardItem(record.get('sales_owner_name', '') or '未分配'),
                QStandardItem(record.get('updated_at', '').split('.')[0] if record.get('updated_at') else ''),
            ]
            self.model.appendRow(items)
            self.add_action_buttons(row)
    
    def reset_filters(self):
        """重置所有筛选条件"""
        self.customer_name_filter.clear()
        self.province_filter.setCurrentIndex(0)
        self.city_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.intention_filter.setCurrentIndex(0)
        self.sales_owner_filter.setCurrentIndex(0)
        self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = SalesManagementView()
    view.resize(1200, 700)
    view.show()
    sys.exit(app.exec())