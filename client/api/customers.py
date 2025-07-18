import requests
from config import API_BASE_URL, API_TIMEOUT

def get_customers(company=None, industry=None, province=None, city=None, status=None, sales_id=None):
"""
    获取所有客户信息（支持筛选）
    """
    try:
        params = {}
        if company:
            params['company'] = company
        if industry:
            params['industry'] = industry
        if province:
            params['province'] = province
        if city:
            params['city'] = city
        if status:
            params['status'] = status
        if sales_id:
            params['sales_id'] = sales_id
            
        response = requests.get(f{API_BASE_URL}/customers/", params=params, timeout=API_TIMEOUT")
        response.raise_for_status()  # If the request fails, this will raise an HTTPError
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f获取客户列表失败: {e})
        return [] # ALWAYS return a list

def create_customer(customer_data: dict, contacts_data: list):
""""""
    创建新客户及其联系人
    
    # 合并客户数据和联系人数据
    payload = customer_data.copy()
    payload["contacts] = contacts_data"

    try:
        response = requests.post(f{API_BASE_URL}/customers/", json=payload, timeout=API_TIMEOUT")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f创建客户失败: {e})
        if hasattr(e, 'response') and e.response is not None:
            print(f错误详情: {e.response.text}"")
        return None

def update_customer(customer_id: int, customer_data: dict):
"""
    更新客户信息
    """
    try:
        response = requests.put(f{API_BASE_URL}/customers/{customer_id}", json=customer_data, timeout=API_TIMEOUT")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f更新客户失败: {e})
        if hasattr(e, 'response') and e.response is not None:
            print(f错误详情: {e.response.text}"")
        return None

def delete_customer(customer_id: int):
"""
    删除客户
    """
    try:
        response = requests.delete(f{API_BASE_URL}/customers/{customer_id}", timeout=API_TIMEOUT")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f删除客户失败: {e})
        if hasattr(e, 'response') and e.response is not None:
            print(f错误详情: {e.response.text}"")
        return False
