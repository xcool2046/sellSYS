import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableView, QHeaderView, QLineEdit, QComboBox,
    QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from PySide6.QtCore import Qt

from ..api import service_records as service_records_api
from ..api import customers as customers_api
from ..api import employees as employees_api
from ..api import contacts as contacts_api

from .contact_view_dialog import ContactViewDialog
from .service_record_dialog import ServiceRecordDialog

class ServiceRecordView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("售后服务")
        
        # 存储数据
        self.customer_service_data_map = {} # 用于存储按行索引的客户数据
        self.customers_data = []
        self.employees_data = []
        self.all_service_records = []
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 筛选栏
        self.setup_filter_section(main_layout)
        
        # 表格内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 表格
        self.setup_table_view(content_layout)
        
        main_layout.addWidget(content_widget)
        
        # 初始化数据
        self.load_initial_data()
        
    def setup_filter_section(self, main_layout):
        """设置筛选栏"""
        filter_widget = QWidget()
        filter_widget.setObjectName("filterSection")
        filter_widget.setFixedHeight(70)
        filter_layout = QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(20, 15, 20, 15)
        filter_layout.setSpacing(10)
        
        # 客户单位名称输入框
        self.customer_name_filter = QLineEdit()
        self.customer_name_filter.setPlaceholderText("客户单位名称")
        self.customer_name_filter.setObjectName("filterInput")
        self.customer_name_filter.setFixedWidth(200)
        filter_layout.addWidget(self.customer_name_filter)
        
        # 客服下拉框
        self.service_employee_filter = QComboBox()
        self.service_employee_filter.addItem("客服", None)
        self.service_employee_filter.setObjectName("filterCombo")
        self.service_employee_filter.setFixedWidth(120)
        filter_layout.addWidget(self.service_employee_filter)
        
        # 处理状态下拉框
        self.status_filter = QComboBox()
        self.status_filter.addItem("处理状态", None)
        self.status_filter.addItem("待处理", "待处理")
        self.status_filter.addItem("处理中", "处理中")
        self.status_filter.addItem("已完成", "已完成")
        self.status_filter.addItem("已关闭", "已关闭")
        self.status_filter.setObjectName("filterCombo")
        self.status_filter.setFixedWidth(120)
        filter_layout.addWidget(self.status_filter)
        
        # 查询按钮
        self.search_button = QPushButton("查询")
        self.search_button.setFixedSize(80, 28)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        filter_layout.addWidget(self.search_button)
        
        # 重置按钮
        self.reset_button = QPushButton("重置")
        self.reset_button.setFixedSize(80, 28)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        filter_layout.addWidget(self.reset_button)
        
        filter_layout.addStretch()
        
        # 连接信号
        self.search_button.clicked.connect(self.filter_data)
        self.reset_button.clicked.connect(self.reset_filters)
        
        main_layout.addWidget(filter_widget)
        
    def setup_table_view(self, content_layout):
        """设置表格视图"""
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.clicked.connect(self.on_table_clicked)
        
        # 创建模型
        self.model = QStandardItemModel()
        self.setup_table_headers()
        self.table_view.setModel(self.model)
        
        # 设置列宽
        header = self.table_view.horizontalHeader()
        header.resizeSection(0, 60)   # 序号
        header.resizeSection(1, 80)   # 省份
        header.resizeSection(2, 80)   # 城市
        header.resizeSection(3, 200)  # 客户单位名称
        header.resizeSection(4, 80)   # 联系人
        header.resizeSection(5, 100)  # 销售
        header.resizeSection(6, 100)  # 客服
        header.resizeSection(7, 100)  # 客服记录
        header.resizeSection(8, 120)  # 操作
        
        content_layout.addWidget(self.table_view)
        
    def setup_table_headers(self):
        """设置表格标题"""
        headers = [
            "序号", "省份", "城市", "客户单位名称",
            "联系人", "销售", "客服", "客服记录", "操作"
        ]
        self.model.setHorizontalHeaderLabels(headers)
        
    def load_initial_data(self):
        """加载初始数据"""
        try:
            # 加载员工数据
            self.employees_data = employees_api.get_employees() or []
            employees_map = {emp['id']: emp['name'] for emp in self.employees_data}
            
            # 填充客服筛选下拉框
            for emp in self.employees_data:
                # 假设客服人员的role包含'service'或者职位包含'客服'
                if 'service' in emp.get('role', '').lower() or '客服' in emp.get('position', ''):
                    self.service_employee_filter.addItem(emp['name'], emp['id'])
            
            # 加载客户数据
            self.customers_data = customers_api.get_customers() or []
            
            # 加载售后服务数据
            self.load_service_data()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据失败: {str(e)}")
            
    def load_service_data(self):
        """加载售后服务数据"""
        try:
            # 获取所有售后服务记录
            service_records = service_records_api.get_service_records() or []
            self.all_service_records = service_records
            
            # 清空表格
            self.model.removeRows(0, self.model.rowCount())
            
            # 创建客户映射
            customers_map = {c['id']: c for c in self.customers_data}
            employees_map = {emp['id']: emp['name'] for emp in self.employees_data}
            
            # 按客户分组统计数据
            self.customer_service_data_map.clear()
            customer_service_data = {}
            
            for record in service_records:
                customer_id = record.get('customer_id')
                if customer_id and customer_id in customers_map:
                    customer = customers_map[customer_id]
                    
                    if customer_id not in customer_service_data:
                        # 获取该客户的联系人数量
                        contacts = contacts_api.get_contacts_for_customer(customer_id) or []
                        contact_count = len(contacts)
                        
                        customer_service_data[customer_id] = {
                            'customer': customer,
                            'contact_count': contact_count,
                            'service_records': [],
                            'sales_name': employees_map.get(customer.get('sales_owner_id', 0), '未分配'),
                            'service_name': employees_map.get(customer.get('service_owner_id', 0), '未分配')
                        }
                    
                    customer_service_data[customer_id]['service_records'].append(record)
            
            # 填充表格数据
            row_index = 0
            for customer_id, data in customer_service_data.items():
                self.customer_service_data_map[row_index] = data
                customer = data['customer']
                contact_count = data['contact_count']
                service_record_count = len(data['service_records'])
                
                # 创建行数据
                row_items = []
                
                # 序号
                seq_item = QStandardItem(str(row_index + 1))
                seq_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(seq_item)
                
                # 省份
                province_item = QStandardItem(customer.get('province', ''))
                province_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(province_item)
                
                # 城市
                city_item = QStandardItem(customer.get('city', ''))
                city_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(city_item)
                
                # 客户单位名称
                company_item = QStandardItem(customer.get('company', ''))
                company_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                row_items.append(company_item)
                
                # 联系人（红色数字）
                contact_item = QStandardItem(str(contact_count))
                contact_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                contact_item.setForeground(QColor("#d32f2f"))
                row_items.append(contact_item)
                
                # 销售
                sales_item = QStandardItem(data['sales_name'])
                sales_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(sales_item)
                
                # 客服
                service_item = QStandardItem(data['service_name'])
                service_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(service_item)
                
                # 客服记录（红色数字）
                service_record_item = QStandardItem(str(service_record_count))
                service_record_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                service_record_item.setForeground(QColor("#d32f2f"))
                row_items.append(service_record_item)
                self.model.appendRow(row_items)
                self.add_action_buttons(row_index, customer_id)
                row_index += 1

                self.add_action_buttons(idx, customer_id)
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载售后服务数据失败: {str(e)}")
            print(f"详细错误信息: {e}")
            
    def filter_data(self):
        """筛选数据"""
        try:
            # 获取筛选条件
            customer_name = self.customer_name_filter.text().strip()
            service_employee_id = self.service_employee_filter.currentData()
            status = self.status_filter.currentData()
            
            # 清空表格
            self.model.removeRows(0, self.model.rowCount())
            
            # 创建映射
            customers_map = {c['id']: c for c in self.customers_data}
            employees_map = {emp['id']: emp['name'] for emp in self.employees_data}
            
            # 按客户分组统计数据
            customer_service_data = {}
            
            for record in self.all_service_records:
                customer_id = record.get('customer_id')
                if customer_id and customer_id in customers_map:
                    customer = customers_map[customer_id]
                    
                    # 应用筛选条件
                    if customer_name and customer_name.lower() not in customer.get('company', '').lower():
                        continue
                        
                    if service_employee_id and customer.get('service_owner_id') != service_employee_id:
                        continue
                        
                    if status and record.get('status') != status:
                        continue
                    
                    if customer_id not in customer_service_data:
                        # 获取该客户的联系人数量
                        contacts = contacts_api.get_contacts_for_customer(customer_id) or []
                        contact_count = len(contacts)
                        
                        customer_service_data[customer_id] = {
                            'customer': customer,
                            'contact_count': contact_count,
                            'service_records': [],
                            'sales_name': employees_map.get(customer.get('sales_owner_id', 0), '未分配'),
                            'service_name': employees_map.get(customer.get('service_owner_id', 0), '未分配')
                        }
                    
                    customer_service_data[customer_id]['service_records'].append(record)
            
            # 填充筛选后的数据
            for idx, (customer_id, data) in enumerate(customer_service_data.items()):
                customer = data['customer']
                contact_count = data['contact_count']
                service_record_count = len(data['service_records'])
                
                # 创建行数据
                row_items = []
                
                # 序号
                seq_item = QStandardItem(str(idx + 1))
                seq_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(seq_item)
                
                # 省份
                province_item = QStandardItem(customer.get('province', ''))
                province_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(province_item)
                
                # 城市
                city_item = QStandardItem(customer.get('city', ''))
                city_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(city_item)
                
                # 客户单位名称
                company_item = QStandardItem(customer.get('company', ''))
                company_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                row_items.append(company_item)
                
                # 联系人（红色数字）
                contact_item = QStandardItem(str(contact_count))
                contact_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                contact_item.setForeground(QColor("#d32f2f"))
                row_items.append(contact_item)
                
                # 销售
                sales_item = QStandardItem(data['sales_name'])
                sales_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(sales_item)
                
                # 客服
                service_item = QStandardItem(data['service_name'])
                service_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(service_item)
                
                # 客服记录（红色数字）
                service_record_item = QStandardItem(str(service_record_count))
                service_record_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                service_record_item.setForeground(QColor("#d32f2f"))
                row_items.append(service_record_item)
                
                self.model.appendRow(row_items)
                self.add_action_buttons(idx, customer_id)
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"筛选数据失败: {str(e)}")
            
    def reset_filters(self):
        """重置筛选条件"""
        self.customer_name_filter.clear()
        self.service_employee_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.load_service_data()


    def add_action_buttons(self, row, customer_id):
        """为表格行添加操作按钮"""
        record_button = QPushButton("客服记录")
        record_button.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        record_button.setProperty("customer_id", customer_id)
        record_button.clicked.connect(self.view_service_records_dialog)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.addWidget(record_button)
        buttons_layout.setContentsMargins(5, 2, 5, 2)
        buttons_layout.setSpacing(5)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        self.table_view.setIndexWidget(self.model.index(row, 8), buttons_widget)
        
    def view_service_records_dialog(self):
        """显示客服记录对话框"""
        sender = self.sender()
        customer_id = sender.property("customer_id")
        dialog = ServiceRecordDialog(customer_id, self)
        dialog.exec()

    def on_table_clicked(self, index):
        """处理表格点击事件"""
        row = index.row()
        column = index.column()

        if row not in self.customer_service_data_map:
            return
            
        customer_data = self.customer_service_data_map[row]['customer']
        customer_id = customer_data['id']

        # 点击“联系人”列
        if column == 4:
            contacts = contacts_api.get_contacts_for_customer(customer_id) or []
            dialog = ContactViewDialog(customer_data, contacts, self)
            dialog.exec()
        
        # 点击“客服记录”列
        elif column == 7:
            dialog = ServiceRecordDialog(customer_id, self)
            dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = ServiceRecordView()
    view.resize(1200, 700)
    view.show()
    sys.exit(app.exec())