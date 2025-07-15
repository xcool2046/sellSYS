from .client import api_client

def get_customers(params=None):
    """
    Fetches a list of customers.
    Supports optional query parameters for filtering, sorting, and pagination.
    
    :param params: A dictionary of query parameters.
                   e.g., {"skip": 0, "limit": 10, "status": "active"}
    :return: A list of customer dictionaries or None on failure.
    """
    try:
        customers = api_client.get("/customers/", params=params)
        return customers
    except Exception as e:
        print(f"An error occurred while fetching customers: {e}")
        return None

def create_customer(customer_data):
    """
    Creates a new customer.
    
    :param customer_data: A dictionary containing the new customer's info.
    :return: The created customer's data or None on failure.
    """
    try:
        customer = api_client.post("/customers/", json=customer_data)
        return customer
    except Exception as e:
        print(f"An error occurred while creating a customer: {e}")
        return None

# Add other customer-related API functions (update, delete, get by id) here as needed.