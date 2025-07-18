#!/usr/bin/env python3
"""
测试联系人验证功能
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

class ContactValidationTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("联系人验证测试")
        self.setGeometry(100, 100, 600, 500)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("联系人信息界面和验证测试")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px; color: #333;")
        layout.addWidget(title_label)
        
        # 修改说明
        changes_info = QLabel("""
🔧 界面修改:
• 联系人输入框布局优化，更符合原型图
• 添加了 + 和 - 按钮（功能性装饰）
• 调整了输入框宽度和间距

✅ 验证规则:
• 必须至少添加一个联系人
• 如果填写了联系人姓名，必须填写对应的电话号码
• 保持原有的公司名称和行业类型验证
        """)
        changes_info.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #2196f3;
                border-radius: 5px;
                padding: 15px;
                margin: 10px;
                color: #1565c0;
                font-size: 12px;
            }
        """)
        layout.addWidget(changes_info)
        
        # 测试按钮
        test_dialog_btn = QPushButton("🧪 测试客户添加对话框")
        test_dialog_btn.clicked.connect(self.test_customer_dialog)
        test_dialog_btn.setStyleSheet("""
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
        layout.addWidget(test_dialog_btn)
        
        # 验证测试按钮
        test_validation_btn = QPushButton("✅ 测试验证逻辑")
        test_validation_btn.clicked.connect(self.test_validation_logic)
        test_validation_btn.setStyleSheet("""
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
        layout.addWidget(test_validation_btn)
        
        # 预填充测试按钮
        test_prefill_btn = QPushButton("📝 测试预填充数据")
        test_prefill_btn.clicked.connect(self.test_prefill_data)
        test_prefill_btn.setStyleSheet("""
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
        layout.addWidget(test_prefill_btn)
        
        layout.addStretch()
    
    def test_customer_dialog(self):
        """测试客户对话框"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            dialog.exec()
            print("✅ 客户对话框测试完成")
        except Exception as e:
            print(f"❌ 对话框测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_validation_logic(self):
        """测试验证逻辑"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            
            print("🧪 开始测试验证逻辑...")
            
            # 测试1: 空数据验证
            print("1. 测试空数据验证...")
            result = dialog.validate()
            print(f"   空数据验证结果: {result} (应该为False)")
            
            # 测试2: 只填公司名称
            print("2. 测试只填公司名称...")
            dialog.company_edit.setText("测试公司")
            result = dialog.validate()
            print(f"   只填公司名称验证结果: {result} (应该为False)")
            
            # 测试3: 填写公司名称和行业
            print("3. 测试填写公司名称和行业...")
            dialog.industry_combo.setCurrentIndex(1)  # 选择第一个行业
            result = dialog.validate()
            print(f"   填写公司和行业验证结果: {result} (应该为False，因为没有联系人)")
            
            # 测试4: 添加联系人姓名但没有电话
            print("4. 测试添加联系人姓名但没有电话...")
            dialog.contact1_name.setText("张三")
            result = dialog.validate()
            print(f"   有姓名无电话验证结果: {result} (应该为False)")
            
            # 测试5: 完整信息
            print("5. 测试完整信息...")
            dialog.contact1_phone.setText("13800138000")
            result = dialog.validate()
            print(f"   完整信息验证结果: {result} (应该为True)")
            
            print("✅ 验证逻辑测试完成")
            
        except Exception as e:
            print(f"❌ 验证逻辑测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_prefill_data(self):
        """测试预填充数据"""
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            
            # 模拟编辑模式的数据
            sample_data = {
                'id': '123',
                'industry': '制造业',
                'company': '测试科技有限公司',
                'province': '北京市',
                'city': '朝阳区',
                'address': '测试地址123号',
                'notes': '这是一个测试客户',
                'contacts': [
                    {'name': '刘乾立', 'phone': '15862184966', 'is_primary': True},
                    {'name': '李达', 'phone': '13956774892', 'is_primary': False}
                ]
            }
            
            dialog = CustomerDialog(sample_data, parent=self)
            dialog.exec()
            print("✅ 预填充数据测试完成")
            
        except Exception as e:
            print(f"❌ 预填充数据测试失败: {e}")
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
    window = ContactValidationTestWindow()
    window.show()
    
    print("🔧 联系人验证测试工具已启动")
    print("📋 测试内容:")
    print("   ✅ 联系人界面布局优化")
    print("   ✅ 联系人验证逻辑")
    print("   ✅ 必须至少一个联系人的规则")
    print("   ✅ 联系人信息完整性验证")
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
