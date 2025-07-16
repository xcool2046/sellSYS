import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QFrame, QLabel
)
from PySide6.QtCore import Qt, QSize
from .customer_view import CustomerView
from .product_view import ProductView
from .order_view import OrderView
from .sales_follow_view import SalesFollowView
from .service_record_view import ServiceRecordView
from .finance_view import FinanceView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("巨伟科技客户管理信息系统")
        self.setGeometry(100, 100, 1200, 800)

        # --- Main Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- 1. Top Title Bar ---
        title_bar = QFrame()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(60)
        title_layout = QHBoxLayout(title_bar)
        title_label = QLabel("巨伟科技客户管理信息系统")
        title_label.setObjectName("titleLabel")
        title_layout.addWidget(title_label)
        main_layout.addWidget(title_bar)

        # --- 2. Main Content Area (Sidebar + Content) ---
        content_area_layout = QHBoxLayout()
        content_area_layout.setSpacing(0)
        
        # --- 2.1 Left Navigation Panel ---
        nav_panel = QFrame()
        nav_panel.setObjectName("navPanel")
        nav_panel.setFixedWidth(200)
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        nav_layout.setContentsMargins(0, 10, 0, 10)
        nav_layout.setSpacing(5)

        nav_buttons_text = [
            "数据视窗", "客户管理", "销售管理", "订单管理",
            "售后服务", "产品管理", "财务管理", "系统设置"
        ]
        
        self.nav_buttons = []
        for i, text in enumerate(nav_buttons_text):
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.setCheckable(True) # Make button checkable
            if i == 0: button.setChecked(True) # Set first button as default checked
            
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)

        content_area_layout.addWidget(nav_panel)
        
        # --- 2.2 Right Content Panel ---
        self.content_stack = QStackedWidget()
        content_area_layout.addWidget(self.content_stack)

        main_layout.addLayout(content_area_layout)

        # --- Add pages to the stack ---
        self.setup_pages()
        
        # Connect buttons
        for i, button in enumerate(self.nav_buttons):
            button.clicked.connect(lambda checked=False, index=i: self.on_nav_button_clicked(index))

    def on_nav_button_clicked(self, index):
        # Set the current page
        self.content_stack.setCurrentIndex(index)
        # Ensure only the clicked button is checked
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)

    def setup_pages(self):
        """Creates and adds pages to the QStackedWidget."""
        # Placeholder for "数据视窗"
        data_view = QWidget()
        data_view_layout = QVBoxLayout(data_view)
        data_view_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        data_view_label = QLabel("本期不做")
        data_view_label.setStyleSheet("font-size: 24px; color: #999;")
        data_view_layout.addWidget(data_view_label)
        
        self.content_stack.addWidget(data_view)             # Index 0
        self.content_stack.addWidget(CustomerView())         # Index 1
        self.content_stack.addWidget(SalesFollowView())      # Index 2
        self.content_stack.addWidget(OrderView())            # Index 3
        self.content_stack.addWidget(ServiceRecordView())    # Index 4
        self.content_stack.addWidget(ProductView())          # Index 5
        self.content_stack.addWidget(FinanceView())          # Index 6
        
        # Placeholder for "系统设置"
        settings_view = QWidget()
        settings_layout = QVBoxLayout(settings_view)
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_label = QLabel("系统设置 页面")
        settings_label.setStyleSheet("font-size: 24px; color: #999;")
        settings_layout.addWidget(settings_label)
        self.content_stack.addWidget(settings_view)          # Index 7

if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        with open("client/ui/styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: styles.qss not found.")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())