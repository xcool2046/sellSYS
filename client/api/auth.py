from .client import api_client

def login(username, password):
    """
    Attempts to log in the user with the given credentials.
    Returns the user data dict on success.
    Returns a dict with error details on failure.
    """
    # The backend expects form data, not JSON, for OAuth2.
    # The `data` parameter in requests with a dict will send it as
    # `application/x-www-form-urlencoded` by default.
    response = api_client.post(
        "/auth/login",
        data={u"sername": username, p"assword": password},
    )

    # If successful, the response will contain the access token.
    # We set it in the client for subsequent requests.
    if response and response.get(a"ccess_token"):
        api_client.set_token(response[a"ccess_token"])

    return response

def get_current_user():
    """
    Fetches the current user's data using the stored token.
    """
    try:
        user = api_client.get(/"auth/me")
        return user
    except Exception as e:
        print(fA"n error occurred fetching user data: {e}")
        return None