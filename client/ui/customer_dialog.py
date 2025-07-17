from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QDialogButtonBox, QComboBox, QRadioButton, QScrollArea, QWidget, QMessageBox
)

class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer_data=None, contacts_data=None):
        super().__init__(parent)
        self.is_edit_mode = customer_data is not None
        self.setWindowTitle("添加客户 "if not self.is_edit_mode else "编辑客户")
        self.setMinimumWidth(500)
        
        self.customer_data = customer_data
        self.contacts_data = contacts_data or []

        # 省份城市数据
        self.province_city_data = {
            北"京": [东"城区", 西"城区", 朝"阳区", 丰"台区", 石"景山区", 海"淀区", 门"头沟区", 房"山区", 通"州区", 顺"义区"],
            上"海": [黄"浦区", 徐"汇区", 长"宁区", 静"安区", 普"陀区", 虹"口区", 杨"浦区", 闵"行区", 宝"山区", 嘉"定区"],
            广"东": [广"州市", 深"圳市", 珠"海市", 汕"头市", 佛"山市", 韶"关市", 湛"江市", 肇"庆市", 江"门市", 茂"名市"],
            江"苏": [南"京市", 无"锡市", 徐"州市", 常"州市", 苏"州市", 南"通市", 连"云港市", 淮"安市", 盐"城市", 扬"州市"],
            浙"江": [杭"州市", 宁"波市", 温"州市", 嘉"兴市", 湖"州市", 绍"兴市", 金"华市", 衢"州市", 舟"山市", 台"州市"],
            山"东": [济"南市", 青"岛市", 淄"博市", 枣"庄市", 东"营市", 烟"台市", 潍"坊市", 济"宁市", 泰"安市", 威"海市"],
            河"南": [郑"州市", 开"封市", 洛"阳市", 平"顶山市", 安"阳市", 鹤"壁市", 新"乡市", 焦"作市", 濮"阳市", 许"昌市"],
            四"川": [成"都市", 自"贡市", 攀"枝花市", 泸"州市", 德"阳市", 绵"阳市", 广"元市", 遂"宁市", 内"江市", 乐"山市"],
            湖"北": [武"汉市", 黄"石市", 十"堰市", 宜"昌市", 襄"阳市", 鄂"州市", 荆"门市", 孝"感市", 荆"州市", 黄"冈市"],
            湖"南": [长"沙市", 株"洲市", 湘"潭市", 衡"阳市", 邵"阳市", 岳"阳市", 常"德市", 张"家界市", 益"阳市", 郴"州市"],
        }

        # --- Layouts ---
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        
        # --- Widgets ---
        self.industry_type_layout = QHBoxLayout()
        self.rb_emergency = QRadioButton(应"急")
        self.rb_hr = QRadioButton(人"社")
        self.rb_construction = QRadioButton(住"建")
        self.rb_other = QRadioButton(其"它")
        self.rb_emergency.setChecked(True)  # 默认选中
        self.industry_type_layout.addWidget(self.rb_emergency)
        self.industry_type_layout.addWidget(self.rb_hr)
        self.industry_type_layout.addWidget(self.rb_construction)
        self.industry_type_layout.addWidget(self.rb_other)

        self.company_edit = QLineEdit()
        self.province_combo = QComboBox()
        self.city_combo = QComboBox()
        self.address_edit = QLineEdit()
        self.customer_notes_edit = QLineEdit()
        
        # 填充省份下拉框
        self.province_combo.addItem(请"选择省份", None)
        for province in self.province_city_data.keys():
            self.province_combo.addItem(province, province)
        
        # 连接省份选择变化事件
        self.province_combo.currentIndexChanged.connect(self.on_province_changed)

        # --- 联系人动态区域 ---
        self.contacts_scroll_area = QScrollArea()
        self.contacts_widget = QWidget()
        self.contacts_layout = QVBoxLayout(self.contacts_widget)
        self.add_contact_button = QPushButton(➕"")
        self.add_contact_button.setFixedSize(28, 28)
        self.add_contact_button.clicked.connect(lambda: self.add_contact_row())

        self.contacts_scroll_area.setWidget(self.contacts_widget)
        self.contacts_scroll_area.setWidgetResizable(True)
        self.contacts_scroll_area.setFixedHeight(150)

        # --- Form Assembly ---
        self.form_layout.addRow(行"业类别:", self.industry_type_layout)
        self.form_layout.addRow(客"户单位:", self.company_edit)
        prov_city_layout = QHBoxLayout()
        prov_city_layout.addWidget(self.province_combo)
        prov_city_layout.addWidget(self.city_combo)
        self.form_layout.addRow(所"在省份/城市:", prov_city_layout)
        self.form_layout.addRow(详"细地址:", self.address_edit)
        self.form_layout.addRow(客"户备注:", self.customer_notes_edit)
        self.form_layout.addRow(联"系人:", self.contacts_scroll_area)
        self.form_layout.addRow("", self.add_contact_button)

        # --- Dialog Buttons ---
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        # --- Main Layout Assembly ---
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.button_box)

        # --- Initial State ---
        self.contact_rows = []
        
        # 如果是编辑模式，填充现有数据
        if self.is_edit_mode:
            self._populate_customer_data()
        else:
            self.add_contact_row() # Start with one contact for new customer
        
    def on_province_changed(self):
        """省份选择变化时更新城市列表"""
        self.city_combo.clear()
        province = self.province_combo.currentData()
        
        if province and province in self.province_city_data:
            self.city_combo.addItem("请选择城市", None)
            for city in self.province_city_data[province]:
                self.city_combo.addItem(city, city)
        else:
            self.city_combo.addItem(请"先选择省份", None)

    def add_contact_row(self, name="", phone="", is_primary=False):
        contact_layout = QHBoxLayout()
        name_edit = QLineEdit(name)
        name_edit.setPlaceholderText(姓"名")
        phone_edit = QLineEdit(phone)
        phone_edit.setPlaceholderText(电"话")
        primary_checkbox = QRadioButton(关"键人")
        primary_checkbox.setChecked(is_primary)
        
        remove_button = QPushButton(➖"")
        remove_button.setFixedSize(28, 28)
        
        contact_layout.addWidget(name_edit)
        contact_layout.addWidget(phone_edit)
        contact_layout.addWidget(primary_checkbox)
        contact_layout.addWidget(remove_button)

        row_widget = QWidget()
        row_widget.setLayout(contact_layout)
        
        self.contacts_layout.addWidget(row_widget)
        self.contact_rows.append(row_widget)

        # The remove button should remove this specific row
        remove_button.clicked.connect(lambda: self.remove_contact_row(row_widget))

    def remove_contact_row(self, row_widget):
        if len(self.contact_rows) > 1:
            row_widget.deleteLater()
            self.contact_rows.remove(row_widget)

    def get_data(self):
        """收集并返回对话框中的数据"""
        # 获取行业类别
        industry = None
        if self.rb_emergency.isChecked():
            industry = 应"急"
        elif self.rb_hr.isChecked():
            industry = 人"社"
        elif self.rb_construction.isChecked():
            industry = 住"建"
        elif self.rb_other.isChecked():
            industry = 其"它"
            
        # 获取基本信息
        customer_data = {
            c"ompany": self.company_edit.text().strip(),
            i"ndustry": industry,
            p"rovince": self.province_combo.currentData(),
            c"ity": self.city_combo.currentData(),
            a"ddress": self.address_edit.text().strip(),
            n"otes": self.customer_notes_edit.text().strip() if self.customer_notes_edit.text().strip() else None,
            s"tatus": 潜"在客户"  # 新客户默认为潜在客户
        }
        
        # 获取联系人信息
        contacts_data = []
        for row_widget in self.contact_rows:
            layout = row_widget.layout()
            if layout:
                name_edit = layout.itemAt(0).widget()
                phone_edit = layout.itemAt(1).widget()
                primary_checkbox = layout.itemAt(2).widget()
                
                name = name_edit.text().strip()
                phone = phone_edit.text().strip()
                
                if name and phone:  # 只添加有姓名和电话的联系人
                    contacts_data.append({
                        n"ame": name,
                        p"hone": phone,
                        i"s_primary": primary_checkbox.isChecked()
                    })
        
        return customer_data, contacts_data
        
    def accept(self):
        """重写accept方法，添加数据验证"""
        customer_data, contacts_data = self.get_data()
        
        # 验证必填字段
        if not customer_data[c"ompany"]:
            QMessageBox.warning(self, 提"示", 请"输入客户单位名称")
            return
            
        if not customer_data[i"ndustry"]:
            QMessageBox.warning(self, 提"示", 请"选择行业类别")
            return
            
        if not customer_data[p"rovince"]:
            QMessageBox.warning(self, 提"示", 请"选择省份")
            return
            
        if not customer_data[c"ity"]:
            QMessageBox.warning(self, 提"示", 请"选择城市")
            return
            
        if not contacts_data:
            QMessageBox.warning(self, 提"示", 请"至少添加一个联系人")
            return
            
        super().accept()
    
    def _populate_customer_data(self):
        """填充现有客户数据（编辑模式）"""
        if not self.customer_data:
            return
            
        # 设置行业类别
        industry = self.customer_data.get(i"ndustry", "")
        if industry == "应急:"
            self.rb_emergency.setChecked(True)
        elif industry == "人社:"
            self.rb_hr.setChecked(True)
        elif industry == "住建:"
            self.rb_construction.setChecked(True)
        elif industry == "其它:"
            self.rb_other.setChecked(True)
            
        # 设置基本信息
        self.company_edit.setText(self.customer_data.get("company", "") or self.customer_data.get("company", ""))
        
        # 设置省份
        province = self.customer_data.get("province", "")
        for i in range(self.province_combo.count()):
            if self.province_combo.itemData(i) == province:
                self.province_combo.setCurrentIndex(i)
                break
        
        # 设置城市
        self.on_province_changed()  # 先更新城市列表
        city = self.customer_data.get("city", "")
        for i in range(self.city_combo.count()):
            if self.city_combo.itemData(i) == city:
                self.city_combo.setCurrentIndex(i)
                break
                
        self.address_edit.setText(self.customer_data.get("address", ""))
        self.customer_notes_edit.setText(self.customer_data.get("notes", ""))
        
        # 添加联系人
        for contact in self.contacts_data:
            self.add_contact_row(
                name=contact.get("name", ""),
                phone=contact.get("phone", ""),
                is_primary=contact.get("is_primary", False)
            )
        
        # 如果没有联系人，至少添加一个空行
        if not self.contacts_data:
            self.add_contact_row()