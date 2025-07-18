"""
客户添加/编辑对话框 - 按照原型图设计
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QTextEdit, QDialogButtonBox, QMessageBox, QTabWidget,
    QWidget, QTableView, QPushButton, QHeaderView, QLabel, QCheckBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide6.QtCore import Qt
from typing import Dict, Any, List, Optional

from config_clean import INDUSTRY_CATEGORIES, CUSTOMER_STATUS, PROVINCE_CITY_DATA, COMPANY_SCALES
from models.base_model import Customer, Contact
from ..common_styles import (
    COMBOBOX_STYLE, LINEEDIT_STYLE, TEXTEDIT_STYLE,
    BUTTON_PRIMARY_STYLE, BUTTON_SECONDARY_STYLE, CHECKBOX_STYLE,
    DIALOG_TITLE_STYLE, DIALOG_CONTENT_STYLE
)

class CustomerDialog(QDialog):
    """客户添加/编辑对话框"""

    def __init__(self, customer_data: Optional[Dict[str, Any]] = None, parent=None):
        super().__init__(parent)
        self.customer_data = customer_data
        self.contacts_data = []

        self.setWindowTitle("添加客户" if not customer_data else "编辑客户")
        self.setFixedSize(500, 600)
        self.setModal(True)

        self.setup_ui()
        self.setup_connections()

        if customer_data:
            self.load_customer_data()

    def setup_ui(self):
        """设置用户界面"""
        # 设置对话框样式
        self.setStyleSheet(DIALOG_CONTENT_STYLE)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 标题栏
        title_label = QLabel("添加客户" if not self.customer_data else "编辑客户")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #4a90e2;
                padding: 15px 20px;
                margin: 0;
            }
        """)
        main_layout.addWidget(title_label)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # 表单布局
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # 行业类型
        self.industry_combo = QComboBox()
        self.industry_combo.addItem("请选择行业类型", None)  # 使用None而不是空字符串
        for industry in INDUSTRY_CATEGORIES:
            self.industry_combo.addItem(industry, industry)
        self.industry_combo.setStyleSheet(COMBOBOX_STYLE)
        form_layout.addRow("行业类型:", self.industry_combo)

        # 客户单位
        self.company_edit = QLineEdit()
        self.company_edit.setPlaceholderText("请输入客户单位名称")
        self.company_edit.setStyleSheet(LINEEDIT_STYLE)
        form_layout.addRow("客户单位:", self.company_edit)

        # 所在省份
        self.province_combo = QComboBox()
        self.province_combo.addItem("请选择省份", None)  # 使用None而不是空字符串
        for province in PROVINCE_CITY_DATA.keys():
            self.province_combo.addItem(province, province)
        self.province_combo.setStyleSheet(COMBOBOX_STYLE)
        form_layout.addRow("所在省份:", self.province_combo)

        # 城市名称
        self.city_combo = QComboBox()
        self.city_combo.addItem("请选择城市", None)  # 使用None而不是空字符串
        self.city_combo.setStyleSheet(COMBOBOX_STYLE)
        form_layout.addRow("城市名称:", self.city_combo)

        # 详细地址
        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("请输入详细地址")
        self.address_edit.setStyleSheet(LINEEDIT_STYLE)
        form_layout.addRow("详细地址:", self.address_edit)

        # 客户备注
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("请输入客户备注信息")
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setStyleSheet(TEXTEDIT_STYLE)
        form_layout.addRow("客户备注:", self.notes_edit)

        content_layout.addLayout(form_layout)

        # 联系人信息
        self.setup_contacts_section(content_layout)

        # 按钮区域
        self.setup_buttons(content_layout)

        main_layout.addWidget(content_widget)

    def setup_contacts_section(self, main_layout):
        """设置联系人信息区域"""
        # 联系人标题
        contacts_label = QLabel("联系人信息:")
        contacts_label.setStyleSheet("font-weight: bold; margin-top: 10px; color: #333333;")
        main_layout.addWidget(contacts_label)

        # 存储联系人行的列表
        self.contact_rows = []

        # 创建第一个联系人行
        self.add_contact_row()

        # 将联系人行添加到主布局
        for contact_widget in self.contact_rows:
            main_layout.addWidget(contact_widget)

    def add_contact_row(self):
        """添加一个联系人行"""
        contact_widget = QWidget()
        contact_layout = QHBoxLayout(contact_widget)
        contact_layout.setContentsMargins(0, 0, 0, 0)
        contact_layout.setSpacing(8)

        contact_layout.addWidget(QLabel("联系人:"))

        # 联系人姓名输入框
        name_edit = QLineEdit()
        name_edit.setFixedWidth(120)
        name_edit.setStyleSheet(LINEEDIT_STYLE)
        contact_layout.addWidget(name_edit)

        contact_layout.addWidget(QLabel("电话:"))

        # 联系人电话输入框
        phone_edit = QLineEdit()
        phone_edit.setFixedWidth(140)
        phone_edit.setStyleSheet(LINEEDIT_STYLE)
        contact_layout.addWidget(phone_edit)

        # 关键人复选框
        primary_checkbox = QCheckBox("关键人")
        primary_checkbox.setStyleSheet(CHECKBOX_STYLE)
        contact_layout.addWidget(primary_checkbox)

        # 添加按钮
        add_btn = QPushButton("+")
        add_btn.setFixedSize(24, 24)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        add_btn.clicked.connect(self.on_add_contact)
        contact_layout.addWidget(add_btn)

        # 删除按钮
        del_btn = QPushButton("-")
        del_btn.setFixedSize(24, 24)
        del_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        del_btn.clicked.connect(lambda: self.on_remove_contact(contact_widget))
        contact_layout.addWidget(del_btn)

        contact_layout.addStretch()

        # 存储控件引用
        contact_widget.name_edit = name_edit
        contact_widget.phone_edit = phone_edit
        contact_widget.primary_checkbox = primary_checkbox
        contact_widget.add_btn = add_btn
        contact_widget.del_btn = del_btn

        self.contact_rows.append(contact_widget)

        # 更新删除按钮状态
        self.update_delete_buttons()

        return contact_widget

    def on_add_contact(self):
        """添加联系人按钮点击事件"""
        new_contact = self.add_contact_row()

        # 将新联系人行添加到布局中
        # 找到联系人信息标题的位置
        main_layout = self.layout()
        contact_label_index = -1
        for i in range(main_layout.count()):
            item = main_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QLabel):
                if item.widget().text() == "联系人信息:":
                    contact_label_index = i
                    break

        if contact_label_index >= 0:
            # 在按钮区域之前插入新的联系人行
            insert_index = contact_label_index + len(self.contact_rows)
            main_layout.insertWidget(insert_index, new_contact)

    def on_remove_contact(self, contact_widget):
        """删除联系人按钮点击事件"""
        if len(self.contact_rows) > 1:  # 至少保留一个联系人
            self.contact_rows.remove(contact_widget)
            contact_widget.setParent(None)
            contact_widget.deleteLater()
            self.update_delete_buttons()

    def update_delete_buttons(self):
        """更新删除按钮的状态"""
        # 如果只有一个联系人，禁用删除按钮
        for contact_widget in self.contact_rows:
            contact_widget.del_btn.setEnabled(len(self.contact_rows) > 1)

    def setup_buttons(self, main_layout):
        """设置按钮区域"""
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.addStretch()

        # 取消按钮
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                min-width: 80px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        button_layout.addWidget(self.cancel_btn)

        # 保存按钮
        self.save_btn = QPushButton("保存")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                min-width: 80px;
                padding: 10px 20px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        button_layout.addWidget(self.save_btn)

        main_layout.addLayout(button_layout)

    def setup_connections(self):
        """设置信号连接"""
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.accept)
        self.province_combo.currentTextChanged.connect(self.on_province_changed)

    def on_province_changed(self, province: str):
        """省份变化事件"""
        self.city_combo.clear()
        self.city_combo.addItem("请选择城市", None)  # 使用None而不是空字符串

        if province and province in PROVINCE_CITY_DATA:
            for city in PROVINCE_CITY_DATA[province]:
                self.city_combo.addItem(city, city)

    def load_customer_data(self):
        """加载客户数据"""
        if not self.customer_data:
            return

        # 加载客户基本信息
        if self.customer_data.get('industry'):
            index = self.industry_combo.findData(self.customer_data['industry'])
            if index >= 0:
                self.industry_combo.setCurrentIndex(index)

        self.company_edit.setText(self.customer_data.get('company', ''))

        if self.customer_data.get('province'):
            index = self.province_combo.findData(self.customer_data['province'])
            if index >= 0:
                self.province_combo.setCurrentIndex(index)
                self.on_province_changed(self.customer_data['province'])

        if self.customer_data.get('city'):
            index = self.city_combo.findData(self.customer_data['city'])
            if index >= 0:
                self.city_combo.setCurrentIndex(index)

        self.address_edit.setText(self.customer_data.get('address', ''))
        self.notes_edit.setPlainText(self.customer_data.get('notes', ''))

        # 加载联系人信息
        contacts = self.customer_data.get('contacts', [])

        # 清除现有联系人行（除了第一个）
        while len(self.contact_rows) > 1:
            contact_widget = self.contact_rows.pop()
            contact_widget.setParent(None)
            contact_widget.deleteLater()

        # 确保至少有一个联系人行
        if len(self.contact_rows) == 0:
            self.add_contact_row()

        # 加载联系人数据
        for i, contact in enumerate(contacts):
            # 如果需要更多联系人行，添加它们
            while i >= len(self.contact_rows):
                self.on_add_contact()

            # 设置联系人数据
            if i < len(self.contact_rows):
                contact_widget = self.contact_rows[i]
                contact_widget.name_edit.setText(contact.get('name', ''))
                contact_widget.phone_edit.setText(contact.get('phone', ''))
                contact_widget.primary_checkbox.setChecked(contact.get('is_primary', False))

        # 更新删除按钮状态
        self.update_delete_buttons()

    def get_customer_data(self) -> Dict[str, Any]:
        """获取客户数据"""
        return {
            'industry': self.industry_combo.currentData() or '',
            'company': self.company_edit.text().strip(),
            'province': self.province_combo.currentData() or '',
            'city': self.city_combo.currentData() or '',
            'address': self.address_edit.text().strip(),
            'notes': self.notes_edit.toPlainText().strip(),
            'status': 'LEAD'  # 新客户默认状态为潜在客户
        }

    def get_contacts_data(self) -> List[Dict[str, Any]]:
        """获取联系人数据"""
        contacts = []

        # 遍历所有联系人行
        for contact_widget in self.contact_rows:
            name = contact_widget.name_edit.text().strip()
            if name:  # 只有填写了姓名的联系人才添加
                contacts.append({
                    'name': name,
                    'phone': contact_widget.phone_edit.text().strip(),
                    'is_primary': contact_widget.primary_checkbox.isChecked()
                })

        return contacts

    def validate(self) -> bool:
        """验证数据"""
        # 验证必填字段
        if not self.company_edit.text().strip():
            QMessageBox.warning(self, "验证失败", "请输入客户单位名称")
            self.company_edit.setFocus()
            return False

        # 检查行业类型是否已选择（不是默认的None值）
        if self.industry_combo.currentData() is None:
            QMessageBox.warning(self, "验证失败", "请选择行业类型")
            self.industry_combo.setFocus()
            return False

        # 验证至少有一个联系人
        has_any_contact = False
        for i, contact_widget in enumerate(self.contact_rows):
            name = contact_widget.name_edit.text().strip()
            phone = contact_widget.phone_edit.text().strip()

            if name:
                has_any_contact = True
                # 如果填写了联系人姓名，必须填写电话号码
                if not phone:
                    QMessageBox.warning(self, "验证失败", f"请输入联系人{i+1}的电话号码")
                    contact_widget.phone_edit.setFocus()
                    return False

        if not has_any_contact:
            QMessageBox.warning(self, "验证失败", "请至少添加一个联系人")
            if self.contact_rows:
                self.contact_rows[0].name_edit.setFocus()
            return False

        return True

    def accept(self):
        """确认按钮"""
        if self.validate():
            super().accept()

# 导出
__all__ = ['CustomerDialog']
