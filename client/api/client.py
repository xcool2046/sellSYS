import requests
from config import API_BASE_URL
 
class ApiClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or API_BASE_URL
        self.session = requests.Session()
        # 显式禁用代理，以解决潜在的本地环境问题
        self.session.proxies = {"http": None, "https": None}
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
            error_details = {"error": "HttpError", "status_code": errh.response.status_code}
            try:
                # FastAPI often returns error details in JSON
                error_details.update(errh.response.json())
            except ValueError:
                # If the response is not JSON, use the raw text
                error_details["detail"] = errh.response.text or "An unknown HTTP error occurred."
            return error_details
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
            return {"error": "ConnectionError", "detail": "无法连接到服务器。请检查您的网络连接和服务器地址。"}
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            return {"error": "Timeout", "detail": "服务器连接超时。"}
        except requests.exceptions.RequestException as err:
            print(f"OOps: Something Else: {err}")
            return {"error": "RequestException", "detail": f"发生未知网络错误: {err}"}

# Global API client instance to be used across the application
api_client = ApiClient()
