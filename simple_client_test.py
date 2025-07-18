#!/usr/bin/env python3
"""
简化的客户端测试脚本
用于测试和完善客户端功能，绕过语法错误
"""
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QMessageBox

class SimpleMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("巨炜科技客户管理系统 - 简化版")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("巨炜科技客户管理系统")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)
        
        # 添加功能按钮
        self.create_buttons(layout)
        
    def create_buttons(self, layout):
        """创建功能按钮"""
        buttons = [
            ("客户管理", self.open_customer_management),
            ("销售跟进", self.open_sales_follow),
            ("订单管理", self.open_order_management),
            ("产品管理", self.open_product_management),
            ("报表统计", self.open_reports),
            ("系统设置", self.open_settings)
        ]
        
        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    padding: 10px;
                    margin: 5px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
    
    def open_customer_management(self):
        """打开客户管理"""
        QMessageBox.information(self, "功能开发中", "客户管理功能正在完善中...")
        
    def open_sales_follow(self):
        """打开销售跟进"""
        QMessageBox.information(self, "功能开发中", "销售跟进功能正在完善中...")
        
    def open_order_management(self):
        """打开订单管理"""
        QMessageBox.information(self, "功能开发中", "订单管理功能正在完善中...")
        
    def open_product_management(self):
        """打开产品管理"""
        QMessageBox.information(self, "功能开发中", "产品管理功能正在完善中...")
        
    def open_reports(self):
        """打开报表统计"""
        QMessageBox.information(self, "功能开发中", "报表统计功能正在完善中...")
        
    def open_settings(self):
        """打开系统设置"""
        QMessageBox.information(self, "功能开发中", "系统设置功能正在完善中...")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0;
        }
        QLabel {
            color: #333;
        }
    """)
    
    # 创建主窗口
    window = SimpleMainWindow()
    window.show()
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
