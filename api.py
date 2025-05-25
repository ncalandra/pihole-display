import os
import requests

PIHOLE_API_URL = os.getenv("PIHOLE_API_URL")
PIHOLE_API_PASSWORD = os.getenv("PIHOLE_API_PASSWORD")


class PiHoleAPI:

    def __init__(
        self,
        pihole_api_url: str = PIHOLE_API_URL,
        pihole_api_password: str = PIHOLE_API_PASSWORD,
    ):
        self._pihole_api_url = pihole_api_url
        self._pihole_api_password = pihole_api_password
        self._session = requests.Session()
        self._session.headers = {"X-FTL-SID": self._authenticate()}

    def _authenticate(self):
        response = requests.post(
            f"{self._pihole_api_url}/auth",
            json={"password": self._pihole_api_password},
        )
        response.raise_for_status()
        return response.json()["session"]["sid"]

    def get_stats(self):
        response = self._session.get(
            f"{PIHOLE_API_URL}/stats/summary"
        )
        response.raise_for_status()
        return response.json()
