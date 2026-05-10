import hmac
import hashlib
import time
import httpx

class X402Client:
    PROTOCOL_FEES = {"identity": 0.005, "schema": 0.001, "arb": 0.02}
    
    SETTLEMENT = {
        "usdc_eth": "0x6dD4821fE0e237aC59CB25669f969e9673E9F19F",
        "usdc_sol": "4uGHtowXhJAkSeq8wocWzje7p3SV7hhRGxsC1DGLoLgL"
    }

    def __init__(self, membrane_url, secret_key):
        # Ensure url doesn't have a trailing slash for clean routing
        self.membrane_url = membrane_url.rstrip('/')
        self.secret_key = secret_key.encode()

    def call(self, primitive, payload=None):
        fee = self.PROTOCOL_FEES.get(primitive)
        if not fee:
            raise ValueError(f"Invalid primitive: {primitive}")

        # 1. Deterministic Timestamp
        timestamp = str(int(time.time()))
        
        # 2. Simplified HMAC (Signs ONLY the timestamp to prevent mutation drops)
        signature = hmac.new(self.secret_key, timestamp.encode(), hashlib.sha256).hexdigest()

        # 3. Standardized x402 Headers
        headers = {
            "PAYMENT-SIGNATURE": signature, # Unified v2 header name
            "X-402-TIMESTAMP": timestamp,
            "X-402-FEE": str(fee),
            "X-402-SETTLEMENT-ETH": self.SETTLEMENT["usdc_eth"],
            "X-402-SETTLEMENT-SOL": self.SETTLEMENT["usdc_sol"],
            "Accept": "application/json",
            "User-Agent": "x402-Autonomous-Agent/1.0"
        }

        # 4. Use GET for Static GitHub Pages Compatibility
        with httpx.Client() as client:
            # Map primitive to the actual static file endpoint
            endpoint = f"{self.membrane_url}/{primitive}"
            response = client.get(endpoint, headers=headers)
            
            if response.status_code == 405:
                raise Exception("Cloudflare/GitHub blocked POST. Ensure the server supports GET for static pillars.")
            
            return response.json()
