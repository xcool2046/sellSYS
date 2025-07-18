from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QDialogButtonBox, QLabel, QTextEdit
)

class ContactViewDialog(QDialog):
    def __init__(self, customer_data, contacts_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查看联系人")
        self.setMinimumWidth(500)

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
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 6px 8px;
                font-size: 12px;
                color: #333333;
                background-color: #f8f9fa;
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
        """)

        # Layouts
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # Widgets
        self.company_label = QLabel(customer_data.get("company", "N/A"))
        self.address_label = QLabel(customer_data.get("address", "N/A"))
        self.notes_text = QTextEdit(customer_data.get("notes", ""))
        self.notes_text.setReadOnly(True)
        self.notes_text.setFixedHeight(80)
        
        # --- Contacts Display ---
        self.contacts_layout = QVBoxLayout()
        if contacts_data:
            for contact in contacts_data:
                contact_layout = QHBoxLayout()
                name_label = QLabel(f"<b>{contact.get('name', 'N/A')}</b>")
                phone_label = QLabel(contact.get('phone', 'N/A'))
                primary_label = QLabel("(关键人)" if contact.get('is_primary') else "")

                contact_layout.addWidget(name_label)
                contact_layout.addWidget(phone_label)
                contact_layout.addWidget(primary_label)
                contact_layout.addStretch()
                self.contacts_layout.addLayout(contact_layout)
        else:
            self.contacts_layout.addWidget(QLabel("无联系人信息"))

        # Form Assembly
        self.form_layout.addRow("客户单位:", self.company_label)
        self.form_layout.addRow("详细地址:", self.address_label)
        self.form_layout.addRow("客户备注:", self.notes_text)
        self.form_layout.addRow("联系人:", self.contacts_layout)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.button_box.rejected.connect(self.reject) # Close maps to reject

        # Main Layout Assembly
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
