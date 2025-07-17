import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt

class DepartmentDialog(QDialog):
    """添加或编辑部门的对话框"""
    def __init__(self, parent=None, department=None):
        super().__init__(parent)
        self.department = department
        self.is_edit_mode = self.department is not None

        self.setWindowTitle("添加部门" if not self.is_edit_mode else "编辑部门")
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

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # --- 部门名称 ---
        name_layout = QHBoxLayout()
        name_label = QLabel("部门名称:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        content_layout.addLayout(name_layout)

        if self.is_edit_mode:
            self.name_edit.setText(self.department.get("name", ""))

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
        return {
            "name": self.name_edit.text().strip()
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        with open("styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: styles.qss not found. Run from the 'ui' directory.")
    
    # 测试添加
    add_dialog = DepartmentDialog()
    if add_dialog.exec():
        print("Added data:", add_dialog.get_data())

    # 测试编辑
    edit_dialog = DepartmentDialog(department={"id": 1, "name": "销售部"})
    if edit_dialog.exec():
        print("Edited data:", edit_dialog.get_data())
        
    sys.exit()