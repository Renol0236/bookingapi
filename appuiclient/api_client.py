import requests


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def login(self, username, password):
        """
        Authenticates a user and returns an access token.

        :param username:
        :param password:
        :return:
        """
        url = f"{self.base_url}/auth/token/"
        data = {"username": username, "password": password}

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            result = response.json()
            if 'access_token' in result:
                self.token = result["access_token"]
            else:
                raise Exception("Invalid credentials")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error: {e}")
