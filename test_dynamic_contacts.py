#!/usr/bin/env python3
"""
测试动态联系人功能
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

class DynamicContactsTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("动态联系人功能测试")
        self.setGeometry(100, 100, 600, 500)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("动态联系人功能测试")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px; color: #333;")
        layout.addWidget(title_label)
        
        # 功能说明
        features_info = QLabel("""
🔧 修复内容:
• 修复了 "+" 和 "-" 按钮的功能
• 默认只显示一个联系人行
• 可以动态添加和删除联系人
• 至少保留一个联系人行（删除按钮会自动禁用）
• 验证逻辑适应动态联系人数量

✅ 功能特性:
• 点击 "+" 按钮添加新的联系人行
• 点击 "-" 按钮删除当前联系人行
• 当只有一个联系人时，"-" 按钮被禁用
• 支持多个联系人的数据保存和加载
        """)
        features_info.setStyleSheet("""
            QLabel {
                background-color: #e8f5e8;
                border: 1px solid #4caf50;
                border-radius: 5px;
                padding: 15px;
                margin: 10px;
                color: #2e7d32;
                font-size: 12px;
            }
        """)
        layout.addWidget(features_info)
        
        # 测试按钮
        test_new_btn = QPushButton("🧪 测试新建客户对话框")
        test_new_btn.clicked.connect(self.test_new_customer_dialog)
        test_new_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 14px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(test_new_btn)
        
        # 测试编辑按钮
        test_edit_btn = QPushButton("📝 测试编辑客户对话框（多联系人）")
        test_edit_btn.clicked.connect(self.test_edit_customer_dialog)
        test_edit_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 14px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        layout.addWidget(test_edit_btn)
        
        # 测试按钮功能
        test_buttons_btn = QPushButton("🔘 测试按钮功能")
        test_buttons_btn.clicked.connect(self.test_button_functionality)
        test_buttons_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 14px;
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        layout.addWidget(test_buttons_btn)
        
        layout.addStretch()
    
    def test_new_customer_dialog(self):
        """测试新建客户对话框"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            
            print("✅ 新建客户对话框测试:")
            print(f"   默认联系人行数量: {len(dialog.contact_rows)}")
            print("   请测试 '+' 和 '-' 按钮功能")
            
            dialog.exec()
            print("✅ 新建客户对话框测试完成")
            
        except Exception as e:
            print(f"❌ 新建客户对话框测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_edit_customer_dialog(self):
        """测试编辑客户对话框（多联系人）"""
        try:
            # 模拟有多个联系人的客户数据
            sample_data = {
                'id': '123',
                'industry': '制造业',
                'company': '测试科技有限公司',
                'province': '北京市',
                'city': '朝阳区',
                'address': '测试地址123号',
                'notes': '这是一个有多个联系人的测试客户',
                'contacts': [
                    {'name': '刘乾立', 'phone': '15862184966', 'is_primary': True},
                    {'name': '李达', 'phone': '13956774892', 'is_primary': False},
                    {'name': '王五', 'phone': '13700137000', 'is_primary': False}
                ]
            }
            
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(sample_data, parent=self)
            
            print("✅ 编辑客户对话框测试:")
            print(f"   加载的联系人数量: {len(sample_data['contacts'])}")
            print(f"   对话框中的联系人行数量: {len(dialog.contact_rows)}")
            print("   请验证联系人数据是否正确加载")
            
            dialog.exec()
            print("✅ 编辑客户对话框测试完成")
            
        except Exception as e:
            print(f"❌ 编辑客户对话框测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_button_functionality(self):
        """测试按钮功能"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            
            print("🔘 按钮功能测试:")
            print(f"   初始联系人行数量: {len(dialog.contact_rows)}")
            
            # 模拟添加联系人
            initial_count = len(dialog.contact_rows)
            dialog.on_add_contact()
            after_add_count = len(dialog.contact_rows)
            print(f"   添加后联系人行数量: {after_add_count}")
            
            if after_add_count > initial_count:
                print("   ✅ 添加联系人功能正常")
            else:
                print("   ❌ 添加联系人功能异常")
            
            # 测试删除按钮状态
            if len(dialog.contact_rows) > 1:
                # 尝试删除一个联系人
                contact_to_remove = dialog.contact_rows[-1]
                dialog.on_remove_contact(contact_to_remove)
                after_remove_count = len(dialog.contact_rows)
                print(f"   删除后联系人行数量: {after_remove_count}")
                
                if after_remove_count < after_add_count:
                    print("   ✅ 删除联系人功能正常")
                else:
                    print("   ❌ 删除联系人功能异常")
            
            # 检查删除按钮状态
            if len(dialog.contact_rows) == 1:
                is_delete_disabled = not dialog.contact_rows[0].del_btn.isEnabled()
                if is_delete_disabled:
                    print("   ✅ 单个联系人时删除按钮正确禁用")
                else:
                    print("   ❌ 单个联系人时删除按钮应该被禁用")
            
            dialog.exec()
            print("✅ 按钮功能测试完成")
            
        except Exception as e:
            print(f"❌ 按钮功能测试失败: {e}")
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
    """)
    
    # 创建测试窗口
    window = DynamicContactsTestWindow()
    window.show()
    
    print("🔧 动态联系人功能测试工具已启动")
    print("📋 测试内容:")
    print("   ✅ 修复了 '+' 和 '-' 按钮功能")
    print("   ✅ 默认只显示一个联系人行")
    print("   ✅ 支持动态添加和删除联系人")
    print("   ✅ 验证逻辑适应动态联系人")
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
