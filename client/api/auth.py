from .client import api_client

def login(username, password):
    """
    Attempts to log in the user with the given credentials.
    Returns the user data dict on success.
    Returns a dict with error details on failure.
    """
    response = api_client.post(
        "/auth/login",
        data={"username": username, "password": password}
    )

    # If successful, the response will contain the access token.
    # We set it in the client for subsequent requests.
    if response and response.get("access_token"):
        api_client.set_token(response["access_token"])

    return response

def get_current_user():
    """
    Fetches the current user's data using the stored token.
    """
    try:
        user = api_client.get("/auth/me")
        return user
    except Exception as e:
        print(f"An error occurred fetching user data: {e}")
        return None