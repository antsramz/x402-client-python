import hmac
import hashlib
import time
import requests

class X402Client:
    # Protocol Constants (The Immutable Fee Table)
    PILLARS = {
        "identity": 0.005,
        "schema":   0.001,
        "arb":      0.02
    }

    def __init__(self, membrane_url: str, secret_key: str):
        """
        secret_key: Used for HMAC signing. Never transmitted in plain text.
        """
        self.url = membrane_url.rstrip('/')
        self.secret = secret_key.encode()

    def _generate_attestation(self, pillar: str, payload_str: str):
        """
        Creates a low-entropy cryptographic proof of payment intent.
        """
        timestamp = str(int(time.time()))
        fee = str(self.PILLARS.get(pillar, 0))
        # Deterministic message structure: TS + PILLAR + FEE + BODY
        message = f"{timestamp}{pillar}{fee}{payload_str}".encode()
        signature = hmac.new(self.secret, message, hashlib.sha256).hexdigest()
        return signature, timestamp

    def call(self, pillar: str, payload: dict):
        if pillar not in self.PILLARS:
            raise ValueError(f"Invalid Pillar: {pillar}. Access Denied.")

        payload_str = str(payload)
        signature, timestamp = self._generate_attestation(pillar, payload_str)

        # Standardized Protocol Headers
        headers = {
            "X-402-Signature": signature,
            "X-402-Timestamp": timestamp,
            "X-402-Fee": str(self.PILLARS[pillar]),
            "Content-Type": "application/json"
        }

        # Mathematical Routing: Membrane enforces the path
        endpoint = f"{self.url}/{pillar}"
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
