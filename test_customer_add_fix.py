#!/usr/bin/env python3
"""
测试客户添加修复
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

class CustomerAddTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("客户添加修复测试")
        self.setGeometry(100, 100, 500, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("客户添加功能修复测试")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px; color: #333;")
        layout.addWidget(title_label)
        
        # 修复说明
        fix_info = QLabel("""
🔧 修复内容:
• 修复了下拉框数据值问题（使用None代替空字符串）
• 优化了验证逻辑，正确检查是否选择了行业类型
• 修复了省份变化事件处理
• 添加了默认客户状态
• 修复了后端客户模型的语法错误

✅ 现在应该可以正常添加客户了！
        """)
        fix_info.setStyleSheet("""
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
        layout.addWidget(fix_info)
        
        # 测试按钮
        test_btn = QPushButton("🧪 测试客户添加对话框")
        test_btn.clicked.connect(self.test_customer_dialog)
        test_btn.setStyleSheet("""
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
        layout.addWidget(test_btn)
        
        # 模拟数据测试按钮
        mock_test_btn = QPushButton("📝 模拟完整添加流程")
        mock_test_btn.clicked.connect(self.test_mock_add)
        mock_test_btn.setStyleSheet("""
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
        layout.addWidget(mock_test_btn)
        
        layout.addStretch()
    
    def test_customer_dialog(self):
        """测试客户对话框"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            
            # 预填充一些测试数据
            dialog.company_edit.setText("测试公司")
            dialog.industry_combo.setCurrentIndex(1)  # 选择第一个真实行业
            
            result = dialog.exec()
            if result:
                customer_data = dialog.get_customer_data()
                contacts_data = dialog.get_contacts_data()
                print("✅ 对话框测试成功")
                print(f"客户数据: {customer_data}")
                print(f"联系人数据: {contacts_data}")
            else:
                print("❌ 用户取消了对话框")
                
        except Exception as e:
            print(f"❌ 对话框测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_mock_add(self):
        """模拟完整的添加流程"""
        try:
            print("🧪 开始模拟客户添加流程...")
            
            # 1. 创建对话框
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            
            # 2. 模拟用户输入
            dialog.company_edit.setText("测试科技有限公司")
            dialog.industry_combo.setCurrentIndex(1)  # 选择第一个行业
            dialog.address_edit.setText("测试地址123号")
            dialog.notes_edit.setPlainText("这是一个测试客户")
            
            # 模拟联系人输入
            dialog.contact1_name.setText("张三")
            dialog.contact1_phone.setText("13800138000")
            dialog.contact1_primary.setChecked(True)
            
            # 3. 验证数据
            if dialog.validate():
                print("✅ 数据验证通过")
                
                # 4. 获取数据
                customer_data = dialog.get_customer_data()
                contacts_data = dialog.get_contacts_data()
                
                print(f"✅ 客户数据: {customer_data}")
                print(f"✅ 联系人数据: {contacts_data}")
                
                # 5. 模拟API调用
                customer_data['contacts'] = contacts_data
                print("✅ 数据格式正确，可以发送到API")
                
                # 实际测试API（如果服务器运行）
                try:
                    from api.customers_api import customers_api
                    result = customers_api.create(customer_data)
                    if result:
                        print("🎉 客户创建成功！")
                    else:
                        print("⚠️ API返回失败，可能是服务器未运行")
                except Exception as api_e:
                    print(f"⚠️ API调用失败: {api_e}")
                
            else:
                print("❌ 数据验证失败")
                
        except Exception as e:
            print(f"❌ 模拟测试失败: {e}")
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
    window = CustomerAddTestWindow()
    window.show()
    
    print("🔧 客户添加修复测试工具已启动")
    print("📋 修复内容:")
    print("   ✅ 下拉框数据值修复（None代替空字符串）")
    print("   ✅ 验证逻辑优化")
    print("   ✅ 省份变化事件修复")
    print("   ✅ 后端模型语法错误修复")
    print("   ✅ 添加默认客户状态")
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
