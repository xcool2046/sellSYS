#!/usr/bin/env python3
"""
代码模板生成器 - 快速生成标准化的代码模板
"""
import os
import sys
from pathlib import Path

class CodeTemplates:
    """代码模板类"""
    
    @staticmethod
    def ui_view_template(class_name, title):
        """UI视图模板"""
        return f'''from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QLineEdit,
    QComboBox, QHeaderView, QMessageBox, QLabel
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

class {class_name}(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("{title}")
        
        self.data = []
        self.setup_ui()
        self.setup_connections()
        self.load_data()
    
    def setup_ui(self):
        """设置用户界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 工具栏
        toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索...")
        toolbar_layout.addWidget(self.search_input)
        
        # 按钮
        self.search_btn = QPushButton("查询")
        self.reset_btn = QPushButton("重置")
        self.add_btn = QPushButton("添加")
        
        toolbar_layout.addWidget(self.search_btn)
        toolbar_layout.addWidget(self.reset_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        
        # 表格
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setAlternatingRowColors(True)
        
        # 组装布局
        main_layout.addWidget(toolbar_container)
        main_layout.addWidget(self.table_view)
        
        self.setup_table_headers()
    
    def setup_table_headers(self):
        """设置表格标题"""
        headers = ["ID", "名称", "创建时间", "操作"]
        self.model.setHorizontalHeaderLabels(headers)
    
    def setup_connections(self):
        """设置信号连接"""
        self.search_btn.clicked.connect(self.on_search_clicked)
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        self.add_btn.clicked.connect(self.on_add_clicked)
    
    def load_data(self):
        """加载数据"""
        # TODO: 实现数据加载逻辑
        pass
    
    def on_search_clicked(self):
        """搜索按钮点击事件"""
        search_text = self.search_input.text().strip()
        # TODO: 实现搜索逻辑
        print(f"搜索: {{search_text}}")
    
    def on_reset_clicked(self):
        """重置按钮点击事件"""
        self.search_input.clear()
        self.load_data()
    
    def on_add_clicked(self):
        """添加按钮点击事件"""
        # TODO: 实现添加逻辑
        QMessageBox.information(self, "提示", "添加功能待实现")
'''
    
    @staticmethod
    def api_client_template(module_name, base_url):
        """API客户端模板"""
        return f'''import requests
from config import API_BASE_URL, API_TIMEOUT

class {module_name.title()}API:
    """{{module_name}}相关API"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
    
    def get_list(self, params=None):
        """获取列表"""
        try:
            response = requests.get(
                f"{{self.base_url}}/{base_url}/",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取{{module_name}}列表失败: {{e}}")
            return []
    
    def get_by_id(self, item_id):
        """根据ID获取详情"""
        try:
            response = requests.get(
                f"{{self.base_url}}/{base_url}/{{item_id}}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取{{module_name}}详情失败: {{e}}")
            return None
    
    def create(self, data):
        """创建新记录"""
        try:
            response = requests.post(
                f"{{self.base_url}}/{base_url}/",
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"创建{{module_name}}失败: {{e}}")
            return None
    
    def update(self, item_id, data):
        """更新记录"""
        try:
            response = requests.put(
                f"{{self.base_url}}/{base_url}/{{item_id}}",
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"更新{{module_name}}失败: {{e}}")
            return None
    
    def delete(self, item_id):
        """删除记录"""
        try:
            response = requests.delete(
                f"{{self.base_url}}/{base_url}/{{item_id}}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"删除{{module_name}}失败: {{e}}")
            return False

# 创建全局实例
{module_name}_api = {module_name.title()}API()
'''

    @staticmethod
    def dialog_template(class_name, title):
        """对话框模板"""
        return f'''from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QDialogButtonBox, QMessageBox
)

class {class_name}(QDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("{title}")
        self.setMinimumWidth(400)
        
        self.setup_ui()
        if data:
            self.load_data()
    
    def setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)
        
        # 表单布局
        form_layout = QFormLayout()
        
        # 输入字段
        self.name_edit = QLineEdit()
        form_layout.addRow("名称:", self.name_edit)
        
        # TODO: 添加更多字段
        
        layout.addLayout(form_layout)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def load_data(self):
        """加载数据到表单"""
        if self.data:
            self.name_edit.setText(self.data.get("name", ""))
            # TODO: 加载更多字段
    
    def get_data(self):
        """获取表单数据"""
        return {{
            "name": self.name_edit.text().strip(),
            # TODO: 添加更多字段
        }}
    
    def accept(self):
        """确认按钮点击事件"""
        data = self.get_data()
        
        # 验证数据
        if not data["name"]:
            QMessageBox.warning(self, "提示", "请输入名称")
            return
        
        super().accept()
'''

class CodeGenerator:
    """代码生成器"""
    
    def __init__(self, project_root="client"):
        self.project_root = Path(project_root)
        self.templates = CodeTemplates()
    
    def generate_ui_view(self, name, title=None):
        """生成UI视图文件"""
        if not title:
            title = name
        
        class_name = f"{name.title()}View"
        file_name = f"{name.lower()}_view.py"
        file_path = self.project_root / "ui" / file_name
        
        content = self.templates.ui_view_template(class_name, title)
        
        self._write_file(file_path, content)
        print(f"✅ 已生成UI视图: {file_path}")
    
    def generate_api_client(self, name, base_url=None):
        """生成API客户端文件"""
        if not base_url:
            base_url = name.lower()
        
        file_name = f"{name.lower()}.py"
        file_path = self.project_root / "api" / file_name
        
        content = self.templates.api_client_template(name, base_url)
        
        self._write_file(file_path, content)
        print(f"✅ 已生成API客户端: {file_path}")
    
    def generate_dialog(self, name, title=None):
        """生成对话框文件"""
        if not title:
            title = f"{name}对话框"
        
        class_name = f"{name.title()}Dialog"
        file_name = f"{name.lower()}_dialog.py"
        file_path = self.project_root / "ui" / file_name
        
        content = self.templates.dialog_template(class_name, title)
        
        self._write_file(file_path, content)
        print(f"✅ 已生成对话框: {file_path}")
    
    def _write_file(self, file_path, content):
        """写入文件"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  python code_generator.py view <name> [title]     # 生成UI视图")
        print("  python code_generator.py api <name> [base_url]   # 生成API客户端")
        print("  python code_generator.py dialog <name> [title]   # 生成对话框")
        print("")
        print("示例:")
        print("  python code_generator.py view product 产品管理")
        print("  python code_generator.py api product products")
        print("  python code_generator.py dialog product 产品编辑")
        return
    
    command = sys.argv[1]
    name = sys.argv[2]
    extra = sys.argv[3] if len(sys.argv) > 3 else None
    
    generator = CodeGenerator()
    
    if command == "view":
        generator.generate_ui_view(name, extra)
    elif command == "api":
        generator.generate_api_client(name, extra)
    elif command == "dialog":
        generator.generate_dialog(name, extra)
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
