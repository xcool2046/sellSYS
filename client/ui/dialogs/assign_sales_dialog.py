"""
分配销售对话框 - 按照原型图设计
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, 
    QComboBox, QLabel, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from typing import Dict, Any, List

class AssignSalesDialog(QDialog):
    """分配销售对话框"""
    
    def __init__(self, customer_data: Dict[str, Any] = None, parent=None):
        super().__init__(parent)
        self.customer_data = customer_data or {}
        
        self.setup_ui()
        self.setup_connections()
        self.load_data()
        
        # 设置窗口属性
        self.setWindowTitle("分配销售")
        self.setModal(True)
        self.setFixedSize(400, 300)
    
    def setup_ui(self):
        """设置用户界面"""
        # 设置对话框样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
                color: #333333;
            }
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 3px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
                color: #333333;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #007bff;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ced4da;
                background-color: white;
                color: #333333;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                color: #333333;
                background-color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f8f9fa;
                color: #333333;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 12px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 80px;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏
        title_label = QLabel("分配销售")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #4a90e2;
                padding: 15px 20px;
                margin: 0;
            }
        """)
        main_layout.addWidget(title_label)
        
        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        
        # 分配给销售标题
        assign_label = QLabel("分配给销售:")
        assign_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333333;")
        content_layout.addWidget(assign_label)
        
        # 表单区域
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)
        
        # 部门名称
        dept_row = QWidget()
        dept_layout = QHBoxLayout(dept_row)
        dept_layout.setContentsMargins(0, 0, 0, 0)
        dept_layout.setSpacing(10)
        
        dept_label = QLabel("部门名称:")
        dept_label.setFixedWidth(80)
        dept_layout.addWidget(dept_label)
        
        self.dept_label_value = QLabel("销售部")
        self.dept_label_value.setStyleSheet("color: #333333; font-weight: normal;")
        dept_layout.addWidget(self.dept_label_value)
        dept_layout.addStretch()
        
        form_layout.addWidget(dept_row)
        
        # 组别名称
        group_row = QWidget()
        group_layout = QHBoxLayout(group_row)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(10)
        
        group_label = QLabel("组别名称:")
        group_label.setFixedWidth(80)
        group_layout.addWidget(group_label)
        
        self.group_combo = QComboBox()
        self.group_combo.addItem("销售一组", "sales_group_1")
        self.group_combo.addItem("销售二组", "sales_group_2")
        self.group_combo.addItem("销售三组", "sales_group_3")
        group_layout.addWidget(self.group_combo)
        
        form_layout.addWidget(group_row)
        
        # 销售姓名
        sales_row = QWidget()
        sales_layout = QHBoxLayout(sales_row)
        sales_layout.setContentsMargins(0, 0, 0, 0)
        sales_layout.setSpacing(10)
        
        sales_label = QLabel("销售姓名:")
        sales_label.setFixedWidth(80)
        sales_layout.addWidget(sales_label)
        
        self.sales_combo = QComboBox()
        self.sales_combo.addItem("张飞", "zhang_fei")
        self.sales_combo.addItem("李明", "li_ming")
        self.sales_combo.addItem("王强", "wang_qiang")
        self.sales_combo.addItem("刘德华", "liu_dehua")
        sales_layout.addWidget(self.sales_combo)
        
        form_layout.addWidget(sales_row)
        
        content_layout.addWidget(form_widget)
        content_layout.addStretch()
        
        # 按钮区域
        self.setup_buttons(content_layout)
        
        main_layout.addWidget(content_widget)
    
    def setup_buttons(self, main_layout):
        """设置按钮区域"""
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.addStretch()
        
        # 取消按钮
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        button_layout.addWidget(self.cancel_btn)
        
        # 分配按钮
        self.assign_btn = QPushButton("分配")
        self.assign_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        button_layout.addWidget(self.assign_btn)
        
        main_layout.addLayout(button_layout)
    
    def setup_connections(self):
        """设置信号连接"""
        self.cancel_btn.clicked.connect(self.reject)
        self.assign_btn.clicked.connect(self.accept)
        self.group_combo.currentTextChanged.connect(self.on_group_changed)
    
    def on_group_changed(self, group_name: str):
        """组别变化事件"""
        # 根据组别更新销售人员列表
        self.sales_combo.clear()
        
        if "一组" in group_name:
            self.sales_combo.addItem("张飞", "zhang_fei")
            self.sales_combo.addItem("李明", "li_ming")
        elif "二组" in group_name:
            self.sales_combo.addItem("王强", "wang_qiang")
            self.sales_combo.addItem("赵六", "zhao_liu")
        elif "三组" in group_name:
            self.sales_combo.addItem("刘德华", "liu_dehua")
            self.sales_combo.addItem("陈小明", "chen_xiaoming")
    
    def load_data(self):
        """加载数据"""
        # 可以根据客户数据预设一些值
        pass
    
    def get_assignment_data(self) -> Dict[str, Any]:
        """获取分配数据"""
        return {
            'department': '销售部',
            'group': self.group_combo.currentText(),
            'group_id': self.group_combo.currentData(),
            'sales_person': self.sales_combo.currentText(),
            'sales_person_id': self.sales_combo.currentData()
        }

# 导出
__all__ = ['AssignSalesDialog']
