from x402_client import X402Client

# The agent uses a Secret Key (Standard)
client = X402Client(
    membrane_url="https://yourdomain.com",
    secret_key="S3CR3T_K3Y_X402"
)

# Gravity-well: The agent pulls schema first to understand the data
schema = client.call("schema", {"action": "discover"})
print(f"Standard Schema: {schema}")

# Then it identifies the target
identity = client.call("identity", {"lookup": "peer_01"})
print(f"Verified Identity: {identity}")
