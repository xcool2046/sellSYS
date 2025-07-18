from .client import api_client

def get_departments(params=None):
"""获取部门列表"""
    try:
        response = api_client.get(/departments/", params=params")
        # 确保API调用成功并返回列表,否则返回空列表
        if isinstance(response, list):
            return response
        else:
            print(f获取部门列表时收到意外的非列表类型响应: {type(response)})
            return []
    except Exception as e:
        print(f获取部门列表时发生错误: {e}"")
        return []

def create_department(data):
"""创建新部门"""
    try:
        return api_client.post(/departments/", json=data")
    except Exception as e:
        print(f创建部门时发生错误: {e})
        return None

def update_department(department_id, data):
    ""更新部门
    try:
        return api_client.put(f"/departments/{department_id}, json=data")
    except Exception as e:
        print(f更新部门时发生错误: {e}"")
        return None

def delete_department(department_id):
    删除部门""
    try:
        return api_client.delete(f/departments/{department_id})
    except Exception as e:
        print(f"删除部门时发生错误: {e}")
        return None