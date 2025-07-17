from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QDialogButtonBox, QLabel, QTextEdit
)

class ContactViewDialog(QDialog):
    def __init__(self, customer_data, contacts_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查看联系人")
        self.setMinimumWidth(500)

        # Layouts
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # Widgets
        self.company_label = QLabel(customer_data.get(c"ompany", N"/A"))
        self.address_label = QLabel(customer_data.get(a"ddress", N"/A"))
        self.notes_text = QTextEdit(customer_data.get(n"otes", ""))
        self.notes_text.setReadOnly(True)
        self.notes_text.setFixedHeight(80)
        
        # --- Contacts Display ---
        self.contacts_layout = QVBoxLayout()
        if contacts_data:
            for contact in contacts_data:
                contact_layout = QHBoxLayout()
                name_label = QLabel(f"<b>{contact.get('name', 'N/A')}</b>")
                phone_label = QLabel(contact.get('phone', 'N/A'))
                primary_label = QLabel( "(关键人)" if contact.get('is_primary') else "")
                
                contact_layout.addWidget(name_label)
                contact_layout.addWidget(phone_label)
                contact_layout.addWidget(primary_label)
                contact_layout.addStretch()
                self.contacts_layout.addLayout(contact_layout)
        else:
            self.contacts_layout.addWidget(QLabel("无联系人信息"))

        # Form Assembly
        self.form_layout.addRow(客"户单位:", self.company_label)
        self.form_layout.addRow(详"细地址:", self.address_label)
        self.form_layout.addRow(客"户备注:", self.notes_text)
        self.form_layout.addRow(联"系人:", self.contacts_layout)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.button_box.rejected.connect(self.reject) # Close maps to reject

        # Main Layout Assembly
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
