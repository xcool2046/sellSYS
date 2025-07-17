from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QLineEdit,
    QComboBox, QSpacerItem, QSizePolicy, QHeaderView, QMessageBox, QLabel,
    QCheckBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QIcon
from PySide6.QtCore import Qt, QModelIndex

from ..api import customers as customers_api, contacts as contacts_api, employees as employees_api
from .customer_dialog import CustomerDialog
from .assign_sales_dialog import AssignSalesDialog
from .assign_service_dialog import AssignServiceDialog
from .contact_view_dialog import ContactViewDialog

class CustomerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("客户管理")

        # --- Data Storage ---
        self.customers_data = []
        self.employees_map = {}
        self.all_customers_data = []  # 用于获取所有可能的筛选值
        self.checkbox_items = []  # 存储复选框项
        self.select_all_checkbox = None  # 全选复选框

        # --- Layouts ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Toolbar (Filters and Actions) ---
        toolbar_container = QWidget()
        toolbar_container.setObjectName("toolbarContainer")
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)

        # --- Filter Widgets ---
        self.customer_name_filter = QLineEdit()
        self.customer_name_filter.setPlaceholderText("客户名称")
        self.customer_name_filter.setObjectName("filterInput")
        toolbar_layout.addWidget(self.customer_name_filter)

        self.industry_filter = QComboBox()
        self.industry_filter.addItem("行业类别", None)
        self.industry_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.industry_filter)

        self.province_filter = QComboBox()
        self.province_filter.addItem("省份", None)
        self.province_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.province_filter)

        self.city_filter = QComboBox()
        self.city_filter.addItem("城市", None)
        self.city_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.city_filter)

        self.status_filter = QComboBox()
        self.status_filter.addItem("联系状态", None)
        self.status_filter.addItem("潜在客户", "LEAD")
        self.status_filter.addItem("已联系", "CONTACTED")
        self.status_filter.addItem("已报价", "PROPOSAL")
        self.status_filter.addItem("成交客户", "WON")
        self.status_filter.addItem("流失客户", "LOST")
        self.status_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.status_filter)

        self.sales_filter = QComboBox()
        self.sales_filter.addItem("销售人", None)
        self.sales_filter.setObjectName("filterCombo")
        toolbar_layout.addWidget(self.sales_filter)

        self.search_button = QPushButton("查询")
        self.search_button.setObjectName("searchButton")
        toolbar_layout.addWidget(self.search_button)

        self.reset_button = QPushButton("重置")
        self.reset_button.setObjectName("resetButton")
        toolbar_layout.addWidget(self.reset_button)

        # --- Spacer to push action buttons to the right ---
        toolbar_layout.addStretch(1)

        # --- Action Buttons ---
        self.add_customer_button = QPushButton("添加客户")
        self.add_customer_button.setObjectName("customerAddButton")
        toolbar_layout.addWidget(self.add_customer_button)
        
        self.assign_sales_button = QPushButton("分配给销售")
        self.assign_sales_button.setObjectName("customerAssignSalesButton")
        toolbar_layout.addWidget(self.assign_sales_button)
        
        self.assign_service_button = QPushButton("分配给客服")
        self.assign_service_button.setObjectName("customerAssignServiceButton")
        toolbar_layout.addWidget(self.assign_service_button)

        # --- Table View ---
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.clicked.connect(self._on_table_clicked)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setObjectName("customerTable")
        
        self.model.itemChanged.connect(self._on_item_changed)

        # --- Content Widget for Table with Margins ---
        table_container = QWidget()
        table_container.setObjectName("tableContainer")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)
        table_layout.addWidget(self.table_view)

        # --- Assembly ---
        main_layout.addWidget(toolbar_container)
        main_layout.addWidget(table_container)

        # --- Connections ---
        self.add_customer_button.clicked.connect(self._on_add_customer_clicked)
        self.assign_sales_button.clicked.connect(self._on_assign_sales_clicked)
        self.assign_service_button.clicked.connect(self._on_assign_support_clicked)
        self.search_button.clicked.connect(self.refresh_data)
        self.reset_button.clicked.connect(self._on_reset_clicked)

        # --- Initialization ---
        self.setup_table_headers()
        self.setup_header_checkbox()
        self.load_filter_options()
        self.refresh_data()

    def setup_table_headers(self):
        headers = [
            "", "ID", "行业类别", "省份", "城市", "客户单位名称", "联系人",
            "客户备注", "客户状态", "销售", "客服", "创建时间", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)
        self.table_view.setColumnHidden(1, True)  # Hide ID column

        # Set column widths for better layout
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive) # Allow manual resize
        self.table_view.setColumnWidth(0, 40)    # Checkbox
        self.table_view.setColumnWidth(2, 100)   # Industry
        self.table_view.setColumnWidth(3, 100)   # Province
        self.table_view.setColumnWidth(4, 100)   # City
        self.table_view.setColumnWidth(6, 80)    # Contacts
        self.table_view.setColumnWidth(8, 100)   # Status
        self.table_view.setColumnWidth(9, 100)   # Sales
        self.table_view.setColumnWidth(10, 100)  # Service
        self.table_view.setColumnWidth(11, 150)  # Created At
        self.table_view.setColumnWidth(12, 130)  # Actions

        # Stretch the main columns
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)

        # Center align headers
        for i in range(self.model.columnCount()):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, Qt.AlignmentFlag.AlignCenter, Qt.TextAlignmentRole)

    def load_filter_options(self):
        """加载筛选选项"""
        # 获取所有员工用于销售筛选
        all_employees = employees_api.get_employees() or []
        self.employees_map = {emp['id']: emp['name'] for emp in all_employees}
        
        # 填充销售筛选下拉框
        for emp_id, emp_name in self.employees_map.items():
            self.sales_filter.addItem(emp_name, emp_id)
        
        # 获取所有客户数据以提取唯一的行业、省份、城市值
        self.all_customers_data = customers_api.get_customers() or []
        
        if self.all_customers_data:
            # 提取唯一的行业
            industries = set()
            provinces = set()
            cities = set()
            
            for customer in self.all_customers_data:
                if customer.get("industry"):
                    industries.add(customer["industry"])
                if customer.get("province"):
                    provinces.add(customer["province"])
                if customer.get("city"):
                    cities.add(customer["city"])
            
            # 填充行业筛选
            for industry in sorted(industries):
                self.industry_filter.addItem(industry, industry)
            
            # 填充省份筛选
            for province in sorted(provinces):
                self.province_filter.addItem(province, province)
            
            # 填充城市筛选
            for city in sorted(cities):
                self.city_filter.addItem(city, city)

    def refresh_data(self):
        # 获取筛选参数
        company = self.customer_name_filter.text().strip() or None
        industry = self.industry_filter.currentData()
        province = self.province_filter.currentData()
        city = self.city_filter.currentData()
        status = self.status_filter.currentData()
        sales_id = self.sales_filter.currentData()

        # 获取客户数据（带筛选）
        self.customers_data = customers_api.get_customers(
            company=company,
            industry=industry,
            province=province,
            city=city,
            status=status,
            sales_id=sales_id
        )
        
        self.model.removeRows(0, self.model.rowCount())
        self.checkbox_items.clear()

        if not self.customers_data:
            return

        for i, customer in enumerate(self.customers_data):
            contacts_count = customer.get("contacts_count", 0)
            
            # Create checkbox item with custom style
            checkbox_item = QStandardItem()
            checkbox_item.setCheckable(True)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            checkbox_item.setData(Qt.AlignmentFlag.AlignCenter, Qt.ItemDataRole.TextAlignmentRole)
            self.checkbox_items.append(checkbox_item)
            
            # Create a clickable item for contacts
            # This will be replaced by a button later
            contacts_item = QStandardItem(str(contacts_count))

            row_items = [
                checkbox_item,
                QStandardItem(str(customer["id"])),
                QStandardItem(customer.get("industry", "N/A")),
                QStandardItem(customer.get("province", "N/A")),
                QStandardItem(customer.get("city", "N/A")),
                QStandardItem(customer.get("company", "N/A")),
                contacts_item, # Placeholder, will be replaced by a button
                QStandardItem(customer.get("notes", "")),
                QStandardItem(customer.get("status", "N/A")),
                QStandardItem(self.employees_map.get(customer.get("sales_id"), "未分配")),
                QStandardItem(self.employees_map.get(customer.get("service_id"), "未分配")),
                QStandardItem(customer.get("created_at", "").split("T")[0]),
            ]
            
            # Center align all items
            for item in row_items:
                if item: # Checkbox item might be None initially
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.model.appendRow(row_items)

            # --- Contact Link Button ---
            contact_button = QPushButton(str(contacts_count))
            contact_button.setObjectName("contactLinkButton")
            contact_button.setProperty("customer_id", customer["id"])
            contact_button.setCursor(Qt.CursorShape.PointingHandCursor)
            contact_button.clicked.connect(self._on_contact_button_clicked)
            self.table_view.setIndexWidget(self.model.index(i, 6), contact_button)

            # --- Action Buttons ---
            edit_button = QPushButton("编辑")
            delete_button = QPushButton("删除")
            edit_button.setProperty("customer_id", customer["id"])
            delete_button.setProperty("customer_id", customer["id"])
            edit_button.setProperty("customer_row", i)
            delete_button.setProperty("customer_row", i)
            edit_button.setObjectName("tableEditButton")
            delete_button.setObjectName("tableDeleteButton")
            edit_button.clicked.connect(self._on_edit_customer_clicked)
            delete_button.clicked.connect(self._on_delete_customer_clicked)

            button_layout = QHBoxLayout()
            button_layout.setSpacing(5)
            button_layout.setContentsMargins(5, 0, 5, 0)
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            button_container = QWidget()
            button_container.setLayout(button_layout)
            self.table_view.setIndexWidget(self.model.index(i, 12), button_container)

    def _get_selected_customer_ids(self):
        # 优先使用复选框选中的客户
        selected_ids = []
        for i, checkbox_item in enumerate(self.checkbox_items):
            if checkbox_item.checkState() == Qt.CheckState.Checked:
                selected_ids.append(self.model.item(i, 1).text())
        
        # 如果没有复选框选中，则使用行选择
        if not selected_ids:
            selected_rows = self.table_view.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(self, "提示", "请先在列表中选择一个或多个客户。")
                return []
            selected_ids = [self.model.item(index.row(), 1).text() for index in selected_rows]
        
        return selected_ids

    def _on_add_customer_clicked(self):
        dialog = CustomerDialog(self)
        if dialog.exec():
            customer_data, contacts_data = dialog.get_data()
            
            # 调用API创建客户
            result = customers_api.create_customer(customer_data, contacts_data)
            
            if result:
                QMessageBox.information(self, "成功", "客户添加成功！")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "失败", "客户添加失败，请重试。")
    
    def _on_assign_sales_clicked(self):
        customer_ids = self._get_selected_customer_ids()
        if not customer_ids:
            return
        
        dialog = AssignSalesDialog(self)
        if dialog.exec():
            sales_id = dialog.get_selected_sales_id()
            if sales_id != -1:
                # TODO: Add API call to assign sales
                print(f"Assigning sales {sales_id} to customers {customer_ids}")
                self.refresh_data()

    def _on_assign_support_clicked(self):
        customer_ids = self._get_selected_customer_ids()
        if not customer_ids:
            return

        dialog = AssignServiceDialog(self)
        if dialog.exec():
            service_id = dialog.get_selected_service_id()
            if service_id != -1:
                # TODO: Add API call to assign service
                print(f"Assigning service {service_id} to customers {customer_ids}")
                self.refresh_data()
    
    def setup_header_checkbox(self):
        """设置表头的全选复选框"""
        self.select_all_checkbox = QCheckBox()
        self.select_all_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #d0d0d0;
                background-color: #ffffff;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #1976d2;
                background-color: #ffffff;
                border-radius: 2px;
                image: url(data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'><path fill='%231976d2' d='M6.5 11.5l-3.5-3.5 1.4-1.4 2.1 2.1 5.1-5.1 1.4 1.4z'/></svg>);
            }
            QCheckBox::indicator:indeterminate {
                border: 1px solid #1976d2;
                background-color: #ffffff;
                border-radius: 2px;
                image: url(data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'><rect fill='%231976d2' x='4' y='7' width='8' height='2'/></svg>);
            }
        """)
        self.select_all_checkbox.stateChanged.connect(self._on_select_all_changed)
        
        # 将全选复选框放在表头
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        
        # 创建一个容器来居中放置复选框
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.addWidget(self.select_all_checkbox)
        layout.addStretch()
        
        # 使用自定义widget作为表头的第一列
        self.table_view.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # 添加到视口的左上角
        container.setParent(self.table_view.viewport())
        container.move(0, 0)
        container.resize(40, header.height())
        container.show()
    
    def _on_select_all_changed(self, state):
        """全选/取消全选处理"""
        # 断开信号连接，避免递归
        self.model.itemChanged.disconnect(self._on_item_changed)
        
        for checkbox_item in self.checkbox_items:
            if state == Qt.CheckState.Checked.value:
                checkbox_item.setCheckState(Qt.CheckState.Checked)
            else:
                checkbox_item.setCheckState(Qt.CheckState.Unchecked)
        
        # 重新连接信号
        self.model.itemChanged.connect(self._on_item_changed)
    
    def _on_item_changed(self, item):
        """处理单个复选框状态变化"""
        if item in self.checkbox_items:
            # 检查是否所有复选框都被选中
            all_checked = all(cb.checkState() == Qt.CheckState.Checked for cb in self.checkbox_items)
            # 检查是否有任何复选框被选中
            any_checked = any(cb.checkState() == Qt.CheckState.Checked for cb in self.checkbox_items)
            
            if self.select_all_checkbox:
                # 断开信号以避免递归
                self.select_all_checkbox.stateChanged.disconnect(self._on_select_all_changed)
                
                if all_checked:
                    self.select_all_checkbox.setCheckState(Qt.CheckState.Checked)
                elif any_checked:
                    self.select_all_checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
                else:
                    self.select_all_checkbox.setCheckState(Qt.CheckState.Unchecked)
                
                # 重新连接信号
                self.select_all_checkbox.stateChanged.connect(self._on_select_all_changed)
    
    def _on_edit_customer_clicked(self):
        """处理编辑按钮点击"""
        sender = self.sender()
        customer_id = sender.property("customer_id")
        customer_row = sender.property("customer_row")
        
        # 从当前数据中获取客户信息
        customer_data = self.customers_data[customer_row]
        
        # 获取客户的联系人信息
        contacts = contacts_api.get_contacts_for_customer(customer_id) or []
        
        # 打开编辑对话框
        dialog = CustomerDialog(self, customer_data, contacts)
        if dialog.exec():
            updated_customer_data, updated_contacts_data = dialog.get_data()
            
            # 调用API更新客户
            result = customers_api.update_customer(customer_id, updated_customer_data)
            
            if result:
                QMessageBox.information(self, "成功", "客户信息更新成功！")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "失败", "客户信息更新失败，请重试。")
    
    def _on_delete_customer_clicked(self):
        """处理删除按钮点击"""
        sender = self.sender()
        customer_id = sender.property("customer_id")
        customer_row = sender.property("customer_row")
        
        # 从当前数据中获取客户名称
        customer_name = self.customers_data[customer_row].get("company", "")
        
        # 确认删除
        reply = QMessageBox.question(
            self,
            "确认删除",
            f'确定要删除客户 "{customer_name}" 吗？\n此操作不可撤销。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 调用API删除客户
            result = customers_api.delete_customer(customer_id)
            
            if result:
                QMessageBox.information(self, "成功", "客户删除成功！")
                self.refresh_data()
            else:
                QMessageBox.warning(self, "失败", "客户删除失败，请重试。")

    def _on_contact_button_clicked(self):
        """处理联系人链接按钮点击"""
        sender = self.sender()
        customer_id = sender.property("customer_id")
        
        customer_data = next((c for c in self.customers_data if str(c['id']) == customer_id), None)
        
        if customer_data:
            contacts = contacts_api.get_contacts_for_customer(customer_id) or []
            dialog = ContactViewDialog(customer_data, contacts, self)
            dialog.exec()
            
    def _on_table_clicked(self, index):
        # The logic for clicking on the contact count is now handled by _on_contact_button_clicked
        pass
    
    def _on_reset_clicked(self):
        """重置所有筛选条件"""
        self.customer_name_filter.clear()
        self.industry_filter.setCurrentIndex(0)
        self.province_filter.setCurrentIndex(0)
        self.city_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.sales_filter.setCurrentIndex(0)
        self.refresh_data()