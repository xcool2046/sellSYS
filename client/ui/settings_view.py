import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QFrame, QLabel, QTableView, QHeaderView, QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap, QPainter, QFont
from PySide6.QtCore import Qt, QSize

from ..api import departments as departments_api
from ..api import department_groups as department_groups_api
from ..api import employees as employees_api
from .department_dialog import DepartmentDialog
from .department_group_dialog import DepartmentGroupDialog
from .employee_dialog import EmployeeDialog
from .permission_dialog import PermissionDialog

class DepartmentTab(QWidget):
    """部门管理页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 按钮
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加部门")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # 表格
        self.table_view = QTableView()
        self.table_view.setObjectName("contentTable")
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["序号", "部门名称", "创建时间", "操作"])
        self.table_view.setModel(self.model)
        
        layout.addWidget(self.table_view)
        
        self.load_data()

    def load_data(self):
        """从API加载数据并填充表格"""
        self.model.removeRows(0, self.model.rowCount())
        departments = departments_api.get_departments()
        if departments:
            for i, dept in enumerate(departments):
                row = [
                    QStandardItem(str(i + 1)),
                    QStandardItem(dept.get('name', 'N/A')),
                    QStandardItem(dept.get('created_at', 'N/A')[:19].replace('T', ' ')),
                ]
                self.model.appendRow(row)
                
                # 添加操作按钮
                edit_button = QPushButton("编辑")
                delete_button = QPushButton("删除")
                
                dept_data = {'id': dept.get('id'), 'name': dept.get('name')}
                edit_button.clicked.connect(lambda checked, d=dept_data: self.edit_item(d))
                delete_button.clicked.connect(lambda checked, d_id=dept.get('id'): self.delete_item(d_id))

                buttons_widget = QWidget()
                buttons_layout = QHBoxLayout(buttons_widget)
                buttons_layout.addWidget(edit_button)
                buttons_layout.addWidget(delete_button)
                buttons_layout.setContentsMargins(0, 0, 0, 0)
                buttons_layout.setAlignment(Qt.AlignCenter)
                
                self.table_view.setIndexWidget(self.model.index(i, 3), buttons_widget)

    def add_item(self):
        """显示添加部门对话框"""
        dialog = DepartmentDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data['name']:
                if departments_api.create_department(data):
                    self.load_data()
                    QMessageBox.information(self, "成功", "部门已成功添加。")
                else:
                    QMessageBox.warning(self, "错误", "无法创建部门。")
            else:
                QMessageBox.warning(self, "警告", "部门名称不能为空。")

    def edit_item(self, department):
        """显示编辑部门对话框"""
        dialog = DepartmentDialog(self, department=department)
        if dialog.exec():
            data = dialog.get_data()
            if data['name']:
                if departments_api.update_department(department['id'], data):
                    self.load_data()
                    QMessageBox.information(self, "成功", "部门已成功更新。")
                else:
                    QMessageBox.warning(self, "错误", f"无法更新ID为 {department['id']} 的部门。")
            else:
                QMessageBox.warning(self, "警告", "部门名称不能为空。")

    def delete_item(self, department_id):
        """删除一个部门"""
        reply = QMessageBox.question(self, '确认删除', f"您确定要删除ID为 {department_id} 的部门吗?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if departments_api.delete_department(department_id):
                self.load_data()
                QMessageBox.information(self, "成功", "部门已成功删除。")
            else:
                QMessageBox.warning(self, "错误", f"无法删除ID为 {department_id} 的部门。")


class DepartmentGroupTab(QWidget):
    """部门分组管理页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加分组")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.table_view = QTableView()
        self.table_view.setObjectName("contentTable")
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["序号", "部门名称", "部门分组", "操作"])
        self.table_view.setModel(self.model)

        layout.addWidget(self.table_view)
        
        self.load_data()

    def load_data(self):
        self.model.removeRows(0, self.model.rowCount())
        
        self.departments_data = departments_api.get_departments() or []
        departments_map = {d['id']: d['name'] for d in self.departments_data}
        
        groups = department_groups_api.get_department_groups()
        if groups:
            for i, group in enumerate(groups):
                dept_name = departments_map.get(group.get('department_id'), "未知部门")
                row = [
                    QStandardItem(str(i + 1)),
                    QStandardItem(dept_name),
                    QStandardItem(group.get('name', 'N/A')),
                ]
                self.model.appendRow(row)
                
                edit_button = QPushButton("编辑")
                delete_button = QPushButton("删除")
                
                group_data = {'id': group.get('id'), 'name': group.get('name'), 'department_id': group.get('department_id')}
                edit_button.clicked.connect(lambda checked, g=group_data: self.edit_item(g))
                delete_button.clicked.connect(lambda checked, g_id=group.get('id'): self.delete_item(g_id))

                buttons_widget = QWidget()
                buttons_layout = QHBoxLayout(buttons_widget)
                buttons_layout.addWidget(edit_button)
                buttons_layout.addWidget(delete_button)
                buttons_layout.setContentsMargins(0, 0, 0, 0)
                buttons_layout.setAlignment(Qt.AlignCenter)
                
                self.table_view.setIndexWidget(self.model.index(i, 3), buttons_widget)

    def add_item(self):
        dialog = DepartmentGroupDialog(self, departments=self.departments_data)
        if dialog.exec():
            data = dialog.get_data()
            if data['name'] and data['department_id']:
                if department_groups_api.create_department_group(data):
                    self.load_data()
                    QMessageBox.information(self, "成功", "分组已成功添加。")
                else:
                    QMessageBox.warning(self, "错误", "无法创建分组。")
            else:
                QMessageBox.warning(self, "警告", "必须提供分组名称和所属部门。")

    def edit_item(self, group):
        dialog = DepartmentGroupDialog(self, group=group, departments=self.departments_data)
        if dialog.exec():
            data = dialog.get_data()
            if data['name'] and data['department_id']:
                if department_groups_api.update_department_group(group['id'], data):
                    self.load_data()
                    QMessageBox.information(self, "成功", "分组已成功更新。")
                else:
                    QMessageBox.warning(self, "错误", f"无法更新ID为 {group['id']} 的分组。")
            else:
                QMessageBox.warning(self, "警告", "必须提供分组名称和所属部门。")

    def delete_item(self, group_id):
        reply = QMessageBox.question(self, '确认删除', f"您确定要删除ID为 {group_id} 的分组吗?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if department_groups_api.delete_department_group(group_id):
                self.load_data()
                QMessageBox.information(self, "成功", "分组已成功删除。")
            else:
                QMessageBox.warning(self, "错误", f"无法删除ID为 {group_id} 的分组。")


class EmployeeTab(QWidget):
    """员工管理页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加员工")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.table_view = QTableView()
        self.table_view.setObjectName("contentTable")
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
        
        self.departments_data = departments_api.get_departments() or []
        self.groups_data = department_groups_api.get_department_groups() or []
        
        departments_map = {d['id']: d['name'] for d in self.departments_data}
        groups_map = {g['id']: g['name'] for g in self.groups_data}
        
        employees = employees_api.get_employees()
        if employees:
            for i, emp in enumerate(employees):
                dept_name = departments_map.get(emp.get('department_id'), 'N/A')
                group_name = groups_map.get(emp.get('group_id'), 'N/A')
                
                row = [
                    QStandardItem(str(emp['id'])), QStandardItem(dept_name),
                    QStandardItem(group_name), QStandardItem(emp.get('name', 'N/A')),
                    QStandardItem(emp.get('position', 'N/A')), QStandardItem(emp.get('username', 'N/A'))
                ]
                self.model.appendRow(row)
                
                edit_button = QPushButton("编辑")
                delete_button = QPushButton("删除")
                
                edit_button.clicked.connect(lambda checked, e=emp: self.edit_item(e))
                delete_button.clicked.connect(lambda checked, e_id=emp.get('id'): self.delete_item(e_id))

                buttons_widget = QWidget()
                buttons_layout = QHBoxLayout(buttons_widget)
                buttons_layout.addWidget(edit_button)
                buttons_layout.addWidget(delete_button)
                buttons_layout.setContentsMargins(0, 0, 0, 0)
                buttons_layout.setAlignment(Qt.AlignCenter)
                
                self.table_view.setIndexWidget(self.model.index(i, 6), buttons_widget)

    def add_item(self):
        dialog = EmployeeDialog(self, departments=self.departments_data, groups=self.groups_data)
        if dialog.exec():
            data = dialog.get_data()
            if data['name'] and data['username']:
                if employees_api.create_employee(data):
                    self.load_data()
                    QMessageBox.information(self, "成功", "员工已成功添加。")
                else:
                    QMessageBox.warning(self, "错误", "无法创建员工。请检查用户名是否已存在。")
            else:
                QMessageBox.warning(self, "警告", "员工姓名和登录账号不能为空。")

    def edit_item(self, employee):
        dialog = EmployeeDialog(self, employee=employee, departments=self.departments_data, groups=self.groups_data)
        if dialog.exec():
            data = dialog.get_data()
            if data['name']:
                if employees_api.update_employee(employee['id'], data):
                    self.load_data()
                    QMessageBox.information(self, "成功", "员工信息已成功更新。")
                else:
                    QMessageBox.warning(self, "错误", f"无法更新ID为 {employee['id']} 的员工信息。")
            else:
                QMessageBox.warning(self, "警告", "员工姓名不能为空。")

    def delete_item(self, employee_id):
        reply = QMessageBox.question(self, '确认删除', f"您确定要删除ID为 {employee_id} 的员工吗?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if employees_api.delete_employee(employee_id):
                self.load_data()
                QMessageBox.information(self, "成功", "员工已成功删除。")
            else:
                QMessageBox.warning(self, "错误", f"无法删除ID为 {employee_id} 的员工。")


class PermissionTab(QWidget):
    """用户权限管理页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加权限")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.table_view = QTableView()
        self.table_view.setObjectName("contentTable")
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model = QStandardItemModel()
        headers = ["序号", "部门", "职位", "角色权限", "操作"]
        self.model.setHorizontalHeaderLabels(headers)
        self.table_view.setModel(self.model)

        layout.addWidget(self.table_view)
        
        self.load_data()

    def load_data(self):
        """加载权限数据（目前为模拟）"""
        self.model.removeRows(0, self.model.rowCount())
        
        self.departments_data = departments_api.get_departments() or []
        self.employees_data = employees_api.get_employees() or []
        departments_map = {d['id']: d['name'] for d in self.departments_data}
        
        # --- MOCK PERMISSION DATA ---
        self.permissions_data = self._get_mock_permissions(departments_map)
        
        if self.permissions_data:
            for i, perm in enumerate(self.permissions_data):
                row = [
                    QStandardItem(str(i + 1)),
                    QStandardItem(perm.get('department_name', 'N/A')),
                    QStandardItem(perm.get('position', 'N/A')),
                    QStandardItem(", ".join(perm.get('permissions', []))),
                ]
                self.model.appendRow(row)
                
                edit_button = QPushButton("编辑")
                delete_button = QPushButton("删除")
                
                edit_button.clicked.connect(lambda checked, p=perm: self.edit_item(p))
                delete_button.clicked.connect(lambda checked, p=perm: self.delete_item(p))

                buttons_widget = QWidget()
                buttons_layout = QHBoxLayout(buttons_widget)
                buttons_layout.addWidget(edit_button)
                buttons_layout.addWidget(delete_button)
                buttons_layout.setContentsMargins(0, 0, 0, 0)
                buttons_layout.setAlignment(Qt.AlignCenter)
                
                self.table_view.setIndexWidget(self.model.index(i, 4), buttons_widget)

    def _get_mock_permissions(self, departments_map):
        """生成模拟的权限数据"""
        roles = {}
        for emp in self.employees_data:
            key = (emp.get('department_id'), emp.get('position'))
            if key not in roles and all(key):
                mock_perms = []
                if "销售" in emp.get('position', ''):
                    mock_perms = ["客户管理", "销售管理", "订单管理"]
                elif "客服" in emp.get('position', ''):
                    mock_perms = ["售后服务", "产品管理"]
                elif "财务" in emp.get('position', ''):
                    mock_perms = ["财务管理", "订单管理"]
                elif "管理" in emp.get('position', '') or "行政" in emp.get('position', ''):
                    mock_perms = ["数据视窗", "系统设置"]
                
                roles[key] = {
                    "department_name": departments_map.get(key[0]),
                    "position": key[1],
                    "permissions": mock_perms
                }
        return list(roles.values())

    def add_item(self):
        dialog = PermissionDialog(self, departments=self.departments_data, employees=self.employees_data)
        if dialog.exec():
            QMessageBox.information(self, "操作", "“添加权限”功能为演示，数据未实际保存。")
            self.load_data()

    def edit_item(self, permission):
        dialog = PermissionDialog(self, permission=permission, departments=self.departments_data, employees=self.employees_data)
        if dialog.exec():
            QMessageBox.information(self, "操作", "“编辑权限”功能为演示，数据未实际保存。")
            self.load_data()

    def delete_item(self, permission):
        reply = QMessageBox.question(self, '确认删除',
                                     f"您确定要删除 “{permission.get('department_name')} - {permission.get('position')}” 的权限配置吗?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "操作", "“删除权限”功能为演示，数据未实际删除。")
            self.load_data()


class SettingsView(QWidget):
    """系统设置主视图"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsView")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Top Navigation Bar ---
        nav_bar = QFrame()
        nav_bar.setObjectName("settingsNavBar")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(20, 10, 20, 10)
        nav_layout.setSpacing(15)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.nav_buttons = {}
        # 创建带图标的导航按钮
        icon_paths = {
            "部门管理": "client/ui/icons/department.svg",
            "部门分组": "client/ui/icons/group.svg",
            "员工管理": "client/ui/icons/employee.svg",
            "角色权限": "client/ui/icons/permission.svg"
        }
        texts = ["部门管理", "部门分组", "员工管理", "角色权限"]
        
        for i, text in enumerate(texts):
            self._create_nav_button(text, icon_paths[text], i, nav_layout)

        main_layout.addWidget(nav_bar)

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)

        # --- Content Stack ---
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("settingsContent")
        main_layout.addWidget(self.content_stack)

        self.department_page = DepartmentTab()
        self.group_page = DepartmentGroupTab()
        self.employee_page = EmployeeTab()
        self.permission_page = PermissionTab()

        self.content_stack.addWidget(self.department_page)
        self.content_stack.addWidget(self.group_page)
        self.content_stack.addWidget(self.employee_page)
        self.content_stack.addWidget(self.permission_page)

        self.on_nav_button_clicked(0) # Set initial page

    def _create_nav_button(self, text, icon_path, index, layout):
        """创建带图标和文本的导航按钮"""
        button = QPushButton()
        button.setObjectName("settingsNavButton")
        button.setCheckable(True)
        button.clicked.connect(lambda: self.on_nav_button_clicked(index))

        button_layout = QHBoxLayout(button)
        button_layout.setContentsMargins(15, 0, 15, 0)
        button_layout.setSpacing(10)

        # 添加图标
        icon_label = QLabel()
        # 在SVG加载时，我们不能直接设置颜色，所以暂时不处理
        pixmap = QPixmap(icon_path)
        icon_label.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.FastTransformation))
        button_layout.addWidget(icon_label)

        # 添加文本
        text_label = QLabel(text)
        text_label.setObjectName("settingsNavLabel")
        button_layout.addWidget(text_label)

        button_layout.addStretch()

        layout.addWidget(button)
        self.nav_buttons[index] = button


    def on_nav_button_clicked(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, button in self.nav_buttons.items():
            button.setChecked(i == index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        with open("client/ui/styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: styles.qss not found.")
    view = SettingsView()
    view.resize(1000, 700)
    view.show()
    sys.exit(app.exec())