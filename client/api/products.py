import requests
from config import API_BASE_URL, API_TIMEOUT

BASE_URL = API_BASE_URL

def get_products(name: str = None):
    """
    获取所有产品信息, 可选地通过名称进行筛选
    """
    try:
        params = {}
        if name:
            params['name'] = name
            
        response = requests.get(f"{BASE_URL}/products/", params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            print(f"获取产品列表时收到意外的非列表类型响应: {type(data)}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"获取产品列表失败: {e}")
        return []

def create_product(product_data):
    """
    创建新产品
    
    Args:
        product_data: 包含产品信息的字典
    
    Returns:
        创建的产品信息，如果失败返回None
    """
    try:
        response = requests.post(f"{BASE_URL}/products/", json=product_data, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"创建产品失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"错误详情: {e.response.text}")
        return None

def update_product(product_id, product_data):
    """
    更新产品信息
    
    Args:
        product_id: 产品ID
        product_data: 包含更新信息的字典
    
    Returns:
        更新后的产品信息，如果失败返回None
    """
    try:
        response = requests.put(f"{BASE_URL}/products/{product_id}", json=product_data, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"更新产品失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"错误详情: {e.response.text}")
        return None

def delete_product(product_id):
    """
    删除产品
    
    Args:
        product_id: 产品ID
    
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.delete(f"{BASE_URL}/products/{product_id}", timeout=API_TIMEOUT)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"删除产品失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"错误详情: {e.response.text}")
        return False
