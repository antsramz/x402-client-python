# x402 Client SDK (Python)

A minimal, deterministic Python client for interacting with the x402 membrane.

## Install dependencies

pip install -r requirements.txt

## Usage

from x402_client import X402Client

client = X402Client(
membrane_url="https://x402-mem.yourdomain.com",
api_key="YOUR_API_KEY"
)

result = client.call(
pillar="schema",
payload={"example": "hello world"}
)

print(result)

## Notes

- All requests must go through the membrane.
- Pillars cannot be called directly.
- Fresh tokens are generated automatically.
- This SDK is immutable and requires no maintenance.
