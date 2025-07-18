"""
客户管理API客户端
"""
from typing import List, Dict, Any, Optional
from .base_client import CRUDAPIClient, APIException

class CustomersAPI(CRUDAPIClient):
    """客户API客户端"""
    
    def __init__(self):
        super().__init__('customers')
    
    def search_customers(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """搜索客户"""
        try:
            # 构建搜索参数
            search_params = {}
            
            # 关键词搜索
            if params.get('search'):
                search_params['search'] = params['search']
            
            # 公司名称
            if params.get('company'):
                search_params['company'] = params['company']
            
            # 行业筛选
            if params.get('industry'):
                search_params['industry'] = params['industry']
            
            # 省份筛选
            if params.get('province'):
                search_params['province'] = params['province']
            
            # 城市筛选
            if params.get('city'):
                search_params['city'] = params['city']
            
            # 状态筛选
            if params.get('status'):
                search_params['status'] = params['status']
            
            # 销售负责人筛选
            if params.get('sales_id'):
                search_params['sales_id'] = params['sales_id']
            
            # 客服负责人筛选
            if params.get('service_id'):
                search_params['service_id'] = params['service_id']
            
            # 分页参数
            if params.get('page'):
                search_params['page'] = params['page']
            if params.get('page_size'):
                search_params['page_size'] = params['page_size']
            
            return self.list(search_params)
            
        except APIException as e:
            print(f"搜索客户失败: {e}")
            return []
    
    def get_customer_contacts(self, customer_id: int) -> List[Dict[str, Any]]:
        """获取客户联系人"""
        try:
            response = self.get(f"{self.endpoint}{customer_id}/contacts/")
            if isinstance(response, list):
                return response
            elif isinstance(response, dict) and 'data' in response:
                return response['data']
            return []
        except APIException as e:
            print(f"获取客户联系人失败: {e}")
            return []
    
    def add_customer_contact(self, customer_id: int, contact_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """添加客户联系人"""
        try:
            return self.post(f"{self.endpoint}{customer_id}/contacts/", contact_data)
        except APIException as e:
            print(f"添加客户联系人失败: {e}")
            return None
    
    def update_customer_contact(self, customer_id: int, contact_id: int, contact_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新客户联系人"""
        try:
            return self.put(f"{self.endpoint}{customer_id}/contacts/{contact_id}/", contact_data)
        except APIException as e:
            print(f"更新客户联系人失败: {e}")
            return None
    
    def delete_customer_contact(self, customer_id: int, contact_id: int) -> bool:
        """删除客户联系人"""
        try:
            self.delete(f"{self.endpoint}{customer_id}/contacts/{contact_id}/")
            return True
        except APIException as e:
            print(f"删除客户联系人失败: {e}")
            return False
    
    def assign_sales_person(self, customer_ids: List[int], sales_id: int) -> bool:
        """分配销售负责人"""
        try:
            data = {
                'customer_ids': customer_ids,
                'sales_id': sales_id
            }
            self.post(f"{self.endpoint}assign_sales/", data)
            return True
        except APIException as e:
            print(f"分配销售负责人失败: {e}")
            return False
    
    def assign_service_person(self, customer_ids: List[int], service_id: int) -> bool:
        """分配客服负责人"""
        try:
            data = {
                'customer_ids': customer_ids,
                'service_id': service_id
            }
            self.post(f"{self.endpoint}assign_service/", data)
            return True
        except APIException as e:
            print(f"分配客服负责人失败: {e}")
            return False
    
    def get_customer_orders(self, customer_id: int) -> List[Dict[str, Any]]:
        """获取客户订单"""
        try:
            response = self.get(f"{self.endpoint}{customer_id}/orders/")
            if isinstance(response, list):
                return response
            elif isinstance(response, dict) and 'data' in response:
                return response['data']
            return []
        except APIException as e:
            print(f"获取客户订单失败: {e}")
            return []
    
    def get_customer_service_records(self, customer_id: int) -> List[Dict[str, Any]]:
        """获取客户服务记录"""
        try:
            response = self.get(f"{self.endpoint}{customer_id}/service_records/")
            if isinstance(response, list):
                return response
            elif isinstance(response, dict) and 'data' in response:
                return response['data']
            return []
        except APIException as e:
            print(f"获取客户服务记录失败: {e}")
            return []
    
    def update_customer_status(self, customer_id: int, status: str) -> bool:
        """更新客户状态"""
        try:
            data = {'status': status}
            result = self.partial_update(customer_id, data)
            return result is not None
        except APIException as e:
            print(f"更新客户状态失败: {e}")
            return False
    
    def get_customers_statistics(self) -> Dict[str, Any]:
        """获取客户统计信息"""
        try:
            response = self.get(f"{self.endpoint}statistics/")
            return response if isinstance(response, dict) else {}
        except APIException as e:
            print(f"获取客户统计信息失败: {e}")
            return {}
    
    def export_customers(self, params: Dict[str, Any] = None) -> Optional[bytes]:
        """导出客户数据"""
        try:
            # 这里应该返回文件内容，但由于是模拟，返回None
            print("导出客户数据功能需要后端支持")
            return None
        except APIException as e:
            print(f"导出客户数据失败: {e}")
            return None
    
    def import_customers(self, file_data: bytes) -> Dict[str, Any]:
        """导入客户数据"""
        try:
            # 这里应该上传文件，但由于是模拟，返回空结果
            print("导入客户数据功能需要后端支持")
            return {"success": 0, "failed": 0, "errors": []}
        except APIException as e:
            print(f"导入客户数据失败: {e}")
            return {"success": 0, "failed": 0, "errors": [str(e)]}

# 创建全局实例
customers_api = CustomersAPI()

# 导出
__all__ = ['CustomersAPI', 'customers_api']
