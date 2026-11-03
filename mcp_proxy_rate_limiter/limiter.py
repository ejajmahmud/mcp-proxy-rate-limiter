"""Sliding-window token bucket rate limiter."""
import time
from typing import Dict, Tuple, Any


class TokenBucketLimiter:
    def __init__(self, default_rate: float = 10.0, default_capacity: float = 20.0):
        self.default_rate = default_rate  # tokens per second
        self.default_capacity = default_capacity
        self._buckets: Dict[str, Dict[str, float]] = {}

    def _get_bucket(self, key: str, rate: float, capacity: float) -> Dict[str, float]:
        if key not in self._buckets:
            self._buckets[key] = {
                "tokens": capacity,
                "last_update": time.time(),
                "rate": rate,
                "capacity": capacity
            }
        return self._buckets[key]

    def acquire(self, key: str, tokens: float = 1.0, rate: float = None, capacity: float = None) -> Tuple[bool, float]:
        r = rate or self.default_rate
        c = capacity or self.default_capacity
        now = time.time()

        bucket = self._get_bucket(key, r, c)
        elapsed = now - bucket["last_update"]
        bucket["last_update"] = now

        # Replenish tokens
        bucket["tokens"] = min(bucket["capacity"], bucket["tokens"] + (elapsed * bucket["rate"]))

        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            return True, 0.0
        else:
            needed = tokens - bucket["tokens"]
            wait_time = needed / bucket["rate"]
            return False, round(wait_time, 4)

    def stats(self, key: str) -> Dict[str, Any]:
        if key not in self._buckets:
            return {"key": key, "tokens": self.default_capacity, "rate": self.default_rate}
        b = self._buckets[key]
        return {
            "key": key,
            "available_tokens": round(b["tokens"], 2),
            "rate_per_sec": b["rate"],
            "capacity": b["capacity"]
        }
