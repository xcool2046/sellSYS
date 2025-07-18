"""
通用UI组件
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, 
    QLineEdit, QComboBox, QHeaderView, QMessageBox, QLabel,
    QDialog, QFormLayout, QDialogButtonBox, QTextEdit, QSpinBox,
    QDateEdit, QCheckBox, QGroupBox, QScrollArea
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide6.QtCore import Qt, Signal, QDate
from typing import List, Dict, Any, Optional

class SearchToolbar(QWidget):
    """搜索工具栏组件"""
    
    search_requested = Signal(dict)  # 搜索请求信号
    reset_requested = Signal()      # 重置请求信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters = {}
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入关键词搜索...")
        self.search_input.setFixedHeight(35)
        layout.addWidget(self.search_input)
        
        # 筛选器容器
        self.filters_layout = QHBoxLayout()
        layout.addLayout(self.filters_layout)
        
        # 按钮
        self.search_btn = QPushButton("搜索")
        self.search_btn.setFixedHeight(35)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(self.search_btn)
        
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setFixedHeight(35)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        layout.addWidget(self.reset_btn)
        
        layout.addStretch()
        
        # 连接信号
        self.search_btn.clicked.connect(self.on_search_clicked)
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        self.search_input.returnPressed.connect(self.on_search_clicked)
    
    def add_filter(self, name: str, widget: QWidget):
        """添加筛选器"""
        self.filters[name] = widget
        self.filters_layout.addWidget(widget)
    
    def add_combo_filter(self, name: str, label: str, options: List[tuple]) -> QComboBox:
        """添加下拉筛选器"""
        combo = QComboBox()
        combo.setFixedHeight(35)
        combo.addItem(label, None)
        
        for text, value in options:
            combo.addItem(text, value)
        
        self.add_filter(name, combo)
        return combo
    
    def get_search_params(self) -> Dict[str, Any]:
        """获取搜索参数"""
        params = {}
        
        # 搜索关键词
        search_text = self.search_input.text().strip()
        if search_text:
            params['search'] = search_text
        
        # 筛选器参数
        for name, widget in self.filters.items():
            if isinstance(widget, QComboBox):
                value = widget.currentData()
                if value is not None:
                    params[name] = value
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
                if value:
                    params[name] = value
        
        return params
    
    def clear_filters(self):
        """清空筛选器"""
        self.search_input.clear()
        
        for widget in self.filters.values():
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QLineEdit):
                widget.clear()
    
    def on_search_clicked(self):
        """搜索按钮点击"""
        params = self.get_search_params()
        self.search_requested.emit(params)
    
    def on_reset_clicked(self):
        """重置按钮点击"""
        self.clear_filters()
        self.reset_requested.emit()

class ActionToolbar(QWidget):
    """操作工具栏组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = {}
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.layout.addStretch()
    
    def add_button(self, name: str, text: str, style: str = "primary") -> QPushButton:
        """添加按钮"""
        button = QPushButton(text)
        button.setFixedHeight(35)
        
        # 设置样式
        styles = {
            "primary": """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """,
            "success": """
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
            """,
            "warning": """
                QPushButton {
                    background-color: #f39c12;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e67e22;
                }
            """,
            "danger": """
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """
        }
        
        button.setStyleSheet(styles.get(style, styles["primary"]))
        
        self.buttons[name] = button
        self.layout.insertWidget(self.layout.count() - 1, button)
        
        return button
    
    def get_button(self, name: str) -> Optional[QPushButton]:
        """获取按钮"""
        return self.buttons.get(name)

class DataTable(QWidget):
    """数据表格组件"""
    
    row_double_clicked = Signal(int, dict)  # 行双击信号
    selection_changed = Signal(list)        # 选择变化信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.headers = []
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 表格
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        
        # 设置表格属性
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        
        # 设置样式
        self.table_view.setStyleSheet("""
            QTableView {
                gridline-color: #bdc3c7;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table_view)
        
        # 连接信号
        self.table_view.doubleClicked.connect(self.on_row_double_clicked)
        self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
    
    def set_headers(self, headers: List[str]):
        """设置表头"""
        self.headers = headers
        self.model.setHorizontalHeaderLabels(headers)
    
    def set_data(self, data: List[Dict[str, Any]]):
        """设置数据"""
        self.data = data
        self.update_view()
    
    def update_view(self):
        """更新视图"""
        self.model.clear()
        if self.headers:
            self.model.setHorizontalHeaderLabels(self.headers)
        
        for row_data in self.data:
            items = []
            for header in self.headers:
                value = row_data.get(header.lower().replace(' ', '_'), '')
                items.append(QStandardItem(str(value)))
            
            # 设置项不可编辑
            for item in items:
                item.setEditable(False)
            
            self.model.appendRow(items)
    
    def get_selected_rows(self) -> List[int]:
        """获取选中的行"""
        selection = self.table_view.selectionModel().selectedRows()
        return [index.row() for index in selection]
    
    def get_selected_data(self) -> List[Dict[str, Any]]:
        """获取选中的数据"""
        selected_rows = self.get_selected_rows()
        return [self.data[row] for row in selected_rows if row < len(self.data)]
    
    def on_row_double_clicked(self, index):
        """行双击事件"""
        if index.isValid():
            row = index.row()
            if row < len(self.data):
                self.row_double_clicked.emit(row, self.data[row])
    
    def on_selection_changed(self):
        """选择变化事件"""
        selected_data = self.get_selected_data()
        self.selection_changed.emit(selected_data)

class BaseDialog(QDialog):
    """基础对话框"""
    
    def __init__(self, title: str = "对话框", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 内容区域
        self.content_widget = QWidget()
        self.content_layout = QFormLayout(self.content_widget)
        layout.addWidget(self.content_widget)
        
        # 按钮区域
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
    
    def add_field(self, label: str, widget: QWidget):
        """添加字段"""
        self.content_layout.addRow(label, widget)
    
    def accept(self):
        """确认按钮"""
        if self.validate():
            super().accept()
    
    def validate(self) -> bool:
        """验证数据"""
        return True

# 导出所有组件
__all__ = ['SearchToolbar', 'ActionToolbar', 'DataTable', 'BaseDialog']
