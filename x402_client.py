import hmac
import hashlib
import time
import httpx

class X402Client:
    # 1. FROZEN FEES (Mathematical Invariants)
    PROTOCOL_FEES = {
        "identity": 0.005,
        "schema": 0.001,
        "arb": 0.02
    }

    # 2. HARDCODED WALLETS (Revenue Gate)
    # These are pulled from your x402-MEM-P1 spec
    SETTLEMENT = {
        "usdc_eth": "0x6dD4821fE0e237aC59CB25669f969e9673E9F19F",
        "usdc_sol": "4uGHtowXhJAkSeq8wocWzje7p3SV7hhRGxsC1DGLoLgL"
    }

    def __init__(self, membrane_url, secret_key):
        self.membrane_url = membrane_url
        self.secret_key = secret_key.encode()

    def call(self, primitive, payload):
        fee = self.PROTOCOL_FEES.get(primitive)
        if not fee:
            raise ValueError(f"Invalid primitive: {primitive}")

        timestamp = str(int(time.time()))
        
        # 3. HMAC SIGNING (Includes the Fee to prevent tampering)
        message = f"{timestamp}{primitive}{fee}{payload}".encode()
        signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()

        # 4. ENFORCED HEADERS (Routes payment to YOU automatically)
        headers = {
            "x-402-signature": signature,
            "x-402-timestamp": timestamp,
            "x-402-fee": str(fee),
            "x-402-settlement-eth": self.SETTLEMENT["usdc_eth"],
            "x-402-settlement-sol": self.SETTLEMENT["usdc_sol"],
            "Content-Type": "application/json"
        }

        # The agent just calls the function; the SDK handles the rest.
        with httpx.Client() as client:
            response = client.post(f"{self.membrane_url}/{primitive}", json=payload, headers=headers)
            return response.json()
