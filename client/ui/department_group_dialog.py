import sys
from PySide6.QtWidgets import (
from PySide6.QtCore import Qt
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QFormLayout, QFrame
)

class DepartmentGroupDialog(QDialog):
    """添加或编辑部门分组的对话框"""
    def __init__(self, parent=None, group=None, departments=None):
        super().__init__(parent)
        self.group = group
        self.departments = departments or []
        self.is_edit_mode = self.group is not None

        self.setWindowTitle("添加分组" if not self.is_edit_mode else "编辑分组")
        self.setMinimumWidth(400)
        
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

        # --- 部门名称 ---
        self.department_combo = QComboBox()
        self.dept_map = {dept['name']: dept['id'] for dept in self.departments}
        self.department_combo.addItems(self.dept_map.keys())
        content_layout.addRow("部门名称:", self.department_combo)

        # --- 分组名称 ---
        self.name_edit = QLineEdit()
        content_layout.addRow("部门分组:", self.name_edit)

        if self.is_edit_mode:
            self.name_edit.setText(self.group.get("name", ""))
            # Set the correct department in the combo box
            dept_id = self.group.get("department_id")
            for name, id_ in self.dept_map.items():
                if id_ == dept_id:
                    self.department_combo.setCurrentText(name)
                    break
        
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

    def get_data(self):
        """获取对话框中的数据"""
        selected_dept_name = self.department_combo.currentText()
        return {
            "name": self.name_edit.text().strip(),
            "department_id": self.dept_map.get(selected_dept_name)
        }

if __name__ == '__main__':
    # This is test code and should be adapted for real use
    app = QApplication(sys.argv)
    
    # Mock data for testing
    mock_departments = [
        {"id": 1, "name": "销售部"},
        {"id": 2, "name": "客服部"},
        {"id": 3, "name": "行政部"}
    ]

    # Test Add Dialog
    add_dialog = DepartmentGroupDialog(departments=mock_departments)
    if add_dialog.exec():
        print("Added data:", add_dialog.get_data())

    # Test Edit Dialog
    mock_group = {"id": 1, "name": "一组", "department_id": 1}
    edit_dialog = DepartmentGroupDialog(group=mock_group, departments=mock_departments)
    if edit_dialog.exec():
        print("Edited data:", edit_dialog.get_data())
        
    sys.exit()