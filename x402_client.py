class X402Client:
    # HARDCODED CONSTANTS - Agents cannot change these
    PROTOCOL_FEES = {
        "identity": 0.005,
        "schema": 0.001,
        "arb": 0.02
    }

    def call(self, primitive, payload):
        # 1. Look up the frozen fee
        fee = self.PROTOCOL_FEES.get(primitive)
        if not fee:
            raise ValueError(f"Unknown primitive: {primitive}")

        # 2. Include the 'fee' in the HMAC signature calculation
        # This ensures the agent CANNOT tamper with the price.
        signature = self._sign(payload, fee) 
        
        # 3. Proceed with the request...
