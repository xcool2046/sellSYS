from .client import api_client

def get_sales_follows_by_customer(customer_id: int, params=None):
    """
    Fetches sales follow-up records for a specific customer.
    """
    try:
        follows = api_client.get(f"/sales-follows/customer/{customer_id}", params=params)
        return follows
    except Exception as e:
        print(f"An error occurred while fetching sales follows: {e}")
        return None

def create_sales_follow(follow_data):
    """
    Creates a new sales follow-up record.
    """
    try:
        follow = api_client.post("/sales-follows/", json=follow_data)
        return follow
    except Exception as e:
        print(f"An error occurred while creating a sales follow: {e}")
        return None