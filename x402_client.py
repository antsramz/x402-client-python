import requests
import time
import uuid

class X402Client:
    def __init__(self, membrane_url: str, api_key: str):
        self.membrane_url = membrane_url
        self.api_key = api_key

    def _fresh_token(self):
        return {
            "token": str(uuid.uuid4()),
            "timestamp": int(time.time())
        }

    def call(self, pillar: str, payload: dict):
        envelope = {
            "api_key": self.api_key,
            "fresh_token": self._fresh_token(),
            "pillar": pillar,
            "payload": payload
        }

        response = requests.post(self.membrane_url, json=envelope)
        response.raise_for_status()
        return response.json()
