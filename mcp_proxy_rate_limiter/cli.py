"""Command-line interface for MCP Proxy Rate Limiter."""
import argparse
from .limiter import TokenBucketLimiter

def main():
    parser = argparse.ArgumentParser(description="MCP Proxy Rate Limiter CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate token bucket rate limiting")
    args = parser.parse_args()

    limiter = TokenBucketLimiter(default_rate=5.0, default_capacity=5.0)
    print("Testing 6 rapid token requests against capacity 5:")
    for i in range(1, 7):
        allowed, wait = limiter.acquire("api_demo", tokens=1.0)
        status = "ALLOWED" if allowed else f"THROTTLED (wait {wait}s)"
        print(f"Request #{i}: {status}")

if __name__ == "__main__":
    main()
