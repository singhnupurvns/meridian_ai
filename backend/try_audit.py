import sys
import time

from agent.agents import ProcurementSupervisor

REQUESTS = {
    "approved": """
    Purchase Request – Aldermoor Industries Global Procurement:
    - Vendor: Mitsubishi Electric (Japan)
    - Item: 20 spare servo motors for the Aldermoor filling line
    - Total Cost: 38,000 EUR
    """,
    "hold": """
    Purchase Request – Aldermoor Industries Global Procurement:
    - Vendor: (put vendor here)
    - Item: (put item here)
    - Total Cost: (put amount here) EUR
    """,
    "rejected": """
    Purchase Request – Aldermoor Industries Global Procurement:
    - Vendor: (put vendor here)
    - Item: (put item here)
    - Total Cost: (put amount here) EUR
    """,
}

scenario = sys.argv[1] if len(sys.argv) > 1 else "hold"
started = time.time()
audit = ProcurementSupervisor().run_audit(REQUESTS[scenario])

print(f"\n=== {scenario}: audit finished in {time.time() - started:.0f} s")
for name in ("risk_result", "tax_result", "control_result"):
    verdicts = [line.strip() for line in audit[name].splitlines() if "VERDICT" in line]
    print(f"{name:15}", verdicts[0] if verdicts else "(no verdict line)")
print("\n" + audit["cfo_memo"])