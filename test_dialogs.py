#!/usr/bin/env python3
"""
测试对话框功能
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

class DialogTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("对话框测试")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("对话框功能测试")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)
        
        # 添加测试按钮
        self.create_test_buttons(layout)
    
    def create_test_buttons(self, layout):
        """创建测试按钮"""
        # 测试添加客户对话框
        add_customer_btn = QPushButton("测试添加客户对话框")
        add_customer_btn.clicked.connect(self.test_add_customer_dialog)
        add_customer_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
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
        layout.addWidget(add_customer_btn)
        
        # 测试编辑客户对话框
        edit_customer_btn = QPushButton("测试编辑客户对话框")
        edit_customer_btn.clicked.connect(self.test_edit_customer_dialog)
        edit_customer_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
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
        layout.addWidget(edit_customer_btn)
        
        # 测试分配销售对话框
        assign_sales_btn = QPushButton("测试分配销售对话框")
        assign_sales_btn.clicked.connect(self.test_assign_sales_dialog)
        assign_sales_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        layout.addWidget(assign_sales_btn)
        
        # 测试分配客服对话框
        assign_service_btn = QPushButton("测试分配客服对话框")
        assign_service_btn.clicked.connect(self.test_assign_service_dialog)
        assign_service_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
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
        layout.addWidget(assign_service_btn)
        
        layout.addStretch()
    
    def test_add_customer_dialog(self):
        """测试添加客户对话框"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            result = dialog.exec()
            if result:
                customer_data = dialog.get_customer_data()
                contacts_data = dialog.get_contacts_data()
                print("客户数据:", customer_data)
                print("联系人数据:", contacts_data)
        except Exception as e:
            print(f"测试添加客户对话框失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_edit_customer_dialog(self):
        """测试编辑客户对话框"""
        try:
            # 模拟客户数据
            sample_customer = {
                'id': '123',
                'industry': '制造业',
                'company': '广汉市学院路技能培训学校',
                'province': '四川省',
                'city': '广汉市',
                'address': '广汉市北京大道北一段15号',
                'notes': '重要客户，需要重点关注',
                'contacts': [
                    {'name': '刘乾立', 'phone': '15862184966', 'is_primary': True},
                    {'name': '李达', 'phone': '13956774892', 'is_primary': False}
                ]
            }
            
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(sample_customer, parent=self)
            result = dialog.exec()
            if result:
                customer_data = dialog.get_customer_data()
                contacts_data = dialog.get_contacts_data()
                print("更新后客户数据:", customer_data)
                print("更新后联系人数据:", contacts_data)
        except Exception as e:
            print(f"测试编辑客户对话框失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_assign_sales_dialog(self):
        """测试分配销售对话框"""
        try:
            from ui.dialogs.assign_sales_dialog import AssignSalesDialog
            dialog = AssignSalesDialog(parent=self)
            result = dialog.exec()
            if result:
                assignment_data = dialog.get_assignment_data()
                print("销售分配数据:", assignment_data)
        except Exception as e:
            print(f"测试分配销售对话框失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_assign_service_dialog(self):
        """测试分配客服对话框"""
        try:
            from ui.dialogs.assign_service_dialog import AssignServiceDialog
            dialog = AssignServiceDialog(parent=self)
            result = dialog.exec()
            if result:
                assignment_data = dialog.get_assignment_data()
                print("客服分配数据:", assignment_data)
        except Exception as e:
            print(f"测试分配客服对话框失败: {e}")
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
    
    # 创建测试窗口
    window = DialogTestWindow()
    window.show()
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
