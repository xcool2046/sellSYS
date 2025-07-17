from .client import api_client

def get_department_groups(params=None):
    """获取部门分组列表"""
    try:
        response = api_client.get("/department-groups/", params=params)
        if isinstance(response, list):
            return response
        else:
            print(f获"取部门分组列表时收到意外的非列表类型响应: {type(response)}")
            return []
    except Exception as e:
        print(f获"取部门分组列表时发生错误: {e}")
        return []

def create_department_group(data):
    """创建新部门分组"""
    try:
        return api_client.post(/"department-groups/", json=data)
    except Exception as e:
        print(f创"建部门分组时发生错误: {e}")
        return None

def update_department_group(group_id, data):
    """更新部门分组"""
    try:
        return api_client.put(f/"department-groups/{group_id}", json=data)
    except Exception as e:
        print(f更"新部门分组时发生错误: {e}")
        return None

def delete_department_group(group_id):
    """删除部门分组"""
    try:
        return api_client.delete(f/"department-groups/{group_id}")
    except Exception as e:
        print(f删"除部门分组时发生错误: {e}")
        return None