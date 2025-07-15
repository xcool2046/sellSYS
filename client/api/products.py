from .client import api_client

def get_products(params=None):
    """
    Fetches a list of products.
    Supports optional query parameters for filtering, sorting, and pagination.
    """
    try:
        products = api_client.get("/products/", params=params)
        return products
    except Exception as e:
        print(f"An error occurred while fetching products: {e}")
        return None

def create_product(product_data):
    """
    Creates a new product.
    """
    try:
        product = api_client.post("/products/", json=product_data)
        return product
    except Exception as e:
        print(f"An error occurred while creating a product: {e}")
        return None

# Add other product-related API functions (update, delete, get by id) here as needed.