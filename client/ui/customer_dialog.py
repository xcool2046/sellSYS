from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QDialogButtonBox, QComboBox, QRadioButton, QScrollArea, QWidget, QMessageBox
)

class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer_data=None):
        super().__init__(parent)
        self.setWindowTitle("添加客户" if customer_data is None else "编辑客户")
        self.setMinimumWidth(500)

        # 省份城市数据
        self.province_city_data = {
            "北京": ["东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区", "门头沟区", "房山区", "通州区", "顺义区"],
            "上海": ["黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区", "杨浦区", "闵行区", "宝山区", "嘉定区"],
            "广东": ["广州市", "深圳市", "珠海市", "汕头市", "佛山市", "韶关市", "湛江市", "肇庆市", "江门市", "茂名市"],
            "江苏": ["南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市", "连云港市", "淮安市", "盐城市", "扬州市"],
            "浙江": ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市"],
            "山东": ["济南市", "青岛市", "淄博市", "枣庄市", "东营市", "烟台市", "潍坊市", "济宁市", "泰安市", "威海市"],
            "河南": ["郑州市", "开封市", "洛阳市", "平顶山市", "安阳市", "鹤壁市", "新乡市", "焦作市", "濮阳市", "许昌市"],
            "四川": ["成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市", "广元市", "遂宁市", "内江市", "乐山市"],
            "湖北": ["武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市", "荆门市", "孝感市", "荆州市", "黄冈市"],
            "湖南": ["长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市", "常德市", "张家界市", "益阳市", "郴州市"],
        }

        # --- Layouts ---
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        
        # --- Widgets ---
        self.industry_type_layout = QHBoxLayout()
        self.rb_emergency = QRadioButton("应急")
        self.rb_hr = QRadioButton("人社")
        self.rb_construction = QRadioButton("住建")
        self.rb_other = QRadioButton("其它")
        self.rb_emergency.setChecked(True)  # 默认选中
        self.industry_type_layout.addWidget(self.rb_emergency)
        self.industry_type_layout.addWidget(self.rb_hr)
        self.industry_type_layout.addWidget(self.rb_construction)
        self.industry_type_layout.addWidget(self.rb_other)

        self.company_name_edit = QLineEdit()
        self.province_combo = QComboBox()
        self.city_combo = QComboBox()
        self.address_edit = QLineEdit()
        self.customer_notes_edit = QLineEdit()
        
        # 填充省份下拉框
        self.province_combo.addItem("请选择省份", None)
        for province in self.province_city_data.keys():
            self.province_combo.addItem(province, province)
        
        # 连接省份选择变化事件
        self.province_combo.currentIndexChanged.connect(self.on_province_changed)

        # --- 联系人动态区域 ---
        self.contacts_scroll_area = QScrollArea()
        self.contacts_widget = QWidget()
        self.contacts_layout = QVBoxLayout(self.contacts_widget)
        self.add_contact_button = QPushButton("➕")
        self.add_contact_button.setFixedSize(28, 28)
        self.add_contact_button.clicked.connect(lambda: self.add_contact_row())

        self.contacts_scroll_area.setWidget(self.contacts_widget)
        self.contacts_scroll_area.setWidgetResizable(True)
        self.contacts_scroll_area.setFixedHeight(150)

        # --- Form Assembly ---
        self.form_layout.addRow("行业类别:", self.industry_type_layout)
        self.form_layout.addRow("客户单位:", self.company_name_edit)
        prov_city_layout = QHBoxLayout()
        prov_city_layout.addWidget(self.province_combo)
        prov_city_layout.addWidget(self.city_combo)
        self.form_layout.addRow("所在省份/城市:", prov_city_layout)
        self.form_layout.addRow("详细地址:", self.address_edit)
        self.form_layout.addRow("客户备注:", self.customer_notes_edit)
        self.form_layout.addRow("联系人:", self.contacts_scroll_area)
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
        self.add_contact_row() # Start with one contact
        
    def on_province_changed(self):
        """省份选择变化时更新城市列表"""
        self.city_combo.clear()
        province = self.province_combo.currentData()
        
        if province and province in self.province_city_data:
            self.city_combo.addItem("请选择城市", None)
            for city in self.province_city_data[province]:
                self.city_combo.addItem(city, city)
        else:
            self.city_combo.addItem("请先选择省份", None)

    def add_contact_row(self, name="", phone="", is_primary=False):
        contact_layout = QHBoxLayout()
        name_edit = QLineEdit(name)
        name_edit.setPlaceholderText("姓名")
        phone_edit = QLineEdit(phone)
        phone_edit.setPlaceholderText("电话")
        primary_checkbox = QRadioButton("关键人")
        primary_checkbox.setChecked(is_primary)
        
        remove_button = QPushButton("➖")
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
            industry = "应急"
        elif self.rb_hr.isChecked():
            industry = "人社"
        elif self.rb_construction.isChecked():
            industry = "住建"
        elif self.rb_other.isChecked():
            industry = "其它"
            
        # 获取基本信息
        customer_data = {
            "company": self.company_name_edit.text().strip(),
            "industry": industry,
            "province": self.province_combo.currentData(),
            "city": self.city_combo.currentData(),
            "address": self.address_edit.text().strip(),
            "notes": self.customer_notes_edit.text().strip() if self.customer_notes_edit.text().strip() else None,
            "status": "潜在客户"  # 新客户默认为潜在客户
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
                        "name": name,
                        "phone": phone,
                        "is_primary": primary_checkbox.isChecked()
                    })
        
        return customer_data, contacts_data
        
    def accept(self):
        """重写accept方法，添加数据验证"""
        customer_data, contacts_data = self.get_data()
        
        # 验证必填字段
        if not customer_data["company"]:
            QMessageBox.warning(self, "提示", "请输入客户单位名称")
            return
            
        if not customer_data["industry"]:
            QMessageBox.warning(self, "提示", "请选择行业类别")
            return
            
        if not customer_data["province"]:
            QMessageBox.warning(self, "提示", "请选择省份")
            return
            
        if not customer_data["city"]:
            QMessageBox.warning(self, "提示", "请选择城市")
            return
            
        if not contacts_data:
            QMessageBox.warning(self, "提示", "请至少添加一个联系人")
            return
            
        super().accept()