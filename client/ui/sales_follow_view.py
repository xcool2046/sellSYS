import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QTableView, QHeaderView, QLineEdit, QComboBox, QDateTimeEdit,
    QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ..api.sales_follows import get_sales_follows_by_customer, create_sales_follow

class SalesFollowView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Toolbar ---
        toolbar_container = QWidget()
        toolbar_container.setObjectName("toolbarContainer")
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        
        toolbar_layout.addStretch(1)

        self.add_follow_button = QPushButton("添加跟进")
        self.add_follow_button.setObjectName("addButton")
        toolbar_layout.addWidget(self.add_follow_button)
        
        main_layout.addWidget(toolbar_container)
        
        # --- Table view ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.model = QStandardItemModel()
        self.setup_model()
        self.table_view.setModel(self.model)
        
        main_layout.addWidget(self.table_view)
        
        self.load_data()
        
        # --- Connections ---
        self.add_follow_button.clicked.connect(self.add_follow)

    def setup_model(self):
        headers = ["ID", "客户名称", "跟进内容", "跟进方式", "跟进日期", "意向等级", "下次跟进"]
        self.model.setHorizontalHeaderLabels(headers)

    def load_data(self):
        # This view should probably get all follow-ups, or be filtered by a customer
        # For now, let's assume we can get all and display them.
        # A filter mechanism would be needed for a real application.
        self.model.removeRows(0, self.model.rowCount())
        # The API endpoint get_sales_follows_by_customer requires a customer_id, 
        # which we don't have in this generic view.
        # This will need to be adjusted based on how this view is integrated.
        # For now, this will likely fail or show nothing.
        # follows = get_sales_follows() # Assuming a generic getter exists
        follows = [] # Placeholder until a proper API endpoint is available

        for follow in follows:
            if not isinstance(follow, dict): continue
            row = [
                QStandardItem(str(follow.get("id", ""))),
                QStandardItem(follow.get("customer_name", "N/A")),  # Assuming customer name is returned
                QStandardItem(follow.get("content", "")),
                QStandardItem(follow.get("follow_type", "")),
                QStandardItem(follow.get("follow_date", "").split("T")[0]),
                QStandardItem(follow.get("intention_level", "")),
                QStandardItem(follow.get("next_follow_date", "").split("T")[0])
            ]
            self.model.appendRow(row)

    def add_follow(self):
        # Here you would open a dialog to create a new follow-up
        # The dialog would need to allow selecting a customer.
        QMessageBox.information(self, "操作", "此功能需要一个对话框来创建新的跟进记录。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = SalesFollowView()
    view.show()
    sys.exit(app.exec())