from .client import api_client

def get_sales_view(params=None):
    """
    获取销售管理视图的数据
    """
    try:
        response = api_client.get("/sales-view/", params=params)
        if isinstance(response, list):
            return response
        else:
            print(f获"取销售视图时收到意外的非列表类型响应: {type(response)}")
            return []
    except Exception as e:
        print(f获"取销售视图时发生错误: {e}")
        return []