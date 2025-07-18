"""
订单管理视图 - 按照原型图设计
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView,
    QLineEdit, QComboBox, QHeaderView, QMessageBox, QLabel
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from typing import List, Dict, Any
from .dialog_styles import show_message_box

from api.customers_api import customers_api
from config_clean import CUSTOMER_STATUS, INDUSTRY_CATEGORIES, PROVINCE_CITY_DATA

class OrderManagementView(QWidget):
    """订单管理视图"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.orders_data = []
        
        self.setup_ui()
        self.setup_connections()
        self.load_sample_data()
        
        print("✅ 订单管理视图初始化完成")
    
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
        self.customer_unit_input = QLineEdit()
        self.customer_unit_input.setPlaceholderText("客户单位")
        self.customer_unit_input.setFixedWidth(120)
        self.customer_unit_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 12px;
                color: #333333;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #6c757d;
                font-style: normal;
            }
        """)
        toolbar_layout.addWidget(self.customer_unit_input)
        
        # 行业类型
        self.industry_combo = QComboBox()
        self.industry_combo.setFixedWidth(100)
        self.industry_combo.addItem("行业类型", None)
        self.industry_combo.addItem("全部", None)
        for industry in INDUSTRY_CATEGORIES:
            self.industry_combo.addItem(industry, industry)
        self.industry_combo.setStyleSheet("""
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
        toolbar_layout.addWidget(self.industry_combo)

        # 省份
        self.province_combo = QComboBox()
        self.province_combo.setFixedWidth(80)
        self.province_combo.addItem("省份", None)
        self.province_combo.addItem("全部", None)
        for province in PROVINCE_CITY_DATA.keys():
            self.province_combo.addItem(province, province)
        self.province_combo.setStyleSheet("""
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
        toolbar_layout.addWidget(self.province_combo)

        # 城市
        self.city_combo = QComboBox()
        self.city_combo.setFixedWidth(80)
        self.city_combo.addItem("城市", None)
        self.city_combo.addItem("全部", None)
        self.city_combo.setStyleSheet("""
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
        toolbar_layout.addWidget(self.city_combo)

        # 联系状态
        self.contact_status_combo = QComboBox()
        self.contact_status_combo.setFixedWidth(100)
        self.contact_status_combo.addItem("联系状态", None)
        self.contact_status_combo.addItem("全部", None)
        for status_key, status_name in CUSTOMER_STATUS.items():
            self.contact_status_combo.addItem(status_name, status_key)
        self.contact_status_combo.setStyleSheet("""
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
        toolbar_layout.addWidget(self.contact_status_combo)

        # 客户意向
        self.customer_manager_combo = QComboBox()
        self.customer_manager_combo.setFixedWidth(100)
        self.customer_manager_combo.addItem("客户意向", None)
        self.customer_manager_combo.addItem("全部", None)
        # 这里应该从API加载意向列表
        sample_intentions = ["有意向", "无意向", "待跟进"]
        for intention in sample_intentions:
            self.customer_manager_combo.addItem(intention, intention)
        self.customer_manager_combo.setStyleSheet("""
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
        toolbar_layout.addWidget(self.customer_manager_combo)

        # 销售人员
        self.sales_person_input = QLineEdit()
        self.sales_person_input.setPlaceholderText("销售人员")
        self.sales_person_input.setFixedWidth(80)
        self.sales_person_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 12px;
                color: #333333;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #6c757d;
                font-style: normal;
            }
        """)
        toolbar_layout.addWidget(self.sales_person_input)
        
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
        
        toolbar_layout.addStretch()
    
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
            "序号", "省份", "城市", "客户单位", "联系人", "联系状态",
            "客户意向", "联系记录", "打分", "下次联系时间", "销售人员", "更新时间", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)
        
        # 设置列宽 - 优化响应式设计
        header = self.table_view.horizontalHeader()

        # 设置列宽策略 - 混合固定和自适应
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 序号 - 固定
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # 省份 - 自适应内容
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # 城市 - 自适应内容
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # 客户单位 - 拉伸填充
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # 联系人 - 自适应内容
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # 联系状态 - 自适应内容
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # 客户负责人 - 自适应内容
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Interactive)  # 联系记录 - 可交互调整
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)  # 打分 - 固定
        header.setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)  # 下次联系时间 - 自适应内容
        header.setSectionResizeMode(10, QHeaderView.ResizeMode.ResizeToContents)  # 销售人员 - 自适应内容
        header.setSectionResizeMode(11, QHeaderView.ResizeMode.ResizeToContents)  # 更新时间 - 自适应内容
        header.setSectionResizeMode(12, QHeaderView.ResizeMode.Fixed)  # 操作 - 固定

        # 设置固定列的宽度
        self.table_view.setColumnWidth(0, 60)   # 序号
        self.table_view.setColumnWidth(8, 60)   # 打分
        self.table_view.setColumnWidth(12, 120) # 操作

        # 设置最小列宽，防止列太窄
        header.setMinimumSectionSize(50)

        # 设置初始列宽（作为建议宽度）
        self.table_view.setColumnWidth(7, 100)  # 联系记录初始宽度

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

    def on_province_changed(self, province: str):
        """省份变化事件"""
        self.city_combo.clear()
        self.city_combo.addItem("全部", None)

        if province in PROVINCE_CITY_DATA:
            for city in PROVINCE_CITY_DATA[province]:
                self.city_combo.addItem(city, city)

    def load_sample_data(self):
        """加载示例数据"""
        # 模拟订单管理数据
        sample_data = [
            {
                "id": 1,
                "province": "四川",
                "city": "成都市",
                "company": "广东省学前教育技术装备中心",
                "contact_person": "许经理",
                "contact_status": "待联系",
                "customer_manager": "高",
                "contact_records": "3",
                "score": "1",
                "next_contact_time": "2025-07-09 11:23:46",
                "sales_person": "黄1",
                "update_time": "2025-07-09 11:23:46"
            },
            {
                "id": 2,
                "province": "四川",
                "city": "成都市",
                "company": "广东省学前教育技术装备中心",
                "contact_person": "温经理",
                "contact_status": "高",
                "customer_manager": "高",
                "contact_records": "3",
                "score": "1",
                "next_contact_time": "2025-07-09 11:23:46",
                "sales_person": "黄1",
                "update_time": "2025-07-09 11:23:46"
            },
            {
                "id": 3,
                "province": "四川",
                "city": "成都市",
                "company": "广东省学前教育技术装备中心",
                "contact_person": "已成交",
                "contact_status": "高",
                "customer_manager": "高",
                "contact_records": "3",
                "score": "1",
                "next_contact_time": "2025-07-09 11:23:46",
                "sales_person": "黄1",
                "update_time": "2025-07-09 11:23:46"
            }
        ]

        self.orders_data = sample_data
        self.update_table_view()

    def update_table_view(self):
        """更新表格视图"""
        self.model.clear()
        headers = [
            "序号", "省份", "城市", "客户单位", "联系人", "联系状态",
            "客户负责人", "联系记录", "打分", "下次联系时间", "销售人员", "更新时间", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)

        for i, order in enumerate(self.orders_data, 1):
            # 创建操作按钮
            operation_text = "联系记录 详情记录"

            items = [
                QStandardItem(str(i)),  # 序号
                QStandardItem(order.get("province", "")),
                QStandardItem(order.get("city", "")),
                QStandardItem(order.get("company", "")),
                QStandardItem(order.get("contact_person", "")),
                QStandardItem(order.get("contact_status", "")),
                QStandardItem(order.get("customer_manager", "")),
                QStandardItem(order.get("contact_records", "")),
                QStandardItem(order.get("score", "")),
                QStandardItem(order.get("next_contact_time", "")),
                QStandardItem(order.get("sales_person", "")),
                QStandardItem(order.get("update_time", "")),
                QStandardItem(operation_text)
            ]

            # 设置项不可编辑
            for item in items:
                item.setEditable(False)

            # 设置联系状态的颜色
            contact_status = order.get("contact_status", "")
            if contact_status == "待联系":
                items[5].setBackground(Qt.GlobalColor.yellow)
            elif contact_status == "高":
                items[5].setBackground(Qt.GlobalColor.red)
            elif contact_status == "已成交":
                items[5].setBackground(Qt.GlobalColor.green)

            self.model.appendRow(items)

    def on_search_clicked(self):
        """搜索按钮点击事件"""
        # 获取搜索条件
        params = {
            'customer_unit': self.customer_unit_input.text().strip(),
            'industry': self.industry_combo.currentData(),
            'province': self.province_combo.currentData(),
            'city': self.city_combo.currentData(),
            'contact_status': self.contact_status_combo.currentData(),
            'customer_manager': self.customer_manager_combo.currentData(),
            'sales_person': self.sales_person_input.text().strip()
        }

        # 移除空值
        params = {k: v for k, v in params.items() if v}

        print(f"订单搜索条件: {params}")
        # 这里应该调用API进行搜索
        # 暂时显示提示
        QMessageBox.information(self, "搜索", f"订单搜索功能正在开发中...\n搜索条件: {params}")

    def on_reset_clicked(self):
        """重置按钮点击事件"""
        self.customer_unit_input.clear()
        self.industry_combo.setCurrentIndex(0)
        self.province_combo.setCurrentIndex(0)
        self.city_combo.setCurrentIndex(0)
        self.contact_status_combo.setCurrentIndex(0)
        self.customer_manager_combo.setCurrentIndex(0)
        self.sales_person_input.clear()

        # 重新加载数据
        self.load_sample_data()
        print("✅ 已重置订单搜索条件")

    def on_row_double_clicked(self, index):
        """行双击事件"""
        if index.isValid():
            row = index.row()
            if row < len(self.orders_data):
                order = self.orders_data[row]
                QMessageBox.information(
                    self,
                    "订单详情",
                    f"客户单位: {order.get('company', '')}\n"
                    f"联系人: {order.get('contact_person', '')}\n"
                    f"联系状态: {order.get('contact_status', '')}\n"
                    f"销售人员: {order.get('sales_person', '')}"
                )

# 导出
__all__ = ['OrderManagementView']
