import sys
import re
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QLineEdit, QPushButton, QComboBox, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt

class EmployeeDialog(QDialog):
    """添加或编辑员工的对话框"""
    def __init__(self, parent=None, employee=None, departments=None, groups=None):
        super().__init__(parent)
        self.employee = employee
        self.departments = departments or []
        self.groups = groups or []
        self.is_edit_mode = self.employee is not None
        self.group_map = {} # Initialize group_map

        self.setWindowTitle("添加员工" if not self.is_edit_mode else "编辑员工")
        self.setMinimumWidth(450)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 20)
        main_layout.setSpacing(0)

        # --- 标题栏 ---
        title_bar = QFrame()
        title_bar.setObjectName("dialogTitleBar")
        title_layout = QHBoxLayout(title_bar)
        title_label = QLabel(self.windowTitle())
        title_label.setObjectName("dialogTitleLabel")
        title_layout.addWidget(title_label)
        main_layout.addWidget(title_bar)

        content_layout = QFormLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        content_layout.setLabelAlignment(Qt.AlignRight)

        # --- 表单字段 ---
        self.department_combo = QComboBox()
        self.group_combo = QComboBox()
        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.position_combo = QComboBox() # 职位
        self.email_edit = QLineEdit() # 邮箱
        self.username_edit = QLineEdit()
        self.password_label = QLabel("abc12345") # 初始密码

        content_layout.addRow("部门名称:", self.department_combo)
        content_layout.addRow("部门分组:", self.group_combo)
        content_layout.addRow("员工姓名:", self.name_edit)
        content_layout.addRow("电子邮箱:", self.email_edit)
        content_layout.addRow("电话号码:", self.phone_edit)
        content_layout.addRow("岗位职务:", self.position_combo)
        content_layout.addRow("登录账号:", self.username_edit)
        content_layout.addRow("初始密码:", self.password_label)

        # --- 填充下拉框数据 ---
        self.dept_map = {d['name']: d['id'] for d in self.departments}
        self.department_combo.addItems(self.dept_map.keys())
        
        # 填充职位
        self.position_combo.addItems(["销售", "客服", "财务", "管理员"]) # 示例职位

        # 连接部门选择变化的信号
        self.department_combo.currentTextChanged.connect(self.update_group_combo)

        if self.is_edit_mode:
            self.populate_edit_data()
        else:
            # 触发一次，加载初始部门对应的分组
            self.update_group_combo(self.department_combo.currentText())

        main_layout.addLayout(content_layout)

        # --- 按钮 ---
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.cancel_button = QPushButton("取消")
        self.save_button = QPushButton("保存")
        self.save_button.setObjectName("primaryDialogButton")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        # --- 连接信号 ---
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)

    def accept(self):
        """重写 accept 方法以添加验证逻辑。"""
        email = self.email_edit.text().strip()
        
        # 对新员工，邮箱是必填项
        if not self.is_edit_mode and not email:
            QMessageBox.warning(self, "输入错误", "电子邮箱不能为空。")
            self.email_edit.setFocus()
            return

        # 基本的邮箱格式验证
        if email and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            QMessageBox.warning(self, "输入错误", "请输入有效的电子邮箱地址。")
            self.email_edit.setFocus()
            return
            
        # 检查其他新员工的必填项
        if not self.is_edit_mode:
            if not self.name_edit.text().strip():
                QMessageBox.warning(self, "输入错误", "员工姓名不能为空。")
                self.name_edit.setFocus()
                return
            if not self.username_edit.text().strip():
                QMessageBox.warning(self, "输入错误", "登录账号不能为空。")
                self.username_edit.setFocus()
                return

        super().accept() # 所有检查通过后，关闭对话框

    def update_group_combo(self, dept_name):
        """根据所选部门更新分组下拉框"""
        self.group_combo.clear()
        dept_id = self.dept_map.get(dept_name)
        if dept_id is not None:
            # Filter groups for the selected department
            filtered_groups = [g for g in self.groups if g.get('department_id') == dept_id]
            self.group_map = {g['name']: g['id'] for g in filtered_groups}
            self.group_combo.addItems(self.group_map.keys())

    def populate_edit_data(self):
        """填充编辑模式下的数据"""
        # Set department
        dept_id = self.employee.get("department_id")
        for name, id_ in self.dept_map.items():
            if id_ == dept_id:
                self.department_combo.setCurrentText(name)
                break
        
        # Update groups for the selected department
        self.update_group_combo(self.department_combo.currentText())

        # Set group
        group_id = self.employee.get("group_id")
        for name, id_ in self.group_map.items():
            if id_ == group_id:
                self.group_combo.setCurrentText(name)
                break

        self.name_edit.setText(self.employee.get("name", ""))
        self.phone_edit.setText(self.employee.get("phone", ""))
        self.email_edit.setText(self.employee.get("email", ""))
        self.position_combo.setCurrentText(self.employee.get("position", ""))
        self.username_edit.setText(self.employee.get("username", ""))
        self.password_label.setText("******" if self.is_edit_mode else "abc12345")
        self.username_edit.setDisabled(self.is_edit_mode) # 登录账号不可编辑
        

    def get_data(self):
        """获取对话框中的数据"""
        selected_dept_name = self.department_combo.currentText()
        selected_group_name = self.group_combo.currentText()
        position = self.position_combo.currentText()

        # Map position to role
        role_map = {
            "销售": "sales",
            "客服": "service",
            "财务": "manager", # Assuming finance is a manager role
            "管理员": "admin"
        }
        
        data = {
            "name": self.name_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "position": position,
            "role": role_map.get(position, "sales"), # Default to sales
            "department_id": self.dept_map.get(selected_dept_name),
            "group_id": self.group_map.get(selected_group_name),
        }
        
        # Only include username and password if it's not edit mode
        if not self.is_edit_mode:
            data["username"] = self.username_edit.text().strip()
            data["password"] = "abc12345" # Default password
            
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    mock_departments = [{"id": 1, "name": "销售部"}, {"id": 2, "name": "客服部"}]
    mock_groups = [
        {"id": 101, "name": "销售一组", "department_id": 1},
        {"id": 102, "name": "销售二组", "department_id": 1},
        {"id": 201, "name": "客服A组", "department_id": 2}
    ]
    mock_employee = {
        "id": 1, "name": "张三", "phone": "123456", "position": "销售", 
        "username": "zhangsan", "department_id": 1, "group_id": 101
    }

    dialog = EmployeeDialog(departments=mock_departments, groups=mock_groups, employee=mock_employee)
    if dialog.exec():
        print("Data:", dialog.get_data())
    sys.exit()