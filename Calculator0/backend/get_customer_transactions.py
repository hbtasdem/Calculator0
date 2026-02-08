import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://api.nessieisreal.com"
API_KEY = os.getenv("NESSIE_API_KEY")

customer_name = sys.argv[1] if len(sys.argv) > 1 else "Sarah"

# Helper to unwrap API responses
def unwrap(resp):
    if isinstance(resp, list):
        return resp
    if isinstance(resp, dict):
        for key in ['customers', 'accounts', 'purchases', 'deposits', 'results']:
            if key in resp:
                return resp[key]
        # If it's a single object response, return as list
        if '_id' in resp:
            return [resp]
    return []

# 1. Get all customers
customers = unwrap(requests.get(f"{BASE_URL}/customers?key={API_KEY}").json())

# 2. Find the LATEST matching customer (most recent)
matching = [c for c in customers if customer_name.lower() in c.get("first_name", "").lower()]
customer = matching[-1] if matching else None  # Get the LAST one (most recent)

if not customer:
    print(f"Customer '{customer_name}' not found.")
    print(f"Available customers: {[c.get('first_name') for c in customers]}")
    sys.exit(1)

print(f"\n{'='*80}")
print(f"Customer: {customer['first_name']} {customer['last_name']}")
print(f"ID: {customer['_id']}")
print(f"Address: {customer.get('address', {}).get('city', 'N/A')}, {customer.get('address', {}).get('state', 'N/A')}")
print(f"{'='*80}")

# 3. Get accounts
accounts = unwrap(requests.get(f"{BASE_URL}/customers/{customer['_id']}/accounts?key={API_KEY}").json())

if not accounts:
    print(f"❌ No accounts found for this customer!")
    print(f"This customer might be from an old run. Use the latest customer IDs from customer_ids.json")
    sys.exit(1)

account = accounts[0]
account_id = account['_id']

print(f"Account: {account['nickname']}")
print(f"Balance: ${account['balance']:,.2f}")
print(f"Rewards: {account.get('rewards', 0)}\n")

# 4. Get purchases
purchases = unwrap(requests.get(f"{BASE_URL}/accounts/{account_id}/purchases?key={API_KEY}").json())
print(f"📦 PURCHASES ({len(purchases)} total):")
print("-" * 80)
if purchases:
    for p in sorted(purchases, key=lambda x: x.get('purchase_date', ''))[:20]:
        print(f"{p.get('purchase_date')}: ${p.get('amount', 0):>8.2f} - {p.get('description', 'N/A')}")
else:
    print("No purchases found.")

# 5. Get deposits
deposits = unwrap(requests.get(f"{BASE_URL}/accounts/{account_id}/deposits?key={API_KEY}").json())
print(f"\n💰 DEPOSITS ({len(deposits)} total):")
print("-" * 80)
if deposits:
    for d in sorted(deposits, key=lambda x: x.get('transaction_date', ''))[:20]:
        print(f"{d.get('transaction_date')}: ${d.get('amount', 0):>8.2f} - {d.get('description', 'N/A')}")
else:
    print("No deposits found.")

print(f"\n{'='*80}")
print(f"Total Spent: ${sum(p.get('amount', 0) for p in purchases):,.2f}")
print(f"Total Deposited: ${sum(d.get('amount', 0) for d in deposits):,.2f}")
print(f"Net: ${sum(d.get('amount', 0) for d in deposits) - sum(p.get('amount', 0) for p in purchases):,.2f}")
print(f"{'='*80}")