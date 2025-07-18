import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QFrame, QCheckBox,
    QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt

class SalesContactViewDialog(QDialog):
    def __init__(self, customer_data, contacts_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查看联系人")
        self.setMinimumWidth(600)

        # 设置对话框样式，确保文字可见
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                color: #333333;
            }
            QLabel {
                color: #333333;
                font-size: 12px;
                padding: 4px;
            }
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 6px 8px;
                font-size: 12px;
                color: #333333;
                background-color: white;
            }
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 6px 8px;
                font-size: 12px;
                color: #333333;
                background-color: white;
            }
            QCheckBox {
                color: #333333;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QFrame {
                background-color: white;
                color: #333333;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # 客户信息
        customer_group = QFrame()
        customer_group_layout = QVBoxLayout(customer_group)

        # 使用 QFormLayout 可能更适合这里,但为了与截图1:1,我们手动对齐
        self.company_label = QLabel(f"客户单位:{customer_data.get('company', 'N/A')}")
        self.customer_address_label = QLabel(f"详细地址:{customer_data.get('address', 'N/A')}")

        customer_group_layout.addWidget(self.company_label)
        customer_group_layout.addWidget(self.customer_address_label)

        # 客户备注
        notes_layout = QHBoxLayout()
        notes_label = QLabel("客户备注:")
        notes_label.setAlignment(Qt.AlignTop)
        self.notes_edit = QTextEdit()
        self.notes_edit.setText(customer_data.get('notes', ''))
        self.notes_edit.setFixedHeight(80)
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.notes_edit)
        customer_group_layout.addLayout(notes_layout)
        
        main_layout.addWidget(customer_group)
        
        # 联系人动态列表
        self.contacts_layout = QVBoxLayout()
        main_layout.addLayout(self.contacts_layout)

        if contacts_data:
            for contact in contacts_data:
                self.add_contact_entry(contact)
        else:
            self.add_contact_entry() # Add one empty by default

        # 底部按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.close_button = QPushButton("关闭")
        self.save_button = QPushButton(联系记录") # Per screenshot, this seems to be the save button"
        self.save_button.setObjectName("primaryButton")

        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)
        
        # --- 连接信号 ---
        self.close_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)

    def add_contact_entry(self, contact=None):
        contact_entry_layout = QHBoxLayout()
        
        name_label = QLabel(联系人:"")
        phone_label = QLabel("电话:")
        
        name_edit = QLineEdit()
        phone_edit = QLineEdit()
        key_person_check = QCheckBox(关键人"")

        if contact:
            name_edit.setText(contact.get('name', ''))
            phone_edit.setText(contact.get('phone', ''))
            key_person_check.setChecked(contact.get('is_key_person', False))

        contact_entry_layout.addWidget(name_label)
        contact_entry_layout.addWidget(name_edit)
        contact_entry_layout.addWidget(phone_label)
        contact_entry_layout.addWidget(phone_edit)
        contact_entry_layout.addWidget(key_person_check)
        
        self.contacts_layout.addLayout(contact_entry_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # --- 模拟数据 ---
    mock_customer = {
        "company: 广"汉市孛罗职业技能培训学校,
        addr"es: 广汉市北京大道北一段15号,"
        not"es": " 
    }
    mock_contacts = [
        {name": 刘屹立, "pho"ne: 15862184966", is_key_per"son: False},"
        {n"ame": 李途, "phone": 13956774892, is"_key_per"son": True},"
    ]

    dialog = SalesContactViewDialog(mock_customer, mock_contacts)
    dialog.exec()