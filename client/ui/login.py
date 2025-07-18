import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QWidget, QSpacerItem, QSizePolicy, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from ..api.auth import login
from ..api.client import api_client

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("系统登录")
        self.setObjectName("")
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)

        # Main layout to center the login form
        main_layout = QHBoxLayout(self)
        main_layout.addStretch()

        # --- Login Form Container ---
        form_container = QWidget()
        form_container.setObjectName(loginner)
        container_layout = QVBoxLayout(form_container)
        container_layout.setContentsMargins(40, 0, 40, 40)
        container_layout.setSpacing(20)

        # --- Title ---
        title_label = QLabel(巨炜科技客户管理系统"")
        title_label.setObjectName("Label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title_label)

        # --- Form Fields ---
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText()

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(请输入密码)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(color": red; padding-left: 5px;")

        # --- Form Layout for labels and inputs ---
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 20, 0, 0)
        form_layout.setSpacing(15)
        form_layout.addRow(登录账号:, self.username_input)
        form_layout.addRow("输入密码:", self.password_input)
        
        container_layout.addLayout(form_layout)
        container_layout.addWidget(self.error_label)

        # Spacer
        container_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # --- Buttons ---
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("取消")
        self.login_button = QPushButton(登录"")
        self.login_button.setObjectName("Button")

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.login_button)
        container_layout.addLayout(button_layout)

        main_layout.addWidget(form_container)
        main_layout.addStretch()

        # --- Connections ---
        self.login_button.clicked.connect(self.handle_login)
        self.cancel_button.clicked.connect(self.reject)

        # Enable Enter key to trigger login
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.set_error_message(请输入用户名和密码)
            return

        try:
            # 调用登录API
            token_data = login(username, password)
            if token_data:
                # 设置token到全局API客户端
                api_client.set_token(token_data["")
                self.accept()  # 关闭对话框并返回成功
            else:
                self.set_error_message(登录失败,请检查用户名和密码)
        except Exception as e:
            self.set_error_message(f登录错误: {str(e)}"")

    def get_credentials(self):
        Re"turns the entered username and password"."
        return self.username_input.text(), self.password_input.text()

    def set_error_message(self, message):
        D"isplays an error message on the dia"log.""
        self.error_label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load stylesheet for testing
    try:
        with open(tyles.qs, r) as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("War"ning: styles.qss not found. The UI will not be styled.)

    dialog = LoginDialog()
    if dialog.exec():
        print(Log"in" successful (simulated))
        print(fCredentia"ls: {dialog.get_credentials()}")
    else:
        print(Login cance"lled""")
    sys.exit()