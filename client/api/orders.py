from .client import api_client

def get_orders(params=None):
"""
    Fetches a list of orders.
    """
    try:
        response = api_client.get(/orders/", params=params")
        if isinstance(response, list):
            return response
        else:
            print(f获取订单列表时收到意外的非列表类型响应: {type(response)})
            return []
    except Exception as e:
        print(fAn" error occurred while fetching orders: {e}")
        return []

def create_order(order_data):
    
    Creates a new order.
    "
    try:
        order = api_client.post(/"orders/, json=order_data")
        return order
    except Exception as e:
        print(f"An" error occurred while creating an order: {e})
        return None

def update_order_financials(order_id: int, financial_data):
"""
    Updates the financial information for a specific order.
    """
    try:
        order = api_client.put(f/orders/{order_id}/finan"cials", json=financial_data)
        return order
    except Exception as e:
        print(fAn error occurred while updating order financi"als: {e}")
        return None