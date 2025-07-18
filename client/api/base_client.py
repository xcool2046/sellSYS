"""
API客户端基础类
"""
import requests
import json
from typing import Dict, Any, Optional, List
from config_clean import API_BASE_URL, API_TIMEOUT, DEBUG

class APIException(Exception):
    """API异常类"""
    def __init__(self, message: str, status_code: int = None, response_data: Dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}

class BaseAPIClient:
    """API客户端基础类"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.session = requests.Session()
        
        # 设置默认请求头
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'SellSYS-Client/1.0'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发起HTTP请求"""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            if DEBUG:
                print(f"[API] {method.upper()} {url}")
                if 'json' in kwargs:
                    print(f"[API] Request data: {kwargs['json']}")
            
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            if DEBUG:
                print(f"[API] Response status: {response.status_code}")
            
            # 检查响应状态
            if response.status_code >= 400:
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise APIException(
                    message=f"API请求失败: {response.status_code}",
                    status_code=response.status_code,
                    response_data=error_data
                )
            
            # 解析响应
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"message": "Success", "data": response.text}
                
        except requests.exceptions.Timeout:
            raise APIException("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise APIException("连接失败，请检查服务器状态")
        except requests.exceptions.RequestException as e:
            raise APIException(f"请求异常: {str(e)}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET请求"""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST请求"""
        return self._make_request('POST', endpoint, json=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """PUT请求"""
        return self._make_request('PUT', endpoint, json=data)
    
    def patch(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """PATCH请求"""
        return self._make_request('PATCH', endpoint, json=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE请求"""
        return self._make_request('DELETE', endpoint)
    
    def set_auth_token(self, token: str):
        """设置认证令牌"""
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def clear_auth_token(self):
        """清除认证令牌"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']

class CRUDAPIClient(BaseAPIClient):
    """CRUD操作API客户端基础类"""
    
    def __init__(self, resource_name: str):
        super().__init__()
        self.resource_name = resource_name
        self.endpoint = f"/{resource_name}/"
    
    def list(self, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """获取列表"""
        try:
            response = self.get(self.endpoint, params=params)
            
            # 处理不同的响应格式
            if isinstance(response, list):
                return response
            elif isinstance(response, dict):
                # 如果是分页响应
                if 'results' in response:
                    return response['results']
                elif 'data' in response:
                    return response['data'] if isinstance(response['data'], list) else [response['data']]
                elif 'items' in response:
                    return response['items']
                else:
                    return [response]
            else:
                return []
                
        except APIException as e:
            print(f"获取{self.resource_name}列表失败: {e}")
            return []
    
    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取详情"""
        try:
            response = self.get(f"{self.endpoint}{item_id}/")
            return response if isinstance(response, dict) else None
        except APIException as e:
            print(f"获取{self.resource_name}详情失败: {e}")
            return None
    
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """创建新记录"""
        try:
            response = self.post(self.endpoint, data=data)
            return response if isinstance(response, dict) else None
        except APIException as e:
            print(f"创建{self.resource_name}失败: {e}")
            return None
    
    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新记录"""
        try:
            response = self.put(f"{self.endpoint}{item_id}/", data=data)
            return response if isinstance(response, dict) else None
        except APIException as e:
            print(f"更新{self.resource_name}失败: {e}")
            return None
    
    def partial_update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """部分更新记录"""
        try:
            response = self.patch(f"{self.endpoint}{item_id}/", data=data)
            return response if isinstance(response, dict) else None
        except APIException as e:
            print(f"更新{self.resource_name}失败: {e}")
            return None
    
    def delete_by_id(self, item_id: int) -> bool:
        """删除记录"""
        try:
            self.delete(f"{self.endpoint}{item_id}/")
            return True
        except APIException as e:
            print(f"删除{self.resource_name}失败: {e}")
            return False

# 创建全局API客户端实例
api_client = BaseAPIClient()

# 导出常用类
__all__ = ['BaseAPIClient', 'CRUDAPIClient', 'APIException', 'api_client']
