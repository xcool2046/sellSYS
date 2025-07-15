import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QStackedWidget, QFrame, QLabel
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from .customer_view import CustomerView
from .product_view import ProductView
from .order_view import OrderView
from .sales_follow_view import SalesFollowView
from .service_record_view import ServiceRecordView
from .finance_view import FinanceView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("巨蜂科技客户管理信息系统")
        self.setGeometry(100, 100, 1200, 800)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Left navigation panel
        nav_panel = QFrame()
        nav_panel.setFixedWidth(180)
        nav_panel.setStyleSheet("background-color: #f0f0f0;")
        main_layout.addWidget(nav_panel)

        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(10)

        # Navigation buttons based on the prototype
        nav_buttons_text = [
            "数据视窗", "客户管理", "销售管理", "订单管理",
            "售后服务", "产品管理", "财务管理", "系统设置"
        ]
        
        self.nav_buttons = []
        for text in nav_buttons_text:
            button = QPushButton(text)
            button.setFixedHeight(40)
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)

        # Right content panel
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        # Add pages to the stack
        self.content_stack.addWidget(QLabel("数据视窗 页面")) # Index 0
        self.content_stack.addWidget(CustomerView())         # Index 1
        self.content_stack.addWidget(SalesFollowView())      # Index 2
        self.content_stack.addWidget(OrderView())            # Index 3
        self.content_stack.addWidget(ServiceRecordView())    # Index 4
        self.content_stack.addWidget(ProductView())          # Index 5
        self.content_stack.addWidget(FinanceView())          # Index 6
        self.content_stack.addWidget(QLabel("系统设置 页面")) # Index 7

        # Connect buttons to switch pages
        for i, button in enumerate(self.nav_buttons):
            button.clicked.connect(lambda checked=False, index=i: self.content_stack.setCurrentIndex(index))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())