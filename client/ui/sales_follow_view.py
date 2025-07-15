import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QTableView, QHeaderView, QLineEdit, QComboBox, QDateTimeEdit
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ..api.sales_follows import get_sales_follows_by_customer, create_sales_follow

class SalesFollowView(QWidget):
    def __init__(self, customer_id=1, parent=None): # Assume customer_id is passed
        super().__init__(parent)
        self.customer_id = customer_id
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(f"客户ID {self.customer_id} - 销售跟进管理")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Add new follow-up form
        form_widget = QWidget()
        form_layout = QHBoxLayout(form_widget)
        form_layout.addWidget(QLabel("跟进内容:"))
        self.content_input = QTextEdit()
        form_layout.addWidget(self.content_input)
        add_button = QPushButton("添加跟进")
        add_button.clicked.connect(self.add_follow)
        form_layout.addWidget(add_button)
        main_layout.addWidget(form_widget)
        
        # Table view for existing follow-ups
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.model = QStandardItemModel()
        self.setup_model()
        self.table_view.setModel(self.model)
        
        main_layout.addWidget(self.table_view)
        
        self.load_data()
        
    def setup_model(self):
        headers = ["ID", "跟进内容", "跟进方式", "跟进日期", "意向等级", "下次跟进"]
        self.model.setHorizontalHeaderLabels(headers)

    def load_data(self):
        self.model.removeRows(0, self.model.rowCount())
        follows = get_sales_follows_by_customer(self.customer_id)
        if not follows:
            return
        for follow in follows:
            row = [
                QStandardItem(str(follow.get("id"))),
                QStandardItem(follow.get("content")),
                QStandardItem(follow.get("follow_type")),
                QStandardItem(follow.get("follow_date", "").split("T")[0]),
                QStandardItem(follow.get("intention_level")),
                QStandardItem(follow.get("next_follow_date", "").split("T")[0]),
            ]
            self.model.appendRow(row)

    def add_follow(self):
        content = self.content_input.toPlainText()
        if not content:
            return
            
        # This is a simplified creation, more fields would be in a proper dialog
        follow_data = {
            "content": content,
            "follow_type": "Manual Entry", # Default value
            "customer_id": self.customer_id,
            "employee_id": 1 # Placeholder for current user's ID
        }
        
        new_follow = create_sales_follow(follow_data)
        if new_follow:
            self.load_data() # Refresh the list
            self.content_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = SalesFollowView()
    view.show()
    sys.exit(app.exec())