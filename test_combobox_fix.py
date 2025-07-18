#!/usr/bin/env python3
"""
测试下拉框文字显示修复
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

class ComboBoxTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("下拉框文字显示测试")
        self.setGeometry(100, 100, 500, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("下拉框文字显示修复验证")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px; color: #333;")
        layout.addWidget(title_label)
        
        # 说明文字
        desc_label = QLabel("点击按钮测试各个对话框中的下拉框文字是否清晰可见")
        desc_label.setStyleSheet("font-size: 12px; color: #666; margin: 10px;")
        layout.addWidget(desc_label)
        
        # 添加测试按钮
        self.create_test_buttons(layout)
    
    def create_test_buttons(self, layout):
        """创建测试按钮"""
        # 测试客户对话框下拉框
        customer_btn = QPushButton("🔍 测试客户对话框下拉框")
        customer_btn.clicked.connect(self.test_customer_combobox)
        customer_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                font-size: 14px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(customer_btn)
        
        # 测试分配销售对话框下拉框
        sales_btn = QPushButton("🔍 测试分配销售对话框下拉框")
        sales_btn.clicked.connect(self.test_sales_combobox)
        sales_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                font-size: 14px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        layout.addWidget(sales_btn)
        
        # 测试分配客服对话框下拉框
        service_btn = QPushButton("🔍 测试分配客服对话框下拉框")
        service_btn.clicked.connect(self.test_service_combobox)
        service_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                font-size: 14px;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        layout.addWidget(service_btn)
        
        # 状态标签
        self.status_label = QLabel("✅ 所有对话框的下拉框文字颜色已修复为 #333333，确保清晰可见")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                padding: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def test_customer_combobox(self):
        """测试客户对话框下拉框"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            dialog.exec()
            print("✅ 客户对话框下拉框测试完成")
        except Exception as e:
            print(f"❌ 客户对话框测试失败: {e}")
            self.status_label.setText(f"❌ 客户对话框测试失败: {e}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 10px;
                }
            """)
    
    def test_sales_combobox(self):
        """测试分配销售对话框下拉框"""
        try:
            from ui.dialogs.assign_sales_dialog import AssignSalesDialog
            dialog = AssignSalesDialog(parent=self)
            dialog.exec()
            print("✅ 分配销售对话框下拉框测试完成")
        except Exception as e:
            print(f"❌ 分配销售对话框测试失败: {e}")
            self.status_label.setText(f"❌ 分配销售对话框测试失败: {e}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 10px;
                }
            """)
    
    def test_service_combobox(self):
        """测试分配客服对话框下拉框"""
        try:
            from ui.dialogs.assign_service_dialog import AssignServiceDialog
            dialog = AssignServiceDialog(parent=self)
            dialog.exec()
            print("✅ 分配客服对话框下拉框测试完成")
        except Exception as e:
            print(f"❌ 分配客服对话框测试失败: {e}")
            self.status_label.setText(f"❌ 分配客服对话框测试失败: {e}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 10px;
                }
            """)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f8f9fa;
        }
    """)
    
    # 创建测试窗口
    window = ComboBoxTestWindow()
    window.show()
    
    print("🎯 下拉框文字显示测试程序已启动")
    print("📋 修复内容:")
    print("   ✅ 客户对话框：所有下拉框文字颜色设置为 #333333")
    print("   ✅ 分配销售对话框：所有下拉框文字颜色设置为 #333333")
    print("   ✅ 分配客服对话框：所有下拉框文字颜色设置为 #333333")
    print("   ✅ 添加了下拉框项目的悬停和选中状态样式")
    print("   ✅ 创建了通用样式类避免将来再次出现此问题")
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
