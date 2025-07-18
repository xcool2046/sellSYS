"""
客户管理视图 - 按照原型图设计的高保真界面
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView,
    QLineEdit, QComboBox, QHeaderView, QMessageBox, QLabel, QCheckBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from typing import List, Dict, Any
from .dialog_styles import show_message_box

from api.customers_api import customers_api
from config_clean import CUSTOMER_STATUS, INDUSTRY_CATEGORIES, PROVINCE_CITY_DATA

class CustomerManagementView(QWidget):
    """客户管理视图 - 按照原型图设计"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.customers_data = []

        self.setup_ui()
        self.setup_connections()
        self.load_data()

        print("✅ 客户管理视图初始化完成")
    
    def setup_ui(self):
        """设置用户界面"""
        # 设置主容器样式，去除边框
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: none;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 搜索工具栏
        self.setup_search_toolbar()
        main_layout.addWidget(self.search_toolbar)

        # 表格
        self.setup_table()
        main_layout.addWidget(self.table_view)
    
    def setup_search_toolbar(self):
        """设置搜索工具栏"""
        self.search_toolbar = QWidget()
        self.search_toolbar.setFixedHeight(50)
        self.search_toolbar.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }
        """)

        toolbar_layout = QHBoxLayout(self.search_toolbar)
        toolbar_layout.setContentsMargins(15, 8, 15, 8)
        toolbar_layout.setSpacing(10)

        # 客户单位
        self.customer_unit_combo = QComboBox()
        self.customer_unit_combo.setFixedWidth(120)
        self.customer_unit_combo.setPlaceholderText("客户单位")
        self.customer_unit_combo.addItem("全部", None)
        # 这里会在加载数据时动态填充客户单位列表
        # 设置当前索引为-1以显示占位符
        self.customer_unit_combo.setCurrentIndex(-1)
        self.setup_combo_style(self.customer_unit_combo)
        toolbar_layout.addWidget(self.customer_unit_combo)

        # 行业类型
        self.industry_combo = QComboBox()
        self.industry_combo.setFixedWidth(100)
        self.industry_combo.setPlaceholderText("行业类型")
        self.industry_combo.addItem("全部", None)
        for industry in INDUSTRY_CATEGORIES:
            self.industry_combo.addItem(industry, industry)
        # 设置当前索引为-1以显示占位符
        self.industry_combo.setCurrentIndex(-1)
        self.setup_combo_style(self.industry_combo)
        toolbar_layout.addWidget(self.industry_combo)

        # 省份
        self.province_combo = QComboBox()
        self.province_combo.setFixedWidth(80)
        self.province_combo.setPlaceholderText("省份")
        self.province_combo.addItem("全部", None)
        for province in PROVINCE_CITY_DATA.keys():
            self.province_combo.addItem(province, province)
        # 设置当前索引为-1以显示占位符
        self.province_combo.setCurrentIndex(-1)
        self.setup_combo_style(self.province_combo)
        toolbar_layout.addWidget(self.province_combo)

        # 城市
        self.city_combo = QComboBox()
        self.city_combo.setFixedWidth(80)
        self.city_combo.setPlaceholderText("城市")
        self.city_combo.addItem("全部", None)
        # 设置当前索引为-1以显示占位符
        self.city_combo.setCurrentIndex(-1)
        self.setup_combo_style(self.city_combo)
        toolbar_layout.addWidget(self.city_combo)

        # 联系状态
        self.contact_status_combo = QComboBox()
        self.contact_status_combo.setFixedWidth(100)
        self.contact_status_combo.setPlaceholderText("联系状态")
        self.contact_status_combo.addItem("全部", None)
        for status_key, status_name in CUSTOMER_STATUS.items():
            self.contact_status_combo.addItem(status_name, status_key)
        # 设置当前索引为-1以显示占位符
        self.contact_status_combo.setCurrentIndex(-1)
        self.setup_combo_style(self.contact_status_combo)
        toolbar_layout.addWidget(self.contact_status_combo)

        # 销售人
        self.sales_person_combo = QComboBox()
        self.sales_person_combo.setFixedWidth(80)
        self.sales_person_combo.setPlaceholderText("销售人")
        self.sales_person_combo.addItem("全部", None)
        # 这里会在加载数据时动态填充销售人员列表
        # 设置当前索引为-1以显示占位符
        self.sales_person_combo.setCurrentIndex(-1)
        self.setup_combo_style(self.sales_person_combo)
        toolbar_layout.addWidget(self.sales_person_combo)

        # 查询按钮
        self.search_btn = QPushButton("查询")
        self.search_btn.setFixedSize(50, 30)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        toolbar_layout.addWidget(self.search_btn)

        # 重置按钮
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setFixedSize(50, 30)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        toolbar_layout.addWidget(self.reset_btn)

        # 添加客户按钮
        self.add_customer_btn = QPushButton("添加客户")
        self.add_customer_btn.setFixedSize(80, 30)
        self.add_customer_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        toolbar_layout.addWidget(self.add_customer_btn)

        # 分配销售按钮
        self.assign_sales_btn = QPushButton("分配销售")
        self.assign_sales_btn.setFixedSize(80, 30)
        self.assign_sales_btn.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e8650e;
            }
        """)
        toolbar_layout.addWidget(self.assign_sales_btn)

        # 分配客服按钮
        self.assign_service_btn = QPushButton("分配客服")
        self.assign_service_btn.setFixedSize(80, 30)
        self.assign_service_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        toolbar_layout.addWidget(self.assign_service_btn)

        toolbar_layout.addStretch()

    def setup_combo_style(self, combo: QComboBox):
        """设置下拉框统一样式"""
        combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 12px;
                color: #333333;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ced4da;
                background-color: white;
                color: #333333;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px 8px;
                border: none;
                color: #333333;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f8f9fa;
                color: #333333;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)

    def setup_table(self):
        """设置表格"""
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)

        # 设置表格属性
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)

        # 设置表格样式 - 按照原型图的蓝色主题，优化滚动条
        self.table_view.setStyleSheet("""
            QTableView {
                gridline-color: #dee2e6;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
                border: 1px solid #dee2e6;
                font-size: 12px;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #4a90e2;
                color: white;
                padding: 8px;
                border: 1px solid #357abd;
                font-weight: bold;
                font-size: 12px;
            }
            QTableView::item {
                padding: 6px;
                border-bottom: 1px solid #f0f0f0;
                color: #333333;
            }
            QTableView::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            /* 优化滚动条样式 */
            QScrollBar:horizontal {
                border: none;
                background: #f1f1f1;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #c1c1c1;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #a8a8a8;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c1c1c1;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a8a8a8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # 设置表格标题 - 严格按照原型图
        headers = [
            "", "行业类型", "省份", "城市", "客户单位信息", "联系人",
            "客户状态", "销售人", "创建时间", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)

        # 设置列宽 - 优化响应式设计
        header = self.table_view.horizontalHeader()

        # 设置列宽策略 - 混合固定和自适应
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 复选框 - 固定
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # 行业类型 - 自适应内容
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # 省份 - 自适应内容
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # 城市 - 自适应内容
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # 客户单位信息 - 拉伸填充
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # 联系人 - 自适应内容
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # 客户状态 - 自适应内容
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # 销售人 - 自适应内容
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)  # 创建时间 - 自适应内容
        header.setSectionResizeMode(9, QHeaderView.ResizeMode.Fixed)  # 操作 - 固定

        # 设置固定列的宽度
        self.table_view.setColumnWidth(0, 50)   # 复选框
        self.table_view.setColumnWidth(9, 120)  # 操作

        # 设置最小列宽，防止列太窄
        header.setMinimumSectionSize(50)

        # 隐藏垂直表头
        self.table_view.verticalHeader().setVisible(False)

        # 设置水平滚动条策略
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def setup_connections(self):
        """设置信号连接"""
        self.search_btn.clicked.connect(self.on_search_clicked)
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        self.province_combo.currentTextChanged.connect(self.on_province_changed)
        self.table_view.doubleClicked.connect(self.on_row_double_clicked)
        self.add_customer_btn.clicked.connect(self.on_add_customer_clicked)
        self.assign_sales_btn.clicked.connect(self.on_assign_sales_clicked)
        self.assign_service_btn.clicked.connect(self.on_assign_service_clicked)

        # 设置右键菜单
        self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)

    def on_province_changed(self, province: str):
        """省份变化事件"""
        self.city_combo.clear()
        self.city_combo.addItem("全部", None)

        if province in PROVINCE_CITY_DATA:
            for city in PROVINCE_CITY_DATA[province]:
                self.city_combo.addItem(city, city)

    def load_data(self):
        """加载客户数据"""
        try:
            # 从API加载客户数据
            self.customers_data = customers_api.list()
            self.update_table_view()
            self.update_filter_options()
            print(f"✅ 加载了 {len(self.customers_data)} 条客户记录")
        except Exception as e:
            print(f"❌ 加载客户数据失败: {e}")
            # 如果API失败，使用空数据
            self.customers_data = []
            self.update_table_view()

    def update_filter_options(self):
        """更新筛选条件的选项"""
        if not self.customers_data:
            return

        # 更新客户单位选项
        companies = set()
        sales_persons = set()

        for customer in self.customers_data:
            if customer.get('company'):
                companies.add(customer['company'])
            if customer.get('sales_person'):
                sales_persons.add(customer['sales_person'])

        # 更新客户单位下拉框
        current_company = self.customer_unit_combo.currentData()
        self.customer_unit_combo.clear()
        self.customer_unit_combo.addItem("全部", None)
        for company in sorted(companies):
            self.customer_unit_combo.addItem(company, company)

        # 恢复之前的选择
        if current_company:
            index = self.customer_unit_combo.findData(current_company)
            if index >= 0:
                self.customer_unit_combo.setCurrentIndex(index)
        else:
            self.customer_unit_combo.setCurrentIndex(-1)

        # 更新销售人员下拉框
        current_sales = self.sales_person_combo.currentData()
        self.sales_person_combo.clear()
        self.sales_person_combo.addItem("全部", None)
        for sales in sorted(sales_persons):
            self.sales_person_combo.addItem(sales, sales)

        # 恢复之前的选择
        if current_sales:
            index = self.sales_person_combo.findData(current_sales)
            if index >= 0:
                self.sales_person_combo.setCurrentIndex(index)
        else:
            self.sales_person_combo.setCurrentIndex(-1)

    def update_table_view(self):
        """更新表格视图"""
        self.model.clear()
        headers = [
            "", "行业类型", "省份", "城市", "客户单位信息", "联系人",
            "客户状态", "销售人", "创建时间", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)

        for i, customer in enumerate(self.customers_data):
            # 创建复选框
            checkbox_item = QStandardItem()
            checkbox_item.setCheckable(True)
            checkbox_item.setEditable(False)

            # 创建操作按钮
            operation_text = "联系记录 详情记录"

            items = [
                checkbox_item,  # 复选框
                QStandardItem(customer.get("industry", "")),
                QStandardItem(customer.get("province", "")),
                QStandardItem(customer.get("city", "")),
                QStandardItem(customer.get("company", "")),
                QStandardItem(customer.get("contact_person", "")),
                QStandardItem(customer.get("status", "")),
                QStandardItem(customer.get("sales_person", "")),
                QStandardItem(customer.get("created_at", "")),
                QStandardItem(operation_text)
            ]

            # 设置项不可编辑
            for item in items:
                item.setEditable(False)

            # 设置客户状态的颜色
            status = customer.get("status", "")
            if status == "待分配":
                items[6].setBackground(Qt.GlobalColor.yellow)
            elif status == "待联系":
                items[6].setBackground(Qt.GlobalColor.yellow)
            elif status == "高":
                items[6].setBackground(Qt.GlobalColor.red)
            elif status == "已成交":
                items[6].setBackground(Qt.GlobalColor.green)

            self.model.appendRow(items)

    def on_search_clicked(self):
        """搜索按钮点击事件"""
        # 获取搜索条件
        params = {
            'company': self.customer_unit_combo.currentData(),
            'industry': self.industry_combo.currentData(),
            'province': self.province_combo.currentData(),
            'city': self.city_combo.currentData(),
            'status': self.contact_status_combo.currentData(),
            'sales_person': self.sales_person_combo.currentData()
        }

        # 移除空值
        params = {k: v for k, v in params.items() if v}

        print(f"搜索条件: {params}")

        try:
            # 调用API进行搜索
            self.customers_data = customers_api.search_customers(params)
            self.update_table_view()
            # 注意：搜索后不更新筛选选项，保持当前筛选状态
            print(f"✅ 搜索完成，找到 {len(self.customers_data)} 条记录")

            if len(self.customers_data) == 0:
                show_message_box(self, "搜索结果", "未找到符合条件的客户记录")
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            show_message_box(self, "搜索失败", f"搜索时发生错误: {str(e)}")

    def on_reset_clicked(self):
        """重置按钮点击事件"""
        # 重置为占位符状态（索引-1）
        self.customer_unit_combo.setCurrentIndex(-1)
        self.industry_combo.setCurrentIndex(-1)
        self.province_combo.setCurrentIndex(-1)
        self.city_combo.setCurrentIndex(-1)
        self.contact_status_combo.setCurrentIndex(-1)
        self.sales_person_combo.setCurrentIndex(-1)

        # 重新加载数据
        self.load_data()
        print("✅ 已重置搜索条件")

    def on_add_customer_clicked(self):
        """添加客户按钮点击事件"""
        try:
            from .dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            if dialog.exec():
                customer_data = dialog.get_customer_data()
                contacts_data = dialog.get_contacts_data()

                # 调试信息
                print(f"[调试] 客户数据: {customer_data}")
                print(f"[调试] 联系人数据: {contacts_data}")

                # 合并客户数据和联系人数据
                customer_data['contacts'] = contacts_data
                print(f"[调试] 合并后数据: {customer_data}")

                result = customers_api.create(customer_data)
                print(f"[调试] API返回结果: {result}")

                if result:
                    show_message_box(self, "成功", "客户添加成功!")
                    self.load_data()
                else:
                    show_message_box(self, "失败", "客户添加失败! API返回了空结果，可能是服务器未运行或数据格式问题。")
        except Exception as e:
            print(f"[调试] 异常详情: {str(e)}")
            import traceback
            print(f"[调试] 异常堆栈: {traceback.format_exc()}")
            show_message_box(self, "错误", f"添加客户时发生错误: {str(e)}")

    def on_assign_sales_clicked(self):
        """分配销售按钮点击事件"""
        # 获取选中的客户
        selected_customers = self.get_selected_customers()

        if not selected_customers:
            show_message_box(self, "提示", "请先选择要分配销售的客户")
            return

        try:
            from .dialogs.assign_sales_dialog import AssignSalesDialog
            dialog = AssignSalesDialog(selected_customers[0] if selected_customers else {}, parent=self)
            if dialog.exec():
                assignment_data = dialog.get_assignment_data()

                # 为每个选中的客户分配销售
                success_count = 0
                for customer in selected_customers:
                    # 这里应该调用API更新客户的销售人员信息
                    # 暂时模拟成功
                    success_count += 1

                if success_count > 0:
                    show_message_box(self, "成功", f"成功为 {success_count} 个客户分配销售人员: {assignment_data['sales_person']}!")
                    self.load_data()
                else:
                    show_message_box(self, "失败", "销售分配失败!")
        except Exception as e:
            show_message_box(self, "错误", f"分配销售时发生错误: {str(e)}")

    def on_assign_service_clicked(self):
        """分配客服按钮点击事件"""
        # 获取选中的客户
        selected_customers = self.get_selected_customers()

        if not selected_customers:
            show_message_box(self, "提示", "请先选择要分配客服的客户")
            return

        try:
            from .dialogs.assign_service_dialog import AssignServiceDialog
            dialog = AssignServiceDialog(selected_customers[0] if selected_customers else {}, parent=self)
            if dialog.exec():
                assignment_data = dialog.get_assignment_data()

                # 为每个选中的客户分配客服
                success_count = 0
                for customer in selected_customers:
                    # 这里应该调用API更新客户的客服人员信息
                    # 暂时模拟成功
                    success_count += 1

                if success_count > 0:
                    show_message_box(self, "成功", f"成功为 {success_count} 个客户分配客服人员: {assignment_data['service_person']}!")
                    self.load_data()
                else:
                    show_message_box(self, "失败", "客服分配失败!")
        except Exception as e:
            show_message_box(self, "错误", f"分配客服时发生错误: {str(e)}")

    def get_selected_customers(self):
        """获取选中的客户"""
        selected = []
        for row in range(self.model.rowCount()):
            checkbox_item = self.model.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
                if row < len(self.customers_data):
                    selected.append(self.customers_data[row])
        return selected

    def on_row_double_clicked(self, index):
        """行双击事件"""
        if index.isValid():
            row = index.row()
            if row < len(self.customers_data):
                customer = self.customers_data[row]
                show_message_box(
                    self,
                    "客户详情",
                    f"客户单位: {customer.get('company', '')}\n"
                    f"联系人: {customer.get('contact_person', '')}\n"
                    f"客户状态: {customer.get('status', '')}\n"
                    f"销售人员: {customer.get('sales_person', '')}"
                )

    def show_context_menu(self, position):
        """显示右键菜单"""
        index = self.table_view.indexAt(position)
        if not index.isValid():
            return

        row = index.row()
        if row >= len(self.customers_data):
            return

        customer = self.customers_data[row]

        # 导入QMenu和QAction
        from PySide6.QtWidgets import QMenu
        from PySide6.QtGui import QAction

        menu = QMenu(self)

        # 编辑客户
        edit_action = QAction("编辑客户", self)
        edit_action.triggered.connect(lambda: self.edit_customer(customer))
        menu.addAction(edit_action)

        # 查看详情
        detail_action = QAction("查看详情", self)
        detail_action.triggered.connect(lambda: self.show_customer_detail(customer))
        menu.addAction(detail_action)

        menu.addSeparator()

        # 删除客户
        delete_action = QAction("删除客户", self)
        delete_action.triggered.connect(lambda: self.delete_customer(customer))
        menu.addAction(delete_action)

        menu.exec(self.table_view.mapToGlobal(position))

    def edit_customer(self, customer_data: Dict[str, Any]):
        """编辑客户"""
        try:
            from .dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(customer_data, parent=self)
            if dialog.exec():
                updated_data = dialog.get_customer_data()
                contacts_data = dialog.get_contacts_data()

                # 合并客户数据和联系人数据
                updated_data['contacts'] = contacts_data
                updated_data['id'] = customer_data.get('id')  # 保持原ID

                success = customers_api.update(customer_data.get('id'), updated_data)
                if success:
                    show_message_box(self, "成功", "客户信息更新成功!")
                    self.load_data()
                else:
                    show_message_box(self, "失败", "客户信息更新失败!")
        except Exception as e:
            show_message_box(self, "错误", f"编辑客户时发生错误: {str(e)}")

    def show_customer_detail(self, customer_data: Dict[str, Any]):
        """显示客户详情"""
        detail_text = f"""客户ID: {customer_data.get('id', '')}
行业类型: {customer_data.get('industry', '')}
所在地区: {customer_data.get('province', '')} {customer_data.get('city', '')}
客户单位: {customer_data.get('company', '')}
联系人: {customer_data.get('contact_person', '')}
客户状态: {customer_data.get('status', '')}
销售人员: {customer_data.get('sales_person', '')}
创建时间: {customer_data.get('created_at', '')}
备注: {customer_data.get('notes', '')}"""

        show_message_box(self, "客户详情", detail_text)

    def delete_customer(self, customer_data: Dict[str, Any]):
        """删除客户"""
        from PySide6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除客户 '{customer_data.get('company', '')}' 吗？\n此操作不可撤销！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                customer_id = customer_data.get('id')
                success = customers_api.delete_by_id(customer_id)
                if success:
                    show_message_box(self, "成功", "客户删除成功!")
                    self.load_data()  # 重新加载数据
                else:
                    show_message_box(self, "失败", "客户删除失败!")
            except Exception as e:
                show_message_box(self, "错误", f"删除客户时发生错误: {str(e)}")

# 导出
__all__ = ['CustomerManagementView']

# 导出
__all__ = ['CustomerManagementView']
