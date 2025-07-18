#!/usr/bin/env python3
"""
调试客户添加失败问题
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit

class CustomerAddDebugWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("客户添加问题调试")
        self.setGeometry(100, 100, 600, 500)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("客户添加失败问题调试")
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
                font-size: 12px;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.debug_text)
        
        # 测试按钮
        test_btn = QPushButton("🔍 测试客户添加流程")
        test_btn.clicked.connect(self.test_customer_add)
        test_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
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
        
        # 测试API按钮
        api_test_btn = QPushButton("🌐 测试API连接")
        api_test_btn.clicked.connect(self.test_api_connection)
        api_test_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
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
        layout.addWidget(api_test_btn)
    
    def log(self, message):
        """添加日志信息"""
        self.debug_text.append(f"[{self.get_timestamp()}] {message}")
        self.debug_text.ensureCursorVisible()
    
    def get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def test_customer_add(self):
        """测试客户添加流程"""
        self.debug_text.clear()
        self.log("开始测试客户添加流程...")
        
        try:
            # 1. 测试对话框导入
            self.log("1. 测试客户对话框导入...")
            from ui.dialogs.customer_dialog import CustomerDialog
            self.log("✅ 客户对话框导入成功")
            
            # 2. 测试对话框创建
            self.log("2. 测试对话框创建...")
            dialog = CustomerDialog(parent=self)
            self.log("✅ 客户对话框创建成功")
            
            # 3. 测试数据获取方法
            self.log("3. 测试数据获取方法...")
            customer_data = dialog.get_customer_data()
            contacts_data = dialog.get_contacts_data()
            self.log(f"✅ 客户数据结构: {customer_data}")
            self.log(f"✅ 联系人数据结构: {contacts_data}")
            
            # 4. 测试验证方法
            self.log("4. 测试验证方法...")
            validation_result = dialog.validate()
            self.log(f"✅ 验证方法可调用，当前结果: {validation_result}")
            
            # 5. 测试API导入
            self.log("5. 测试API导入...")
            from api.customers_api import customers_api
            self.log("✅ 客户API导入成功")
            
            # 6. 模拟完整数据测试
            self.log("6. 测试完整数据结构...")
            test_data = {
                'industry': '制造业',
                'company': '测试公司',
                'province': '北京市',
                'city': '朝阳区',
                'address': '测试地址',
                'notes': '测试备注',
                'contacts': [
                    {'name': '张三', 'phone': '13800138000', 'is_primary': True}
                ]
            }
            self.log(f"✅ 测试数据: {test_data}")
            
            self.log("🎯 客户添加流程组件测试完成")
            
        except Exception as e:
            self.log(f"❌ 测试过程中发生错误: {str(e)}")
            import traceback
            self.log(f"❌ 错误详情: {traceback.format_exc()}")
    
    def test_api_connection(self):
        """测试API连接"""
        self.log("开始测试API连接...")
        
        try:
            # 1. 测试API导入
            self.log("1. 导入API客户端...")
            from api.customers_api import customers_api
            self.log("✅ API客户端导入成功")
            
            # 2. 测试获取客户列表
            self.log("2. 测试获取客户列表...")
            customers = customers_api.get_all()
            if customers is not None:
                self.log(f"✅ 获取客户列表成功，共 {len(customers)} 条记录")
            else:
                self.log("⚠️ 获取客户列表返回None，可能是服务器连接问题")
            
            # 3. 测试创建客户（模拟数据）
            self.log("3. 测试创建客户API...")
            test_customer = {
                'industry': '测试行业',
                'company': '测试公司' + str(self.get_timestamp()),
                'province': '北京市',
                'city': '朝阳区',
                'address': '测试地址',
                'notes': '这是一个API测试客户',
                'contacts': [
                    {'name': '测试联系人', 'phone': '13800138000', 'is_primary': True}
                ]
            }
            
            result = customers_api.create(test_customer)
            if result:
                self.log(f"✅ 创建客户成功: {result}")
            else:
                self.log("❌ 创建客户失败，API返回None")
            
        except Exception as e:
            self.log(f"❌ API测试过程中发生错误: {str(e)}")
            import traceback
            self.log(f"❌ 错误详情: {traceback.format_exc()}")

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
    window = CustomerAddDebugWindow()
    window.show()
    
    print("🔍 客户添加问题调试工具已启动")
    print("📋 调试内容:")
    print("   1. 测试客户对话框组件")
    print("   2. 测试数据获取和验证")
    print("   3. 测试API连接和调用")
    print("   4. 识别具体失败原因")
    
    # 启动应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
