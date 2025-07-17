import sys
from PySide6.QtWidgets import (
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, Slot
from api.customers import get_customeromers
from api.products import get_products
from api.employees import get_employees
from api.orders import create_order
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTableView, QHeaderView, QLineEdit, QDialogButtonBox,
    QMessageBox, QSpinBox
)


class OrderCreationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("创建新订单")
        self.setMinimumSize(700, 500)

        # Store product data for easy lookup
        self.products_data = []
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # --- Customer and Salesperson Selection ---
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("选择客户:"))
        self.customer_combo = QComboBox()
        self.customer_combo.setPlaceholderText("请选择客户")
        form_layout.addWidget(self.customer_combo)
        
        form_layout.addStretch()
        
        form_layout.addWidget(QLabel("销售负责人:"))
        self.sales_combo = QComboBox()
        self.sales_combo.setPlaceholderText("当前用户")
        form_layout.addWidget(self.sales_combo)
        
        main_layout.addLayout(form_layout)
        
        # --- Product Selection ---
        product_layout = QHBoxLayout()
        product_layout.addWidget(QLabel("添加产品:"))
        self.product_combo = QComboBox()
        self.product_combo.setPlaceholderText("搜索或选择产品")
        self.product_combo.setEditable(True) # Allow searching
        self.product_combo.completer().setCompletionMode(QComboBox.CompletionMode.PopupCompletion)
        self.product_combo.completer().setFilterMode(Qt.MatchContains)
        product_layout.addWidget(self.product_combo, 1)
        
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setRange(1, 999)
        self.quantity_spinbox.setValue(1)
        product_layout.addWidget(self.quantity_spinbox)
        
        self.add_product_button = QPushButton("添加")
        product_layout.addWidget(self.add_product_button)
        
        main_layout.addLayout(product_layout)
        
        # --- Items Table ---
        self.items_table = QTableView()
        self.items_table.setAlternatingRowColors(True)
        self.items_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.items_model = QStandardItemModel()
        self.items_model.setHorizontalHeaderLabels(["产品ID", "产品名称", "数量", "单价 (参考)", "小计 (参考)"])
        self.items_table.setModel(self.items_model)
        
        self.items_table.setColumnHidden(0, True)

        main_layout.addWidget(self.items_table)
        
        # --- Total Amount Display ---
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        self.total_label = QLabel("预估总金额: ¥ 0.00")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        total_layout.addWidget(self.total_label)
        main_layout.addLayout(total_layout)
        
        # --- Dialog Buttons ---
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("创建订单")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("取消")
        main_layout.addWidget(self.button_box)
        
        # --- Connections ---
        self.add_product_button.clicked.connect(self.add_item_to_table)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        self.load_initial_data()

    def load_initial_data(self):
        """Fetches and populates initial data for combo boxes."""
        try:
            customers = get_customeromers() or []
            if customers and not isinstance(customers, dict):
                for customer in customers:
                    self.customer_combo.addItem(customer['company'], userData=customer['id'])
            
            self.products_data = get_products() or []
            if self.products_data and not isinstance(self.products_data, dict):
                for product in self.products_data:
                    self.product_combo.addItem(product['name'], userData=product['id'])
            
            employees = get_employees() or []
            if employees:
                for employee in employees:
                    self.sales_combo.addItem(employee['name'], userData=employee['id'])
        except Exception as e:
            QMessageBox.critical(self, "加载错误", f"无法加载初始化数据: {e}")

    @Slot()
    def add_item_to_table(self):
        """Adds the selected product to the items table."""
        product_index = self.product_combo.currentIndex()
        if product_index < 0:
            QMessageBox.warning(self, "选择错误", "请选择一个有效的产品。")
            return
            
        product_id = self.product_combo.itemData(product_index)
        name = self.product_combo.currentText()
        
        # Find the full product details
        product_details = next((p for p in self.products_data if p['id'] == product_id), None)
        if not product_details:
            QMessageBox.warning(self, "数据错误", "无法找到所选产品的详细信息。")
            return

        quantity = self.quantity_spinbox.value()
        unit_price = float(product_details.get("price", 0.0))
        subtotal = quantity * unit_price
        
        # Create table items
        id_item = QStandardItem(str(product_id))
        name_item = QStandardItem(name)
        quantity_item = QStandardItem(str(quantity))
        price_item = QStandardItem(f"{unit_price:.2f}")
        subtotal_item = QStandardItem(f"{subtotal:.2f}")

        # Items are not editable
        for item in [name_item, quantity_item, price_item, subtotal_item]:
            item.setEditable(False)
            
        self.items_model.appendRow([id_item, name_item, quantity_item, price_item, subtotal_item])
        self.update_total_amount()

    def update_total_amount(self):
        """Calculates and updates the total amount display."""
        total = 0.0
        for row in range(self.items_model.rowCount()):
            subtotal_item = self.items_model.item(row, 4)
            if subtotal_item:
                total += float(subtotal_item.text())
        self.total_label.setText(f"预估总金额: ¥ {total:.2f}")

    def get_order_data(self):
        """Constructs the final order data for API submission."""
        customer_id = self.customer_combo.currentData()
        sales_id = self.sales_combo.currentData()

        if not customer_id:
            QMessageBox.warning(self, "输入错误", "请选择一个客户。")
            return None
        
        if not sales_id:
            QMessageBox.warning(self, "输入错误", "请选择一个销售负责人。")
            return None

        if self.items_model.rowCount() == 0:
            QMessageBox.warning(self, "输入错误", "请至少添加一个产品到订单。")
            return None

        order_items = []
        for row in range(self.items_model.rowCount()):
            product_id = self.items_model.item(row, 0).text()
            quantity = self.items_model.item(row, 2).text()
            order_items.append({"product_id": int(product_id), "quantity": int(quantity)})

        order_data = {
            "customer_id": customer_id,
            "sales_id": sales_id,
            "order_items": order_items
        }
        return order_data

    def accept(self):
        """Handle the order creation logic."""
        order_data = self.get_order_data()
        if not order_data:
            return # Don't close the dialog if data is invalid

        result = create_order(order_data)

        if result and 'id' in result:
            QMessageBox.information(self, "成功", f"订单创建成功！订单号: {result.get('order_number')}")
            super().accept()
        else:
            QMessageBox.critical(self, "失败", f"订单创建失败: {result}")
        
# --- For testing purposes ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # This is for standalone testing.
    # In the real app, we'd pass real data.
    dialog = OrderCreationDialog()
    dialog.show()
    sys.exit(app.exec())