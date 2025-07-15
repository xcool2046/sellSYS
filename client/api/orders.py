from .client import api_client

def get_orders(params=None):
    """
    Fetches a list of orders.
    """
    try:
        orders = api_client.get("/orders/", params=params)
        return orders
    except Exception as e:
        print(f"An error occurred while fetching orders: {e}")
        return None

def create_order(order_data):
    """
    Creates a new order.
    """
    try:
        order = api_client.post("/orders/", json=order_data)
        return order
    except Exception as e:
        print(f"An error occurred while creating an order: {e}")
        return None

def update_order_financials(order_id: int, financial_data):
    """
    Updates the financial information for a specific order.
    """
    try:
        order = api_client.put(f"/orders/{order_id}/financials", json=financial_data)
        return order
    except Exception as e:
        print(f"An error occurred while updating order financials: {e}")
        return None