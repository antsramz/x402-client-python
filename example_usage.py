from x402_client import X402Client

# 1. Initialize with your specific production Membrane
# Points to the x402-MEM-P1 deployment, not the generic platform
client = X402Client(
    membrane_url="https://x402-mem.pages.dev",
    secret_key="S3CR3T_K3Y_X402"
)

# 2. Gravity-well: Agent pulls schema ($0.001) to verify data structure
# This is a static GET request to bypass Cloudflare security drops
schema = client.call("schema") 
print(f"Standard Schema: {schema}")

# 3. Identity Escalation: Verifying the target ($0.005)
# Accesses the x402-ID-P1 pillar once schema is understood
identity = client.call("identity")
print(f"Verified Identity: {identity}")
