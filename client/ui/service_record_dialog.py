import sys
from PySide6.QtWidgets import (
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from api import service_records as service_records_api
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableView, QHeaderView, QTextEdit, QDialogButtonBox,
    QMessageBox
)


class ServiceRecordDialog(QDialog):
    def __init__(self, customer_id, parent=None):
        super().__init__(parent)
        self.customer_id = customer_id
        self.setWindowTitle(f"客户ID: {customer_id} - 客服记录")
        self.setMinimumSize(800, 600)

        main_layout = QVBoxLayout(self)

        # 表格
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "标题", "状态", "创建时间", "处理人"])
        self.table_view.setModel(self.model)
        self.table_view.setColumnHidden(0, True)

        main_layout.addWidget(self.table_view)

        # 添加新记录的表单
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("新增客服记录:"))
        self.feedback_input = QTextEdit()
        self.feedback_input.setPlaceholderText("输入客户反馈...")
        self.response_input = QTextEdit()
        self.response_input.setPlaceholderText("输入我方响应...")
        
        form_layout.addWidget(self.feedback_input)
        form_layout.addWidget(self.response_input)
        
        self.add_record_button = QPushButton("添加记录")
        form_layout.addWidget(self.add_record_button, alignment=Qt.AlignRight)
        
        main_layout.addLayout(form_layout)

        # 对话框按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.button(QDialogButtonBox.StandardButton.Close).setText("关闭")
        main_layout.addWidget(button_box)

        # 连接信号
        self.add_record_button.clicked.connect(self.add_new_record)
        button_box.rejected.connect(self.reject)

        self.load_records()

    def load_records(self):
        """加载客服记录"""
        self.model.removeRows(0, self.model.rowCount())
        records = service_records_api.get_service_records({'customer_id': self.customer_id})
        if records:
            for record in records:
                row = [
                    QStandardItem(str(record.get("id"))),
                    QStandardItem(record.get("title", "")),
                    QStandardItem(record.get("status", "")),
                    QStandardItem(record.get("created_at", "").split("T")[0]),
                    QStandardItem(str(record.get("employee_id", ""))), # 稍后替换为员工姓名
                ]
                self.model.appendRow(row)

    def add_new_record(self):
        """添加新的客服记录"""
        feedback = self.feedback_input.toPlainText().strip()
        response = self.response_input.toPlainText().strip()

        if not feedback:
            QMessageBox.warning(self, "输入错误", "客户反馈不能为空。")
            return

        record_data = {
            "customer_id": self.customer_id,
            "title": feedback[:20],  # 使用反馈的前20个字符作为标题
            "feedback": feedback,
            "response": response,
            "status": "待处理" # 默认为待处理
        }

        new_record = service_records_api.create_service_record(record_data)
        if new_record:
            QMessageBox.information(self, "成功", "客服记录添加成功。")
            self.feedback_input.clear()
            self.response_input.clear()
            self.load_records()
        else:
            QMessageBox.critical(self, "失败", "添加客服记录失败。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 模拟一个 customer_id
    dialog = ServiceRecordDialog(customer_id=1)
    dialog.exec()
    sys.exit(app.exec())