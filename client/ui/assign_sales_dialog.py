from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QPushButton, QDialogButtonBox
from ..api import departments, department_groups, employees

class AssignSalesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("分配销售")
        self.setMinimumWidth(350)

        # Layouts
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # Widgets
        self.department_combo = QComboBox()
        self.group_combo = QComboBox()
        self.sales_combo = QComboBox()

        # Form Assembly
        self.form_layout.addRow("部门名称:", self.department_combo)
        self.form_layout.addRow("组别名称:", self.group_combo)
        self.form_layout.addRow("销售姓名:", self.sales_combo)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Main Layout Assembly
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)
        
        # Connections
        self.department_combo.currentIndexChanged.connect(self.update_groups_and_employees)
        self.group_combo.currentIndexChanged.connect(self.update_employees)

        # Initial Data Load
        self.load_initial_data()

    def load_initial_data(self):
        # Load all data needed for filtering
        self.all_departments = departments.get_departments() or []
        self.all_groups = department_groups.get_department_groups() or []
        self.all_employees = employees.get_employees() or []

        self.department_combo.clear()
        self.department_combo.addItem("所有部门", -1)
        for dept in self.all_departments:
            self.department_combo.addItem(dept['name'], dept['id'])

    def update_groups_and_employees(self):
        dept_id = self.department_combo.currentData()
        
        self.group_combo.clear()
        self.group_combo.addItem("所有组别", -1)
        
        # Filter groups by department
        groups_in_dept = [g for g in self.all_groups if dept_id == -1 or g.get('department_id') == dept_id]
        for group in groups_in_dept:
            self.group_combo.addItem(group['name'], group['id'])
        
        self.update_employees()

    def update_employees(self):
        dept_id = self.department_combo.currentData()
        group_id = self.group_combo.currentData()

        self.sales_combo.clear()
        self.sales_combo.addItem("选择销售", -1)
        
        # Filter employees
        filtered_employees = self.all_employees
        if dept_id != -1:
            filtered_employees = [e for e in filtered_employees if e.get('department_id') == dept_id]
        if group_id != -1:
            filtered_employees = [e for e in filtered_employees if e.get('group_id') == group_id]
            
        for emp in filtered_employees:
            self.sales_combo.addItem(emp['name'], emp['id'])
            
    def get_selected_sales_id(self):
        return self.sales_combo.currentData()
