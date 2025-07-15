import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.login import LoginDialog
from api.auth import login
from api.client import ApiClient

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configure the API client to point to the deployed server
    # NOTE: This assumes the server is accessible. If deployment was paused,
    # this needs to be pointed to a local instance or the correct IP.
    api_client_instance = ApiClient(base_url="http://8.156.69.42:8000/api/v1")

    login_dialog = LoginDialog()
    
    # Loop until login is successful or dialog is cancelled
    while True:
        if login_dialog.exec():
            username, password = login_dialog.get_credentials()
            user_data = login(username, password)
            if user_data:
                # Login successful
                main_window = MainWindow()
                main_window.show()
                sys.exit(app.exec())
            else:
                # Login failed, show error and loop again
                login_dialog.set_error_message("登录失败，请检查用户名和密码。")
        else:
            # User cancelled the login dialog
            sys.exit(0)