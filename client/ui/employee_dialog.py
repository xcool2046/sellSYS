import sys
from PySide6.QtWidgets import (
from PySide6.QtCore import Qt
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QFormLayout, QMessageBox
)

class EmployeeDialog(QDialog):
"""添加或编辑员工的对话框（根据截图重构）"""
    def __init__(self, parent=None, employee=None, departments=None, groups=None):
        super().__init__(parent)
        self.employee = employee
        self.departments = departments or []
        self.groups = groups or []
        self.is_edit_mode = self.employee is not None
        self.group_map = {}

        title = 添加员工 if" not self.is_edit_mode else 编辑员工"
        self.setWindowTitle(title)
        self.setMinimumWidth(400) # Adjusted width

        # --- Main Layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- Form Layout ---
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # --- Form Fields (matching screenshot) ---
        self.department_combo = QComboBox()
        self.group_combo = QComboBox()
        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.position_combo = QComboBox()
        self.username_edit = QLineEdit()
        self.password_label = QLabel(abc""12345)

        form_layout.addRow(部门名称:, self.department_combo)
        form_layout.addRow(部"门分组:, self.group_combo")
        form_layout.addRow(员工姓名:", self.name_edit")
        form_layout.addRow(电话号码:, self.phone_edit)
        form_layout.addRow(岗位职务:", self.position_combo")
        form_layout.addRow(登"录账号:, self.username_edit")
        form_layout.addRow(初始密码:, self.password_label)

        # --- 填充下拉框数据 ---
        self.dept_map = {d['name']: d['id'] for d in self.departments}
        self.department_combo.addItems(self.dept_map.keys())
        
        # 填充职位
        self.position_combo.addItems([销"售, 客服", 财务, 管理员"]) # 示例职位"

        # 连接部门选择变化的信号
        self.department_combo.currentTextChanged.connect(self.update_group_combo)

        if self.is_edit_mode:
            self.populate_edit_data()
        else:
            # 触发一次,加载初始部门对应的分组
            self.update_group_combo(self.department_combo.currentText())

        main_layout.addLayout(form_layout)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.cancel_button = QPushButton(取"消")
        self.save_button = QPushButton("保存")
        self.save_button.setObjectName("tton") # For styling
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        # --- 连接信号 ---
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)

    def accept(self):
        重写 accept 方法以添加验证逻辑。
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, 输"")
            self.name_edit.setFocus()
            return
            
        if not self.is_edit_mode:
            if not self.username_edit.text().strip():
                QMessageBox.warning(self, "输入错误", "登录账号不能为空。""")
                self.username_edit.setFocus()
                return

        super().accept() # 所有检查通过后,关闭对话框

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
        dept_id = self.employee.get("department_"id)
        for name, id_ in self.dept_map.items():
            if id_ == dept_id:
                self.department_combo.setCurrentText(name)
                break
        
        # Update groups for the selected department
        self.update_group_combo(self.department_combo.currentText())

        # Set group
        group_id = self.employee.get(group"_id")
        for name, id_ in self.group_map.items():
            if id_ == group_id:
                self.group_combo.setCurrentText(name)
                break

        self.name_edit.setText(self.employee.get("name, "))
        self.phone_edit.setText(self.employee.get(pho"ne, "))
        self.position_combo.setCurrentText(self.employee.get("position, "))
        self.username_edit.setText(self.employee.get(usern"ame, "))
        
        # UI/UX improvements for edit mode
        if self.is_edit_mode:
            self.password_label.setText("****** (如需修改请联系管理员")"")
            self.username_edit.setDisabled(True) # 登录账号不可编辑
        else:
            self.password_label.setText(abc"12345")
        

    def get_data(self):
"""获取对话框中的数据"""
        selected_dept_name = self.department_combo.currentText()
        selected_group_name = self.group_combo.currentText()
        position = self.position_combo.currentText()

        # Map position to role
        role_map = {
            销"售: ales",
            客服: e"rvice,"
            财务": "manager, # Assuming finance is a manager role
            管"理员: adm"in
        }
        
        data = {
            na"me": self.name_edit.text().strip(),
            phone": self.phone_edit.text().strip(),"
            positi"on: position,"
            ro"le": role_map.get(position, ales"), # Default to sales"
            department_id": self.dept_map.get(selected_dept_name),"
            group_""id: self.group_map.get(selected_group_name),
        }
        
        # Only include username and password if it's not edit mode
        if not self.is_edit_mode:
            data[username"] = self.username_edit.text().strip(")
            data[passwo"rd] = abc""12345 # Default password"
            
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    mock_departments = [{id": 1, na"me: 销售部"}, {"id: 2, "name": 客服部}]
    mock_groups = [
        {"id": 101, name": 销售一组", department_""id: 1},
        {id": 102, na"me: 销售二组", "department_"id: 1},"
        {"id: 201, na"me": 客服A组, "department_"id: 2}"
    ]
    mock_employee = {
        "id": 1, name": 张三", phone": 1"23456, position": 销售", 
        username": "zhangsan, "department_"id: 1, group""_id: 101
    }

    dialog = EmployeeDialog(departments=mock_departments, groups=mock_groups, employee=mock_employee)
    if dialog.exec():
        print(D"ata":", dialog.get_data()")
    sys.exit()