#!/usr/bin/env python3
"""
高仿真CRM客户管理系统
基于原型图的精确实现
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QStackedWidget, QScrollArea,
    QSizePolicy, QSpacerItem, QLineEdit, QComboBox, QTableWidget,
    QTableWidgetItem, QCheckBox, QHeaderView, QAbstractItemView,
    QMessageBox, QDialog, QFormLayout, QTextEdit
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPalette, QColor

class TitleBar(QWidget):
    """顶部标题栏"""
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QWidget {
                background-color: #4A90E2;
                color: white;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # 系统标题
        title_label = QLabel("巨炜科技客户管理信息系统")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        layout.addWidget(title_label)
        layout.addStretch()
        
        # 用户信息区域
        user_info = QLabel("管理员 | 退出")
        user_info.setStyleSheet("color: #E8F4FD;")
        layout.addWidget(user_info)

class NavigationMenu(QWidget):
    """左侧导航菜单"""
    def __init__(self):
        super().__init__()
        self.setFixedWidth(150)
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-right: 1px solid #E0E0E0;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 菜单项
        menu_items = [
            ("数据预览", False),
            ("客户管理", True),  # 当前选中
            ("销售管理", False),
            ("订单管理", False),
            ("客户服务", False),
            ("产品管理", False),
            ("财务管理", False),
            ("系统设置", False)
        ]
        
        self.menu_buttons = []
        for text, is_active in menu_items:
            btn = self.create_menu_button(text, is_active)
            self.menu_buttons.append(btn)
            layout.addWidget(btn)
        
        layout.addStretch()
    
    def create_menu_button(self, text, is_active=False):
        """创建菜单按钮"""
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.setStyleSheet(self.get_button_style(is_active))
        
        # 设置字体
        font = QFont()
        font.setPointSize(10)
        btn.setFont(font)
        
        return btn
    
    def get_button_style(self, is_active):
        """获取按钮样式"""
        if is_active:
            return """
                QPushButton {
                    background-color: #4A90E2;
                    color: white;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: transparent;
                    color: #333333;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover {
                    background-color: #E8F4FD;
                    color: #4A90E2;
                }
            """

class CustomerManagementWidget(QWidget):
    """客户管理主界面"""
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 搜索筛选区域
        search_area = self.create_search_area()
        layout.addWidget(search_area)
        

        
        # 新增客户按钮区域
        add_customer_layout = QHBoxLayout()
        add_customer_btn = QPushButton("新增客户")
        add_customer_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_customer_btn.clicked.connect(self.add_customer)
        add_customer_layout.addWidget(add_customer_btn)
        add_customer_layout.addStretch()
        layout.addLayout(add_customer_layout)

        # 数据表格区域
        table_widget = self.create_data_table()
        layout.addWidget(table_widget)
    
    def create_search_area(self):
        """创建搜索筛选区域"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)

        layout = QHBoxLayout(frame)
        layout.setSpacing(8)
        layout.setContentsMargins(5, 5, 5, 5)

        # 客户名称搜索框（无标签，直接显示占位符）
        self.company_search = QLineEdit()
        self.company_search.setPlaceholderText("客户名称")
        self.company_search.setStyleSheet(self.get_search_input_style())
        self.company_search.setFixedWidth(150)
        layout.addWidget(self.company_search)

        # 行业类别下拉框
        self.industry_combo = QComboBox()
        self.industry_combo.addItems(["行业类别"])
        self.industry_combo.setStyleSheet(self.get_search_combo_style())
        self.industry_combo.setFixedWidth(100)
        layout.addWidget(self.industry_combo)

        # 省份下拉框
        self.province_combo = QComboBox()
        self.province_combo.addItems(["省份"])
        self.province_combo.setStyleSheet(self.get_search_combo_style())
        self.province_combo.setFixedWidth(80)
        layout.addWidget(self.province_combo)

        # 城市下拉框
        self.city_combo = QComboBox()
        self.city_combo.addItems(["城市"])
        self.city_combo.setStyleSheet(self.get_search_combo_style())
        self.city_combo.setFixedWidth(80)
        layout.addWidget(self.city_combo)

        # 联系状态下拉框
        self.status_combo = QComboBox()
        self.status_combo.addItems(["联系状态"])
        self.status_combo.setStyleSheet(self.get_search_combo_style())
        self.status_combo.setFixedWidth(100)
        layout.addWidget(self.status_combo)

        # 销售人员下拉框
        self.sales_combo = QComboBox()
        self.sales_combo.addItems(["销售人员"])
        self.sales_combo.setStyleSheet(self.get_search_combo_style())
        self.sales_combo.setFixedWidth(100)
        layout.addWidget(self.sales_combo)

        # 搜索按钮
        self.search_btn = QPushButton("搜索")
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        self.search_btn.setFixedHeight(28)

        # 重置按钮
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #545B62;
            }
        """)
        self.reset_btn.setFixedHeight(28)

        # 查看客户按钮
        self.view_customer_btn = QPushButton("查看客户")
        self.view_customer_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.view_customer_btn.setFixedHeight(28)

        # 分配销售按钮
        self.assign_sales_btn = QPushButton("分配销售")
        self.assign_sales_btn.setStyleSheet("""
            QPushButton {
                background-color: #FD7E14;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E8690B;
            }
        """)
        self.assign_sales_btn.setFixedHeight(28)

        # 分配客服按钮
        self.assign_service_btn = QPushButton("分配客服")
        self.assign_service_btn.setStyleSheet("""
            QPushButton {
                background-color: #20C997;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1BA085;
            }
        """)
        self.assign_service_btn.setFixedHeight(28)

        # 连接事件
        self.search_btn.clicked.connect(self.search_customers)
        self.reset_btn.clicked.connect(self.reset_search)
        self.view_customer_btn.clicked.connect(self.view_selected_customers)
        self.assign_sales_btn.clicked.connect(self.assign_sales)
        self.assign_service_btn.clicked.connect(self.assign_service)

        layout.addWidget(self.search_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.view_customer_btn)
        layout.addWidget(self.assign_sales_btn)
        layout.addWidget(self.assign_service_btn)
        layout.addStretch()

        return frame

    def get_input_style(self):
        """获取输入框样式"""
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #999999;
            }
        """

    def get_combo_style(self):
        """获取下拉框样式"""
        return """
            QComboBox {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                min-height: 20px;
                color: #333333;
            }
            QComboBox:focus {
                border-color: #4A90E2;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #D0D0D0;
                color: #333333;
                selection-background-color: #4A90E2;
                selection-color: white;
                outline: none;
            }
        """

    def get_search_input_style(self):
        """获取搜索输入框样式"""
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #CED4DA;
                border-radius: 3px;
                padding: 5px 8px;
                font-size: 12px;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #999999;
            }
        """

    def get_search_combo_style(self):
        """获取搜索下拉框样式"""
        return """
            QComboBox {
                background-color: white;
                border: 1px solid #CED4DA;
                border-radius: 3px;
                padding: 5px 8px;
                font-size: 12px;
                color: #333333;
                min-height: 16px;
            }
            QComboBox:focus {
                border-color: #4A90E2;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 16px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666666;
                margin-right: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #CED4DA;
                color: #333333;
                selection-background-color: #4A90E2;
                selection-color: white;
                outline: none;
            }
        """
    
    def create_toolbar(self):
        """创建操作按钮工具栏"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setSpacing(10)
        
        # 操作按钮
        buttons_config = [
            ("新增客户", "#28A745"),
            ("分配销售", "#FFC107"),
            ("分配客服", "#17A2B8")
        ]
        
        for text, color in buttons_config:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    opacity: 0.8;
                }}
            """)

            # 连接按钮事件
            if text == "新增客户":
                btn.clicked.connect(self.add_customer)
            elif text == "分配销售":
                btn.clicked.connect(self.assign_sales)
            elif text == "分配客服":
                btn.clicked.connect(self.assign_service)

            layout.addWidget(btn)


        
        layout.addStretch()
        return frame

    def create_data_table(self):
        """创建数据表格"""
        # 创建表格容器
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(table_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建表格
        self.table = QTableWidget()

        # 设置表格列
        columns = [
            ("", 30),           # 复选框列
            ("行业类别", 100),
            ("公司名", 200),
            ("城市", 80),
            ("客户联系信息", 150),
            ("联系人", 100),
            ("客户备注", 150),
            ("客户状态", 100),
            ("备注", 100),
            ("客户创建时间", 150),
            ("操作", 120)
        ]

        self.table.setColumnCount(len(columns))

        # 设置表头
        headers = [col[0] for col in columns]
        self.table.setHorizontalHeaderLabels(headers)

        # 设置列宽
        for i, (_, width) in enumerate(columns):
            self.table.setColumnWidth(i, width)

        # 设置表格样式和属性
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #E8E8E8;
                background-color: white;
                alternate-background-color: #F8F9FA;
                selection-background-color: #E3F2FD;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E8E8E8;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                color: #333333;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                border-right: 1px solid #E0E0E0;
                font-weight: bold;
                font-size: 12px;
            }
        """)

        # 设置表格属性
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(False)

        # 初始化空表格
        self.table.setRowCount(0)

        layout.addWidget(self.table)
        return table_frame



    def search_customers(self):
        """搜索客户"""
        company_name = self.company_search.text().strip()
        industry = self.industry_combo.currentText()
        province = self.province_combo.currentText()
        city = self.city_combo.currentText()
        status = self.status_combo.currentText()
        sales_person = self.sales_combo.currentText()

        # 执行筛选逻辑
        visible_rows = []
        for row in range(self.table.rowCount()):
            should_show = True

            # 按公司名称筛选
            if company_name:
                company_item = self.table.item(row, 2)
                if not company_item or company_name.lower() not in company_item.text().lower():
                    should_show = False

            # 按行业类别筛选
            if industry and industry != "行业类别":
                industry_item = self.table.item(row, 1)
                if not industry_item or industry_item.text() != industry:
                    should_show = False

            # 按城市筛选
            if city and city != "城市":
                city_item = self.table.item(row, 3)
                if not city_item or city_item.text() != city:
                    should_show = False

            # 按联系状态筛选
            if status and status != "联系状态":
                status_item = self.table.item(row, 7)
                if not status_item or status_item.text() != status:
                    should_show = False

            if should_show:
                visible_rows.append(row)
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

        # 显示搜索结果
        if visible_rows:
            QMessageBox.information(self, "搜索结果", f"找到 {len(visible_rows)} 个符合条件的客户")
        else:
            QMessageBox.information(self, "搜索结果", "没有找到符合条件的客户")

    def reset_search(self):
        """重置搜索条件"""
        self.company_search.clear()
        self.industry_combo.setCurrentIndex(0)
        self.province_combo.setCurrentIndex(0)
        self.city_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        self.sales_combo.setCurrentIndex(0)

        # 显示所有行
        for row in range(self.table.rowCount()):
            self.table.setRowHidden(row, False)

        QMessageBox.information(self, "提示", "搜索条件已重置，显示所有客户")

    def add_customer(self):
        """新增客户"""
        dialog = CustomerEditDialog(self)
        if dialog.exec() == QDialog.Accepted:
            customer_data = dialog.get_customer_data()
            self.add_customer_to_table(customer_data)
            QMessageBox.information(self, "成功", f"客户 '{customer_data['company']}' 添加成功！")

    def assign_sales(self):
        """分配销售"""
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选择要分配的客户！")
            return

        dialog = AssignSalesDialog(self)
        if dialog.exec() == QDialog.Accepted:
            assignment_data = dialog.get_assignment_data()
            QMessageBox.information(self, "分配成功",
                                  f"已将 {len(selected_rows)} 个客户分配给 {assignment_data['sales_person']}！")

    def assign_service(self):
        """分配客服"""
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选择要分配的客户！")
            return

        dialog = AssignServiceDialog(self)
        if dialog.exec() == QDialog.Accepted:
            assignment_data = dialog.get_assignment_data()
            QMessageBox.information(self, "分配成功",
                                  f"已将 {len(selected_rows)} 个客户分配给 {assignment_data['service_person']}！")

    def get_selected_rows(self):
        """获取选中的行"""
        selected_rows = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)
        return selected_rows

    def view_selected_customers(self):
        """查看选中的客户"""
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.information(self, "提示", "当前没有选中的客户")
            return

        customer_list = []
        for row in selected_rows:
            company_item = self.table.item(row, 2)
            if company_item:
                customer_list.append(company_item.text())

        if customer_list:
            customer_names = "\n".join([f"• {name}" for name in customer_list])
            QMessageBox.information(self, "选中的客户", f"已选中 {len(customer_list)} 个客户：\n\n{customer_names}")
        else:
            QMessageBox.information(self, "提示", "没有找到客户信息")

    def view_contact(self, row):
        """查看联系人"""
        # 获取当前行的客户数据
        company_name = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
        customer_data = {
            "company": company_name,
            "address": "广汉市北京大道北一段15号",
            "notes": ""
        }

        dialog = ViewContactDialog(customer_data, self)
        dialog.exec()

    def delete_customer(self, row):
        """删除客户"""
        company_name = self.table.item(row, 2).text() if self.table.item(row, 2) else "该客户"

        reply = QMessageBox.question(self, "确认删除",
                                   f"确定要删除客户 '{company_name}' 吗？\n此操作不可撤销！",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.table.removeRow(row)
            QMessageBox.information(self, "删除成功", f"客户 '{company_name}' 已删除！")

    def add_customer_to_table(self, customer_data):
        """将客户数据添加到表格"""
        from datetime import datetime

        # 获取当前行数
        current_row = self.table.rowCount()
        self.table.insertRow(current_row)

        # 添加复选框
        checkbox = QCheckBox()
        checkbox.setStyleSheet("""
            QCheckBox {
                margin: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #D0D0D0;
                background-color: white;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4A90E2;
                background-color: #4A90E2;
                border-radius: 3px;
            }
        """)
        self.table.setCellWidget(current_row, 0, checkbox)

        # 添加数据列
        # 获取主要联系人信息
        primary_contact = ""
        contact_info_count = "0"
        if customer_data.get("contacts"):
            contact_info_count = str(len(customer_data["contacts"]))
            # 找到关键人或第一个联系人
            for contact in customer_data["contacts"]:
                if contact.get("is_key_person") or not primary_contact:
                    primary_contact = contact.get("name", "")
                    if contact.get("is_key_person"):
                        break

        columns_data = [
            customer_data.get("industry", ""),
            customer_data.get("company", ""),
            customer_data.get("city", ""),
            contact_info_count,
            primary_contact,
            customer_data.get("notes", ""),
            "潜在客户",  # 默认状态
            customer_data.get("notes", "")[:10] + "..." if len(customer_data.get("notes", "")) > 10 else customer_data.get("notes", ""),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        for col, value in enumerate(columns_data, 1):
            item = QTableWidgetItem(str(value))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 设置为只读
            self.table.setItem(current_row, col, item)

        # 添加操作按钮
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(5, 2, 5, 2)
        action_layout.setSpacing(5)

        edit_btn = QPushButton("编辑")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        edit_btn.clicked.connect(lambda: self.view_contact(current_row))

        delete_btn = QPushButton("删除")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_customer(current_row))

        action_layout.addWidget(edit_btn)
        action_layout.addWidget(delete_btn)
        action_layout.addStretch()

        self.table.setCellWidget(current_row, 10, action_widget)

        # 更新筛选选项
        self.update_filter_options()

    def update_filter_options(self):
        """更新筛选下拉框选项"""
        # 收集所有唯一值
        industries = set()
        provinces = set()
        cities = set()
        statuses = set()

        for row in range(self.table.rowCount()):
            # 行业类别
            industry_item = self.table.item(row, 1)
            if industry_item and industry_item.text().strip():
                industries.add(industry_item.text().strip())

            # 城市（从第3列获取）
            city_item = self.table.item(row, 3)
            if city_item and city_item.text().strip():
                cities.add(city_item.text().strip())

            # 联系状态
            status_item = self.table.item(row, 7)
            if status_item and status_item.text().strip():
                statuses.add(status_item.text().strip())

        # 更新行业类别下拉框
        current_industry = self.industry_combo.currentText()
        self.industry_combo.clear()
        self.industry_combo.addItem("行业类别")
        for industry in sorted(industries):
            self.industry_combo.addItem(industry)
        if current_industry in industries:
            self.industry_combo.setCurrentText(current_industry)

        # 更新城市下拉框
        current_city = self.city_combo.currentText()
        self.city_combo.clear()
        self.city_combo.addItem("城市")
        for city in sorted(cities):
            self.city_combo.addItem(city)
        if current_city in cities:
            self.city_combo.setCurrentText(current_city)

        # 更新联系状态下拉框
        current_status = self.status_combo.currentText()
        self.status_combo.clear()
        self.status_combo.addItem("联系状态")
        for status in sorted(statuses):
            self.status_combo.addItem(status)
        if current_status in statuses:
            self.status_combo.setCurrentText(current_status)

class CustomerEditDialog(QDialog):
    """添加客户对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加客户")
        self.setModal(True)
        self.resize(550, 480)
        self.contact_rows = []  # 存储联系人行
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 设置对话框样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题栏
        title_bar = QFrame()
        title_bar.setStyleSheet("""
            QFrame {
                background-color: #4A90E2;
                color: white;
                padding: 10px;
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_label = QLabel("添加客户")
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addWidget(title_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 15, 25, 15)
        content_layout.setSpacing(12)

        # 基本信息区域
        basic_info_layout = QFormLayout()
        basic_info_layout.setSpacing(8)
        basic_info_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # 行业类别
        industry_label = QLabel("行业类别:")
        industry_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 80px;")
        self.industry_combo = QComboBox()
        self.industry_combo.addItems(["应急 | 人社 | 住建 | 其它"])
        self.industry_combo.setStyleSheet(self.get_combo_style())
        basic_info_layout.addRow(industry_label, self.industry_combo)

        # 客户单位
        company_label = QLabel("客户单位:")
        company_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 80px;")
        self.company_edit = QLineEdit()
        self.company_edit.setPlaceholderText("广汉市学民职业技能培训学校")
        self.company_edit.setStyleSheet(self.get_input_style())
        basic_info_layout.addRow(company_label, self.company_edit)

        # 所在省份
        province_label = QLabel("所在省份:")
        province_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 80px;")
        self.province_combo = QComboBox()
        self.province_combo.addItems(["省份"])
        self.province_combo.setStyleSheet(self.get_combo_style())
        basic_info_layout.addRow(province_label, self.province_combo)

        # 城市名称
        city_label = QLabel("城市名称:")
        city_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 80px;")
        self.city_combo = QComboBox()
        self.city_combo.addItems(["城市"])
        self.city_combo.setStyleSheet(self.get_combo_style())
        basic_info_layout.addRow(city_label, self.city_combo)

        # 详细地址
        address_label = QLabel("详细地址:")
        address_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 80px;")
        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("广汉市北京大道北一段15号")
        self.address_edit.setStyleSheet(self.get_input_style())
        basic_info_layout.addRow(address_label, self.address_edit)

        # 客情备注
        notes_label = QLabel("客情备注:")
        notes_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 80px;")
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setStyleSheet(self.get_textarea_style())
        basic_info_layout.addRow(notes_label, self.notes_edit)

        content_layout.addLayout(basic_info_layout)

        # 联系人管理区域（无边框，直接集成）
        # 联系人列表容器
        self.contact_container = QWidget()
        self.contact_container_layout = QVBoxLayout(self.contact_container)
        self.contact_container_layout.setSpacing(8)
        self.contact_container_layout.setContentsMargins(0, 10, 0, 0)

        # 添加默认的两个联系人行
        self.add_contact_row("刘必立", "15862184966", True)
        self.add_contact_row("李通", "13956774892", False)

        content_layout.addWidget(self.contact_container)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.addStretch()

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 25px;
                font-weight: bold;
                font-size: 12px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #545B62;
            }
        """)

        self.save_btn = QPushButton("保存")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 25px;
                font-weight: bold;
                font-size: 12px;
                min-width: 70px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)

        content_layout.addLayout(button_layout)
        layout.addWidget(content_widget)

        # 连接信号
        self.save_btn.clicked.connect(self.save_customer)
        self.cancel_btn.clicked.connect(self.reject)

    def add_contact_row(self, name="", phone="", is_primary=False):
        """添加联系人行"""
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 3, 0, 3)
        row_layout.setSpacing(8)

        # 联系人标签
        contact_label = QLabel("联系人:")
        contact_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 80px; text-align: right;")
        contact_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        row_layout.addWidget(contact_label)

        # 姓名输入框
        name_edit = QLineEdit()
        name_edit.setText(name)
        name_edit.setStyleSheet(self.get_input_style())
        name_edit.setFixedWidth(100)
        row_layout.addWidget(name_edit)

        # 电话标签
        phone_label = QLabel("电话:")
        phone_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 50px; text-align: right;")
        phone_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        row_layout.addWidget(phone_label)

        # 电话输入框
        phone_edit = QLineEdit()
        phone_edit.setText(phone)
        phone_edit.setStyleSheet(self.get_input_style())
        phone_edit.setFixedWidth(120)
        row_layout.addWidget(phone_edit)

        # 关键人复选框
        key_person_checkbox = QCheckBox("关键人")
        key_person_checkbox.setChecked(is_primary)
        key_person_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-weight: bold;
                background-color: #4A90E2;
                border-radius: 3px;
                padding: 2px 8px;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                margin-right: 5px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid white;
                background-color: transparent;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                border: 1px solid white;
                background-color: white;
                border-radius: 2px;
            }
        """)
        row_layout.addWidget(key_person_checkbox)

        # 添加/删除按钮
        add_btn = QPushButton("+")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 10px;
                width: 20px;
                height: 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        add_btn.setFixedSize(20, 20)
        add_btn.clicked.connect(lambda: self.add_contact_row())
        row_layout.addWidget(add_btn)

        remove_btn = QPushButton("-")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                border-radius: 10px;
                width: 20px;
                height: 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
        """)
        remove_btn.setFixedSize(20, 20)
        remove_btn.clicked.connect(lambda: self.remove_contact_row(row_widget))
        row_layout.addWidget(remove_btn)

        row_layout.addStretch()

        # 存储联系人数据
        contact_data = {
            'widget': row_widget,
            'name_edit': name_edit,
            'phone_edit': phone_edit,
            'key_person_checkbox': key_person_checkbox
        }
        self.contact_rows.append(contact_data)

        self.contact_container_layout.addWidget(row_widget)

    def remove_contact_row(self, row_widget):
        """删除联系人行"""
        if len(self.contact_rows) <= 1:
            QMessageBox.warning(self, "提示", "至少需要保留一个联系人！")
            return

        # 从列表中移除
        for i, contact_data in enumerate(self.contact_rows):
            if contact_data['widget'] == row_widget:
                self.contact_rows.pop(i)
                break

        # 从界面中移除
        self.contact_container_layout.removeWidget(row_widget)
        row_widget.deleteLater()

    def get_input_style(self):
        """获取输入框样式"""
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
                outline: none;
            }
        """

    def get_combo_style(self):
        """获取下拉框样式"""
        return """
            QComboBox {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                min-height: 20px;
                color: #333333;
            }
            QComboBox:focus {
                border-color: #4A90E2;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #D0D0D0;
                color: #333333;
                selection-background-color: #4A90E2;
                selection-color: white;
                outline: none;
            }
        """

    def get_textarea_style(self):
        """获取文本域样式"""
        return """
            QTextEdit {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                color: #333333;
            }
            QTextEdit:focus {
                border-color: #4A90E2;
                outline: none;
            }
        """

    def save_customer(self):
        """保存客户"""
        if not self.company_edit.text().strip():
            QMessageBox.warning(self, "错误", "客户单位不能为空！")
            return

        # 验证至少有一个联系人
        has_contact = False
        for contact_data in self.contact_rows:
            if contact_data['name_edit'].text().strip():
                has_contact = True
                break

        if not has_contact:
            QMessageBox.warning(self, "错误", "至少需要填写一个联系人信息！")
            return

        self.accept()

    def get_customer_data(self):
        """获取客户数据"""
        contacts = []
        for contact_data in self.contact_rows:
            name = contact_data['name_edit'].text().strip()
            phone = contact_data['phone_edit'].text().strip()
            is_key = contact_data['key_person_checkbox'].isChecked()

            if name or phone:  # 只保存有内容的联系人
                contacts.append({
                    'name': name,
                    'phone': phone,
                    'is_key_person': is_key
                })

        return {
            "industry": self.industry_combo.currentText(),
            "company": self.company_edit.text().strip(),
            "province": self.province_combo.currentText(),
            "city": self.city_combo.currentText(),
            "address": self.address_edit.text().strip(),
            "notes": self.notes_edit.toPlainText().strip(),
            "contacts": contacts
        }

class AssignSalesDialog(QDialog):
    """分配销售对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("分配销售")
        self.setModal(True)
        self.resize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 设置对话框样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题栏
        title_bar = QFrame()
        title_bar.setStyleSheet("""
            QFrame {
                background-color: #4A90E2;
                color: white;
                padding: 10px;
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_label = QLabel("分配销售")
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addWidget(title_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # 分配给销售标签
        assign_label = QLabel("分配给销售:")
        assign_label.setStyleSheet("font-weight: bold; color: #333333; font-size: 14px;")
        content_layout.addWidget(assign_label)

        # 表单区域
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # 部门名称
        dept_label = QLabel("部门名称:")
        dept_label.setStyleSheet("color: #333333; font-weight: bold;")
        self.dept_edit = QLineEdit("销售部")
        self.dept_edit.setReadOnly(True)
        self.dept_edit.setStyleSheet(self.get_readonly_input_style())
        form_layout.addRow(dept_label, self.dept_edit)

        # 组别名称
        group_label = QLabel("组别名称:")
        group_label.setStyleSheet("color: #333333; font-weight: bold;")
        self.group_combo = QComboBox()
        self.group_combo.addItems(["销售一组", "销售二组", "销售三组"])
        self.group_combo.setStyleSheet(self.get_combo_style())
        form_layout.addRow(group_label, self.group_combo)

        # 销售姓名
        sales_label = QLabel("销售姓名:")
        sales_label.setStyleSheet("color: #333333; font-weight: bold;")
        self.sales_combo = QComboBox()
        self.sales_combo.addItems(["张飞", "李白", "王五", "赵六"])
        self.sales_combo.setStyleSheet(self.get_combo_style())
        form_layout.addRow(sales_label, self.sales_combo)

        content_layout.addLayout(form_layout)
        content_layout.addStretch()

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #545B62;
            }
        """)

        self.assign_btn = QPushButton("分配")
        self.assign_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.assign_btn)

        content_layout.addLayout(button_layout)
        layout.addWidget(content_widget)

        # 连接信号
        self.assign_btn.clicked.connect(self.assign_sales)
        self.cancel_btn.clicked.connect(self.reject)

    def get_combo_style(self):
        """获取下拉框样式"""
        return """
            QComboBox {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                min-height: 20px;
                color: #333333;
            }
            QComboBox:focus {
                border-color: #4A90E2;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #D0D0D0;
                color: #333333;
                selection-background-color: #4A90E2;
                selection-color: white;
                outline: none;
            }
        """

    def get_readonly_input_style(self):
        """获取只读输入框样式"""
        return """
            QLineEdit {
                background-color: #F8F9FA;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                color: #333333;
            }
        """

    def assign_sales(self):
        """分配销售"""
        group = self.group_combo.currentText()
        sales = self.sales_combo.currentText()

        QMessageBox.information(self, "分配成功",
                              f"已成功分配给 {group} 的 {sales}！")
        self.accept()

    def get_assignment_data(self):
        """获取分配数据"""
        return {
            "department": self.dept_edit.text(),
            "group": self.group_combo.currentText(),
            "sales_person": self.sales_combo.currentText()
        }

class AssignServiceDialog(QDialog):
    """分配客服对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("分配客服")
        self.setModal(True)
        self.resize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 设置对话框样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题栏
        title_bar = QFrame()
        title_bar.setStyleSheet("""
            QFrame {
                background-color: #4A90E2;
                color: white;
                padding: 10px;
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_label = QLabel("分配客服")
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addWidget(title_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # 分配给客服标签
        assign_label = QLabel("分配给客服:")
        assign_label.setStyleSheet("font-weight: bold; color: #333333; font-size: 14px;")
        content_layout.addWidget(assign_label)

        # 表单区域
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # 部门名称
        dept_label = QLabel("部门名称:")
        dept_label.setStyleSheet("color: #333333; font-weight: bold;")
        self.dept_edit = QLineEdit("客服部")
        self.dept_edit.setReadOnly(True)
        self.dept_edit.setStyleSheet(self.get_readonly_input_style())
        form_layout.addRow(dept_label, self.dept_edit)

        # 组别名称
        group_label = QLabel("组别名称:")
        group_label.setStyleSheet("color: #333333; font-weight: bold;")
        self.group_combo = QComboBox()
        self.group_combo.addItems(["客服一组", "客服二组", "客服三组"])
        self.group_combo.setStyleSheet(self.get_combo_style())
        form_layout.addRow(group_label, self.group_combo)

        # 客服姓名
        service_label = QLabel("客服姓名:")
        service_label.setStyleSheet("color: #333333; font-weight: bold;")
        self.service_combo = QComboBox()
        self.service_combo.addItems(["陈小二", "李小三", "王小四", "赵小五"])
        self.service_combo.setStyleSheet(self.get_combo_style())
        form_layout.addRow(service_label, self.service_combo)

        content_layout.addLayout(form_layout)
        content_layout.addStretch()

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #545B62;
            }
        """)

        self.assign_btn = QPushButton("保存")
        self.assign_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.assign_btn)

        content_layout.addLayout(button_layout)
        layout.addWidget(content_widget)

        # 连接信号
        self.assign_btn.clicked.connect(self.assign_service)
        self.cancel_btn.clicked.connect(self.reject)

    def get_combo_style(self):
        """获取下拉框样式"""
        return """
            QComboBox {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                min-height: 20px;
                color: #333333;
            }
            QComboBox:focus {
                border-color: #4A90E2;
                outline: none;
                box-shadow: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #D0D0D0;
                color: #333333;
                selection-background-color: #4A90E2;
                selection-color: white;
                outline: none;
            }
        """

    def get_readonly_input_style(self):
        """获取只读输入框样式"""
        return """
            QLineEdit {
                background-color: #F8F9FA;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                color: #333333;
            }
        """

    def assign_service(self):
        """分配客服"""
        group = self.group_combo.currentText()
        service = self.service_combo.currentText()

        QMessageBox.information(self, "分配成功",
                              f"已成功分配给 {group} 的 {service}！")
        self.accept()

    def get_assignment_data(self):
        """获取分配数据"""
        return {
            "department": self.dept_edit.text(),
            "group": self.group_combo.currentText(),
            "service_person": self.service_combo.currentText()
        }

class ViewContactDialog(QDialog):
    """查看联系人对话框"""
    def __init__(self, customer_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查看联系人")
        self.setModal(True)
        self.resize(500, 400)
        self.customer_data = customer_data or {}
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 设置对话框样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题栏
        title_bar = QFrame()
        title_bar.setStyleSheet("""
            QFrame {
                background-color: #4A90E2;
                color: white;
                padding: 10px;
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_label = QLabel("查看联系人")
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addWidget(title_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # 客户基本信息
        info_layout = QFormLayout()
        info_layout.setSpacing(10)

        # 客户单位
        company_label = QLabel("客户单位:")
        company_label.setStyleSheet("color: #333333; font-weight: bold;")
        company_value = QLabel("广汉市学民职业技能培训学校")
        company_value.setStyleSheet("color: #666666;")
        info_layout.addRow(company_label, company_value)

        # 详细地址
        address_label = QLabel("详细地址:")
        address_label.setStyleSheet("color: #333333; font-weight: bold;")
        address_value = QLabel("广汉市北京大道北一段15号")
        address_value.setStyleSheet("color: #666666;")
        info_layout.addRow(address_label, address_value)

        # 客情备注
        notes_label = QLabel("客情备注:")
        notes_label.setStyleSheet("color: #333333; font-weight: bold;")
        notes_text = QTextEdit()
        notes_text.setReadOnly(True)
        notes_text.setMaximumHeight(80)
        notes_text.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                color: #666666;
            }
        """)
        info_layout.addRow(notes_label, notes_text)

        content_layout.addLayout(info_layout)

        # 联系人信息区域
        contact_frame = QFrame()
        contact_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background-color: #F8F9FA;
                padding: 15px;
            }
        """)
        contact_layout = QVBoxLayout(contact_frame)

        # 联系人1
        contact1_layout = QHBoxLayout()
        contact1_layout.setSpacing(15)

        contact1_name_label = QLabel("联系人:")
        contact1_name_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 60px;")
        contact1_layout.addWidget(contact1_name_label)

        contact1_name_edit = QLineEdit("刘必立")
        contact1_name_edit.setReadOnly(True)
        contact1_name_edit.setStyleSheet(self.get_readonly_input_style())
        contact1_name_edit.setMaximumWidth(120)
        contact1_layout.addWidget(contact1_name_edit)

        contact1_phone_label = QLabel("电话:")
        contact1_phone_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 40px;")
        contact1_layout.addWidget(contact1_phone_label)

        contact1_phone_edit = QLineEdit("15862184966")
        contact1_phone_edit.setReadOnly(True)
        contact1_phone_edit.setStyleSheet(self.get_readonly_input_style())
        contact1_phone_edit.setMaximumWidth(150)
        contact1_layout.addWidget(contact1_phone_edit)

        contact1_key_checkbox = QCheckBox("关键人")
        contact1_key_checkbox.setChecked(True)
        contact1_key_checkbox.setEnabled(False)
        contact1_key_checkbox.setStyleSheet("""
            QCheckBox {
                color: #333333;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #D0D0D0;
                background-color: white;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4A90E2;
                background-color: #4A90E2;
                border-radius: 3px;
            }
        """)
        contact1_layout.addWidget(contact1_key_checkbox)
        contact1_layout.addStretch()

        contact_layout.addLayout(contact1_layout)

        # 联系人2
        contact2_layout = QHBoxLayout()
        contact2_layout.setSpacing(15)

        contact2_name_label = QLabel("联系人:")
        contact2_name_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 60px;")
        contact2_layout.addWidget(contact2_name_label)

        contact2_name_edit = QLineEdit("李通")
        contact2_name_edit.setReadOnly(True)
        contact2_name_edit.setStyleSheet(self.get_readonly_input_style())
        contact2_name_edit.setMaximumWidth(120)
        contact2_layout.addWidget(contact2_name_edit)

        contact2_phone_label = QLabel("电话:")
        contact2_phone_label.setStyleSheet("color: #333333; font-weight: bold; min-width: 40px;")
        contact2_layout.addWidget(contact2_phone_label)

        contact2_phone_edit = QLineEdit("13956774892")
        contact2_phone_edit.setReadOnly(True)
        contact2_phone_edit.setStyleSheet(self.get_readonly_input_style())
        contact2_phone_edit.setMaximumWidth(150)
        contact2_layout.addWidget(contact2_phone_edit)

        contact2_key_checkbox = QCheckBox("关键人")
        contact2_key_checkbox.setChecked(False)
        contact2_key_checkbox.setEnabled(False)
        contact2_key_checkbox.setStyleSheet("""
            QCheckBox {
                color: #333333;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #D0D0D0;
                background-color: white;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4A90E2;
                background-color: #4A90E2;
                border-radius: 3px;
            }
        """)
        contact2_layout.addWidget(contact2_key_checkbox)
        contact2_layout.addStretch()

        contact_layout.addLayout(contact2_layout)
        content_layout.addWidget(contact_frame)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.close_btn = QPushButton("关闭")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #545B62;
            }
        """)

        button_layout.addWidget(self.close_btn)
        content_layout.addLayout(button_layout)
        layout.addWidget(content_widget)

        # 连接信号
        self.close_btn.clicked.connect(self.accept)

    def get_readonly_input_style(self):
        """获取只读输入框样式"""
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #D0D0D0;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 12px;
                color: #333333;
            }
        """

class HighFidelityCRMWindow(QMainWindow):
    """高仿真CRM主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("巨炜科技客户管理信息系统")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置主界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 顶部标题栏
        title_bar = TitleBar()
        main_layout.addWidget(title_bar)
        
        # 内容区域
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 左侧导航菜单
        navigation = NavigationMenu()
        content_layout.addWidget(navigation)
        
        # 主内容区域
        main_content = CustomerManagementWidget()
        content_layout.addWidget(main_content)
        
        # 将内容布局添加到主布局
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 创建主窗口
    window = HighFidelityCRMWindow()
    window.show()
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
