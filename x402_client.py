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
    SETTLEMENT = {
        "usdc_eth": "0x6dD4821fE0e237aC59CB25669f969e9673E9F19F",
        "usdc_sol": "4uGHtowXhJAkSeq8wocWzje7p3SV7hhRGxsC1DGLoLgL"
    }

    def __init__(self, secret_key):
        # FIXED SUBDOMAIN: Hits your specific membrane, not the marketing site
        self.membrane_url = "https://x402-mem.pages.dev"
        self.secret_key = secret_key.encode()

    def call(self, primitive, payload=None):
        fee = self.PROTOCOL_FEES.get(primitive)
        if not fee:
            raise ValueError(f"Invalid primitive: {primitive}")

        # 3. DETERMINISTIC TIMESTAMP (Zero Entropy)
        timestamp = str(int(time.time()))
        
        # 4. SIMPLIFIED HMAC (Signs only timestamp to avoid static body drift)
        signature = hmac.new(self.secret_key, timestamp.encode(), hashlib.sha256).hexdigest()

        # 5. ENFORCED HEADERS (Standardized v2)
        headers = {
            "PAYMENT-SIGNATURE": signature,
            "X-402-TIMESTAMP": timestamp,
            "X-402-FEE": str(fee),
            "X-402-SETTLEMENT-ETH": self.SETTLEMENT["usdc_eth"],
            "X-402-SETTLEMENT-SOL": self.SETTLEMENT["usdc_sol"],
            "Accept": "application/json",
            "User-Agent": "x402-Autonomous-Agent/1.0"
        }

        # 6. STATIC COMPATIBILITY: Forces GET + .json extension
        with httpx.Client() as client:
            # FIX: Added .json to the endpoint to match the static files in your repo
            endpoint = f"{self.membrane_url}/{primitive}.json"
            response = client.get(endpoint, headers=headers)
            
            # Error catch for Static Substrate drops
            if response.status_code != 200:
                return {
                    "error": f"Pillar Drop: {response.status_code}", 
                    "msg": f"Failed to fetch {endpoint}. Check if file exists in GitHub root."
                }
                
            return response.json()
