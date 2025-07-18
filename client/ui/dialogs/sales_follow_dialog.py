"""
销售跟进对话框
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QTextEdit, QDialogButtonBox, QMessageBox, QDateTimeEdit,
    QLabel, QSpinBox, QCheckBox
)
from PySide6.QtCore import Qt, QDateTime
from typing import Dict, Any, Optional

class SalesFollowDialog(QDialog):
    """销售跟进对话框"""
    
    def __init__(self, follow_data: Optional[Dict[str, Any]] = None, customer_data: Optional[Dict[str, Any]] = None, parent=None):
        super().__init__(parent)
        self.follow_data = follow_data
        self.customer_data = customer_data
        
        self.setWindowTitle("销售跟进记录" if follow_data else "添加跟进记录")
        self.setMinimumSize(500, 400)
        
        self.setup_ui()
        
        if follow_data:
            self.load_follow_data()
        elif customer_data:
            self.load_customer_info()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 客户信息区域（只读）
        if self.customer_data:
            self.setup_customer_info_section(layout)
        
        # 跟进信息表单
        form_layout = QFormLayout()
        
        # 跟进类型
        self.follow_type_combo = QComboBox()
        self.follow_type_combo.addItems([
            "电话沟通", "邮件联系", "上门拜访", "会议讨论", 
            "产品演示", "报价提交", "合同谈判", "其他"
        ])
        form_layout.addRow("跟进类型 *:", self.follow_type_combo)
        
        # 跟进时间
        self.follow_time_edit = QDateTimeEdit()
        self.follow_time_edit.setDateTime(QDateTime.currentDateTime())
        self.follow_time_edit.setCalendarPopup(True)
        form_layout.addRow("跟进时间 *:", self.follow_time_edit)
        
        # 联系人
        self.contact_person_edit = QLineEdit()
        self.contact_person_edit.setPlaceholderText("请输入联系人姓名")
        form_layout.addRow("联系人:", self.contact_person_edit)
        
        # 沟通内容
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("请详细描述本次跟进的内容...")
        self.content_edit.setMinimumHeight(100)
        form_layout.addRow("沟通内容 *:", self.content_edit)
        
        # 客户反馈
        self.feedback_edit = QTextEdit()
        self.feedback_edit.setPlaceholderText("请记录客户的反馈和意见...")
        self.feedback_edit.setMinimumHeight(80)
        form_layout.addRow("客户反馈:", self.feedback_edit)
        
        # 下次跟进时间
        self.next_follow_time_edit = QDateTimeEdit()
        self.next_follow_time_edit.setDateTime(QDateTime.currentDateTime().addDays(7))
        self.next_follow_time_edit.setCalendarPopup(True)
        form_layout.addRow("下次跟进时间:", self.next_follow_time_edit)
        
        # 重要程度
        self.priority_combo = QComboBox()
        self.priority_combo.addItem("低", 1)
        self.priority_combo.addItem("中", 2)
        self.priority_combo.addItem("高", 3)
        self.priority_combo.addItem("紧急", 4)
        self.priority_combo.setCurrentIndex(1)  # 默认中等
        form_layout.addRow("重要程度:", self.priority_combo)
        
        # 预计成交概率
        self.success_rate_spin = QSpinBox()
        self.success_rate_spin.setRange(0, 100)
        self.success_rate_spin.setSuffix("%")
        self.success_rate_spin.setValue(50)
        form_layout.addRow("成交概率:", self.success_rate_spin)
        
        # 预计成交金额
        self.estimated_amount_edit = QLineEdit()
        self.estimated_amount_edit.setPlaceholderText("请输入预计成交金额")
        form_layout.addRow("预计金额:", self.estimated_amount_edit)
        
        # 是否需要提醒
        self.need_reminder_checkbox = QCheckBox("设置提醒")
        self.need_reminder_checkbox.setChecked(True)
        form_layout.addRow("提醒设置:", self.need_reminder_checkbox)
        
        layout.addLayout(form_layout)
        
        # 按钮区域
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def setup_customer_info_section(self, layout):
        """设置客户信息区域"""
        customer_info_widget = QLabel()
        customer_info_widget.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)
        
        customer_name = self.customer_data.get('company', '未知客户')
        customer_status = self.customer_data.get('status', '')
        customer_industry = self.customer_data.get('industry', '')
        
        info_text = f"客户: {customer_name} | 行业: {customer_industry} | 状态: {customer_status}"
        customer_info_widget.setText(info_text)
        
        layout.addWidget(customer_info_widget)
    
    def load_follow_data(self):
        """加载跟进数据"""
        if not self.follow_data:
            return
        
        # 设置跟进类型
        follow_type = self.follow_data.get('follow_type', '')
        index = self.follow_type_combo.findText(follow_type)
        if index >= 0:
            self.follow_type_combo.setCurrentIndex(index)
        
        # 设置跟进时间
        follow_time = self.follow_data.get('follow_time')
        if follow_time:
            self.follow_time_edit.setDateTime(QDateTime.fromString(follow_time, Qt.DateFormat.ISODate))
        
        # 设置其他字段
        self.contact_person_edit.setText(self.follow_data.get('contact_person', ''))
        self.content_edit.setPlainText(self.follow_data.get('content', ''))
        self.feedback_edit.setPlainText(self.follow_data.get('feedback', ''))
        
        # 设置下次跟进时间
        next_follow_time = self.follow_data.get('next_follow_time')
        if next_follow_time:
            self.next_follow_time_edit.setDateTime(QDateTime.fromString(next_follow_time, Qt.DateFormat.ISODate))
        
        # 设置重要程度
        priority = self.follow_data.get('priority', 2)
        index = self.priority_combo.findData(priority)
        if index >= 0:
            self.priority_combo.setCurrentIndex(index)
        
        # 设置成交概率
        success_rate = self.follow_data.get('success_rate', 50)
        self.success_rate_spin.setValue(success_rate)
        
        # 设置预计金额
        estimated_amount = self.follow_data.get('estimated_amount', '')
        self.estimated_amount_edit.setText(str(estimated_amount) if estimated_amount else '')
        
        # 设置提醒
        need_reminder = self.follow_data.get('need_reminder', True)
        self.need_reminder_checkbox.setChecked(need_reminder)
    
    def load_customer_info(self):
        """加载客户信息"""
        if not self.customer_data:
            return
        
        # 可以根据客户信息预填一些字段
        # 比如根据客户状态设置默认的成交概率
        status = self.customer_data.get('status', '')
        if status == 'LEAD':
            self.success_rate_spin.setValue(20)
        elif status == 'CONTACTED':
            self.success_rate_spin.setValue(30)
        elif status == 'PROPOSAL':
            self.success_rate_spin.setValue(60)
        elif status == 'NEGOTIATION':
            self.success_rate_spin.setValue(80)
    
    def get_follow_data(self) -> Dict[str, Any]:
        """获取跟进数据"""
        data = {
            'follow_type': self.follow_type_combo.currentText(),
            'follow_time': self.follow_time_edit.dateTime().toString(Qt.DateFormat.ISODate),
            'contact_person': self.contact_person_edit.text().strip(),
            'content': self.content_edit.toPlainText().strip(),
            'feedback': self.feedback_edit.toPlainText().strip(),
            'next_follow_time': self.next_follow_time_edit.dateTime().toString(Qt.DateFormat.ISODate),
            'priority': self.priority_combo.currentData(),
            'success_rate': self.success_rate_spin.value(),
            'need_reminder': self.need_reminder_checkbox.isChecked()
        }
        
        # 预计金额
        estimated_amount = self.estimated_amount_edit.text().strip()
        if estimated_amount:
            try:
                data['estimated_amount'] = float(estimated_amount)
            except ValueError:
                data['estimated_amount'] = 0
        
        # 如果有客户数据，添加客户ID
        if self.customer_data:
            data['customer_id'] = self.customer_data.get('id')
        
        return data
    
    def validate(self) -> bool:
        """验证数据"""
        # 验证必填字段
        if not self.content_edit.toPlainText().strip():
            QMessageBox.warning(self, "验证失败", "请输入沟通内容")
            self.content_edit.setFocus()
            return False
        
        # 验证预计金额格式
        estimated_amount = self.estimated_amount_edit.text().strip()
        if estimated_amount:
            try:
                float(estimated_amount)
            except ValueError:
                QMessageBox.warning(self, "验证失败", "预计金额格式不正确")
                self.estimated_amount_edit.setFocus()
                return False
        
        return True
    
    def accept(self):
        """确认按钮"""
        if self.validate():
            super().accept()

class AssignSalesDialog(QDialog):
    """分配销售对话框"""
    
    def __init__(self, customers: List[Dict[str, Any]], parent=None):
        super().__init__(parent)
        self.customers = customers
        
        self.setWindowTitle("分配销售负责人")
        self.setMinimumWidth(400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 客户信息
        info_label = QLabel(f"将为 {len(self.customers)} 个客户分配销售负责人")
        info_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # 表单
        form_layout = QFormLayout()
        
        # 销售人员选择
        self.sales_combo = QComboBox()
        self.sales_combo.addItem("请选择销售人员", None)
        
        # 这里应该从API加载销售人员列表
        # 暂时使用模拟数据
        sample_sales = [
            {"id": 1, "name": "张三"},
            {"id": 2, "name": "李四"},
            {"id": 3, "name": "王五"},
        ]
        
        for sales in sample_sales:
            self.sales_combo.addItem(sales['name'], sales['id'])
        
        form_layout.addRow("销售负责人 *:", self.sales_combo)
        
        # 备注
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("请输入分配说明...")
        self.notes_edit.setMaximumHeight(80)
        form_layout.addRow("分配说明:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_assignment_data(self) -> Dict[str, Any]:
        """获取分配数据"""
        return {
            'sales_id': self.sales_combo.currentData(),
            'customer_ids': [customer.get('id') for customer in self.customers],
            'notes': self.notes_edit.toPlainText().strip()
        }
    
    def validate(self) -> bool:
        """验证数据"""
        if not self.sales_combo.currentData():
            QMessageBox.warning(self, "验证失败", "请选择销售负责人")
            self.sales_combo.setFocus()
            return False
        
        return True
    
    def accept(self):
        """确认按钮"""
        if self.validate():
            super().accept()

# 导出
__all__ = ['SalesFollowDialog', 'AssignSalesDialog']
