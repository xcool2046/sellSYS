import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QFrame, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, QSize

from .customer_view import CustomerView
from .products_view import ProductsView
from .order_view import OrderView
from .sales_follow_view import SalesFollowView
from .service_record_view import ServiceRecordView
from .finance_view import FinanceView
from .settings_view import SettingsView
from .sales_management_view import SalesManagementView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("巨炜科技客户管理信息系统")
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置窗口可调整大小
        self.setMinimumSize(800, 600)  # 设置最小尺寸
        self.setMaximumSize(1920, 1080)  # 设置最大尺寸
        
        # 设置窗口属性，允许拖拽边框调整大小
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | 
                           Qt.WindowType.WindowSystemMenuHint | Qt.WindowType.WindowMinMaxButtonsHint |
                           Qt.WindowType.WindowCloseButtonHint)

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
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        
        # 标题
        title_label = QLabel("巨炜科技客户管理信息系统")
        title_label.setObjectName("titleLabel")
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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

        self.nav_buttons = {}

        # --- 导航按钮 ---
        self._create_nav_button("数据视窗", 0, nav_layout)
        self._create_nav_button("客户管理", 1, nav_layout)
        self._create_nav_button("销售管理", 2, nav_layout)
        self._create_nav_button("订单管理", 3, nav_layout)
        self._create_nav_button("售后服务", 4, nav_layout)
        self._create_nav_button("产品管理", 5, nav_layout)
        self._create_nav_button("财务管理", 6, nav_layout)
        self._create_nav_button("系统设置", 7, nav_layout)
        
        nav_layout.addStretch() # Pushes everything to the top
        content_area_layout.addWidget(nav_panel)
        
        # --- 2.2 Right Content Panel ---
        self.content_stack = QStackedWidget()
        content_area_layout.addWidget(self.content_stack)

        main_layout.addLayout(content_area_layout)

        # --- Add pages to the stack ---
        self.setup_pages()
        
        # Set default page to customer management (index 1)
        self.content_stack.setCurrentIndex(1)
        
        # Connect buttons
    def _create_nav_button(self, text, index, layout):
        button = QPushButton(text)
        button.setObjectName("navButton")
        button.setCheckable(True)
        button.clicked.connect(lambda: self.on_nav_button_clicked(index))
        layout.addWidget(button)
        self.nav_buttons[index] = button
        # Set customer management as default checked (index 1)
        if index == 1:  # 客户管理
            button.setChecked(True)

    def on_nav_button_clicked(self, index):
        # Set the current page
        self.content_stack.setCurrentIndex(index)

        # Uncheck all other main buttons
        for i, button in self.nav_buttons.items():
            if i != index:
                button.setChecked(False)
        self.nav_buttons[index].setChecked(True)

    def setup_pages(self):
        """Creates and adds pages to the QStackedWidget."""
        # Placeholder for 数"据视窗"
        data_view = QWidget()
        data_view_layout = QVBoxLayout(data_view)
        data_view_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.content_stack.addWidget(data_view)             # Index 0
        self.content_stack.addWidget(CustomerView())         # Index 1
        self.content_stack.addWidget(SalesManagementView())  # Index 2 (was SalesFollowView)
        self.content_stack.addWidget(OrderView())            # Index 3
        self.content_stack.addWidget(ServiceRecordView())    # Index 4
        self.content_stack.addWidget(ProductsView())          # Index 5
        self.content_stack.addWidget(FinanceView())          # Index 6
        
        # 系"统设置" Page
        self.content_stack.addWidget(SettingsView())          # Index 7
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Note: Styles are loaded in the main entry point (client/main.py)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())