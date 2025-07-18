"""
销售管理API客户端
"""
from typing import List, Dict, Any, Optional
from .base_client import CRUDAPIClient, APIException

class SalesFollowAPI(CRUDAPIClient):
    """销售跟进API客户端"""
    
    def __init__(self):
        super().__init__('sales_follows')
    
    def get_follows_by_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        """获取客户的销售跟进记录"""
        try:
            response = self.get(f"/customers/{customer_id}/follows/")
            if isinstance(response, list):
                return response
            elif isinstance(response, dict) and 'data' in response:
                return response['data']
            return []
        except APIException as e:
            print(f"获取客户销售跟进记录失败: {e}")
            return []
    
    def get_follows_by_sales_person(self, sales_id: int, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """获取销售人员的跟进记录"""
        try:
            search_params = params or {}
            search_params['sales_id'] = sales_id
            return self.list(search_params)
        except APIException as e:
            print(f"获取销售人员跟进记录失败: {e}")
            return []
    
    def create_follow(self, follow_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """创建销售跟进记录"""
        try:
            return self.create(follow_data)
        except APIException as e:
            print(f"创建销售跟进记录失败: {e}")
            return None
    
    def update_follow(self, follow_id: int, follow_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新销售跟进记录"""
        try:
            return self.update(follow_id, follow_data)
        except APIException as e:
            print(f"更新销售跟进记录失败: {e}")
            return None
    
    def get_follow_statistics(self, sales_id: int = None, date_range: Dict[str, str] = None) -> Dict[str, Any]:
        """获取销售跟进统计"""
        try:
            params = {}
            if sales_id:
                params['sales_id'] = sales_id
            if date_range:
                params.update(date_range)
            
            response = self.get(f"{self.endpoint}statistics/", params)
            return response if isinstance(response, dict) else {}
        except APIException as e:
            print(f"获取销售跟进统计失败: {e}")
            return {}

class SalesReportAPI(CRUDAPIClient):
    """销售报表API客户端"""
    
    def __init__(self):
        super().__init__('sales_reports')
    
    def get_sales_performance(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取销售业绩报表"""
        try:
            response = self.get(f"{self.endpoint}performance/", params)
            return response if isinstance(response, dict) else {}
        except APIException as e:
            print(f"获取销售业绩报表失败: {e}")
            return {}
    
    def get_customer_conversion(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取客户转化报表"""
        try:
            response = self.get(f"{self.endpoint}conversion/", params)
            return response if isinstance(response, dict) else {}
        except APIException as e:
            print(f"获取客户转化报表失败: {e}")
            return {}
    
    def get_sales_funnel(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取销售漏斗数据"""
        try:
            response = self.get(f"{self.endpoint}funnel/", params)
            return response if isinstance(response, dict) else {}
        except APIException as e:
            print(f"获取销售漏斗数据失败: {e}")
            return {}
    
    def get_monthly_report(self, year: int, month: int, sales_id: int = None) -> Dict[str, Any]:
        """获取月度销售报表"""
        try:
            params = {'year': year, 'month': month}
            if sales_id:
                params['sales_id'] = sales_id
            
            response = self.get(f"{self.endpoint}monthly/", params)
            return response if isinstance(response, dict) else {}
        except APIException as e:
            print(f"获取月度销售报表失败: {e}")
            return {}

class EmployeeAPI(CRUDAPIClient):
    """员工API客户端"""
    
    def __init__(self):
        super().__init__('employees')
    
    def get_sales_employees(self) -> List[Dict[str, Any]]:
        """获取销售人员列表"""
        try:
            params = {'role': 'sales'}
            return self.list(params)
        except APIException as e:
            print(f"获取销售人员列表失败: {e}")
            return []
    
    def get_service_employees(self) -> List[Dict[str, Any]]:
        """获取客服人员列表"""
        try:
            params = {'role': 'service'}
            return self.list(params)
        except APIException as e:
            print(f"获取客服人员列表失败: {e}")
            return []
    
    def get_employee_customers(self, employee_id: int, role: str = 'sales') -> List[Dict[str, Any]]:
        """获取员工负责的客户"""
        try:
            response = self.get(f"{self.endpoint}{employee_id}/customers/", {'role': role})
            if isinstance(response, list):
                return response
            elif isinstance(response, dict) and 'data' in response:
                return response['data']
            return []
        except APIException as e:
            print(f"获取员工负责的客户失败: {e}")
            return []

# 创建全局实例
sales_follow_api = SalesFollowAPI()
sales_report_api = SalesReportAPI()
employee_api = EmployeeAPI()

# 导出
__all__ = ['SalesFollowAPI', 'SalesReportAPI', 'EmployeeAPI', 'sales_follow_api', 'sales_report_api', 'employee_api']
