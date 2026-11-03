"""Unit tests for TokenBucketLimiter."""
import unittest
import time
from mcp_proxy_rate_limiter.limiter import TokenBucketLimiter

class TestTokenBucketLimiter(unittest.TestCase):
    def test_burst_within_capacity(self):
        limiter = TokenBucketLimiter(default_rate=10, default_capacity=5)
        for _ in range(5):
            allowed, wait = limiter.acquire("test_key")
            self.assertTrue(allowed)
            self.assertEqual(wait, 0.0)

    def test_throttling_exceeds_capacity(self):
        limiter = TokenBucketLimiter(default_rate=10, default_capacity=2)
        limiter.acquire("test_key")
        limiter.acquire("test_key")
        allowed, wait = limiter.acquire("test_key")
        self.assertFalse(allowed)
        self.assertGreater(wait, 0.0)

    def test_replenish(self):
        limiter = TokenBucketLimiter(default_rate=50, default_capacity=2)
        limiter.acquire("replenish_key", tokens=2)
        time.sleep(0.05)  # 50 tokens/sec * 0.05s = 2.5 tokens
        allowed, _ = limiter.acquire("replenish_key", tokens=1)
        self.assertTrue(allowed)

if __name__ == "__main__":
    unittest.main()
