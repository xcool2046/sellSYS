import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QLabel
)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("登录")
        self.setModal(True) # Make it a modal dialog

        # Widgets
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("登录")
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")

        # Layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("用户名:", self.username_input)
        form_layout.addRow("密  码:", self.password_input)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.error_label)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

        # Connections
        self.login_button.clicked.connect(self.accept) # `accept` will be handled by the caller

    def get_credentials(self):
        """Returns the entered username and password."""
        return self.username_input.text(), self.password_input.text()

    def set_error_message(self, message):
        """Displays an error message on the dialog."""
        self.error_label.setText(message)

if __name__ == '__main__':
    # For testing the dialog appearance
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    if dialog.exec():
        print("Login successful (simulated)")
        print(f"Credentials: {dialog.get_credentials()}")
    else:
        print("Login cancelled")
    sys.exit()