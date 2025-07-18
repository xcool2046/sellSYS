"""
主窗口 - 干净版本
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QStackedWidget, QLabel, QSizePolicy, QButtonGroup
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("巨炜科技客户管理信息系统")
        self.setMinimumSize(1200, 800)

        # 设置主窗口样式，去除边框
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
                border: none;
            }
        """)

        # 创建中央部件
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: none;
            }
        """)
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建顶部标题栏
        self.create_title_bar()
        main_layout.addWidget(self.title_bar)

        # 创建内容区域（左侧导航 + 右侧内容）
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 创建左侧导航栏
        self.create_navigation()
        content_layout.addWidget(self.nav_widget)

        # 创建右侧内容区域
        self.create_content_area()
        content_layout.addWidget(self.content_widget)

        # 设置布局比例
        content_layout.setStretch(0, 0)  # 导航栏固定宽度
        content_layout.setStretch(1, 1)  # 内容区域自适应

        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)

        print("✅ 主窗口初始化完成")

    def create_title_bar(self):
        """创建顶部标题栏"""
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(50)
        self.title_bar.setStyleSheet("""
            QWidget {
                background-color: #4a90e2;
                color: white;
            }
        """)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(20, 0, 20, 0)

        # 系统标题
        title_label = QLabel("巨炜科技客户管理信息系统")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: white;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

    def create_navigation(self):
        """创建导航栏"""
        self.nav_widget = QWidget()
        self.nav_widget.setFixedWidth(200)
        self.nav_widget.setStyleSheet("""
            QWidget {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QPushButton {
                background-color: transparent;
                color: #1976d2;
                border: none;
                padding: 10px 8px;
                text-align: center;
                font-size: 13px;
                font-weight: bold;
                min-height: 35px;
                max-height: 35px;
                margin: 2px 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #bbdefb;
            }
            QPushButton:checked {
                background-color: #2196f3;
                color: white;
            }
        """)
        
        nav_layout = QVBoxLayout(self.nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        
        # 删除标题区域，直接开始导航菜单
        
        # 导航按钮
        self.nav_buttons = []
        self.button_group = QButtonGroup()
        
        nav_items = [
            ("数据视窗", 0),
            ("客户管理", 1),
            ("销售管理", 2),
            ("订单管理", 3),
            ("售后服务", 4),
            ("产品管理", 5),
            ("财务管理", 6),
            ("系统设置", 7),
        ]
        
        for text, index in nav_items:
            button = QPushButton(text)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, idx=index: self.switch_page(idx))
            
            self.nav_buttons.append(button)
            self.button_group.addButton(button, index)
            nav_layout.addWidget(button)
        
        # 设置默认选中第一个按钮
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
        
        nav_layout.addStretch()
    
    def create_content_area(self):
        """创建内容区域"""
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: none;
            }
        """)
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 创建堆叠窗口
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: white;
                border: none;
            }
        """)
        content_layout.addWidget(self.content_stack)

        # 添加页面
        self.setup_pages()
    
    def setup_pages(self):
        """设置页面"""
        # 数据视窗页面
        data_page = self.create_placeholder_page("数据视窗", "这里将显示系统数据概览")
        self.content_stack.addWidget(data_page)
        
        # 客户管理页面
        try:
            from .customer_management_view import CustomerManagementView
            customer_page = CustomerManagementView()
            self.content_stack.addWidget(customer_page)
        except ImportError as e:
            print(f"导入客户管理视图失败: {e}")
            customer_page = self.create_placeholder_page("客户管理", "客户管理功能加载失败，请检查相关模块")
            self.content_stack.addWidget(customer_page)
        
        # 销售管理页面
        try:
            from .sales_management_view_new import SalesManagementView
            sales_page = SalesManagementView()
            self.content_stack.addWidget(sales_page)
        except ImportError as e:
            print(f"导入销售管理视图失败: {e}")
            sales_page = self.create_placeholder_page("销售管理", "销售管理功能加载失败，请检查相关模块")
            self.content_stack.addWidget(sales_page)

        # 订单管理页面
        try:
            from .order_management_view import OrderManagementView
            order_page = OrderManagementView()
            self.content_stack.addWidget(order_page)
        except ImportError as e:
            print(f"导入订单管理视图失败: {e}")
            order_page = self.create_placeholder_page("订单管理", "订单管理功能加载失败，请检查相关模块")
            self.content_stack.addWidget(order_page)

        # 其他页面（占位符）
        pages = [
            ("售后服务", "售后服务功能正在开发中..."),
            ("产品管理", "产品管理功能正在开发中..."),
            ("财务管理", "财务管理功能正在开发中..."),
            ("系统设置", "系统设置功能正在开发中..."),
        ]

        for title, description in pages:
            page = self.create_placeholder_page(title, description)
            self.content_stack.addWidget(page)
    
    def create_placeholder_page(self, title, description):
        """创建占位符页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Microsoft YaHei", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Microsoft YaHei", 14))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #7f8c8d;")
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
        return page
    
    def switch_page(self, index):
        """切换页面"""
        if 0 <= index < self.content_stack.count():
            self.content_stack.setCurrentIndex(index)
            print(f"✅ 切换到页面: {index}")
        else:
            print(f"⚠️ 无效的页面索引: {index}")
