import sys
from PySide6.QtWidgets import QApplication
from .ui.main_window import MainWindow
from .ui.login import LoginDialog
from .api.auth import login
from .api.client import api_client # Import the global instance
from .config import API_BASE_URL  # Import configuration

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load global stylesheet
    try:
        with open("client/ui/styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: styles.qss not found. The UI will not be fully styled.")

    # Configure the global API client instance using config
    api_client.base_url = API_BASE_URL

    login_dialog = LoginDialog()
    
    # Loop to allow login retries
    while True:
        # Show the dialog. If the user cancels, exec() returns False.
        if login_dialog.exec():
            username, password = login_dialog.get_credentials()
            login_result = login(username, password)

            if login_result and login_result.get("access_token"):
                # Login successful, break the loop to proceed
                break
            else:
                # Login failed, prepare and show error message
                error_detail = "登录失败，发生未知错误。"
                if login_result and "detail" in login_result:
                    error_detail = login_result["detail"]
                
                if isinstance(error_detail, str):
                    if "incorrect" in error_detail.lower():
                        error_detail = "用户名或密码不正确。"
                    elif "not found" in error_detail.lower():
                        error_detail = "用户不存在。"
                
                login_dialog.set_error_message(error_detail)
        else:
            # User cancelled the login dialog, exit application
            sys.exit(0)

    # If the loop is broken, login was successful.
    # Set the token and show the main window.
    token = login_result["access_token"]
    api_client.set_token(token)
    
    main_window = MainWindow()
    main_window.show()
    
    # Start the main event loop
    sys.exit(app.exec())