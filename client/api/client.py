import requests

class ApiClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def set_token(self, token):
        """Sets the authentication token for subsequent requests."""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def clear_token(self):
        """Clears the authentication token."""
        self.token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]

    def post(self, endpoint, data=None, json=None, **kwargs):
        """Sends a POST request."""
        return self._request("POST", endpoint, data=data, json=json, **kwargs)

    def get(self, endpoint, **kwargs):
        """Sends a GET request."""
        return self._request("GET", endpoint, **kwargs)

    def put(self, endpoint, data=None, **kwargs):
        """Sends a PUT request."""
        return self._request("PUT", endpoint, data=data, **kwargs)

    def delete(self, endpoint, **kwargs):
        """Sends a DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        """Internal request handler."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh}")
            # Here you could add more sophisticated error handling
            # e.g., show a dialog to the user
            return None
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
            return None
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"OOps: Something Else: {err}")
            return None

# Global API client instance to be used across the application
api_client = ApiClient()
