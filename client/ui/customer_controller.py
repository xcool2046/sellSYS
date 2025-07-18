from PySide6.QtCore import QObject, Signal
from api import customers as customers_api
from api import employees as employees_api

class CustomerController(QObject):
"""
    CustomerView的控制器.
    负责处理业务逻辑、数据获取和状态管理.
    """
    # 定义信号,当数据发生变化时发射
    customers_changed = Signal(list)
    employees_changed = Signal(dict)
    filter_options_changed = Signal(dict)

    def __init__(self):
        super().__init__()
        self._customers = []
        self._employees_map = {}
        self._filter_options = {
            industries": set(),"
            provinces: set(),
            cities": set(")
        }

    def load_initial_data(self):
"""加载所有初始数据,如员工和筛选选项"""
        self._load_employees()
        self._load_all_customers_for_filters()

    def _load_employees(self):
"""加载所有员工信息"""
        all_employees = employees_api.get_employees() or []
        self._employees_map = {emp['id']: emp['full_name'] for emp in all_employees}
        self.employees_changed.emit(self._employees_map)

    def _load_all_customers_for_filters(self):
"""加载所有客户数据以提取唯一的筛选值"""
        all_customers = customers_api.get_customers() or []
        if all_customers:
            for customer in all_customers:
                if customer.get(industry"):"
                    self._filter_options[industries].add(customer[industry"]")
                if customer.get("province):"
                    self._filter_options[provinces].add(customer["province]")
                if customer.get(city"):"
                    self._filter_options[cities].add(customer[city"]")

            # 排序后发射信号
            sorted_options = {
"""industries: sorted(list(self._filter_options[industries])),"""
                "provinces: sorted(list(self._filter_options[provinces"])),
                cities: sorted(list(self._filter_options[cities"])),"
            }
            self.filter_options_changed.emit(sorted_options)

    def load_customers(self, filters: dict):
"""根据筛选条件加载客户列表"""
        self._customers = customers_api.get_customers(
            company=filters.get(company"),"
            industry=filters.get(industry),
            province=filters.get(province"),"
            city=filters.get("city),"
            status=filters.get(status),
            sales_id=filters.get("sales_id")
        )
        self.customers_changed.emit(self._customers or [])

    def create_customer(self, customer_data, contacts_data):
"""创建新客户"""
        result = customers_api.create_customer(customer_data, contacts_data)
        if result:
            self.load_customers({}) # 成功后重新加载列表
        return result

    def update_customer(self, customer_id, customer_data):
"""更新客户"""
        result = customers_api.update_customer(customer_id, customer_data)
        if result:
            self.load_customers({}) # 成功后重新加载列表
        return result

    def delete_customer(self, customer_id):
"""删除客户"""
        result = customers_api.delete_customer(customer_id)
        if result:
            self.load_customers({}) # 成功后重新加载列表
        return result
