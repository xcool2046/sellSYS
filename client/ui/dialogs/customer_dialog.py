"""
客户信息对话框
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QTextEdit, QDialogButtonBox, QMessageBox, QTabWidget,
    QWidget, QTableView, QPushButton, QHeaderView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from typing import Dict, Any, List, Optional

from config_clean import INDUSTRY_CATEGORIES, CUSTOMER_STATUS, PROVINCE_CITY_DATA, COMPANY_SCALES
from models.base_model import Customer, Contact

class CustomerDialog(QDialog):
    """客户信息对话框"""
    
    def __init__(self, customer_data: Optional[Dict[str, Any]] = None, parent=None):
        super().__init__(parent)
        self.customer_data = customer_data
        self.contacts_data = []
        
        self.setWindowTitle("客户信息" if customer_data else "添加客户")
        self.setMinimumSize(600, 500)
        
        self.setup_ui()
        self.setup_connections()
        
        if customer_data:
            self.load_customer_data()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 基本信息标签页
        self.setup_basic_info_tab()
        
        # 联系人标签页
        self.setup_contacts_tab()
        
        # 按钮区域
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
    
    def setup_basic_info_tab(self):
        """设置基本信息标签页"""
        basic_widget = QWidget()
        self.tab_widget.addTab(basic_widget, "基本信息")
        
        form_layout = QFormLayout(basic_widget)
        
        # 客户名称
        self.company_edit = QLineEdit()
        self.company_edit.setPlaceholderText("请输入客户公司名称")
        form_layout.addRow("客户名称 *:", self.company_edit)
        
        # 行业类别
        self.industry_combo = QComboBox()
        self.industry_combo.addItem("请选择行业", "")
        for industry in INDUSTRY_CATEGORIES:
            self.industry_combo.addItem(industry, industry)
        form_layout.addRow("行业类别 *:", self.industry_combo)
        
        # 省份
        self.province_combo = QComboBox()
        self.province_combo.addItem("请选择省份", "")
        for province in PROVINCE_CITY_DATA.keys():
            self.province_combo.addItem(province, province)
        form_layout.addRow("省份:", self.province_combo)
        
        # 城市
        self.city_combo = QComboBox()
        self.city_combo.addItem("请选择城市", "")
        form_layout.addRow("城市:", self.city_combo)
        
        # 详细地址
        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("请输入详细地址")
        form_layout.addRow("详细地址:", self.address_edit)
        
        # 公司网站
        self.website_edit = QLineEdit()
        self.website_edit.setPlaceholderText("请输入公司网站")
        form_layout.addRow("公司网站:", self.website_edit)
        
        # 公司规模
        self.scale_combo = QComboBox()
        self.scale_combo.addItem("请选择规模", "")
        for scale in COMPANY_SCALES:
            self.scale_combo.addItem(scale, scale)
        form_layout.addRow("公司规模:", self.scale_combo)
        
        # 客户状态
        self.status_combo = QComboBox()
        for status_key, status_name in CUSTOMER_STATUS.items():
            self.status_combo.addItem(status_name, status_key)
        form_layout.addRow("客户状态:", self.status_combo)
        
        # 备注
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setPlaceholderText("请输入备注信息")
        form_layout.addRow("备注:", self.notes_edit)
    
    def setup_contacts_tab(self):
        """设置联系人标签页"""
        contacts_widget = QWidget()
        self.tab_widget.addTab(contacts_widget, "联系人")
        
        layout = QVBoxLayout(contacts_widget)
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        self.add_contact_btn = QPushButton("添加联系人")
        self.add_contact_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        toolbar_layout.addWidget(self.add_contact_btn)
        
        self.edit_contact_btn = QPushButton("编辑联系人")
        self.edit_contact_btn.setEnabled(False)
        self.edit_contact_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        toolbar_layout.addWidget(self.edit_contact_btn)
        
        self.delete_contact_btn = QPushButton("删除联系人")
        self.delete_contact_btn.setEnabled(False)
        self.delete_contact_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        toolbar_layout.addWidget(self.delete_contact_btn)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        # 联系人表格
        self.contacts_table = QTableView()
        self.contacts_model = QStandardItemModel()
        self.contacts_table.setModel(self.contacts_model)
        
        # 设置表格属性
        self.contacts_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.contacts_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.contacts_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.contacts_table.setAlternatingRowColors(True)
        
        # 设置表头
        headers = ["姓名", "职位", "电话", "邮箱", "是否主要联系人"]
        self.contacts_model.setHorizontalHeaderLabels(headers)
        
        layout.addWidget(self.contacts_table)
    
    def setup_connections(self):
        """设置信号连接"""
        # 省份变化时更新城市
        self.province_combo.currentTextChanged.connect(self.on_province_changed)
        
        # 联系人操作
        self.add_contact_btn.clicked.connect(self.on_add_contact)
        self.edit_contact_btn.clicked.connect(self.on_edit_contact)
        self.delete_contact_btn.clicked.connect(self.on_delete_contact)
        
        # 联系人表格选择变化
        self.contacts_table.selectionModel().selectionChanged.connect(self.on_contact_selection_changed)
        self.contacts_table.doubleClicked.connect(self.on_edit_contact)
    
    def on_province_changed(self, province: str):
        """省份变化事件"""
        self.city_combo.clear()
        self.city_combo.addItem("请选择城市", "")
        
        if province in PROVINCE_CITY_DATA:
            for city in PROVINCE_CITY_DATA[province]:
                self.city_combo.addItem(city, city)
    
    def on_add_contact(self):
        """添加联系人"""
        dialog = ContactDialog(parent=self)
        if dialog.exec():
            contact_data = dialog.get_contact_data()
            self.contacts_data.append(contact_data)
            self.update_contacts_table()
    
    def on_edit_contact(self):
        """编辑联系人"""
        selected_rows = self.get_selected_contact_rows()
        if not selected_rows:
            return
        
        row = selected_rows[0]
        if row < len(self.contacts_data):
            contact_data = self.contacts_data[row]
            dialog = ContactDialog(contact_data, parent=self)
            if dialog.exec():
                updated_data = dialog.get_contact_data()
                self.contacts_data[row] = updated_data
                self.update_contacts_table()
    
    def on_delete_contact(self):
        """删除联系人"""
        selected_rows = self.get_selected_contact_rows()
        if not selected_rows:
            return
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除选中的 {len(selected_rows)} 个联系人吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 从后往前删除，避免索引问题
            for row in sorted(selected_rows, reverse=True):
                if row < len(self.contacts_data):
                    del self.contacts_data[row]
            
            self.update_contacts_table()
    
    def on_contact_selection_changed(self):
        """联系人选择变化"""
        selected_rows = self.get_selected_contact_rows()
        has_selection = len(selected_rows) > 0
        
        self.edit_contact_btn.setEnabled(len(selected_rows) == 1)
        self.delete_contact_btn.setEnabled(has_selection)
    
    def get_selected_contact_rows(self) -> List[int]:
        """获取选中的联系人行"""
        selection = self.contacts_table.selectionModel().selectedRows()
        return [index.row() for index in selection]
    
    def update_contacts_table(self):
        """更新联系人表格"""
        self.contacts_model.clear()
        headers = ["姓名", "职位", "电话", "邮箱", "是否主要联系人"]
        self.contacts_model.setHorizontalHeaderLabels(headers)
        
        for contact in self.contacts_data:
            items = [
                QStandardItem(contact.get('name', '')),
                QStandardItem(contact.get('position', '')),
                QStandardItem(contact.get('phone', '')),
                QStandardItem(contact.get('email', '')),
                QStandardItem('是' if contact.get('is_primary', False) else '否')
            ]
            
            for item in items:
                item.setEditable(False)
            
            self.contacts_model.appendRow(items)
    
    def load_customer_data(self):
        """加载客户数据"""
        if not self.customer_data:
            return
        
        # 加载基本信息
        self.company_edit.setText(self.customer_data.get('company', ''))
        
        # 设置行业
        industry = self.customer_data.get('industry', '')
        index = self.industry_combo.findData(industry)
        if index >= 0:
            self.industry_combo.setCurrentIndex(index)
        
        # 设置省份
        province = self.customer_data.get('province', '')
        index = self.province_combo.findData(province)
        if index >= 0:
            self.province_combo.setCurrentIndex(index)
            self.on_province_changed(province)
        
        # 设置城市
        city = self.customer_data.get('city', '')
        index = self.city_combo.findData(city)
        if index >= 0:
            self.city_combo.setCurrentIndex(index)
        
        self.address_edit.setText(self.customer_data.get('address', ''))
        self.website_edit.setText(self.customer_data.get('website', ''))
        
        # 设置规模
        scale = self.customer_data.get('scale', '')
        index = self.scale_combo.findData(scale)
        if index >= 0:
            self.scale_combo.setCurrentIndex(index)
        
        # 设置状态
        status = self.customer_data.get('status', 'LEAD')
        index = self.status_combo.findData(status)
        if index >= 0:
            self.status_combo.setCurrentIndex(index)
        
        self.notes_edit.setPlainText(self.customer_data.get('notes', ''))
        
        # 加载联系人数据（如果有）
        if 'contacts' in self.customer_data:
            self.contacts_data = self.customer_data['contacts']
            self.update_contacts_table()
    
    def get_customer_data(self) -> Dict[str, Any]:
        """获取客户数据"""
        return {
            'company': self.company_edit.text().strip(),
            'industry': self.industry_combo.currentData() or '',
            'province': self.province_combo.currentData() or '',
            'city': self.city_combo.currentData() or '',
            'address': self.address_edit.text().strip(),
            'website': self.website_edit.text().strip(),
            'scale': self.scale_combo.currentData() or '',
            'status': self.status_combo.currentData(),
            'notes': self.notes_edit.toPlainText().strip()
        }
    
    def get_contacts_data(self) -> List[Dict[str, Any]]:
        """获取联系人数据"""
        return self.contacts_data.copy()
    
    def validate(self) -> bool:
        """验证数据"""
        # 验证必填字段
        if not self.company_edit.text().strip():
            QMessageBox.warning(self, "验证失败", "请输入客户名称")
            self.company_edit.setFocus()
            return False
        
        if not self.industry_combo.currentData():
            QMessageBox.warning(self, "验证失败", "请选择行业类别")
            self.industry_combo.setFocus()
            return False
        
        return True
    
    def accept(self):
        """确认按钮"""
        if self.validate():
            super().accept()

class ContactDialog(QDialog):
    """联系人对话框"""
    
    def __init__(self, contact_data: Optional[Dict[str, Any]] = None, parent=None):
        super().__init__(parent)
        self.contact_data = contact_data
        
        self.setWindowTitle("联系人信息" if contact_data else "添加联系人")
        self.setMinimumWidth(400)
        
        self.setup_ui()
        
        if contact_data:
            self.load_contact_data()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 表单
        form_layout = QFormLayout()
        
        # 姓名
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("请输入联系人姓名")
        form_layout.addRow("姓名 *:", self.name_edit)
        
        # 职位
        self.position_edit = QLineEdit()
        self.position_edit.setPlaceholderText("请输入职位")
        form_layout.addRow("职位:", self.position_edit)
        
        # 电话
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("请输入电话号码")
        form_layout.addRow("电话:", self.phone_edit)
        
        # 邮箱
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("请输入邮箱地址")
        form_layout.addRow("邮箱:", self.email_edit)
        
        # 是否主要联系人
        self.is_primary_combo = QComboBox()
        self.is_primary_combo.addItem("否", False)
        self.is_primary_combo.addItem("是", True)
        form_layout.addRow("主要联系人:", self.is_primary_combo)
        
        layout.addLayout(form_layout)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_contact_data(self):
        """加载联系人数据"""
        if not self.contact_data:
            return
        
        self.name_edit.setText(self.contact_data.get('name', ''))
        self.position_edit.setText(self.contact_data.get('position', ''))
        self.phone_edit.setText(self.contact_data.get('phone', ''))
        self.email_edit.setText(self.contact_data.get('email', ''))
        
        is_primary = self.contact_data.get('is_primary', False)
        index = self.is_primary_combo.findData(is_primary)
        if index >= 0:
            self.is_primary_combo.setCurrentIndex(index)
    
    def get_contact_data(self) -> Dict[str, Any]:
        """获取联系人数据"""
        return {
            'name': self.name_edit.text().strip(),
            'position': self.position_edit.text().strip(),
            'phone': self.phone_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'is_primary': self.is_primary_combo.currentData()
        }
    
    def validate(self) -> bool:
        """验证数据"""
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "验证失败", "请输入联系人姓名")
            self.name_edit.setFocus()
            return False
        
        # 电话和邮箱至少填写一个
        if not self.phone_edit.text().strip() and not self.email_edit.text().strip():
            QMessageBox.warning(self, "验证失败", "电话和邮箱至少填写一个")
            self.phone_edit.setFocus()
            return False
        
        return True
    
    def accept(self):
        """确认按钮"""
        if self.validate():
            super().accept()

# 导出
__all__ = ['CustomerDialog', 'ContactDialog']
