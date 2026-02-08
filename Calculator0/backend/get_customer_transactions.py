import requests
import sys
import os

API_KEY = "9d787b27cf859b503a82cd83e58be1ec"
BASE_URL = "http://api.nessieisreal.com"

# Get customer name from command line (default to Sarah)
customer_name = sys.argv[1] if len(sys.argv) > 1 else "Sarah"

# 1. Get all customers
resp = requests.get(f"{BASE_URL}/customers?key={API_KEY}").json()
# API may return a list or a dict like {"customers": [...]}
if isinstance(resp, list):
    customers = resp
else:
    customers = resp.get("customers") or resp.get("results")
    if customers is None and isinstance(resp, dict):
        for v in resp.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                customers = v
                break
        if customers is None:
            customers = []

# 2. Find the customer (each item must be a dict with first_name)
customer = next(
    (c for c in customers if isinstance(c, dict) and customer_name.lower() in c.get("first_name", "").lower()),
    None
)
if not customer:
    print(f"Customer '{customer_name}' not found. Available: {[c.get('first_name') for c in customers if isinstance(c, dict)]}")
    sys.exit(1)
print(f"\n{'='*80}")
print(f"Customer: {customer['first_name']} {customer['last_name']}")
print(f"{'='*80}")

# 3. Get accounts
accounts = requests.get(f"{BASE_URL}/customers/{customer['_id']}/accounts?key={API_KEY}").json()
account = accounts[0]
account_id = account['_id']

print(f"Account: {account['nickname']}")
print(f"Balance: ${account['balance']:,.2f}\n")

# 4. Get purchases
purchases = requests.get(f"{BASE_URL}/accounts/{account_id}/purchases?key={API_KEY}").json()
print(f"📦 PURCHASES ({len(purchases)} total):")
print("-" * 80)
for p in sorted(purchases, key=lambda x: x.get('purchase_date', ''))[:20]:  # Show first 20
    print(f"{p.get('purchase_date')}: ${p.get('amount', 0):>8.2f} - {p.get('description', 'N/A')}")

# 5. Get deposits
deposits = requests.get(f"{BASE_URL}/accounts/{account_id}/deposits?key={API_KEY}").json()
print(f"\n💰 DEPOSITS ({len(deposits)} total):")
print("-" * 80)
for d in sorted(deposits, key=lambda x: x.get('transaction_date', ''))[:20]:  # Show first 20
    print(f"{d.get('transaction_date')}: ${d.get('amount', 0):>8.2f} - {d.get('description', 'N/A')}")

print(f"\n{'='*80}")
print(f"Total Spent: ${sum(p.get('amount', 0) for p in purchases):,.2f}")
print(f"Total Deposited: ${sum(d.get('amount', 0) for d in deposits):,.2f}")