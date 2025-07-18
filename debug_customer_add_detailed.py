#!/usr/bin/env python3
"""
详细调试客户添加失败问题
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit

class DetailedDebugWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("客户添加失败详细调试")
        self.setGeometry(100, 100, 700, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("客户添加失败详细调试工具")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px; color: #333;")
        layout.addWidget(title_label)
        
        # 调试信息显示区域
        self.debug_text = QTextEdit()
        self.debug_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.debug_text)
        
        # 按钮区域
        button_layout = QVBoxLayout()
        
        # 步骤1：测试对话框创建
        step1_btn = QPushButton("步骤1: 测试对话框创建和数据获取")
        step1_btn.clicked.connect(self.test_dialog_creation)
        step1_btn.setStyleSheet(self.get_button_style("#007bff"))
        button_layout.addWidget(step1_btn)
        
        # 步骤2：测试验证逻辑
        step2_btn = QPushButton("步骤2: 测试验证逻辑")
        step2_btn.clicked.connect(self.test_validation)
        step2_btn.setStyleSheet(self.get_button_style("#28a745"))
        button_layout.addWidget(step2_btn)
        
        # 步骤3：测试API调用
        step3_btn = QPushButton("步骤3: 测试API调用")
        step3_btn.clicked.connect(self.test_api_call)
        step3_btn.setStyleSheet(self.get_button_style("#17a2b8"))
        button_layout.addWidget(step3_btn)
        
        # 步骤4：完整流程测试
        step4_btn = QPushButton("步骤4: 完整流程模拟测试")
        step4_btn.clicked.connect(self.test_full_process)
        step4_btn.setStyleSheet(self.get_button_style("#ffc107"))
        
        button_layout.addWidget(step4_btn)
        
        layout.addLayout(button_layout)
    
    def get_button_style(self, color):
        return f"""
            QPushButton {{
                padding: 12px;
                font-size: 13px;
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                margin: 5px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """
    
    def log(self, message):
        """添加日志信息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.debug_text.append(f"[{timestamp}] {message}")
        self.debug_text.ensureCursorVisible()
        print(f"[{timestamp}] {message}")
    
    def test_dialog_creation(self):
        """测试对话框创建和数据获取"""
        self.debug_text.clear()
        self.log("=== 步骤1: 测试对话框创建和数据获取 ===")
        
        try:
            # 1. 导入对话框
            self.log("1.1 导入客户对话框...")
            from ui.dialogs.customer_dialog import CustomerDialog
            self.log("✅ 对话框导入成功")
            
            # 2. 创建对话框实例
            self.log("1.2 创建对话框实例...")
            dialog = CustomerDialog(parent=self)
            self.log("✅ 对话框实例创建成功")
            
            # 3. 测试数据获取方法
            self.log("1.3 测试数据获取方法...")
            customer_data = dialog.get_customer_data()
            contacts_data = dialog.get_contacts_data()
            self.log(f"✅ 客户数据结构: {customer_data}")
            self.log(f"✅ 联系人数据结构: {contacts_data}")
            
            # 4. 测试验证方法
            self.log("1.4 测试验证方法...")
            validation_result = dialog.validate()
            self.log(f"✅ 验证方法返回: {validation_result}")
            
            self.log("=== 步骤1 完成 ===")
            
        except Exception as e:
            self.log(f"❌ 步骤1 失败: {str(e)}")
            import traceback
            self.log(f"❌ 详细错误: {traceback.format_exc()}")
    
    def test_validation(self):
        """测试验证逻辑"""
        self.debug_text.clear()
        self.log("=== 步骤2: 测试验证逻辑 ===")
        
        try:
            from ui.dialogs.customer_dialog import CustomerDialog
            dialog = CustomerDialog(parent=self)
            
            # 测试场景1: 完全空数据
            self.log("2.1 测试完全空数据...")
            result = dialog.validate()
            self.log(f"   空数据验证结果: {result} (期望: False)")
            
            # 测试场景2: 填写公司名称
            self.log("2.2 测试填写公司名称...")
            dialog.company_edit.setText("测试公司")
            result = dialog.validate()
            self.log(f"   有公司名验证结果: {result} (期望: False)")
            
            # 测试场景3: 填写公司名称和行业
            self.log("2.3 测试填写公司名称和行业...")
            dialog.industry_combo.setCurrentIndex(1)  # 选择第一个行业
            result = dialog.validate()
            self.log(f"   有公司和行业验证结果: {result} (期望: False)")
            
            # 测试场景4: 添加联系人姓名
            self.log("2.4 测试添加联系人姓名...")
            dialog.contact1_name.setText("张三")
            result = dialog.validate()
            self.log(f"   有联系人姓名验证结果: {result} (期望: False)")
            
            # 测试场景5: 完整数据
            self.log("2.5 测试完整数据...")
            dialog.contact1_phone.setText("13800138000")
            result = dialog.validate()
            self.log(f"   完整数据验证结果: {result} (期望: True)")
            
            if result:
                # 获取完整数据
                customer_data = dialog.get_customer_data()
                contacts_data = dialog.get_contacts_data()
                self.log(f"✅ 完整客户数据: {customer_data}")
                self.log(f"✅ 完整联系人数据: {contacts_data}")
            
            self.log("=== 步骤2 完成 ===")
            
        except Exception as e:
            self.log(f"❌ 步骤2 失败: {str(e)}")
            import traceback
            self.log(f"❌ 详细错误: {traceback.format_exc()}")
    
    def test_api_call(self):
        """测试API调用"""
        self.debug_text.clear()
        self.log("=== 步骤3: 测试API调用 ===")
        
        try:
            # 1. 导入API
            self.log("3.1 导入客户API...")
            from api.customers_api import customers_api
            self.log("✅ API导入成功")
            
            # 2. 测试API连接
            self.log("3.2 测试API连接...")
            customers = customers_api.get_all()
            if customers is not None:
                self.log(f"✅ API连接成功，当前客户数量: {len(customers)}")
            else:
                self.log("⚠️ API连接失败或返回None")
            
            # 3. 准备测试数据
            self.log("3.3 准备测试数据...")
            test_data = {
                'industry': '制造业',
                'company': f'API测试公司_{self.get_timestamp()}',
                'province': '北京市',
                'city': '朝阳区',
                'address': '测试地址123号',
                'notes': '这是API测试数据',
                'status': 'LEAD',
                'contacts': [
                    {'name': '测试联系人', 'phone': '13800138000', 'is_primary': True}
                ]
            }
            self.log(f"✅ 测试数据准备完成: {test_data}")
            
            # 4. 调用创建API
            self.log("3.4 调用创建API...")
            result = customers_api.create(test_data)
            self.log(f"API调用结果: {result}")
            
            if result:
                self.log("✅ API调用成功")
            else:
                self.log("❌ API调用失败")
            
            self.log("=== 步骤3 完成 ===")
            
        except Exception as e:
            self.log(f"❌ 步骤3 失败: {str(e)}")
            import traceback
            self.log(f"❌ 详细错误: {traceback.format_exc()}")
    
    def test_full_process(self):
        """完整流程模拟测试"""
        self.debug_text.clear()
        self.log("=== 步骤4: 完整流程模拟测试 ===")
        
        try:
            # 模拟完整的添加流程
            self.log("4.1 模拟用户操作...")
            from ui.dialogs.customer_dialog import CustomerDialog
            from api.customers_api import customers_api
            
            # 创建对话框
            dialog = CustomerDialog(parent=self)
            
            # 模拟用户输入
            dialog.company_edit.setText("完整测试公司")
            dialog.industry_combo.setCurrentIndex(1)
            dialog.province_combo.setCurrentIndex(1)
            dialog.address_edit.setText("完整测试地址")
            dialog.notes_edit.setPlainText("完整测试备注")
            dialog.contact1_name.setText("完整测试联系人")
            dialog.contact1_phone.setText("13900139000")
            dialog.contact1_primary.setChecked(True)
            
            self.log("✅ 模拟用户输入完成")
            
            # 验证数据
            self.log("4.2 验证数据...")
            if dialog.validate():
                self.log("✅ 数据验证通过")
                
                # 获取数据
                customer_data = dialog.get_customer_data()
                contacts_data = dialog.get_contacts_data()
                
                # 合并数据
                customer_data['contacts'] = contacts_data
                self.log(f"✅ 合并后的数据: {customer_data}")
                
                # 调用API
                self.log("4.3 调用API创建客户...")
                result = customers_api.create(customer_data)
                
                if result:
                    self.log("🎉 完整流程测试成功！客户创建成功！")
                else:
                    self.log("❌ 完整流程测试失败：API返回失败")
            else:
                self.log("❌ 完整流程测试失败：数据验证失败")
            
            self.log("=== 步骤4 完成 ===")
            
        except Exception as e:
            self.log(f"❌ 步骤4 失败: {str(e)}")
            import traceback
            self.log(f"❌ 详细错误: {traceback.format_exc()}")
    
    def get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%H%M%S")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f8f9fa;
        }
    """)
    
    # 创建调试窗口
    window = DetailedDebugWindow()
    window.show()
    
    print("🔍 客户添加失败详细调试工具已启动")
    print("📋 调试步骤:")
    print("   1. 测试对话框创建和数据获取")
    print("   2. 测试验证逻辑")
    print("   3. 测试API调用")
    print("   4. 完整流程模拟测试")
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
