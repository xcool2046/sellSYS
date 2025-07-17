import sys
import os
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from .ui.main_window import MainWindow
from .ui.login import LoginDialog
from .api.auth import login
from .api.client import api_client # Import the global instance
from .config import API_BASE_URL  # Import configuration

def main():
    """Main function to initialize and run the application."""
    app = QApplication(sys.argv)

    try:
        # Load global stylesheet using an absolute path to be robust
        try:
            # Get the directory where this main.py script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the full path to the stylesheet
            stylesheet_path = os.path.join(script_dir, "ui", "styles.qss")
            with open(stylesheet_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
                print(f"Successfully loaded stylesheet from: {stylesheet_path}")
        except FileNotFoundError:
            # This is not a fatal error, just a warning
            print(f"Warning: styles.qss not found. The UI will not be fully styled.")

        # Configure the global API client instance using config
        api_client.base_url = API_BASE_URL

        # --- Development: Skip Login ---
        print("--- [开发模式] 跳过登录流程 ---")
        placeholder_token = "DEV_MODE_TOKEN_--_SKIP_LOGIN"
        api_client.set_token(placeholder_token)

        main_window = MainWindow()
        main_window.show()
        
        # Start the main event loop
        sys.exit(app.exec())

    except Exception as e:
        # Catch any unhandled exception
        print("CRITICAL ERROR: An unhandled exception occurred.")
        # Get the full traceback
        error_details = traceback.format_exc()
        print(error_details)
        
        # Display an error message box to the user
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText("发生了一个致命错误，应用即将关闭。")
        error_box.setInformativeText("详细的错误信息已经打印到控制台，请将此信息提供给开发人员进行问题排查。")
        error_box.setWindowTitle("应用崩溃")
        error_box.setDetailedText(str(error_details))
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec()
        
        # Exit with a non-zero code to indicate an error
        sys.exit(1)

if __name__ == "__main__":
    main()