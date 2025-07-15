import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableView, QHeaderView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ..api.service_records import get_service_records, create_service_record

class ServiceRecordView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("售后服务工单")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Action buttons
        action_layout = QHBoxLayout()
        # In a real app, this would open a proper dialog for creating a new record
        add_button = QPushButton("新建工单 (简化)")
        add_button.clicked.connect(self.add_record)
        action_layout.addWidget(add_button)
        action_layout.addStretch()
        main_layout.addLayout(action_layout)
        
        # Table view
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
        headers = ["ID", "工单标题", "客户ID", "负责人ID", "状态", "创建日期"]
        self.model.setHorizontalHeaderLabels(headers)

    def load_data(self):
        self.model.removeRows(0, self.model.rowCount())
        records = get_service_records()
        if not records:
            return
        for record in records:
            row = [
                QStandardItem(str(record.get("id"))),
                QStandardItem(record.get("title")),
                QStandardItem(str(record.get("customer_id"))),
                QStandardItem(str(record.get("employee_id"))),
                QStandardItem(record.get("status")),
                QStandardItem(record.get("created_at", "").split("T")[0]),
            ]
            self.model.appendRow(row)

    def add_record(self):
        # Simplified creation for demonstration
        record_data = {
            "title": "新工单",
            "customer_id": 1, # Placeholder
            "employee_id": 1, # Placeholder
        }
        new_record = create_service_record(record_data)
        if new_record:
            self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = ServiceRecordView()
    view.show()
    sys.exit(app.exec())