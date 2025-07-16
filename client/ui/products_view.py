from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableView,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QHeaderView,
    QMessageBox,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from api import products as products_api
from .product_dialog import ProductDialog

class ProductsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("产品管理")
        self.products_data = []  # 存储产品数据

        # --- Layouts ---
        main_layout = QVBoxLayout(self)
        top_bar_layout = QHBoxLayout()
        
        # --- Widgets ---
        self.add_product_button = QPushButton("➕ 添加产品")
        self.table_view = QTableView()
        
        # --- Top Bar ---
        top_bar_layout.addWidget(self.add_product_button)
        top_bar_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # --- Table View ---
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        # --- Assembly ---
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(self.table_view)
        
        # --- Connections ---
        self.add_product_button.clicked.connect(self.handle_add_product)
        
        # --- Initialization ---
        self.setup_table_headers()
        self.load_data()

    def setup_table_headers(self):
        """设置表格标题"""
        headers = [
            "ID", "产品名称", "型号规格", "计量单位", "产品定价", 
            "最低控价", "销售提成", "主管提成", "经理提成", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)

    def load_data(self):
        """从API加载数据并填充表格"""
        self.model.removeRows(0, self.model.rowCount())
        self.products_data = products_api.get_products()
        if not self.products_data:
            self.products_data = []
            return

        for i, product in enumerate(self.products_data):
            row_items = [
                QStandardItem(str(product.get("id", ""))),
                QStandardItem(product.get("name", "N/A")),
                QStandardItem(product.get("spec", "N/A")),
                QStandardItem(product.get("unit", "N/A")),
                QStandardItem(f"{float(product.get('base_price', 0)):.2f}"),
                QStandardItem(f"{float(product.get('real_price', 0)):.2f}"),
                QStandardItem(f"{float(product.get('sales_commission', 0)):.2f}"),
                QStandardItem(f"{float(product.get('manager_commission', 0)):.2f}"),
                QStandardItem(f"{float(product.get('director_commission', 0)):.2f}"),
            ]
            self.model.appendRow(row_items)

            # --- 操作按钮 ---
            edit_button = QPushButton("编辑")
            delete_button = QPushButton("删除")
            edit_button.setProperty("product_id", product["id"])
            delete_button.setProperty("product_id", product["id"])
            edit_button.setProperty("product_row", i)
            delete_button.setProperty("product_row", i)
            edit_button.clicked.connect(self.handle_edit_product)
            delete_button.clicked.connect(self.handle_delete_product)

            button_layout = QHBoxLayout()
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button_container = QWidget()
            button_container.setLayout(button_layout)
            
            self.table_view.setIndexWidget(self.model.index(i, 9), button_container)

    def refresh_data(self):
        """刷新数据"""
        self.load_data()
    
    def handle_add_product(self):
        """处理添加产品"""
        dialog = ProductDialog(self)
        if dialog.exec():
            self.refresh_data()
    
    def handle_edit_product(self):
        """处理编辑产品"""
        sender = self.sender()
        product_id = sender.property("product_id")
        product_row = sender.property("product_row")
        
        if product_row is not None and product_row < len(self.products_data):
            product_data = self.products_data[product_row]
            dialog = ProductDialog(self, product_data)
            if dialog.exec():
                self.refresh_data()
    
    def handle_delete_product(self):
        """处理删除产品"""
        sender = self.sender()
        product_id = sender.property("product_id")
        product_row = sender.property("product_row")
        
        if product_row is not None and product_row < len(self.products_data):
            product_data = self.products_data[product_row]
            
            # 确认对话框
            reply = QMessageBox.question(
                self,
                "确认删除",
                f"确定要删除产品 '{product_data.get('name', '')}' 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 调用API删除产品
                if products_api.delete_product(product_id):
                    QMessageBox.information(self, "成功", "产品删除成功！")
                    self.refresh_data()
                else:
                    QMessageBox.critical(self, "错误", "产品删除失败！")