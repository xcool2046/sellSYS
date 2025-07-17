import sys
from PySide6.QtWidgets import (
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QFont
from PySide6.QtCore import Qt
from api import sales_view as sales_view_api
from api import employees as employees_api
from api import contacts as contacts_api
from .sales_contact_view_dialog import SalesContactViewDialog
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableView,
    QHeaderView, QMessageBox
)


class SalesManagementView(QWidget):
    """
    销售管理视图
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("销售管理")
        
        # --- Layouts ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Data Storage ---
        self.table_data = []  # To store full dictionary for each row
        
        # --- Toolbar (Filters and Actions) ---
        toolbar_container = QWidget()
        toolbar_container.setObjectName("toolbarContainer")
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)

        self.customer_filter = QLineEdit()
        self.customer_filter.setPlaceholderText("客户单位")
        self.customer_filter.setObjectName("filterInput")
        toolbar_layout.addWidget(self.customer_filter)
        
        self.industry_filter = QComboBox()
        self.industry_filter.addItem("行业类别")
        self.industry_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.industry_filter)

        self.province_filter = QComboBox()
        self.province_filter.addItem("省份")
        self.province_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.province_filter)
        
        self.city_filter = QComboBox()
        self.city_filter.addItem("城市")
        self.city_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.city_filter)

        self.status_filter = QComboBox()
        self.status_filter.addItem("联系状态")
        self.status_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.status_filter)
        
        self.intention_filter = QComboBox()
        self.intention_filter.addItem("客户意向")
        self.intention_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.intention_filter)
        
        self.sales_filter = QComboBox()
        self.sales_filter.addItem("销售人")
        self.sales_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.sales_filter)

        self.search_button = QPushButton("查询")
        self.search_button.setObjectName("searchButton")
        toolbar_layout.addWidget(self.search_button)
        
        self.reset_button = QPushButton("重置")
        self.reset_button.setObjectName("resetButton")
        toolbar_layout.addWidget(self.reset_button)
        
        toolbar_layout.addStretch()
        
        # --- Table View ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.setup_table_headers()
        
        # --- Assembly ---
        main_layout.addWidget(toolbar_container)
        main_layout.addWidget(self.table_view)
        
        # --- Connections ---
        self.search_button.clicked.connect(self.filter_data)
        self.reset_button.clicked.connect(self.reset_filters)
        self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        # --- Initialization ---
        self.populate_filters()
        self.load_data()

    def setup_table_headers(self):
        """设置表格标题和列宽"""
        headers = [
            "序号", "省份", "城市", "客户单位", "联系人(人)", "联系状态",
            "客户意向", "联系记录(次)", "订单(个)", "下次预约日期", "销售人",
            "更新时间"
        ]
        self.model.setHorizontalHeaderLabels(headers)

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # 设置固定或最小宽度
        self.table_view.setColumnWidth(0, 50)   # 序号
        self.table_view.setColumnWidth(4, 90)   # 联系人(人)
        self.table_view.setColumnWidth(5, 100)  # 联系状态
        self.table_view.setColumnWidth(6, 100)  # 客户意向
        self.table_view.setColumnWidth(7, 100)  # 联系记录(次)
        self.table_view.setColumnWidth(8, 90)   # 订单(个)
        self.table_view.setColumnWidth(9, 150)  # 下次预约日期
        self.table_view.setColumnWidth(10, 100) # 销售人
        self.table_view.setColumnWidth(11, 150) # 更新时间
        
        # 设置可拉伸的列
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # 省份
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # 城市
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # 客户单位

    def load_data(self):
        """加载主数据"""
        """加载初始数据"""
        all_data = sales_view_api.get_sales_view() or []
        self._populate_table(all_data)
        
    def populate_filters(self):
        """填充所有筛选器的下拉选项"""
        all_data = sales_view_api.get_sales_view() or []
        
        # 使用集合来自动处理唯一值
        industries = sorted(list(set(r['industry'] for r in all_data if r.get('industry'))))
        provinces = sorted(list(set(r['province'] for r in all_data if r.get('province'))))
        cities = sorted(list(set(r['city'] for r in all_data if r.get('city'))))
        statuses = sorted(list(set(r['status'] for r in all_data if r.get('status'))))
        intentions = sorted(list(set(r['intention_level'] for r in all_data if r.get('intention_level'))))
        
        # 填充下拉框，并将None作为 "全部" 选项的 userData
        self.industry_filter.addItem("行业类别", userData=None)
        self.industry_filter.addItems(industries)
        
        self.province_filter.addItem("省份", userData=None)
        self.province_filter.addItems(provinces)
        
        self.city_filter.addItem("城市", userData=None)
        self.city_filter.addItems(cities)
        
        self.status_filter.addItem("联系状态", userData=None)
        self.status_filter.addItems(statuses)

        self.intention_filter.addItem("客户意向", userData=None)
        self.intention_filter.addItems(intentions)

        self.sales_filter.addItem("销售人", userData=None)
        sales_people = employees_api.get_employees({'role': 'sales'}) or []
        for emp in sales_people:
            self.sales_filter.addItem(emp.get('name'), emp.get('id'))

    def _on_view_contacts_clicked(self, row):
        """Handles the logic to open the contact view dialog."""
        if row >= len(self.table_data):
            return

        customer_data = self.table_data[row]
        customer_id = customer_data.get('id')

        # Fetch contacts for the customer
        contacts_data = contacts_api.get_contacts({"customer_id": customer_id}) or []

        dialog = SalesContactViewDialog(customer_data, contacts_data, self)
        dialog.exec()

    def view_contacts(self, row):
        self._on_view_contacts_clicked(row)

    def view_orders(self, row):
        if row >= len(self.table_data):
            return
        customer_id = self.table_data[row].get('id')
        company = self.table_data[row].get('company')
        QMessageBox.information(self, "查看订单记录", f"查看客户 [{company}] (ID: {customer_id}) 的订单记录。\n\n(此功能待实现)")

    def on_selection_changed(self, selected, deselected):
        """处理表格选择变化事件 (placeholder)"""
        pass
    
    def filter_data(self):
        """根据筛选条件过滤数据"""
        """根据UI中的筛选条件过滤并显示数据"""
        params = {
            'company': self.customer_filter.text().strip(),
            'industry': self.industry_filter.currentText() if self.industry_filter.currentIndex() > 0 else None,
            'province': self.province_filter.currentText() if self.province_filter.currentIndex() > 0 else None,
            'city': self.city_filter.currentText() if self.city_filter.currentIndex() > 0 else None,
            'status': self.status_filter.currentText() if self.status_filter.currentIndex() > 0 else None,
            'intention_level': self.intention_filter.currentText() if self.intention_filter.currentIndex() > 0 else None,
            'sales_owner_id': self.sales_filter.currentData(),
        }
        # 移除值为None的参数
        active_params = {k: v for k, v in params.items() if v is not None and v != ''}
        
        filtered_data = sales_view_api.get_sales_view(active_params) or []
        self._populate_table(filtered_data)
    
    def reset_filters(self):
        """重置所有筛选条件"""
        self.customer_filter.clear()
        self.industry_filter.setCurrentIndex(0)
        self.province_filter.setCurrentIndex(0)
        self.city_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.intention_filter.setCurrentIndex(0)
        self.sales_filter.setCurrentIndex(0)
        # 重置后，重新从API获取全部数据并填充
        self.load_data()

    def _create_clickable_cell(self, text, callback, row_index, enabled=True):
        """创建一个可点击的、像链接一样的按钮"""
        button = QPushButton(text)
        button.setProperty("flat", True) # Use stylesheet for link-like appearance
        button.setCursor(Qt.PointingHandCursor if enabled else Qt.ForbiddenCursor)
        button.setEnabled(enabled)
        if enabled:
            button.clicked.connect(lambda: callback(row_index))
        return button

    def _populate_table(self, data):
        """用给定的数据填充表格，取代 load_data 和 filter_data 中的重复代码"""
        self.model.removeRows(0, self.model.rowCount())
        self.table_data = data

        for row_index, record in enumerate(self.table_data):
            seq_item = QStandardItem(str(row_index + 1))
            seq_item.setTextAlignment(Qt.AlignCenter)

            # 更新时间（只显示日期）
            updated_date_str = record.get('updated_at', '')
            if updated_date_str and 'T' in updated_date_str:
                updated_date_str = updated_date_str.split('T')[0]

            # 下次预约日期（红色文字）
            # TODO: 此处应从 sales_follow 表获取最新的预约日期
            next_follow_item = QStandardItem("待更新")
            next_follow_item.setForeground(QColor("#d32f2f"))

            items = [
                seq_item,
                QStandardItem(record.get('province', '')),
                QStandardItem(record.get('city', '')),
                QStandardItem(record.get('company', '')),
                QStandardItem(),  # Placeholder for contact_count button
                QStandardItem(record.get('status', '')),
                QStandardItem(record.get('intention_level', '')),
                QStandardItem(),  # Placeholder for sales_follow_count button
                QStandardItem(),  # Placeholder for order_count button
                next_follow_item,
                QStandardItem(record.get('sales_owner_name', '未分配')),
                QStandardItem(updated_date_str)
            ]
            self.model.appendRow(items)

            # --- 创建并设置动态小部件 ---
            contact_count = record.get('contact_count', 0)
            contact_button = self._create_clickable_cell(
                str(contact_count), self.view_contacts, row_index, enabled=contact_count > 0
            )
            self.table_view.setIndexWidget(self.model.index(row_index, 4), contact_button)
            
            follow_count = record.get('sales_follow_count', 0)
            follow_button = self._create_clickable_cell(
                str(follow_count), self.view_contacts, row_index, enabled=follow_count > 0
            )
            self.table_view.setIndexWidget(self.model.index(row_index, 7), follow_button)

            order_count = record.get('order_count', 0)
            order_button = self._create_clickable_cell(
                str(order_count), self.view_orders, row_index, enabled=order_count > 0
            )
            self.table_view.setIndexWidget(self.model.index(row_index, 8), order_button)


if __name__ == '__main__':
    # 这部分代码仅用于独立测试此视图
    app = QApplication(sys.argv)
    
    # 在独立运行时，需要加载应用的全局样式
    try:
        with open("client/ui/styles.qss", "r", encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: Stylesheet 'client/ui/styles.qss' not found. Running without styles.")

    view = SalesManagementView()
    view.resize(1600, 800) # 增大窗口尺寸以更好地显示所有列
    view.show()
    sys.exit(app.exec())