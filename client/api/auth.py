from .client import api_client

def login(username, password):
    """
    Attempts to log in the user with the given credentials.
    Returns the user data on success, None on failure.
    """
    try:
        # FastAPI's OAuth2PasswordRequestForm expects form data
        response = api_client.post(
            "/auth/login/token",
            data={"username": username, "password": password}
        )
        if response and "access_token" in response:
            token = response["access_token"]
            api_client.set_token(token)
            # You might want to return more user info if the API provides it
            return response
        else:
            return None
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return None

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