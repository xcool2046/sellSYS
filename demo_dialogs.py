#!/usr/bin/env python3
"""
演示对话框功能 - 自动展示所有对话框
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTimer
from PySide6.QtCore import QTimer

class DialogDemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("对话框演示")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("高保真对话框演示")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px; text-align: center;")
        layout.addWidget(title_label)
        
        # 添加说明
        desc_label = QLabel("点击按钮查看按照原型图设计的高保真对话框")
        desc_label.setStyleSheet("font-size: 12px; color: #666; margin: 10px; text-align: center;")
        layout.addWidget(desc_label)
        
        # 添加演示按钮
        self.create_demo_buttons(layout)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
        """)
    
    def create_demo_buttons(self, layout):
        """创建演示按钮"""
        # 演示添加客户对话框
        add_customer_btn = QPushButton("📝 添加客户对话框")
        add_customer_btn.clicked.connect(self.demo_add_customer_dialog)
        add_customer_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 14px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        layout.addWidget(add_customer_btn)
        
        # 演示编辑客户对话框
        edit_customer_btn = QPushButton("✏️ 编辑客户对话框（含数据）")
        edit_customer_btn.clicked.connect(self.demo_edit_customer_dialog)
        edit_customer_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 14px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        layout.addWidget(edit_customer_btn)
        
        # 演示分配销售对话框
        assign_sales_btn = QPushButton("👨‍💼 分配销售对话框")
        assign_sales_btn.clicked.connect(self.demo_assign_sales_dialog)
        assign_sales_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 14px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                margin: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        layout.addWidget(assign_sales_btn)
        
        # 演示分配客服对话框
        assign_service_btn = QPushButton("🎧 分配客服对话框")
        assign_service_btn.clicked.connect(self.demo_assign_service_dialog)
        assign_service_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 14px;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        layout.addWidget(assign_service_btn)
        
        layout.addStretch()
    
    def demo_add_customer_dialog(self):
        """演示添加客户对话框"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            dialog.exec()
        except Exception as e:
            print(f"演示添加客户对话框失败: {e}")
            import traceback
            traceback.print_exc()
    
    def demo_edit_customer_dialog(self):
        """演示编辑客户对话框"""
        try:
            # 模拟客户数据 - 按照原型图的数据
            sample_customer = {
                'id': '123',
                'industry': '教育培训',
                'company': '广汉市学院路技能培训学校',
                'province': '四川省',
                'city': '广汉市',
                'address': '广汉市北京大道北一段15号',
                'notes': '重要客户，提供职业技能培训服务',
                'contacts': [
                    {'name': '刘乾立', 'phone': '15862184966', 'is_primary': True},
                    {'name': '李达', 'phone': '13956774892', 'is_primary': False}
                ]
            }
            
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(sample_customer, parent=self)
            dialog.exec()
        except Exception as e:
            print(f"演示编辑客户对话框失败: {e}")
            import traceback
            traceback.print_exc()
    
    def demo_assign_sales_dialog(self):
        """演示分配销售对话框"""
        try:
            from ui.dialogs.assign_sales_dialog import AssignSalesDialog
            dialog = AssignSalesDialog(parent=self)
            dialog.exec()
        except Exception as e:
            print(f"演示分配销售对话框失败: {e}")
            import traceback
            traceback.print_exc()
    
    def demo_assign_service_dialog(self):
        """演示分配客服对话框"""
        try:
            from ui.dialogs.assign_service_dialog import AssignServiceDialog
            dialog = AssignServiceDialog(parent=self)
            dialog.exec()
        except Exception as e:
            print(f"演示分配客服对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f8f9fa;
        }
        QLabel {
            color: #333;
        }
    """)
    
    # 创建演示窗口
    window = DialogDemoWindow()
    window.show()
    
    print("🎯 对话框演示程序已启动")
    print("📋 功能说明:")
    print("   - 添加客户对话框：完全按照原型图设计，包含行业类型、客户单位、地址、联系人等字段")
    print("   - 编辑客户对话框：预填充示例数据，展示编辑功能")
    print("   - 分配销售对话框：部门、组别、销售姓名的三级选择")
    print("   - 分配客服对话框：部门、组别、客服姓名的三级选择")
    print("💡 所有对话框都采用了高保真设计，严格按照原型图的样式和布局")
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
