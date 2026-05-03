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
