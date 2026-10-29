"""See a tool the way the model sees it, then check the FX rule twice.
Run from backend/: uv run python try_tools.py"""
import requests
from agent.tools import validate_fx_hedge

print("name:", validate_fx_hedge.name)
print("description:", validate_fx_hedge.description)
print("arguments:", validate_fx_hedge.args)

response = requests.get(
    "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=INR", timeout=10
)
response.raise_for_status()
live_rate = response.json()["rates"]["INR"]
print("Live rate:", live_rate)

for factor in (1.01, 1.07):  # 1% and 7% away from the live rate
    rate_used = round(live_rate * factor, 2)
    result = validate_fx_hedge.invoke(
        {"currency_pair": "EUR_INR", "rate_used": rate_used}  # names must match .args
    )
    print(f"factor {factor} -> rate {rate_used}: {result}")
