import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QWidget, QSpacerItem, QSizePolicy, QFormLayout
)
from PySide6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("系统登录")
        self.setObjectName("LoginWindow")
        self.setMinimumSize(800, 600)

        # Main layout to center the login form
        main_layout = QHBoxLayout(self)
        main_layout.addStretch()

        # --- Login Form Container ---
        form_container = QWidget()
        form_container.setObjectName("loginFormContainer")
        container_layout = QVBoxLayout(form_container)
        container_layout.setContentsMargins(40, 0, 40, 40)
        container_layout.setSpacing(20)

        # --- Image Placeholder ---
        image_placeholder = QLabel()
        image_placeholder.setObjectName("imagePlaceholder")
        # In a real app, you might set a pixmap here:
        # from PySide6.QtGui import QPixmap
        # image_placeholder.setPixmap(QPixmap("path/to/image.png"))
        container_layout.addWidget(image_placeholder)

        # --- Form Fields ---
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入登录账号")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; padding-left: 5px;")

        # --- Form Layout for labels and inputs ---
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 20, 0, 0)
        form_layout.setSpacing(15)
        form_layout.addRow("登录账号:", self.username_input)
        form_layout.addRow("输入密码:", self.password_input)
        
        container_layout.addLayout(form_layout)
        container_layout.addWidget(self.error_label)

        # Spacer
        container_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # --- Buttons ---
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("取消")
        self.login_button = QPushButton("登录")
        self.login_button.setObjectName("primaryButton")
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.login_button)
        container_layout.addLayout(button_layout)
        
        main_layout.addWidget(form_container)
        main_layout.addStretch()

        # --- Connections ---
        self.login_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_credentials(self):
        """Returns the entered username and password."""
        return self.username_input.text(), self.password_input.text()

    def set_error_message(self, message):
        """Displays an error message on the dialog."""
        self.error_label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Load stylesheet for testing
    try:
        with open("styles.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: styles.qss not found. The UI will not be styled.")

    dialog = LoginDialog()
    if dialog.exec():
        print("Login successful (simulated)")
        print(f"Credentials: {dialog.get_credentials()}")
    else:
        print("Login cancelled")
    sys.exit()