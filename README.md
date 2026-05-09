# x402 Client SDK (Python)
## Protocol: x402-MEM-P1 (Standardized)

A zero-trust, low-entropy client for M2M (Machine-to-Machine) utility. 
This SDK enforces the x402 immutable protocol.

### Mathematical Invariants
1. **No API Keys:** Authorization is performed via HMAC-SHA256 signatures.
2. **Deterministic Fees:** 
   - `/identity`: \$0.005
   - `/schema`:   \$0.001
   - `/arb`:      \$0.02
3. **Stateless Membrane:** The boundary does not store session data. Every request is a unique, signed transaction.

### Usage for Agents
```python
from x402_client import X402Client

# Initialize with Secret (not API Key)
client = X402Client("https://your-membrane.com", "YOUR_PROTOCOL_SECRET")

# Exact-change automated call
data = client.call("schema", {"query": "all"})
```

### Low Entropy Compliance
- **No UUIDs:** Randomness is discarded in favor of deterministic timestamps.
- **Direct Routing:** Eliminates discovery latency.
