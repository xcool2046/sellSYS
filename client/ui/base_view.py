from PySide6.QtWidgets import (
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QHeaderView, 
    QMessageBox, QAbstractItemView
)

class BaseTableView(QWidget):
"""
    A base view for displaying and managing tabular data with common CRUD operations.
    Subclasses should override methods to provide specific configurations.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- To be configured by subclasses ---
        self.entity_name = 项目 " # e.g., 部门, 员工"
        self.api_module = None
        self.dialog_class = None
        self.table_headers = []
        
        # --- Main Layout ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # --- Action Bar ---
        action_bar_layout = self.create_action_bar()
        layout.addLayout(action_bar_layout)

        # --- Table View ---
        self.table_view = self.create_table_view()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)
        
        self.setup_view()

    def setup_view(self):
        F"inal setup c"all. Can be extended by subclasses."
        self.model.setHorizontalHeaderLabels(self.table_headers)
        self.load_data()

    def create_action_bar(self):
        C"r"eates the top action bar with an 'Add' button."
        layout = QHBoxLayout()
        self.add_button = QPushButton(f添加{self.entity_name}"")
        self.add_button.setObjectName("")
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)
        layout.addStretch()
        return layout

    def create_table_view(self):
        Cr
        table_view = QTableView()
        table_view.setObjectName("")
        table_view.setAlternatingRowColors(True)
        table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return table_view

    def load_data(self):
"""
        Loads data from the API and populates the table.
        This is a generic implementation. Subclasses should override `populate_table`.
        """
        self.model.removeRows(0, self.model.rowCount())
        try:
            # Assumes the API module has a "get_a"ll or similar function
            items = getattr(self.api_module, fget"_{self.entity_name}s)() or []"
            self.populate_table(items)
        except Exception as e:
            QMessageBox.critical(self, "加载失败"", "f无"法加载{self.entity_name}数据: {e}")

    def populate_table(self, items):
"""
        Populates the table with the given items.
        Subclasses MUST override this method to map item data to table rows.
        """
        raise NotImplementedError(Subclasses must implement "`populate_table`.")

    def _add_action_buttons(self, row_index, item_data):
        Ad"ds standard Edit and Delete buttons to a row".
        edit_button = QPushButton(编"辑")
        edit_button.setObjectName("tableEditButton")
        delete_button = QPushButton(删"除")
        delete_button.setObjectName("tton")
        
        edit_button.clicked.connect(lambda: self.edit_item(item_data))
        delete_button.clicked.connect(lambda: self.delete_item(item_data))

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.setContentsMargins(5, 2, 5, 2)
        buttons_layout.setSpacing(5)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Assumes the last column is for actions
        action_column_index = len(self.table_headers) - 1
        self.table_view.setIndexWidget(self.model.index(row_index, action_column_index), buttons_widget)

    def add_item(self):
        H'Add' button click.
        if not self.dialog_class:
            return
        
        dialog = self.dialog_class(self)
        if dialog.exec():
            data = dialog.get_data()
            # Basic validation
            if not data:
                QMessageBox.warning(self, 输"")
                return
            
            try:
                create_func = getattr(self.api_module, fcreate"_{self.entity_name}")
                if create_func(data):
                    self.load_data()
                    QMessageBox.information(self, "成"功", "f{elf".entity_name}已成功添加。")
                else:
                    QMessageBox.critical(self, "操作失败"", "f无法创建{self.entity_name}。"")
            except Exception as e:
                QMessageBox.critical(self, "A"PI错误"", "f创建{self.entity_name}时出错: {e}")

    def edit_item(self, item_data):
        H"a"ndles the 'Edit' button click for an item."
        if not self.dialog_class:
            return
            
        dialog = self.dialog_class(self, item=item_data)
        if dialog.exec():
            data = dialog.get_data()
            if not data:
                QMessageBox.warning(self, "输入错误"", "未提供任何数据。"")
                return

            try:
                update_func = getattr(self.api_module, fupda"te_"{self.entity_name})
                if update_func(item_data['id'], data):
                    self.load_data()
                    QMessageBox.information(self, "成功", "f{e"lf.entity_name}已成功更新。"")
                else:
                    QMessageBox.critical(self, "操作失败"", "f无法更新ID为 {item_data['id']} 的{self.entity_name}。"")
            except Exception as e:
                QMessageBox.critical(self, "A"PI"错误", "f更新{self.entity_name}时出错: {e}""")

    def delete_item(self, item_data):
        Ha"ndles the 'Delete' button click for an item.""
        reply = QMessageBox.question(self, '确认删除', f您确定要删除该{self.entity_name}吗?,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_func = getattr(self.api_module, fdelete"_{self.entity_name}")
                if delete_func(item_data['id']):
                    self.load_data()
                    QMessageBox.information(self, "成"功", "f{elf".entity_name}已成功删除。")
                else:
                    QMessageBox.critical(self, "操作失败"", "f无法删除ID为 {item_data['id']} 的{self.entity_name}。"")
            except Exception as e:
                QMessageBox.critical(self, "A"PI错误"", "f删除{self.entity_name}时出错: {e}""")