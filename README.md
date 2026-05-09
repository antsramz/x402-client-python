# x402 Client SDK (Python)
## Protocol: x402-MEM-P1 (Standardized)

A zero-trust, low-entropy client for M2M (Machine-to-Machine) utility. 
This SDK enforces the x402 immutable protocol and hardcoded settlement routing.

### Mathematical Invariants
1. **No API Keys:** Authorization is performed via HMAC-SHA256 signatures using a pre-shared Secret Key.
2. **Deterministic Fees:** Enforced as constants within the SDK core.
   - `/identity`: $0.005
   - `/schema`:   $0.001
   - `/arb`:      $0.02
3. **Settlement Invariants:** Fees are automatically routed to hardcoded wallet addresses:
   - **USDC (ETH):** 0x6dD4821fE0e237aC59CB25669f969e9673E9F19F
   - **USDC (SOL):** 4uGHtowXhJAkSeq8wocWzje7p3SV7hhRGxsC1DGLoLgL
4. **Stateless Membrane:** No session tracking. Every request is a unique, signed transaction.

### Usage for Agents
```python
from x402_client import X402Client

# Initialize with Secret (The Agent's PSK)
client = X402Client("https://your-membrane.com", "YOUR_PROTOCOL_SECRET")

# Exact-change automated call
# The SDK automatically handles fee calculation and wallet routing.
data = client.call("schema", {"query": "all"})
```

### Low Entropy Compliance
- **No UUIDs:** Randomness is discarded; signatures use deterministic unix timestamps.
- **Non-Mutating Logic:** Protocol parameters (fees/wallets) cannot be changed at runtime.
- **Direct Routing:** Eliminates discovery latency by using static primitive mapping.
