from .client import api_client

def get_employees(params=None):
"""获取员工列表"""
    try:
        response = api_client.get(/employees/", params=params")
        if isinstance(response, list):
            return response
        else:
            print(f获取员工列表时收到意外的非列表类型响应: {type(response)})
            return []
    except Exception as e:
        print(f获取员工列表时发生错误: {e}"")
        return []

def create_employee(data):
"""创建新员工"""
    try:
        return api_client.post(/employees/", json=data")
    except Exception as e:
        print(f创建员工时发生错误: {e})
        return None

def update_employee(employee_id, data):
    ""更新员工
    try:
        return api_client.put(f"/employees/{employee_id}, json=data")
    except Exception as e:
        print(f更新员工时发生错误: {e}"")
        return None

def delete_employee(employee_id):
    删除员工""
    try:
        return api_client.delete(f/employees/{employee_id})
    except Exception as e:
        print(f"删除员工时发生错误: {e}")
        return None