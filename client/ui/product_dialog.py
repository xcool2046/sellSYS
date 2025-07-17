from PySide6.QtWidgets import (
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from decimal import Decimal
from typing import Optional
from api.products import create_product, update_product
from schemas.product import Product
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QMessageBox,
    QDialogButtonBox
)



class ProductDialog(QDialog):
    """产品添加/编辑对话框"""
    
    def __init__(self, parent=None, product: Optional[Product] = None):
        super().__init__(parent)
        self.product = product
        self.setup_ui()
        
        if product:
            self.load_product_data()
    
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("编辑产品" if self.product else "添加产品")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        # 主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 表单布局
        form_layout = QFormLayout()
        
        # 产品名称
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(100)
        form_layout.addRow("产品名称:", self.name_edit)
        
        # 产品代码
        self.code_edit = QLineEdit()
        self.code_edit.setMaxLength(50)
        form_layout.addRow("产品代码:", self.code_edit)
        
        # 型号规格
        self.spec_edit = QLineEdit()
        self.spec_edit.setMaxLength(100)
        form_layout.addRow("型号规格:", self.spec_edit)
        
        # 单位
        self.unit_edit = QLineEdit()
        self.unit_edit.setMaxLength(20)
        form_layout.addRow("单位:", self.unit_edit)
        
        # 供应商报价
        self.supplier_price_edit = QLineEdit()
        price_validator = QDoubleValidator(0.0, 999999999.99, 2)
        price_validator.setNotation(QDoubleValidator.StandardNotation)
        self.supplier_price_edit.setValidator(price_validator)
        form_layout.addRow("供应商报价:", self.supplier_price_edit)
        
        # 报价
        self.price_edit = QLineEdit()
        self.price_edit.setValidator(price_validator)
        form_layout.addRow("报价:", self.price_edit)
        
        # 提成
        self.commission_edit = QLineEdit()
        self.commission_edit.setValidator(price_validator)
        form_layout.addRow("提成:", self.commission_edit)
        
        # 描述
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("描述:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # 设置焦点
        self.name_edit.setFocus()
    
    def load_product_data(self):
        """加载产品数据到表单"""
        if not self.product:
            return
            
        self.name_edit.setText(self.product.name)
        self.code_edit.setText(self.product.code or "")
        self.spec_edit.setText(self.product.spec or "")
        self.unit_edit.setText(self.product.unit or "")
        
        if self.product.supplier_price:
            self.supplier_price_edit.setText(str(self.product.supplier_price))
        if self.product.price:
            self.price_edit.setText(str(self.product.price))
        if self.product.commission:
            self.commission_edit.setText(str(self.product.commission))
            
        self.description_edit.setPlainText(self.product.description or "")
    
    def get_product_data(self) -> dict:
        """从表单获取产品数据"""
        data = {
            "name": self.name_edit.text().strip(),
            "code": self.code_edit.text().strip() or None,
            "spec": self.spec_edit.text().strip() or None,
            "unit": self.unit_edit.text().strip() or None,
            "description": self.description_edit.toPlainText().strip() or None
        }
        
        # 处理价格字段
        supplier_price_text = self.supplier_price_edit.text().strip()
        if supplier_price_text:
            data["supplier_price"] = float(supplier_price_text)
        else:
            data["supplier_price"] = None
            
        price_text = self.price_edit.text().strip()
        if price_text:
            data["price"] = float(price_text)
        else:
            data["price"] = None
            
        commission_text = self.commission_edit.text().strip()
        if commission_text:
            data["commission"] = float(commission_text)
        else:
            data["commission"] = None
        
        return data
    
    def accept(self):
        """保存产品"""
        # 验证必填字段
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "警告", "请输入产品名称")
            self.name_edit.setFocus()
            return
        
        try:
            data = self.get_product_data()
            
            if self.product:
                # 更新产品
                success, result = update_product(self.product.id, data)
            else:
                # 创建产品
                success, result = create_product(data)
            
            if success:
                QMessageBox.information(
                    self, 
                    "成功", 
                    "产品已保存" if self.product else "产品已创建"
                )
                super().accept()
            else:
                QMessageBox.critical(self, "错误", f"保存失败: {result}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"发生错误: {str(e)}")
