"""
客户管理视图 - 完整功能版本
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, 
    QLineEdit, QComboBox, QHeaderView, QMessageBox, QLabel, QCheckBox,
    QMenu, QProgressBar, QSplitter
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtCore import Qt, QTimer, Signal
from typing import List, Dict, Any, Optional

from api.customers_api import customers_api
from ui.dialogs.customer_dialog import CustomerDialog
from config_clean import CUSTOMER_STATUS, INDUSTRY_CATEGORIES, PROVINCE_CITY_DATA
from models.base_model import Customer

class CustomerManagementView(QWidget):
    """客户管理视图"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.customers_data = []
        self.selected_customers = []
        self.employees_data = {}
        self.current_page = 1
        self.total_pages = 1
        
        self.setup_ui()
        self.setup_connections()
        self.load_data()
        
        print("✅ 客户管理视图初始化完成")
    
    def setup_ui(self):
        """设置用户界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("客户管理")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px 0;
            }
        """)
        main_layout.addWidget(title_label)
        
        # 搜索工具栏
        self.setup_search_toolbar()
        main_layout.addWidget(self.search_toolbar)
        
        # 操作工具栏
        self.setup_action_toolbar()
        main_layout.addWidget(self.action_toolbar)
        
        # 主要内容区域
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # 客户列表
        self.setup_customer_table()
        content_splitter.addWidget(self.table_widget)
        
        # 设置分割器比例
        content_splitter.setStretchFactor(0, 1)
        
        # 状态栏
        self.setup_status_bar()
        main_layout.addWidget(self.status_bar)
    
    def setup_search_toolbar(self):
        """设置搜索工具栏"""
        self.search_toolbar = QWidget()
        toolbar_layout = QHBoxLayout(self.search_toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入客户名称、行业或地区搜索...")
        self.search_input.setFixedHeight(35)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        toolbar_layout.addWidget(self.search_input)
        
        # 行业筛选
        self.industry_filter = QComboBox()
        self.industry_filter.setFixedHeight(35)
        self.industry_filter.addItem("全部行业", None)
        for industry in INDUSTRY_CATEGORIES:
            self.industry_filter.addItem(industry, industry)
        toolbar_layout.addWidget(self.industry_filter)
        
        # 省份筛选
        self.province_filter = QComboBox()
        self.province_filter.setFixedHeight(35)
        self.province_filter.addItem("全部省份", None)
        for province in PROVINCE_CITY_DATA.keys():
            self.province_filter.addItem(province, province)
        toolbar_layout.addWidget(self.province_filter)
        
        # 状态筛选
        self.status_filter = QComboBox()
        self.status_filter.setFixedHeight(35)
        self.status_filter.addItem("全部状态", None)
        for status_key, status_name in CUSTOMER_STATUS.items():
            self.status_filter.addItem(status_name, status_key)
        toolbar_layout.addWidget(self.status_filter)
        
        # 搜索按钮
        self.search_btn = QPushButton("搜索")
        self.search_btn.setFixedHeight(35)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        toolbar_layout.addWidget(self.search_btn)
        
        # 重置按钮
        self.reset_btn = QPushButton("重置")
        self.reset_btn.setFixedHeight(35)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        toolbar_layout.addWidget(self.reset_btn)
    
    def setup_action_toolbar(self):
        """设置操作工具栏"""
        self.action_toolbar = QWidget()
        toolbar_layout = QHBoxLayout(self.action_toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        
        # 全选复选框
        self.select_all_checkbox = QCheckBox("全选")
        toolbar_layout.addWidget(self.select_all_checkbox)
        
        # 批量操作按钮
        self.batch_assign_sales_btn = QPushButton("分配销售")
        self.batch_assign_sales_btn.setEnabled(False)
        self.batch_assign_sales_btn.setFixedHeight(35)
        self.batch_assign_sales_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        toolbar_layout.addWidget(self.batch_assign_sales_btn)
        
        self.batch_assign_service_btn = QPushButton("分配客服")
        self.batch_assign_service_btn.setEnabled(False)
        self.batch_assign_service_btn.setFixedHeight(35)
        self.batch_assign_service_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        toolbar_layout.addWidget(self.batch_assign_service_btn)
        
        toolbar_layout.addStretch()
        
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setFixedHeight(35)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        toolbar_layout.addWidget(self.refresh_btn)
        
        # 添加客户按钮
        self.add_customer_btn = QPushButton("添加客户")
        self.add_customer_btn.setFixedHeight(35)
        self.add_customer_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        toolbar_layout.addWidget(self.add_customer_btn)
    
    def setup_customer_table(self):
        """设置客户表格"""
        self.table_widget = QWidget()
        table_layout = QVBoxLayout(self.table_widget)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
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
        self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # 设置表格样式
        self.table_view.setStyleSheet("""
            QTableView {
                gridline-color: #bdc3c7;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #3498db;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
            QTableView::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableView::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        table_layout.addWidget(self.table_view)
        
        # 设置表格标题
        self.setup_table_headers()
    
    def setup_table_headers(self):
        """设置表格标题"""
        headers = [
            "", "ID", "客户名称", "行业类别", "省份", "城市", 
            "联系状态", "销售负责人", "客服负责人", "创建时间", "更新时间"
        ]
        self.model.setHorizontalHeaderLabels(headers)
        
        # 设置第一列（复选框列）宽度
        self.table_view.setColumnWidth(0, 50)
    
    def setup_status_bar(self):
        """设置状态栏"""
        self.status_bar = QWidget()
        status_layout = QHBoxLayout(self.status_bar)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        # 统计信息
        self.stats_label = QLabel("总计: 0 个客户")
        self.stats_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        status_layout.addWidget(self.stats_label)
        
        status_layout.addStretch()
        
        # 加载进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedWidth(200)
        status_layout.addWidget(self.progress_bar)
    
    def setup_connections(self):
        """设置信号连接"""
        # 搜索相关
        self.search_btn.clicked.connect(self.on_search_clicked)
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        self.search_input.returnPressed.connect(self.on_search_clicked)
        
        # 操作相关
        self.add_customer_btn.clicked.connect(self.on_add_customer_clicked)
        self.refresh_btn.clicked.connect(self.on_refresh_clicked)
        
        # 批量操作
        self.select_all_checkbox.stateChanged.connect(self.on_select_all_changed)
        self.batch_assign_sales_btn.clicked.connect(self.on_batch_assign_sales)
        self.batch_assign_service_btn.clicked.connect(self.on_batch_assign_service)
        
        # 表格相关
        self.table_view.doubleClicked.connect(self.on_row_double_clicked)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)
        self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
    
    def load_data(self):
        """加载数据"""
        self.show_loading(True)
        
        try:
            # 加载客户数据
            self.customers_data = customers_api.list()
            self.update_table_view()
            self.update_stats()
            
            # 加载员工数据（用于显示负责人姓名）
            # self.load_employees_data()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据失败: {str(e)}")
        finally:
            self.show_loading(False)
    
    def show_loading(self, show: bool):
        """显示/隐藏加载状态"""
        self.progress_bar.setVisible(show)
        if show:
            self.progress_bar.setRange(0, 0)  # 无限进度条
        else:
            self.progress_bar.setRange(0, 1)
            self.progress_bar.setValue(1)
    
    def update_table_view(self):
        """更新表格视图"""
        self.model.clear()
        self.setup_table_headers()
        
        for customer in self.customers_data:
            # 创建复选框
            checkbox_item = QStandardItem()
            checkbox_item.setCheckable(True)
            checkbox_item.setEditable(False)
            
            # 创建其他列
            items = [
                checkbox_item,
                QStandardItem(str(customer.get("id", ""))),
                QStandardItem(customer.get("company", "")),
                QStandardItem(customer.get("industry", "")),
                QStandardItem(customer.get("province", "")),
                QStandardItem(customer.get("city", "")),
                QStandardItem(CUSTOMER_STATUS.get(customer.get("status", ""), "")),
                QStandardItem(customer.get("sales_person_name", "")),
                QStandardItem(customer.get("service_person_name", "")),
                QStandardItem(customer.get("created_at", "")),
                QStandardItem(customer.get("updated_at", ""))
            ]
            
            # 设置项不可编辑（除了复选框）
            for i, item in enumerate(items):
                if i > 0:  # 跳过复选框列
                    item.setEditable(False)
            
            self.model.appendRow(items)
    
    def update_stats(self):
        """更新统计信息"""
        total = len(self.customers_data)
        selected = len(self.get_selected_customers())
        
        if selected > 0:
            self.stats_label.setText(f"总计: {total} 个客户，已选择: {selected} 个")
        else:
            self.stats_label.setText(f"总计: {total} 个客户")
    
    def get_selected_customers(self) -> List[Dict[str, Any]]:
        """获取选中的客户"""
        selected = []
        for row in range(self.model.rowCount()):
            checkbox_item = self.model.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
                if row < len(self.customers_data):
                    selected.append(self.customers_data[row])
        return selected
    
    def on_search_clicked(self):
        """搜索按钮点击事件"""
        params = {
            'search': self.search_input.text().strip(),
            'industry': self.industry_filter.currentData(),
            'province': self.province_filter.currentData(),
            'status': self.status_filter.currentData()
        }
        
        # 移除空值
        params = {k: v for k, v in params.items() if v}
        
        self.show_loading(True)
        try:
            self.customers_data = customers_api.search_customers(params)
            self.update_table_view()
            self.update_stats()
            print(f"✅ 搜索完成，找到 {len(self.customers_data)} 条记录")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"搜索失败: {str(e)}")
        finally:
            self.show_loading(False)
    
    def on_reset_clicked(self):
        """重置按钮点击事件"""
        self.search_input.clear()
        self.industry_filter.setCurrentIndex(0)
        self.province_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.load_data()
        print("✅ 已重置搜索条件")
    
    def on_refresh_clicked(self):
        """刷新按钮点击事件"""
        self.load_data()
        print("✅ 数据已刷新")
    
    def on_add_customer_clicked(self):
        """添加客户按钮点击事件"""
        dialog = CustomerDialog(parent=self)
        if dialog.exec():
            customer_data = dialog.get_customer_data()
            contacts_data = dialog.get_contacts_data()
            
            self.show_loading(True)
            try:
                # 创建客户
                result = customers_api.create(customer_data)
                if result:
                    # 如果有联系人数据，也要创建
                    if contacts_data:
                        customer_id = result.get('id')
                        for contact in contacts_data:
                            customers_api.add_customer_contact(customer_id, contact)
                    
                    QMessageBox.information(self, "成功", "客户添加成功!")
                    self.load_data()  # 重新加载数据
                else:
                    QMessageBox.warning(self, "失败", "客户添加失败!")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"添加客户时发生错误: {str(e)}")
            finally:
                self.show_loading(False)
    
    def on_select_all_changed(self, state):
        """全选复选框状态变化"""
        checked = state == Qt.CheckState.Checked.value
        
        for row in range(self.model.rowCount()):
            checkbox_item = self.model.item(row, 0)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
        
        self.update_selection_buttons()
        self.update_stats()
    
    def on_selection_changed(self):
        """选择变化事件"""
        self.update_selection_buttons()
        self.update_stats()
    
    def update_selection_buttons(self):
        """更新选择相关按钮状态"""
        selected = self.get_selected_customers()
        has_selection = len(selected) > 0
        
        self.batch_assign_sales_btn.setEnabled(has_selection)
        self.batch_assign_service_btn.setEnabled(has_selection)
    
    def on_batch_assign_sales(self):
        """批量分配销售"""
        selected = self.get_selected_customers()
        if not selected:
            return
        
        QMessageBox.information(self, "提示", f"批量分配销售功能正在开发中...\n选中了 {len(selected)} 个客户")
    
    def on_batch_assign_service(self):
        """批量分配客服"""
        selected = self.get_selected_customers()
        if not selected:
            return
        
        QMessageBox.information(self, "提示", f"批量分配客服功能正在开发中...\n选中了 {len(selected)} 个客户")
    
    def on_row_double_clicked(self, index):
        """行双击事件"""
        if index.isValid():
            row = index.row()
            if row < len(self.customers_data):
                customer = self.customers_data[row]
                self.edit_customer(customer)
    
    def edit_customer(self, customer_data: Dict[str, Any]):
        """编辑客户"""
        dialog = CustomerDialog(customer_data, parent=self)
        if dialog.exec():
            updated_data = dialog.get_customer_data()
            contacts_data = dialog.get_contacts_data()
            
            self.show_loading(True)
            try:
                customer_id = customer_data.get('id')
                result = customers_api.update(customer_id, updated_data)
                if result:
                    QMessageBox.information(self, "成功", "客户信息更新成功!")
                    self.load_data()  # 重新加载数据
                else:
                    QMessageBox.warning(self, "失败", "客户信息更新失败!")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"更新客户信息时发生错误: {str(e)}")
            finally:
                self.show_loading(False)
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        index = self.table_view.indexAt(position)
        if not index.isValid():
            return
        
        row = index.row()
        if row >= len(self.customers_data):
            return
        
        customer = self.customers_data[row]
        
        menu = QMenu(self)
        
        # 编辑客户
        edit_action = QAction("编辑客户", self)
        edit_action.triggered.connect(lambda: self.edit_customer(customer))
        menu.addAction(edit_action)
        
        # 查看详情
        detail_action = QAction("查看详情", self)
        detail_action.triggered.connect(lambda: self.show_customer_detail(customer))
        menu.addAction(detail_action)
        
        menu.addSeparator()
        
        # 删除客户
        delete_action = QAction("删除客户", self)
        delete_action.triggered.connect(lambda: self.delete_customer(customer))
        menu.addAction(delete_action)
        
        menu.exec(self.table_view.mapToGlobal(position))
    
    def show_customer_detail(self, customer_data: Dict[str, Any]):
        """显示客户详情"""
        detail_text = f"""
客户名称: {customer_data.get('company', '')}
行业类别: {customer_data.get('industry', '')}
所在地区: {customer_data.get('province', '')} {customer_data.get('city', '')}
详细地址: {customer_data.get('address', '')}
公司网站: {customer_data.get('website', '')}
公司规模: {customer_data.get('scale', '')}
客户状态: {CUSTOMER_STATUS.get(customer_data.get('status', ''), '')}
销售负责人: {customer_data.get('sales_person_name', '')}
客服负责人: {customer_data.get('service_person_name', '')}
创建时间: {customer_data.get('created_at', '')}
更新时间: {customer_data.get('updated_at', '')}
备注: {customer_data.get('notes', '')}
        """.strip()
        
        QMessageBox.information(self, "客户详情", detail_text)
    
    def delete_customer(self, customer_data: Dict[str, Any]):
        """删除客户"""
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除客户 '{customer_data.get('company', '')}' 吗？\n此操作不可撤销！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.show_loading(True)
            try:
                customer_id = customer_data.get('id')
                success = customers_api.delete_by_id(customer_id)
                if success:
                    QMessageBox.information(self, "成功", "客户删除成功!")
                    self.load_data()  # 重新加载数据
                else:
                    QMessageBox.warning(self, "失败", "客户删除失败!")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除客户时发生错误: {str(e)}")
            finally:
                self.show_loading(False)

# 导出
__all__ = ['CustomerManagementView']
