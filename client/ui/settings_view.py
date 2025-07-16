import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget,
    QTableView, QPushButton, QHBoxLayout, QHeaderView, QLabel, QFrame, QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from api import departments as departments_api
from api import department_groups as department_groups_api
from api import employees as employees_api

class DepartmentTab(QWidget):
    """部门管理标签页"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 按钮
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加部门")
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # 表格
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "部门名称", "操作"])
        self.table_view.setModel(self.model)
        self.table_view.setColumnHidden(0, True) # Hide ID column

        layout.addWidget(self.table_view)
        
        self.load_data()

    def load_data(self):
        """从API加载数据并填充表格"""
        self.model.removeRows(0, self.model.rowCount())
        departments = departments_api.get_departments()
        if departments:
            for i, dept in enumerate(departments):
                id_item = QStandardItem(str(dept['id']))
                name_item = QStandardItem(dept['name'])

                self.model.appendRow([id_item, name_item])
                
                # 添加操作按钮
                edit_button = QPushButton("编辑")
                delete_button = QPushButton("删除")
                
                edit_button.clicked.connect(lambda checked, r=i: self.edit_item(r))
                delete_button.clicked.connect(lambda checked, r=i: self.delete_item(r))

                buttons_widget = QWidget()
                buttons_layout = QHBoxLayout(buttons_widget)
                buttons_layout.addWidget(edit_button)
                buttons_layout.addWidget(delete_button)
                buttons_layout.setContentsMargins(0, 0, 0, 0)
                buttons_layout.setAlignment(Qt.AlignCenter)
                
                self.table_view.setIndexWidget(self.model.index(i, 2), buttons_widget)

    def edit_item(self, row):
        QMessageBox.information(self, "操作", f"编辑第 {row + 1} 行。")

    def delete_item(self, row):
        QMessageBox.information(self, "操作", f"删除第 {row + 1} 行。")

class DepartmentGroupTab(QWidget):
    """部门分组管理标签页"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加分组")
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "分组名称", "操作"])
        self.table_view.setModel(self.model)
        self.table_view.setColumnHidden(0, True)

        layout.addWidget(self.table_view)
        
        self.load_data()

    def load_data(self):
        self.model.removeRows(0, self.model.rowCount())
        groups = department_groups_api.get_department_groups()
        if groups:
            for i, group in enumerate(groups):
                id_item = QStandardItem(str(group['id']))
                name_item = QStandardItem(group['name'])
                self.model.appendRow([id_item, name_item])
                
                edit_button = QPushButton("编辑")
                delete_button = QPushButton("删除")
                
                edit_button.clicked.connect(lambda checked, r=i: self.edit_item(r))
                delete_button.clicked.connect(lambda checked, r=i: self.delete_item(r))

                buttons_widget = QWidget()
                buttons_layout = QHBoxLayout(buttons_widget)
                buttons_layout.addWidget(edit_button)
                buttons_layout.addWidget(delete_button)
                buttons_layout.setContentsMargins(0, 0, 0, 0)
                buttons_layout.setAlignment(Qt.AlignCenter)
                
                self.table_view.setIndexWidget(self.model.index(i, 2), buttons_widget)

    def edit_item(self, row):
        QMessageBox.information(self, "操作", f"编辑第 {row + 1} 行。")

    def delete_item(self, row):
        QMessageBox.information(self, "操作", f"删除第 {row + 1} 行。")


class EmployeeTab(QWidget):
    """员工管理标签页"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加员工")
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model = QStandardItemModel()
        headers = ["ID", "部门", "分组", "姓名", "职位", "登录账号", "操作"]
        self.model.setHorizontalHeaderLabels(headers)
        self.table_view.setModel(self.model)
        self.table_view.setColumnHidden(0, True)

        layout.addWidget(self.table_view)
        
        self.load_data()

    def load_data(self):
        self.model.removeRows(0, self.model.rowCount())
        
        # Pre-fetch departments and groups for mapping
        departments = {d['id']: d['name'] for d in departments_api.get_departments() or []}
        groups = {g['id']: g['name'] for g in department_groups_api.get_department_groups() or []}
        
        employees = employees_api.get_employees()
        if employees:
            for i, emp in enumerate(employees):
                dept_name = departments.get(emp.get('department_id'), 'N/A')
                group_name = groups.get(emp.get('group_id'), 'N/A')
                
                id_item = QStandardItem(str(emp['id']))
                dept_item = QStandardItem(dept_name)
                group_item = QStandardItem(group_name)
                name_item = QStandardItem(emp['name'])
                position_item = QStandardItem(emp['position'])
                username_item = QStandardItem(emp['username'])
                
                self.model.appendRow([id_item, dept_item, group_item, name_item, position_item, username_item])
                
                edit_button = QPushButton("编辑")
                delete_button = QPushButton("删除")
                
                edit_button.clicked.connect(lambda checked, r=i: self.edit_item(r))
                delete_button.clicked.connect(lambda checked, r=i: self.delete_item(r))

                buttons_widget = QWidget()
                buttons_layout = QHBoxLayout(buttons_widget)
                buttons_layout.addWidget(edit_button)
                buttons_layout.addWidget(delete_button)
                buttons_layout.setContentsMargins(0, 0, 0, 0)
                buttons_layout.setAlignment(Qt.AlignCenter)
                
                self.table_view.setIndexWidget(self.model.index(i, 6), buttons_widget)

    def edit_item(self, row):
        QMessageBox.information(self, "操作", f"编辑第 {row + 1} 行。")

    def delete_item(self, row):
        QMessageBox.information(self, "操作", f"删除第 {row + 1} 行。")

class PermissionTab(QWidget):
    """用户权限管理标签页"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加权限")
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model = QStandardItemModel()
        headers = ["ID", "部门", "职位", "角色权限", "操作"]
        self.model.setHorizontalHeaderLabels(headers)
        self.table_view.setModel(self.model)
        self.table_view.setColumnHidden(0, True)

        layout.addWidget(self.table_view)
        
        self.load_data()

    def load_data(self):
        self.model.removeRows(0, self.model.rowCount())
        
        departments = {d['id']: d['name'] for d in departments_api.get_departments() or []}
        employees = employees_api.get_employees()
        
        if employees:
            for i, emp in enumerate(employees):
                dept_name = departments.get(emp.get('department_id'), 'N/A')
                
                id_item = QStandardItem(str(emp['id']))
                dept_item = QStandardItem(dept_name)
                position_item = QStandardItem(emp['position'])
                role_item = QStandardItem(emp['role'])
                
                self.model.appendRow([id_item, dept_item, position_item, role_item])
                
                edit_button = QPushButton("编辑")
                delete_button = QPushButton("删除")
                
                edit_button.clicked.connect(lambda checked, r=i: self.edit_item(r))
                delete_button.clicked.connect(lambda checked, r=i: self.delete_item(r))

                buttons_widget = QWidget()
                buttons_layout = QHBoxLayout(buttons_widget)
                buttons_layout.addWidget(edit_button)
                buttons_layout.addWidget(delete_button)
                buttons_layout.setContentsMargins(0, 0, 0, 0)
                buttons_layout.setAlignment(Qt.AlignCenter)
                
                self.table_view.setIndexWidget(self.model.index(i, 4), buttons_widget)

    def edit_item(self, row):
        QMessageBox.information(self, "操作", f"编辑第 {row + 1} 行。")

    def delete_item(self, row):
        QMessageBox.information(self, "操作", f"删除第 {row + 1} 行。")

class SettingsView(QWidget):
    """系统设置主视图"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("系统设置")
        
        main_layout = QVBoxLayout(self)
        
        self.tab_widget = QTabWidget()
        
        # 创建各个标签页
        self.department_tab = DepartmentTab()
        self.group_tab = DepartmentGroupTab()
        self.employee_tab = EmployeeTab()
        self.permission_tab = PermissionTab()
        
        self.tab_widget.addTab(self.department_tab, "部门管理")
        self.tab_widget.addTab(self.group_tab, "部门分组")
        self.tab_widget.addTab(self.employee_tab, "员工管理")
        self.tab_widget.addTab(self.permission_tab, "用户权限")
        
        main_layout.addWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = SettingsView()
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec())