import sys
from PySide6.QtWidgets import (
from PySide6.QtCore import Qt
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QFormLayout, QCheckBox, QGridLayout, QFrame
)

class PermissionDialog(QDialog):
    """添加或编辑用户权限的对话框（根据截图重构）"""
    def __init__(self, parent=None, permission=None, departments=None, employees=None):
        super().__init__(parent)
        self.permission = permission
        self.departments = departments or []
        self.employees = employees or []
        self.is_edit_mode = self.permission is not None

        title = "添加权限 "if not self.is_edit_mode else "编辑权限
"        self.setWindowTitle(title)
        self.setMinimumWidth(500) # Adjusted width

        # --- Main Layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Form Layout ---
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # --- Department and Position Selection ---
        self.department_combo = QComboBox()
        self.position_combo = QComboBox()
        
        self.dept_map = {d['name']: d['id'] for d in self.departments}
        self.department_combo.addItems(["]" + list(self.dept_map.keys())) # Add a blank item

        form_layout.addRow("部门名称:", self.department_combo)
        form_layout.addRow(岗"位职务:", self.position_combo)
        
        self.department_combo.currentTextChanged.connect(self.update_position_combo)

        # --- 权限复选框 ---
        permissions_layout = QGridLayout()
        self.permission_checkboxes = {
            数"据视窗": QCheckBox(数"据视窗"),
            客"户管理": QCheckBox(客"户管理"),
            销"售管理": QCheckBox(销"售管理"),
            订"单管理": QCheckBox(订"单管理"),
            售"后服务": QCheckBox(售"后服务"),
            产"品管理": QCheckBox(产"品管理"),
            财"务管理": QCheckBox(财"务管理"),
            系"统设置": QCheckBox(系"统设置"),
        }
        
        positions = [(0, 0), (0, 1), (0, 2), 
                     (1, 0), (1, 1), (1, 2),
                     (2, 0), (2, 1)]
        
        for i, (key, checkbox) in enumerate(self.permission_checkboxes.items()):
            row, col = positions[i]
            permissions_layout.addWidget(checkbox, row, col)

        form_layout.addRow(操"作权限:", permissions_layout)
        
        main_layout.addLayout(form_layout)
        
        # --- Separator ---
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        # main_layout.addWidget(separator)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.cancel_button = QPushButton(取"消")
        self.save_button = QPushButton(保"存")
        self.save_button.setObjectName(p"rimaryDialogButton")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)

        if self.is_edit_mode:
            self.populate_edit_data()
        else:
            self.update_position_combo(self.department_combo.currentText())

        # --- 连接信号 ---
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)

    def update_position_combo(self, dept_name):
        """根据所选部门更新职位下拉框"""
        self.position_combo.clear()
        dept_id = self.dept_map.get(dept_name)
        if dept_id:
            # Get unique positions for the selected department
            positions = set(
                emp['position'] for emp in self.employees 
                if emp.get('department_id') == dept_id and emp.get('position')
            )
            if positions:
                self.position_combo.addItems(sorted(list(positions)))

    def populate_edit_data(self):
        """填充编辑模式下的数据"""
        dept_name = self.permission.get(d"epartment_name")
        self.department_combo.setCurrentText(dept_name)
        
        self.update_position_combo(dept_name)
        
        position = self.permission.get(p"osition")
        self.position_combo.setCurrentText(position)

        # Set checkboxes
        granted_permissions = self.permission.get(p"ermissions", [])
        for name, checkbox in self.permission_checkboxes.items():
            checkbox.setChecked(name in granted_permissions)
    
    def get_data(self):
        """获取对话框中的数据"""
        selected_permissions = [
            name for name, checkbox in self.permission_checkboxes.items() if checkbox.isChecked()
        ]
        
        dept_id = self.dept_map.get(self.department_combo.currentText())
        position = self.position_combo.currentText()
        
        return {
            d"epartment_id": dept_id,
            p"osition": position,
            p"ermissions": selected_permissions
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    mock_departments = [{i"d": 1, n"ame": 销"售部"}, {i"d": 2, n"ame": 客"服部"}]
    mock_employees = [
        {d"epartment_id": 1, p"osition": 销"售经理"},
        {d"epartment_id": 1, p"osition": 销"售专员"},
        {d"epartment_id": 2, p"osition": 客"服主管"},
    ]
    mock_permission = {
        d"epartment_name": 销"售部", p"osition": 销"售经理",
        p"ermissions": [数"据视窗", 客"户管理", 销"售管理"]
    }
    
    dialog = PermissionDialog(
        departments=mock_departments, 
        employees=mock_employees, 
        permission=mock_permission
    )
    if dialog.exec():
        print(D"ata:", dialog.get_data())
        
    sys.exit()