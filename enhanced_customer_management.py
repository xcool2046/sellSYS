#!/usr/bin/env python3
"""
完善的客户管理功能模块
"""
import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QLabel, QMessageBox, QDialog, QFormLayout, QTextEdit, QCheckBox,
    QHeaderView, QTabWidget, QGroupBox, QGridLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class CustomerDialog(QDialog):
    """客户信息编辑对话框"""
    def __init__(self, customer_data=None, parent=None):
        super().__init__(parent)
        self.customer_data = customer_data
        self.setWindowTitle("客户信息" if customer_data else "新增客户")
        self.setModal(True)
        self.resize(600, 500)
        
        self.setup_ui()
        if customer_data:
            self.load_customer_data()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 基本信息标签页
        basic_tab = QWidget()
        self.setup_basic_info_tab(basic_tab)
        tab_widget.addTab(basic_tab, "基本信息")
        
        # 联系人标签页
        contacts_tab = QWidget()
        self.setup_contacts_tab(contacts_tab)
        tab_widget.addTab(contacts_tab, "联系人")
        
        layout.addWidget(tab_widget)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.save_btn = QPushButton("保存")
        self.cancel_btn = QPushButton("取消")
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # 连接信号
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
    
    def setup_basic_info_tab(self, tab):
        """设置基本信息标签页"""
        layout = QFormLayout(tab)
        
        # 公司信息
        self.company_edit = QLineEdit()
        self.company_edit.setPlaceholderText("请输入公司名称")
        layout.addRow("公司名称*:", self.company_edit)
        
        self.industry_combo = QComboBox()
        self.industry_combo.setEditable(True)
        self.industry_combo.addItems([
            "制造业", "信息技术", "金融服务", "教育培训", "医疗健康",
            "房地产", "零售贸易", "物流运输", "能源化工", "其他"
        ])
        layout.addRow("行业:", self.industry_combo)
        
        # 地址信息
        address_group = QGroupBox("地址信息")
        address_layout = QGridLayout(address_group)
        
        self.province_combo = QComboBox()
        self.province_combo.setEditable(True)
        self.province_combo.addItems([
            "北京", "上海", "广东", "江苏", "浙江", "山东", "河南", "四川", "湖北", "湖南"
        ])
        address_layout.addWidget(QLabel("省份:"), 0, 0)
        address_layout.addWidget(self.province_combo, 0, 1)
        
        self.city_combo = QComboBox()
        self.city_combo.setEditable(True)
        address_layout.addWidget(QLabel("城市:"), 0, 2)
        address_layout.addWidget(self.city_combo, 0, 3)
        
        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("详细地址")
        address_layout.addWidget(QLabel("详细地址:"), 1, 0)
        address_layout.addWidget(self.address_edit, 1, 1, 1, 3)
        
        layout.addRow(address_group)
        
        # 其他信息
        self.website_edit = QLineEdit()
        self.website_edit.setPlaceholderText("http://www.example.com")
        layout.addRow("公司网站:", self.website_edit)
        
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["1-50人", "51-200人", "201-500人", "501-1000人", "1000人以上"])
        layout.addRow("公司规模:", self.scale_combo)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["潜在客户", "已联系", "已报价", "成交客户", "流失客户"])
        layout.addRow("客户状态:", self.status_combo)
    
    def setup_contacts_tab(self, tab):
        """设置联系人标签页"""
        layout = QVBoxLayout(tab)
        
        # 联系人列表
        self.contacts_table = QTableWidget()
        self.contacts_table.setColumnCount(4)
        self.contacts_table.setHorizontalHeaderLabels(["姓名", "电话", "邮箱", "是否关键人"])
        self.contacts_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(QLabel("联系人信息:"))
        layout.addWidget(self.contacts_table)
        
        # 联系人操作按钮
        contact_btn_layout = QHBoxLayout()
        self.add_contact_btn = QPushButton("添加联系人")
        self.remove_contact_btn = QPushButton("删除联系人")
        
        contact_btn_layout.addWidget(self.add_contact_btn)
        contact_btn_layout.addWidget(self.remove_contact_btn)
        contact_btn_layout.addStretch()
        
        layout.addLayout(contact_btn_layout)
        
        # 连接信号
        self.add_contact_btn.clicked.connect(self.add_contact)
        self.remove_contact_btn.clicked.connect(self.remove_contact)
    
    def add_contact(self):
        """添加联系人"""
        row = self.contacts_table.rowCount()
        self.contacts_table.insertRow(row)
        
        # 添加默认项
        self.contacts_table.setItem(row, 0, QTableWidgetItem(""))
        self.contacts_table.setItem(row, 1, QTableWidgetItem(""))
        self.contacts_table.setItem(row, 2, QTableWidgetItem(""))
        
        # 添加复选框
        checkbox = QCheckBox()
        self.contacts_table.setCellWidget(row, 3, checkbox)
    
    def remove_contact(self):
        """删除选中的联系人"""
        current_row = self.contacts_table.currentRow()
        if current_row >= 0:
            self.contacts_table.removeRow(current_row)
    
    def load_customer_data(self):
        """加载客户数据"""
        if not self.customer_data:
            return
        
        # 加载基本信息
        self.company_edit.setText(self.customer_data.get("company", ""))
        self.industry_combo.setCurrentText(self.customer_data.get("industry", ""))
        self.province_combo.setCurrentText(self.customer_data.get("province", ""))
        self.city_combo.setCurrentText(self.customer_data.get("city", ""))
        self.address_edit.setText(self.customer_data.get("address", ""))
        self.website_edit.setText(self.customer_data.get("website", ""))
        self.scale_combo.setCurrentText(self.customer_data.get("scale", ""))
        self.status_combo.setCurrentText(self.customer_data.get("status", ""))
        
        # 加载联系人信息
        contacts = self.customer_data.get("contacts", [])
        self.contacts_table.setRowCount(len(contacts))
        
        for i, contact in enumerate(contacts):
            self.contacts_table.setItem(i, 0, QTableWidgetItem(contact.get("name", "")))
            self.contacts_table.setItem(i, 1, QTableWidgetItem(contact.get("phone", "")))
            self.contacts_table.setItem(i, 2, QTableWidgetItem(contact.get("email", "")))
            
            checkbox = QCheckBox()
            checkbox.setChecked(contact.get("is_key_person", False))
            self.contacts_table.setCellWidget(i, 3, checkbox)
    
    def get_customer_data(self):
        """获取客户数据"""
        # 获取基本信息
        customer_data = {
            "company": self.company_edit.text().strip(),
            "industry": self.industry_combo.currentText(),
            "province": self.province_combo.currentText(),
            "city": self.city_combo.currentText(),
            "address": self.address_edit.text().strip(),
            "website": self.website_edit.text().strip(),
            "scale": self.scale_combo.currentText(),
            "status": self.status_combo.currentText()
        }
        
        # 获取联系人信息
        contacts = []
        for i in range(self.contacts_table.rowCount()):
            name_item = self.contacts_table.item(i, 0)
            phone_item = self.contacts_table.item(i, 1)
            email_item = self.contacts_table.item(i, 2)
            checkbox = self.contacts_table.cellWidget(i, 3)
            
            if name_item and phone_item and name_item.text().strip():
                contact = {
                    "name": name_item.text().strip(),
                    "phone": phone_item.text().strip(),
                    "email": email_item.text().strip() if email_item else "",
                    "is_key_person": checkbox.isChecked() if checkbox else False
                }
                contacts.append(contact)
        
        customer_data["contacts"] = contacts
        return customer_data

class CustomerManagementWindow(QMainWindow):
    """客户管理主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("客户管理系统")
        self.setGeometry(100, 100, 1200, 800)
        
        # 模拟数据
        self.customers_data = []
        
        self.setup_ui()
        self.load_sample_data()
    
    def setup_ui(self):
        """设置界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("客户管理")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 搜索和筛选区域
        self.setup_search_area(layout)
        
        # 操作按钮区域
        self.setup_toolbar(layout)
        
        # 客户列表表格
        self.setup_table(layout)
        
        # 状态栏
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)
    
    def setup_search_area(self, layout):
        """设置搜索区域"""
        search_group = QGroupBox("搜索筛选")
        search_layout = QGridLayout(search_group)
        
        # 搜索框
        search_layout.addWidget(QLabel("公司名称:"), 0, 0)
        self.company_search = QLineEdit()
        self.company_search.setPlaceholderText("输入公司名称搜索")
        search_layout.addWidget(self.company_search, 0, 1)
        
        # 行业筛选
        search_layout.addWidget(QLabel("行业:"), 0, 2)
        self.industry_filter = QComboBox()
        self.industry_filter.addItems(["全部", "制造业", "信息技术", "金融服务", "教育培训", "其他"])
        search_layout.addWidget(self.industry_filter, 0, 3)
        
        # 状态筛选
        search_layout.addWidget(QLabel("状态:"), 1, 0)
        self.status_filter = QComboBox()
        self.status_filter.addItems(["全部", "潜在客户", "已联系", "已报价", "成交客户", "流失客户"])
        search_layout.addWidget(self.status_filter, 1, 1)
        
        # 搜索按钮
        self.search_btn = QPushButton("搜索")
        self.reset_btn = QPushButton("重置")
        search_layout.addWidget(self.search_btn, 1, 2)
        search_layout.addWidget(self.reset_btn, 1, 3)
        
        layout.addWidget(search_group)
        
        # 连接信号
        self.search_btn.clicked.connect(self.search_customers)
        self.reset_btn.clicked.connect(self.reset_search)
    
    def setup_toolbar(self, layout):
        """设置工具栏"""
        toolbar_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("新增客户")
        self.edit_btn = QPushButton("编辑客户")
        self.delete_btn = QPushButton("删除客户")
        self.export_btn = QPushButton("导出数据")
        
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.export_btn)
        
        layout.addLayout(toolbar_layout)
        
        # 连接信号
        self.add_btn.clicked.connect(self.add_customer)
        self.edit_btn.clicked.connect(self.edit_customer)
        self.delete_btn.clicked.connect(self.delete_customer)
        self.export_btn.clicked.connect(self.export_data)
    
    def setup_table(self, layout):
        """设置表格"""
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "公司名称", "行业", "省份", "城市", "状态", "联系人数", "操作"
        ])
        
        # 设置表格属性
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table)
    
    def load_sample_data(self):
        """加载示例数据"""
        sample_data = [
            {
                "id": 1,
                "company": "北京科技有限公司",
                "industry": "信息技术",
                "province": "北京",
                "city": "北京",
                "status": "潜在客户",
                "contacts": [{"name": "张三", "phone": "13800138000", "email": "zhang@example.com", "is_key_person": True}]
            },
            {
                "id": 2,
                "company": "上海制造集团",
                "industry": "制造业",
                "province": "上海",
                "city": "上海",
                "status": "已联系",
                "contacts": [{"name": "李四", "phone": "13900139000", "email": "li@example.com", "is_key_person": False}]
            }
        ]
        
        self.customers_data = sample_data
        self.refresh_table()
    
    def refresh_table(self):
        """刷新表格"""
        self.table.setRowCount(len(self.customers_data))
        
        for i, customer in enumerate(self.customers_data):
            self.table.setItem(i, 0, QTableWidgetItem(str(customer["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(customer["company"]))
            self.table.setItem(i, 2, QTableWidgetItem(customer["industry"]))
            self.table.setItem(i, 3, QTableWidgetItem(customer["province"]))
            self.table.setItem(i, 4, QTableWidgetItem(customer["city"]))
            self.table.setItem(i, 5, QTableWidgetItem(customer["status"]))
            self.table.setItem(i, 6, QTableWidgetItem(str(len(customer.get("contacts", [])))))
            
            # 操作按钮
            action_btn = QPushButton("查看详情")
            action_btn.clicked.connect(lambda checked, row=i: self.view_customer_details(row))
            self.table.setCellWidget(i, 7, action_btn)
        
        self.status_label.setText(f"共 {len(self.customers_data)} 条客户记录")
    
    def search_customers(self):
        """搜索客户"""
        company_text = self.company_search.text().strip().lower()
        industry_filter = self.industry_filter.currentText()
        status_filter = self.status_filter.currentText()
        
        # 这里应该调用API进行搜索，现在用模拟数据演示
        QMessageBox.information(self, "搜索", f"搜索条件：\n公司：{company_text}\n行业：{industry_filter}\n状态：{status_filter}")
    
    def reset_search(self):
        """重置搜索"""
        self.company_search.clear()
        self.industry_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.refresh_table()
    
    def add_customer(self):
        """新增客户"""
        dialog = CustomerDialog(parent=self)
        if dialog.exec() == QDialog.Accepted:
            customer_data = dialog.get_customer_data()
            if customer_data["company"]:
                # 这里应该调用API保存客户
                customer_data["id"] = len(self.customers_data) + 1
                self.customers_data.append(customer_data)
                self.refresh_table()
                QMessageBox.information(self, "成功", "客户添加成功！")
            else:
                QMessageBox.warning(self, "错误", "公司名称不能为空！")
    
    def edit_customer(self):
        """编辑客户"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            customer_data = self.customers_data[current_row]
            dialog = CustomerDialog(customer_data, parent=self)
            if dialog.exec() == QDialog.Accepted:
                updated_data = dialog.get_customer_data()
                updated_data["id"] = customer_data["id"]
                self.customers_data[current_row] = updated_data
                self.refresh_table()
                QMessageBox.information(self, "成功", "客户信息更新成功！")
        else:
            QMessageBox.warning(self, "提示", "请选择要编辑的客户！")
    
    def delete_customer(self):
        """删除客户"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            customer = self.customers_data[current_row]
            reply = QMessageBox.question(
                self, "确认删除", 
                f"确定要删除客户 '{customer['company']}' 吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.customers_data.pop(current_row)
                self.refresh_table()
                QMessageBox.information(self, "成功", "客户删除成功！")
        else:
            QMessageBox.warning(self, "提示", "请选择要删除的客户！")
    
    def view_customer_details(self, row):
        """查看客户详情"""
        customer = self.customers_data[row]
        details = f"""
客户详情：
公司名称：{customer['company']}
行业：{customer['industry']}
地址：{customer['province']} {customer['city']}
状态：{customer['status']}
联系人数量：{len(customer.get('contacts', []))}
        """
        QMessageBox.information(self, "客户详情", details.strip())
    
    def export_data(self):
        """导出数据"""
        QMessageBox.information(self, "导出", "数据导出功能开发中...")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QTableWidget {
            gridline-color: #d0d0d0;
            background-color: white;
        }
        QTableWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
    """)
    
    # 创建主窗口
    window = CustomerManagementWindow()
    window.show()
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
