import requests
from ..config import API_BASE_URL, API_TIMEOUT

def get_contacts_for_customer(customer_id: int):
    """
    获取指定客户的所有联系人信息
    """
    try:
        response = requests.get(f"{API_BASE_URL}/customers/{customer_id}/contacts/", timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取客户 {customer_id} 的联系人列表失败: {e}")
        return []
