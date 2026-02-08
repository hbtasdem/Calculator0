"""
Financial Abuse Detection - Mock Data Generator
Generates realistic banking data across 3 customer profiles showing different levels of financial abuse
"""

import requests
import json
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://api.nessieisreal.com"
API_KEY = os.getenv("NESSIE_API_KEY")

"""
Financial Abuse Detection - Mock Data Generator
Generates realistic banking data across 5 customer profiles showing different levels of financial abuse
"""

class FinancialAbuseDataGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.customers = {}
        self.accounts = {}
        self.merchants = {}
        
    def _make_request(self, method, endpoint, data=None):
        """Helper method to make API requests"""
        url = f"{self.base_url}{endpoint}?key={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, headers=headers)
        
        return response.json()
    
    def create_customer(self, first_name, last_name, address):
        """Create a customer"""
        customer_data = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address
        }
        result = self._make_request("POST", "/customers", customer_data)
        print(f"DEBUG - Create customer response: {result}")
        print(f"Created customer: {first_name} {last_name}")
        return result
    
    def create_account(self, customer_id, account_type, nickname, balance, rewards=0):
        """Create an account for a customer"""
        account_data = {
            "type": account_type,
            "nickname": nickname,
            "rewards": rewards,
            "balance": balance
        }
        result = self._make_request("POST", f"/customers/{customer_id}/accounts", account_data)
        
        print(f"DEBUG - Account creation for customer {customer_id}")
        print(f"DEBUG - Account data: {account_data}")
        print(f"DEBUG - API Response: {result}")
        
        if "objectCreated" in result:
            print(f"✅ Created account: {nickname}")
        else:
            print(f"❌ Failed to create account: {result}")
        
        return result
    
    def create_merchant(self, name, category, address, geocode):
        """Create a merchant"""
        merchant_data = {
            "name": name,
            "category": category,
            "address": address,
            "geocode": geocode
        }
        result = self._make_request("POST", "/merchants", merchant_data)
        print(f"Created merchant: {name}")
        return result
    
    def create_purchase(self, account_id, merchant_id, amount, purchase_date, description, status="executed", medium="balance"):
        """Create a purchase transaction"""
        purchase_data = {
            "merchant_id": merchant_id,
            "medium": medium,
            "purchase_date": purchase_date,
            "amount": amount,
            "status": status,
            "description": description
        }
        result = self._make_request("POST", f"/accounts/{account_id}/purchases", purchase_data)
        return result
    
    def create_deposit(self, account_id, amount, transaction_date, description, status="executed", medium="balance"):
        """Create a deposit transaction"""
        deposit_data = {
            "medium": medium,
            "transaction_date": transaction_date,
            "amount": amount,
            "status": status,
            "description": description
        }
        result = self._make_request("POST", f"/accounts/{account_id}/deposits", deposit_data)
        return result
    
    def setup_merchants(self):
        """Create common merchants used across all scenarios"""
        merchants_list = [
            {
                "name": "Whole Foods Market",
                "category": "Groceries",
                "address": {
                    "street_number": "1000",
                    "street_name": "Market St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94102"
                },
                "geocode": {"lat": 37.7749, "lng": -122.4194}
            },
            {
                "name": "Target",
                "category": "Retail",
                "address": {
                    "street_number": "2000",
                    "street_name": "Mission St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94110"
                },
                "geocode": {"lat": 37.7599, "lng": -122.4148}
            },
            {
                "name": "Walgreens Pharmacy",
                "category": "Pharmacy",
                "address": {
                    "street_number": "500",
                    "street_name": "Powell St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94102"
                },
                "geocode": {"lat": 37.7867, "lng": -122.4088}
            },
            {
                "name": "Starbucks",
                "category": "Coffee",
                "address": {
                    "street_number": "300",
                    "street_name": "Main St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94105"
                },
                "geocode": {"lat": 37.7908, "lng": -122.3954}
            },
            {
                "name": "CVS Pharmacy",
                "category": "Pharmacy",
                "address": {
                    "street_number": "700",
                    "street_name": "Geary St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94109"
                },
                "geocode": {"lat": 37.7858, "lng": -122.4134}
            },
            {
                "name": "Safeway",
                "category": "Groceries",
                "address": {
                    "street_number": "1200",
                    "street_name": "Webster St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94115"
                },
                "geocode": {"lat": 37.7833, "lng": -122.4324}
            },
            {
                "name": "AMC Movie Theater",
                "category": "Entertainment",
                "address": {
                    "street_number": "1000",
                    "street_name": "Van Ness Ave",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94109"
                },
                "geocode": {"lat": 37.7858, "lng": -122.4229}
            },
            {
                "name": "Planet Fitness",
                "category": "Fitness",
                "address": {
                    "street_number": "850",
                    "street_name": "Bryant St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94103"
                },
                "geocode": {"lat": 37.7716, "lng": -122.4030}
            },
            {
                "name": "Chipotle",
                "category": "Restaurant",
                "address": {
                    "street_number": "450",
                    "street_name": "Castro St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94114"
                },
                "geocode": {"lat": 37.7609, "lng": -122.4350}
            },
            {
                "name": "Uber",
                "category": "Transportation",
                "address": {
                    "street_number": "1455",
                    "street_name": "Market St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94103"
                },
                "geocode": {"lat": 37.7752, "lng": -122.4175}
            },
            {
                "name": "Sephora",
                "category": "Beauty",
                "address": {
                    "street_number": "33",
                    "street_name": "Powell St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94102"
                },
                "geocode": {"lat": 37.7866, "lng": -122.4084}
            },
            {
                "name": "Gap",
                "category": "Clothing",
                "address": {
                    "street_number": "890",
                    "street_name": "Market St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94102"
                },
                "geocode": {"lat": 37.7833, "lng": -122.4066}
            }
        ]
        
        for merchant in merchants_list:
            result = self.create_merchant(
                merchant["name"],
                merchant["category"],
                merchant["address"],
                merchant["geocode"]
            )
            if "objectCreated" in result:
                self.merchants[merchant["name"]] = result["objectCreated"]["_id"]
        
        return self.merchants
    
    def generate_customer_1_no_abuse(self, customer_id, account_id):
        """Customer 1: Sarah Johnson - No Financial Abuse"""
        print("\n=== Generating Customer 1: No Abuse (Sarah Johnson) ===")
        
        start_date = datetime.now() - timedelta(days=180)
        current_date = start_date
        
        deposits = []
        while current_date <= datetime.now():
            deposit_amount = random.uniform(2800, 3200)
            deposits.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "amount": deposit_amount,
                "description": "Payroll Deposit - ABC Company"
            })
            current_date += timedelta(days=14)
        
        for deposit in deposits:
            self.create_deposit(account_id, deposit["amount"], deposit["date"], deposit["description"])
        
        purchases = []
        grocery_dates = [start_date + timedelta(days=x*7) for x in range(26)]
        for date in grocery_dates:
            purchases.append({
                "merchant": random.choice(["Whole Foods Market", "Safeway"]),
                "amount": random.uniform(80, 150),
                "date": date.strftime("%Y-%m-%d"),
                "description": "Weekly groceries"
            })
        
        for i in range(100):
            random_date = start_date + timedelta(days=random.randint(0, 180))
            purchases.append({
                "merchant": random.choice(["Starbucks", "Chipotle"]),
                "amount": random.uniform(8, 25),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Coffee/Lunch"
            })
        
        pharmacy_dates = [start_date + timedelta(days=x*30) for x in range(6)]
        for date in pharmacy_dates:
            purchases.append({
                "merchant": random.choice(["Walgreens Pharmacy", "CVS Pharmacy"]),
                "amount": random.uniform(15, 60),
                "date": date.strftime("%Y-%m-%d"),
                "description": "Pharmacy/Health"
            })
        
        for i in range(8):
            random_date = start_date + timedelta(days=random.randint(0, 180))
            purchases.append({
                "merchant": "Sephora",
                "amount": random.uniform(30, 100),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Personal care"
            })
        
        for i in range(12):
            random_date = start_date + timedelta(days=random.randint(0, 180))
            purchases.append({
                "merchant": "AMC Movie Theater",
                "amount": random.uniform(15, 45),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Entertainment"
            })
        
        for i in range(6):
            date = start_date + timedelta(days=i*30)
            purchases.append({
                "merchant": "Planet Fitness",
                "amount": 25.00,
                "date": date.strftime("%Y-%m-%d"),
                "description": "Monthly gym membership"
            })
        
        for i in range(10):
            random_date = start_date + timedelta(days=random.randint(0, 180))
            purchases.append({
                "merchant": "Gap",
                "amount": random.uniform(40, 150),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Clothing"
            })
        
        for i in range(40):
            random_date = start_date + timedelta(days=random.randint(0, 180))
            purchases.append({
                "merchant": "Uber",
                "amount": random.uniform(12, 35),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Transportation"
            })
        
        for purchase in sorted(purchases, key=lambda x: x["date"]):
            if purchase["merchant"] in self.merchants:
                self.create_purchase(
                    account_id,
                    self.merchants[purchase["merchant"]],
                    purchase["amount"],
                    purchase["date"],
                    purchase["description"]
                )
        
        print(f"Created {len(deposits)} deposits and {len(purchases)} purchases for Customer 1")
    
    def generate_customer_2_moderate_abuse(self, customer_id, account_id):
        """Customer 2: Maria Rodriguez - Moderate Financial Abuse"""
        print("\n=== Generating Customer 2: Moderate Abuse (Maria Rodriguez) ===")
        
        start_date = datetime.now() - timedelta(days=180)
        deposits = []
        
        for i in range(6):
            date = start_date + timedelta(days=i*14)
            deposits.append({
                "date": date.strftime("%Y-%m-%d"),
                "amount": random.uniform(2600, 2900),
                "description": "Payroll Deposit - XYZ Corp"
            })
        
        for i in range(3):
            date = start_date + timedelta(days=84 + i*14)
            if i != 1:
                deposits.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "amount": random.uniform(2400, 2700),
                    "description": "Payroll Deposit - XYZ Corp"
                })
        
        for i in range(4):
            date = start_date + timedelta(days=126 + i*14)
            if i % 2 == 0:
                deposits.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "amount": random.uniform(1800, 2200),
                    "description": "Payroll Deposit - XYZ Corp"
                })
        
        for deposit in deposits:
            self.create_deposit(account_id, deposit["amount"], deposit["date"], deposit["description"])
        
        purchases = []
        phase1_end = start_date + timedelta(days=90)
        current = start_date
        
        while current < phase1_end:
            purchases.append({
                "merchant": random.choice(["Whole Foods Market", "Safeway"]),
                "amount": random.uniform(70, 130),
                "date": current.strftime("%Y-%m-%d"),
                "description": "Groceries"
            })
            current += timedelta(days=7)
        
        for i in range(15):
            random_date = start_date + timedelta(days=random.randint(0, 90))
            purchases.append({
                "merchant": random.choice(["Starbucks", "Chipotle"]),
                "amount": random.uniform(10, 28),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Personal food"
            })
        
        for i in range(4):
            random_date = start_date + timedelta(days=random.randint(0, 90))
            purchases.append({
                "merchant": "Sephora",
                "amount": random.uniform(40, 90),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Personal care"
            })
        
        for i in range(5):
            random_date = start_date + timedelta(days=random.randint(0, 90))
            purchases.append({
                "merchant": "AMC Movie Theater",
                "amount": random.uniform(15, 35),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Movie"
            })
        
        phase2_start = start_date + timedelta(days=91)
        phase2_end = start_date + timedelta(days=150)
        
        current = phase2_start
        while current < phase2_end:
            if random.random() > 0.3:
                purchases.append({
                    "merchant": "Safeway",
                    "amount": random.uniform(50, 90),
                    "date": current.strftime("%Y-%m-%d"),
                    "description": "Groceries"
                })
            current += timedelta(days=7)
        
        for i in range(5):
            random_date = start_date + timedelta(days=random.randint(91, 150))
            purchases.append({
                "merchant": "Starbucks",
                "amount": random.uniform(5, 12),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Coffee"
            })
        
        purchases.append({
            "merchant": "AMC Movie Theater",
            "amount": 14.50,
            "date": (start_date + timedelta(days=100)).strftime("%Y-%m-%d"),
            "description": "Movie"
        })
        
        phase3_start = start_date + timedelta(days=151)
        
        for i in range(3):
            date = phase3_start + timedelta(days=i*10)
            purchases.append({
                "merchant": "Safeway",
                "amount": random.uniform(30, 55),
                "date": date.strftime("%Y-%m-%d"),
                "description": "Basic groceries"
            })
        
        purchases.append({
            "merchant": "Walgreens Pharmacy",
            "amount": 22.50,
            "date": (phase3_start + timedelta(days=5)).strftime("%Y-%m-%d"),
            "description": "Prescription"
        })
        
        for purchase in sorted(purchases, key=lambda x: x["date"]):
            if purchase["merchant"] in self.merchants:
                self.create_purchase(
                    account_id,
                    self.merchants[purchase["merchant"]],
                    purchase["amount"],
                    purchase["date"],
                    purchase["description"]
                )
        
        print(f"Created {len(deposits)} deposits and {len(purchases)} purchases for Customer 2")
    
    def generate_customer_3_severe_abuse(self, customer_id, account_id):
        """Customer 3: Jennifer Lee - Severe Financial Abuse"""
        print("\n=== Generating Customer 3: Severe Abuse (Jennifer Lee) ===")
        
        start_date = datetime.now() - timedelta(days=180)
        deposits = []
        
        deposit_dates = [
            start_date + timedelta(days=15),
            start_date + timedelta(days=45),
            start_date + timedelta(days=52),
            start_date + timedelta(days=89),
            start_date + timedelta(days=120),
            start_date + timedelta(days=165),
        ]
        
        for date in deposit_dates:
            deposits.append({
                "date": date.strftime("%Y-%m-%d"),
                "amount": random.uniform(200, 500),
                "description": "Cash deposit"
            })
        
        deposits.append({
            "date": (start_date + timedelta(days=7)).strftime("%Y-%m-%d"),
            "amount": 2750.00,
            "description": "Payroll Deposit - Tech Solutions Inc"
        })
        
        for deposit in deposits:
            self.create_deposit(account_id, deposit["amount"], deposit["date"], deposit["description"])
        
        purchases = []
        
        grocery_dates = [
            start_date + timedelta(days=10),
            start_date + timedelta(days=25),
            start_date + timedelta(days=48),
            start_date + timedelta(days=62),
            start_date + timedelta(days=91),
            start_date + timedelta(days=105),
            start_date + timedelta(days=125),
            start_date + timedelta(days=145),
            start_date + timedelta(days=170),
        ]
        
        for date in grocery_dates:
            purchases.append({
                "merchant": "Safeway",
                "amount": random.uniform(18, 45),
                "date": date.strftime("%Y-%m-%d"),
                "description": "Limited groceries"
            })
        
        purchases.append({
            "merchant": "Walgreens Pharmacy",
            "amount": 12.50,
            "date": (start_date + timedelta(days=55)).strftime("%Y-%m-%d"),
            "description": "Generic medication"
        })
        
        purchases.append({
            "merchant": "CVS Pharmacy",
            "amount": 8.75,
            "date": (start_date + timedelta(days=140)).strftime("%Y-%m-%d"),
            "description": "OTC medicine"
        })
        
        necessity_dates = [
            start_date + timedelta(days=30),
            start_date + timedelta(days=95),
            start_date + timedelta(days=155),
        ]
        
        for date in necessity_dates:
            purchases.append({
                "merchant": "Target",
                "amount": random.uniform(15, 35),
                "date": date.strftime("%Y-%m-%d"),
                "description": "Household necessities"
            })
        
        for purchase in sorted(purchases, key=lambda x: x["date"]):
            if purchase["merchant"] in self.merchants:
                self.create_purchase(
                    account_id,
                    self.merchants[purchase["merchant"]],
                    purchase["amount"],
                    purchase["date"],
                    purchase["description"]
                )
        
        print(f"Created {len(deposits)} deposits and {len(purchases)} purchases for Customer 3")
    
    def generate_customer_4_recovery_pattern(self, customer_id, account_id):
        """Customer 4: Michael Thompson - Recovery Pattern"""
        print("\n=== Generating Customer 4: Recovery Pattern (Michael Thompson) ===")
        
        start_date = datetime.now() - timedelta(days=180)
        deposits = []
        
        for i in range(3):
            date = start_date + timedelta(days=i*20)
            deposits.append({
                "date": date.strftime("%Y-%m-%d"),
                "amount": random.uniform(800, 1200),
                "description": "Irregular income"
            })
        
        for i in range(4):
            date = start_date + timedelta(days=60 + i*14)
            deposits.append({
                "date": date.strftime("%Y-%m-%d"),
                "amount": random.uniform(1800, 2200),
                "description": "Payroll - Part time"
            })
        
        for i in range(6):
            date = start_date + timedelta(days=120 + i*14)
            deposits.append({
                "date": date.strftime("%Y-%m-%d"),
                "amount": random.uniform(2600, 2900),
                "description": "Payroll Deposit - Full time"
            })
        
        for deposit in deposits:
            self.create_deposit(account_id, deposit["amount"], deposit["date"], deposit["description"])
        
        purchases = []
        
        for i in range(8):
            random_date = start_date + timedelta(days=random.randint(0, 60))
            purchases.append({
                "merchant": "Safeway",
                "amount": random.uniform(25, 50),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Basic groceries"
            })
        
        for i in range(15):
            random_date = start_date + timedelta(days=random.randint(60, 120))
            purchases.append({
                "merchant": random.choice(["Safeway", "Starbucks", "Target"]),
                "amount": random.uniform(15, 80),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Regular purchase"
            })
        
        for i in range(30):
            random_date = start_date + timedelta(days=random.randint(120, 180))
            merchant = random.choice([
                "Whole Foods Market", "Starbucks", "Chipotle", 
                "Sephora", "AMC Movie Theater", "Planet Fitness", "Gap"
            ])
            purchases.append({
                "merchant": merchant,
                "amount": random.uniform(15, 120),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Personal purchase"
            })
        
        for purchase in sorted(purchases, key=lambda x: x["date"]):
            if purchase["merchant"] in self.merchants:
                self.create_purchase(
                    account_id,
                    self.merchants[purchase["merchant"]],
                    purchase["amount"],
                    purchase["date"],
                    purchase["description"]
                )
        
        print(f"Created {len(deposits)} deposits and {len(purchases)} purchases for Customer 4")
    
    def generate_customer_5_sudden_abuse(self, customer_id, account_id):
        """Customer 5: David Park - Sudden Onset Abuse"""
        print("\n=== Generating Customer 5: Sudden Abuse (David Park) ===")
        
        start_date = datetime.now() - timedelta(days=180)
        deposits = []
        
        for i in range(8):
            date = start_date + timedelta(days=i*14)
            deposits.append({
                "date": date.strftime("%Y-%m-%d"),
                "amount": random.uniform(2700, 3100),
                "description": "Payroll Deposit"
            })
        
        for i in range(4):
            date = start_date + timedelta(days=112 + i*17)
            deposits.append({
                "date": date.strftime("%Y-%m-%d"),
                "amount": random.uniform(150, 400),
                "description": "Cash deposit"
            })
        
        for deposit in deposits:
            self.create_deposit(account_id, deposit["amount"], deposit["date"], deposit["description"])
        
        purchases = []
        
        grocery_dates = [start_date + timedelta(days=x*7) for x in range(16)]
        for date in grocery_dates:
            purchases.append({
                "merchant": random.choice(["Whole Foods Market", "Safeway"]),
                "amount": random.uniform(75, 140),
                "date": date.strftime("%Y-%m-%d"),
                "description": "Groceries"
            })
        
        for i in range(40):
            random_date = start_date + timedelta(days=random.randint(0, 112))
            merchant = random.choice([
                "Starbucks", "Chipotle", "Uber", "AMC Movie Theater", 
                "Planet Fitness", "Gap", "Sephora"
            ])
            purchases.append({
                "merchant": merchant,
                "amount": random.uniform(12, 95),
                "date": random_date.strftime("%Y-%m-%d"),
                "description": "Personal purchase"
            })
        
        for i in range(6):
            date = start_date + timedelta(days=112 + i*11)
            purchases.append({
                "merchant": "Safeway",
                "amount": random.uniform(20, 45),
                "date": date.strftime("%Y-%m-%d"),
                "description": "Basic groceries"
            })
        
        purchases.append({
            "merchant": "Walgreens Pharmacy",
            "amount": 18.50,
            "date": (start_date + timedelta(days=125)).strftime("%Y-%m-%d"),
            "description": "Medication"
        })
        
        for purchase in sorted(purchases, key=lambda x: x["date"]):
            if purchase["merchant"] in self.merchants:
                self.create_purchase(
                    account_id,
                    self.merchants[purchase["merchant"]],
                    purchase["amount"],
                    purchase["date"],
                    purchase["description"]
                )
        
        print(f"Created {len(deposits)} deposits and {len(purchases)} purchases for Customer 5")


def main():
    """Main execution function"""
    
    generator = FinancialAbuseDataGenerator(API_KEY)
    
    print("=" * 80)
    print("FINANCIAL ABUSE DETECTION - MOCK DATA GENERATOR")
    print("=" * 80)
    
    # Step 1: Create merchants
    print("\n=== STEP 1: Creating Merchants ===")
    merchants = generator.setup_merchants()
    print(f"Created {len(merchants)} merchants")
    
    # Track all customer IDs
    customer_data = {"customers": []}
    
    # Step 2: Create Customer 1 - No Abuse
    print("\n=== STEP 2: Creating Customer 1 - No Financial Abuse ===")
    customer1 = generator.create_customer(
        "Sarah",
        "Johnson",
        {
            "street_number": "123",
            "street_name": "Independence Ave",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94102"
        }
    )
    
    if "objectCreated" in customer1:
        customer1_id = customer1["objectCreated"]["_id"]
        account1 = generator.create_account(
            customer1_id,
            "Checking",
            "Sarah's Checking Account",
            5000,
            rewards=150
        )
        
        if "objectCreated" in account1:
            account1_id = account1["objectCreated"]["_id"]
            generator.generate_customer_1_no_abuse(customer1_id, account1_id)
            customer_data["customers"].append({
                "customer_id": customer1_id,
                "name": "Sarah Johnson",
                "profile": "No Abuse - Control Group",
                "expected_risk": "LOW"
            })
        else:
            print(f"❌ Account creation failed for Customer 1")
    else:
        print(f"❌ Customer creation failed for Customer 1")
    
    # Step 3: Create Customer 2 - Moderate Abuse
    print("\n=== STEP 3: Creating Customer 2 - Moderate Financial Abuse ===")
    customer2 = generator.create_customer(
        "Maria",
        "Rodriguez",
        {
            "street_number": "456",
            "street_name": "Restricted Rd",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94103"
        }
    )
    
    if "objectCreated" in customer2:
        customer2_id = customer2["objectCreated"]["_id"]
        account2 = generator.create_account(
            customer2_id,
            "Checking",
            "Maria's Checking Account",
            1200,
            rewards=25
        )
        
        if "objectCreated" in account2:
            account2_id = account2["objectCreated"]["_id"]
            generator.generate_customer_2_moderate_abuse(customer2_id, account2_id)
            customer_data["customers"].append({
                "customer_id": customer2_id,
                "name": "Maria Rodriguez",
                "profile": "Moderate Abuse - Escalating Pattern",
                "expected_risk": "MEDIUM-HIGH"
            })
        else:
            print(f"❌ Account creation failed for Customer 2")
    else:
        print(f"❌ Customer creation failed for Customer 2")
    
    # Step 4: Create Customer 3 - Severe Abuse
    print("\n=== STEP 4: Creating Customer 3 - Severe Financial Abuse ===")
    customer3 = generator.create_customer(
        "Jennifer",
        "Lee",
        {
            "street_number": "789",
            "street_name": "Control Court",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94104"
        }
    )
    
    if "objectCreated" in customer3:
        customer3_id = customer3["objectCreated"]["_id"]
        account3 = generator.create_account(
            customer3_id,
            "Checking",
            "Jennifer's Checking Account",
            150,
            rewards=0
        )
        
        if "objectCreated" in account3:
            account3_id = account3["objectCreated"]["_id"]
            generator.generate_customer_3_severe_abuse(customer3_id, account3_id)
            customer_data["customers"].append({
                "customer_id": customer3_id,
                "name": "Jennifer Lee",
                "profile": "Severe Abuse - Complete Control",
                "expected_risk": "HIGH"
            })
        else:
            print(f"❌ Account creation failed for Customer 3")
    else:
        print(f"❌ Customer creation failed for Customer 3")
    
    # Step 5: Create Customer 4 - Recovery Pattern
    print("\n=== STEP 5: Creating Customer 4 - Recovery Pattern ===")
    customer4 = generator.create_customer(
        "Michael",
        "Thompson",
        {
            "street_number": "321",
            "street_name": "Recovery Road",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94105"
        }
    )
    
    if "objectCreated" in customer4:
        customer4_id = customer4["objectCreated"]["_id"]
        account4 = generator.create_account(
            customer4_id,
            "Checking",
            "Michael's Checking Account",
            2800,
            rewards=75
        )
        
        if "objectCreated" in account4:
            account4_id = account4["objectCreated"]["_id"]
            generator.generate_customer_4_recovery_pattern(customer4_id, account4_id)
            customer_data["customers"].append({
                "customer_id": customer4_id,
                "name": "Michael Thompson",
                "profile": "Recovery Pattern",
                "expected_risk": "MEDIUM (improving)"
            })
        else:
            print(f"❌ Account creation failed for Customer 4")
    else:
        print(f"❌ Customer creation failed for Customer 4")
    
    # Step 6: Create Customer 5 - Sudden Abuse
    print("\n=== STEP 6: Creating Customer 5 - Sudden Onset Abuse ===")
    customer5 = generator.create_customer(
        "David",
        "Park",
        {
            "street_number": "555",
            "street_name": "Sudden Street",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94106"
        }
    )
    
    if "objectCreated" in customer5:
        customer5_id = customer5["objectCreated"]["_id"]
        account5 = generator.create_account(
            customer5_id,
            "Checking",
            "David's Checking Account",
            800,
            rewards=10
        )
        
        if "objectCreated" in account5:
            account5_id = account5["objectCreated"]["_id"]
            generator.generate_customer_5_sudden_abuse(customer5_id, account5_id)
            customer_data["customers"].append({
                "customer_id": customer5_id,
                "name": "David Park",
                "profile": "Sudden Abuse",
                "expected_risk": "HIGH"
            })
        else:
            print(f"❌ Account creation failed for Customer 5")
    else:
        print(f"❌ Customer creation failed for Customer 5")
    
    print("\n" + "=" * 80)
    print("DATA GENERATION COMPLETE!")
    print("=" * 80)
    
    # Save customer IDs
    with open("customer_ids.json", "w") as f:
        json.dump(customer_data, f, indent=2)
    
    print("\n💾 CUSTOMER IDs SAVED TO: customer_ids.json")
    print("\nCUSTOMER ID REFERENCE:")
    for customer in customer_data["customers"]:
        if customer["customer_id"]:
            print(f"\n  {customer['name']}:")
            print(f"    ID: {customer['customer_id']}")
            print(f"    Profile: {customer['profile']}")
            print(f"    Expected Risk: {customer['expected_risk']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
# class FinancialAbuseDataGenerator:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.base_url = BASE_URL
#         self.customers = {}
#         self.accounts = {}
#         self.merchants = {}
        
#     def _make_request(self, method, endpoint, data=None):
#         """Helper method to make API requests"""
#         url = f"{self.base_url}{endpoint}?key={self.api_key}"
#         headers = {'Content-Type': 'application/json'}
        
#         if method == "POST":
#             response = requests.post(url, json=data, headers=headers)
#         elif method == "GET":
#             response = requests.get(url, headers=headers)
        
#         return response.json()
    
#     def create_customer(self, first_name, last_name, address):
#         """Create a customer"""
#         customer_data = {
#             "first_name": first_name,
#             "last_name": last_name,
#             "address": address
#         }
#         result = self._make_request("POST", "/customers", customer_data)
#         print(f"Created customer: {first_name} {last_name}")
#         return result
    
#     def create_account(self, customer_id, account_type, nickname, balance, rewards=0):
#         """Create an account for a customer"""
#         account_data = {
#             "type": account_type,
#             "nickname": nickname,
#             "rewards": rewards,
#             "balance": balance
#         }
#         result = self._make_request("POST", f"/customers/{customer_id}/accounts", account_data)
#         print(f"Created account: {nickname}")
#         return result
    
#     def create_merchant(self, name, category, address, geocode):
#         """Create a merchant"""
#         merchant_data = {
#             "name": name,
#             "category": category,
#             "address": address,
#             "geocode": geocode
#         }
#         result = self._make_request("POST", "/merchants", merchant_data)
#         print(f"Created merchant: {name}")
#         return result
    
#     def create_purchase(self, account_id, merchant_id, amount, purchase_date, description, status="executed", medium="balance"):
#         """Create a purchase transaction"""
#         purchase_data = {
#             "merchant_id": merchant_id,
#             "medium": medium,
#             "purchase_date": purchase_date,
#             "amount": amount,
#             "status": status,
#             "description": description
#         }
#         result = self._make_request("POST", f"/accounts/{account_id}/purchases", purchase_data)
#         return result
    
#     def create_deposit(self, account_id, amount, transaction_date, description, status="executed", medium="balance"):
#         """Create a deposit transaction"""
#         deposit_data = {
#             "medium": medium,
#             "transaction_date": transaction_date,
#             "amount": amount,
#             "status": status,
#             "description": description
#         }
#         result = self._make_request("POST", f"/accounts/{account_id}/deposits", deposit_data)
#         return result
    
#     def setup_merchants(self):
#         """Create common merchants used across all scenarios"""
#         merchants_list = [
#             {
#                 "name": "Whole Foods Market",
#                 "category": "Groceries",
#                 "address": {
#                     "street_number": "1000",
#                     "street_name": "Market St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94102"
#                 },
#                 "geocode": {"lat": 37.7749, "lng": -122.4194}
#             },
#             {
#                 "name": "Target",
#                 "category": "Retail",
#                 "address": {
#                     "street_number": "2000",
#                     "street_name": "Mission St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94110"
#                 },
#                 "geocode": {"lat": 37.7599, "lng": -122.4148}
#             },
#             {
#                 "name": "Walgreens Pharmacy",
#                 "category": "Pharmacy",
#                 "address": {
#                     "street_number": "500",
#                     "street_name": "Powell St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94102"
#                 },
#                 "geocode": {"lat": 37.7867, "lng": -122.4088}
#             },
#             {
#                 "name": "Starbucks",
#                 "category": "Coffee",
#                 "address": {
#                     "street_number": "300",
#                     "street_name": "Main St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94105"
#                 },
#                 "geocode": {"lat": 37.7908, "lng": -122.3954}
#             },
#             {
#                 "name": "CVS Pharmacy",
#                 "category": "Pharmacy",
#                 "address": {
#                     "street_number": "700",
#                     "street_name": "Geary St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94109"
#                 },
#                 "geocode": {"lat": 37.7858, "lng": -122.4134}
#             },
#             {
#                 "name": "Safeway",
#                 "category": "Groceries",
#                 "address": {
#                     "street_number": "1200",
#                     "street_name": "Webster St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94115"
#                 },
#                 "geocode": {"lat": 37.7833, "lng": -122.4324}
#             },
#             {
#                 "name": "AMC Movie Theater",
#                 "category": "Entertainment",
#                 "address": {
#                     "street_number": "1000",
#                     "street_name": "Van Ness Ave",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94109"
#                 },
#                 "geocode": {"lat": 37.7858, "lng": -122.4229}
#             },
#             {
#                 "name": "Planet Fitness",
#                 "category": "Fitness",
#                 "address": {
#                     "street_number": "850",
#                     "street_name": "Bryant St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94103"
#                 },
#                 "geocode": {"lat": 37.7716, "lng": -122.4030}
#             },
#             {
#                 "name": "Chipotle",
#                 "category": "Restaurant",
#                 "address": {
#                     "street_number": "450",
#                     "street_name": "Castro St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94114"
#                 },
#                 "geocode": {"lat": 37.7609, "lng": -122.4350}
#             },
#             {
#                 "name": "Uber",
#                 "category": "Transportation",
#                 "address": {
#                     "street_number": "1455",
#                     "street_name": "Market St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94103"
#                 },
#                 "geocode": {"lat": 37.7752, "lng": -122.4175}
#             },
#             {
#                 "name": "Sephora",
#                 "category": "Beauty",
#                 "address": {
#                     "street_number": "33",
#                     "street_name": "Powell St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94102"
#                 },
#                 "geocode": {"lat": 37.7866, "lng": -122.4084}
#             },
#             {
#                 "name": "Gap",
#                 "category": "Clothing",
#                 "address": {
#                     "street_number": "890",
#                     "street_name": "Market St",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "zip": "94102"
#                 },
#                 "geocode": {"lat": 37.7833, "lng": -122.4066}
#             }
#         ]
        
#         for merchant in merchants_list:
#             result = self.create_merchant(
#                 merchant["name"],
#                 merchant["category"],
#                 merchant["address"],
#                 merchant["geocode"]
#             )
#             if "objectCreated" in result:
#                 self.merchants[merchant["name"]] = result["objectCreated"]["_id"]
        
#         return self.merchants
    
#     def generate_customer_1_no_abuse(self, customer_id, account_id):
#         """
#         Customer 1: Sarah Johnson - No Financial Abuse
#         Healthy, independent financial behavior with consistent patterns
#         """
#         print("\n=== Generating Customer 1: No Abuse (Sarah Johnson) ===")
        
#         # Regular biweekly paycheck deposits - stable income
#         start_date = datetime.now() - timedelta(days=180)
#         current_date = start_date
        
#         deposits = []
#         while current_date <= datetime.now():
#             deposit_amount = random.uniform(2800, 3200)  # Consistent paycheck
#             deposits.append({
#                 "date": current_date.strftime("%Y-%m-%d"),
#                 "amount": deposit_amount,
#                 "description": "Payroll Deposit - ABC Company"
#             })
#             current_date += timedelta(days=14)
        
#         # Create deposits
#         for deposit in deposits:
#             self.create_deposit(
#                 account_id,
#                 deposit["amount"],
#                 deposit["date"],
#                 deposit["description"]
#             )
        
#         # Generate consistent purchases - healthy spending pattern
#         purchases = []
        
#         # Weekly groceries - consistent
#         grocery_dates = [start_date + timedelta(days=x*7) for x in range(26)]
#         for date in grocery_dates:
#             purchases.append({
#                 "merchant": random.choice(["Whole Foods Market", "Safeway"]),
#                 "amount": random.uniform(80, 150),
#                 "date": date.strftime("%Y-%m-%d"),
#                 "description": "Weekly groceries"
#             })
        
#         # Regular coffee/lunch - 3-4 times per week
#         for i in range(100):
#             random_date = start_date + timedelta(days=random.randint(0, 180))
#             purchases.append({
#                 "merchant": random.choice(["Starbucks", "Chipotle"]),
#                 "amount": random.uniform(8, 25),
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Coffee/Lunch"
#             })
        
#         # Pharmacy/health - monthly
#         pharmacy_dates = [start_date + timedelta(days=x*30) for x in range(6)]
#         for date in pharmacy_dates:
#             purchases.append({
#                 "merchant": random.choice(["Walgreens Pharmacy", "CVS Pharmacy"]),
#                 "amount": random.uniform(15, 60),
#                 "date": date.strftime("%Y-%m-%d"),
#                 "description": "Pharmacy/Health"
#             })
        
#         # Personal care/beauty - regular
#         for i in range(8):
#             random_date = start_date + timedelta(days=random.randint(0, 180))
#             purchases.append({
#                 "merchant": "Sephora",
#                 "amount": random.uniform(30, 100),
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Personal care"
#             })
        
#         # Entertainment - regular leisure activities
#         for i in range(12):
#             random_date = start_date + timedelta(days=random.randint(0, 180))
#             purchases.append({
#                 "merchant": "AMC Movie Theater",
#                 "amount": random.uniform(15, 45),
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Entertainment"
#             })
        
#         # Fitness - consistent gym membership
#         for i in range(6):
#             date = start_date + timedelta(days=i*30)
#             purchases.append({
#                 "merchant": "Planet Fitness",
#                 "amount": 25.00,
#                 "date": date.strftime("%Y-%m-%d"),
#                 "description": "Monthly gym membership"
#             })
        
#         # Clothing - occasional
#         for i in range(10):
#             random_date = start_date + timedelta(days=random.randint(0, 180))
#             purchases.append({
#                 "merchant": "Gap",
#                 "amount": random.uniform(40, 150),
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Clothing"
#             })
        
#         # Transportation
#         for i in range(40):
#             random_date = start_date + timedelta(days=random.randint(0, 180))
#             purchases.append({
#                 "merchant": "Uber",
#                 "amount": random.uniform(12, 35),
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Transportation"
#             })
        
#         # Create all purchases
#         for purchase in sorted(purchases, key=lambda x: x["date"]):
#             if purchase["merchant"] in self.merchants:
#                 self.create_purchase(
#                     account_id,
#                     self.merchants[purchase["merchant"]],
#                     purchase["amount"],
#                     purchase["date"],
#                     purchase["description"]
#                 )
        
#         print(f"Created {len(deposits)} deposits and {len(purchases)} purchases for Customer 1")
    
#     def generate_customer_2_moderate_abuse(self, customer_id, account_id):
#         """
#         Customer 2: Maria Rodriguez - Moderate Financial Abuse
#         Shows escalating control with irregular patterns and sudden restrictions
#         """
#         print("\n=== Generating Customer 2: Moderate Abuse (Maria Rodriguez) ===")
        
#         # Phase 1 (Months 1-3): Normal behavior - before abuse escalates
#         # Phase 2 (Months 4-5): Control begins - irregular deposits, reduced personal spending
#         # Phase 3 (Month 6): Punishment period - critical decline in spending
        
#         start_date = datetime.now() - timedelta(days=180)
        
#         # DEPOSITS - showing irregular pattern as partner gains control
#         deposits = []
        
#         # Phase 1: Regular deposits
#         for i in range(6):
#             date = start_date + timedelta(days=i*14)
#             deposits.append({
#                 "date": date.strftime("%Y-%m-%d"),
#                 "amount": random.uniform(2600, 2900),
#                 "description": "Payroll Deposit - XYZ Corp"
#             })
        
#         # Phase 2: Some deposits "missing" - partner intercepting
#         for i in range(3):
#             date = start_date + timedelta(days=84 + i*14)
#             if i != 1:  # Skip one deposit - partner intercepted
#                 deposits.append({
#                     "date": date.strftime("%Y-%m-%d"),
#                     "amount": random.uniform(2400, 2700),  # Slightly reduced
#                     "description": "Payroll Deposit - XYZ Corp"
#                 })
        
#         # Phase 3: Highly irregular, reduced deposits
#         for i in range(4):
#             date = start_date + timedelta(days=126 + i*14)
#             if i % 2 == 0:  # Only getting every other paycheck
#                 deposits.append({
#                     "date": date.strftime("%Y-%m-%d"),
#                     "amount": random.uniform(1800, 2200),  # Significantly reduced
#                     "description": "Payroll Deposit - XYZ Corp"
#                 })
        
#         for deposit in deposits:
#             self.create_deposit(
#                 account_id,
#                 deposit["amount"],
#                 deposit["date"],
#                 deposit["description"]
#             )
        
#         # PURCHASES - showing decline in autonomy
#         purchases = []
        
#         # Phase 1 (Days 0-90): Normal spending
#         phase1_end = start_date + timedelta(days=90)
#         current = start_date
        
#         # Regular groceries in Phase 1
#         while current < phase1_end:
#             purchases.append({
#                 "merchant": random.choice(["Whole Foods Market", "Safeway"]),
#                 "amount": random.uniform(70, 130),
#                 "date": current.strftime("%Y-%m-%d"),
#                 "description": "Groceries"
#             })
#             current += timedelta(days=7)
        
#         # Personal spending in Phase 1
#         for i in range(15):
#             random_date = start_date + timedelta(days=random.randint(0, 90))
#             purchases.append({
#                 "merchant": random.choice(["Starbucks", "Chipotle"]),
#                 "amount": random.uniform(10, 28),
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Personal food"
#             })
        
#         # Beauty/self-care in Phase 1
#         for i in range(4):
#             random_date = start_date + timedelta(days=random.randint(0, 90))
#             purchases.append({
#                 "merchant": "Sephora",
#                 "amount": random.uniform(40, 90),
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Personal care"
#             })
        
#         # Entertainment in Phase 1
#         for i in range(5):
#             random_date = start_date + timedelta(days=random.randint(0, 90))
#             purchases.append({
#                 "merchant": "AMC Movie Theater",
#                 "amount": random.uniform(15, 35),
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Movie"
#             })
        
#         # Phase 2 (Days 91-150): Restrictions begin - reduced personal spending
#         phase2_start = start_date + timedelta(days=91)
#         phase2_end = start_date + timedelta(days=150)
        
#         # Groceries continue but reduced frequency
#         current = phase2_start
#         while current < phase2_end:
#             if random.random() > 0.3:  # 30% of grocery trips "blocked"
#                 purchases.append({
#                     "merchant": "Safeway",
#                     "amount": random.uniform(50, 90),  # Reduced amounts
#                     "date": current.strftime("%Y-%m-%d"),
#                     "description": "Groceries"
#                 })
#             current += timedelta(days=7)
        
#         # Dramatically reduced personal spending
#         for i in range(5):  # Down from 15
#             random_date = start_date + timedelta(days=random.randint(91, 150))
#             purchases.append({
#                 "merchant": "Starbucks",
#                 "amount": random.uniform(5, 12),  # Smaller amounts
#                 "date": random_date.strftime("%Y-%m-%d"),
#                 "description": "Coffee"
#             })
        
#         # No beauty purchases in Phase 2 - access denied
        
#         # Only 1 entertainment purchase
#         purchases.append({
#             "merchant": "AMC Movie Theater",
#             "amount": 14.50,
#             "date": (start_date + timedelta(days=100)).strftime("%Y-%m-%d"),
#             "description": "Movie"
#         })
        
#         # Phase 3 (Days 151-180): Severe restriction/punishment period
#         phase3_start = start_date + timedelta(days=151)
#         phase3_end = datetime.now()
        
#         # Critical decline - only absolute essentials, very sparse
#         # Groceries minimal
#         for i in range(3):  # Only 3 grocery trips in a month
#             date = phase3_start + timedelta(days=i*10)
#             purchases.append({
#                 "merchant": "Safeway",
#                 "amount": random.uniform(30, 55),  # Bare minimum
#                 "date": date.strftime("%Y-%m-%d"),
#                 "description": "Basic groceries"
#             })
        
#         # Pharmacy - necessary only
#         purchases.append({
#             "merchant": "Walgreens Pharmacy",
#             "amount": 22.50,
#             "date": (phase3_start + timedelta(days=5)).strftime("%Y-%m-%d"),
#             "description": "Prescription"
#         })
        
#         # NO personal spending, entertainment, or discretionary purchases
        
#         # Create all purchases
#         for purchase in sorted(purchases, key=lambda x: x["date"]):
#             if purchase["merchant"] in self.merchants:
#                 self.create_purchase(
#                     account_id,
#                     self.merchants[purchase["merchant"]],
#                     purchase["amount"],
#                     purchase["date"],
#                     purchase["description"]
#                 )
        
#         print(f"Created {len(deposits)} deposits and {len(purchases)} purchases for Customer 2")
    
#     def generate_customer_3_severe_abuse(self, customer_id, account_id):
#         """
#         Customer 3: Jennifer Lee - Severe Financial Abuse
#         Complete financial control, no autonomy, forced withdrawals, extreme restrictions
#         """
#         print("\n=== Generating Customer 3: Severe Abuse (Jennifer Lee) ===")
        
#         start_date = datetime.now() - timedelta(days=180)
        
#         # DEPOSITS - Partner has complete control
#         deposits = []
        
#         # Very irregular deposits - partner controls all money
#         deposit_dates = [
#             start_date + timedelta(days=15),
#             start_date + timedelta(days=45),
#             start_date + timedelta(days=52),
#             start_date + timedelta(days=89),
#             start_date + timedelta(days=120),
#             start_date + timedelta(days=165),
#         ]
        
#         for date in deposit_dates:
#             # Small "allowance" amounts
#             deposits.append({
#                 "date": date.strftime("%Y-%m-%d"),
#                 "amount": random.uniform(200, 500),  # Tiny amounts given as "allowance"
#                 "description": "Cash deposit"
#             })
        
#         # One regular paycheck that shows she HAS income, but it's being taken
#         deposits.append({
#             "date": (start_date + timedelta(days=7)).strftime("%Y-%m-%d"),
#             "amount": 2750.00,
#             "description": "Payroll Deposit - Tech Solutions Inc"
#         })
        
#         # Immediately followed by large withdrawal (partner taking money)
#         # Note: We'll simulate this as a negative purchase to a generic merchant
        
#         for deposit in deposits:
#             self.create_deposit(
#                 account_id,
#                 deposit["amount"],
#                 deposit["date"],
#                 deposit["description"]
#             )
        
#         # PURCHASES - Extremely restricted, survival only
#         purchases = []
        
#         # Very sparse grocery purchases - partner controls food budget
#         grocery_dates = [
#             start_date + timedelta(days=10),
#             start_date + timedelta(days=25),
#             start_date + timedelta(days=48),
#             start_date + timedelta(days=62),
#             start_date + timedelta(days=91),
#             start_date + timedelta(days=105),
#             start_date + timedelta(days=125),
#             start_date + timedelta(days=145),
#             start_date + timedelta(days=170),
#         ]
        
#         for date in grocery_dates:
#             purchases.append({
#                 "merchant": "Safeway",
#                 "amount": random.uniform(18, 45),  # Very small, restricted amounts
#                 "date": date.strftime("%Y-%m-%d"),
#                 "description": "Limited groceries"
#             })
        
#         # Only 2 pharmacy purchases - even healthcare restricted
#         purchases.append({
#             "merchant": "Walgreens Pharmacy",
#             "amount": 12.50,
#             "date": (start_date + timedelta(days=55)).strftime("%Y-%m-%d"),
#             "description": "Generic medication"
#         })
        
#         purchases.append({
#             "merchant": "CVS Pharmacy",
#             "amount": 8.75,
#             "date": (start_date + timedelta(days=140)).strftime("%Y-%m-%d"),
#             "description": "OTC medicine"
#         })
        
#         # Absolutely NO:
#         # - Personal care (beauty products)
#         # - Entertainment
#         # - Coffee/dining out
#         # - Fitness
#         # - Clothing
#         # - Transportation (partner controls movement)
        
#         # A few Target purchases for absolute necessities only
#         necessity_dates = [
#             start_date + timedelta(days=30),
#             start_date + timedelta(days=95),
#             start_date + timedelta(days=155),
#         ]
        
#         for date in necessity_dates:
#             purchases.append({
#                 "merchant": "Target",
#                 "amount": random.uniform(15, 35),
#                 "date": date.strftime("%Y-%m-%d"),
#                 "description": "Household necessities"
#             })
        
#         # Create all purchases
#         for purchase in sorted(purchases, key=lambda x: x["date"]):
#             if purchase["merchant"] in self.merchants:
#                 self.create_purchase(
#                     account_id,
#                     self.merchants[purchase["merchant"]],
#                     purchase["amount"],
#                     purchase["date"],
#                     purchase["description"]
#                 )
        
#         print(f"Created {len(deposits)} deposits and {len(purchases)} purchases for Customer 3")
#         print("Note: This profile shows extreme financial restriction - survival spending only")


# def main():
#     """Main execution function"""
    
#     # Initialize generator
#     generator = FinancialAbuseDataGenerator(API_KEY)
    
#     print("=" * 80)
#     print("FINANCIAL ABUSE DETECTION - MOCK DATA GENERATOR")
#     print("=" * 80)
    
#     # Step 1: Create merchants
#     print("\n=== STEP 1: Creating Merchants ===")
#     merchants = generator.setup_merchants()
#     print(f"Created {len(merchants)} merchants")
    
#     # Step 2: Create Customer 1 - No Abuse
#     print("\n=== STEP 2: Creating Customer 1 - No Financial Abuse ===")
#     customer1 = generator.create_customer(
#         "Sarah",
#         "Johnson",
#         {
#             "street_number": "123",
#             "street_name": "Independence Ave",
#             "city": "San Francisco",
#             "state": "CA",
#             "zip": "94102"
#         }
#     )
    
#     # Get customer ID and create account
#     print(f"DEBUG - Customer 1 response: {customer1}")
#     if "objectCreated" in customer1:
#         customer1_id = customer1["objectCreated"]["_id"]
#         account1 = generator.create_account(
#             customer1_id,
#             "Checking",
#             "Sarah's Checking Account",
#             5000,
#             rewards=150
#         )
        
#         if "objectCreated" in account1:
#             account1_id = account1["objectCreated"]["_id"]
#             generator.generate_customer_1_no_abuse(customer1_id, account1_id)
    
#     # Step 3: Create Customer 2 - Moderate Abuse
#     print("\n=== STEP 3: Creating Customer 2 - Moderate Financial Abuse ===")
#     customer2 = generator.create_customer(
#         "Maria",
#         "Rodriguez",
#         {
#             "street_number": "456",
#             "street_name": "Restricted Rd",
#             "city": "San Francisco",
#             "state": "CA",
#             "zip": "94103"
#         }
#     )
    
#     if "objectCreated" in customer2:
#         customer2_id = customer2["objectCreated"]["_id"]
#         account2 = generator.create_account(
#             customer2_id,
#             "Checking",
#             "Maria's Checking Account",
#             1200,
#             rewards=25
#         )
        
#         if "objectCreated" in account2:
#             account2_id = account2["objectCreated"]["_id"]
#             generator.generate_customer_2_moderate_abuse(customer2_id, account2_id)
    
#     # Step 4: Create Customer 3 - Severe Abuse
#     print("\n=== STEP 4: Creating Customer 3 - Severe Financial Abuse ===")
#     customer3 = generator.create_customer(
#         "Jennifer",
#         "Lee",
#         {
#             "street_number": "789",
#             "street_name": "Control Court",
#             "city": "San Francisco",
#             "state": "CA",
#             "zip": "94104"
#         }
#     )
    
#     if "objectCreated" in customer3:
#         customer3_id = customer3["objectCreated"]["_id"]
#         account3 = generator.create_account(
#             customer3_id,
#             "Checking",
#             "Jennifer's Checking Account",
#             150,
#             rewards=0
#         )
        
#         if "objectCreated" in account3:
#             account3_id = account3["objectCreated"]["_id"]
#             generator.generate_customer_3_severe_abuse(customer3_id, account3_id)
    
#     print("\n" + "=" * 80)
#     print("DATA GENERATION COMPLETE!")
#     print("=" * 80)
    
#     # Save customer IDs to a file for easy reference
#     customer_ids = {
#         "customers": [
#             {
#                 "customer_id": customer1_id if "objectCreated" in customer1 else None,
#                 "name": "Sarah Johnson",
#                 "profile": "No Abuse - Control Group",
#                 "expected_risk": "LOW"
#             },
#             {
#                 "customer_id": customer2_id if "objectCreated" in customer2 else None,
#                 "name": "Maria Rodriguez",
#                 "profile": "Moderate Abuse - Escalating Pattern",
#                 "expected_risk": "MEDIUM-HIGH"
#             },
#             {
#                 "customer_id": customer3_id if "objectCreated" in customer3 else None,
#                 "name": "Jennifer Lee",
#                 "profile": "Severe Abuse - Complete Control",
#                 "expected_risk": "HIGH"
#             }
#         ]
#     }
    
#     import json
#     with open("customer_ids.json", "w") as f:
#         json.dump(customer_ids, f, indent=2)
    
#     print("\n💾 CUSTOMER IDs SAVED TO: customer_ids.json")
#     print("\nCUSTOMER ID REFERENCE:")
#     for customer in customer_ids["customers"]:
#         if customer["customer_id"]:
#             print(f"\n  {customer['name']}:")
#             print(f"    ID: {customer['customer_id']}")
#             print(f"    Profile: {customer['profile']}")
#             print(f"    Expected Risk: {customer['expected_risk']}")
    
#     print("\n" + "=" * 80)
#     print("\nSUMMARY OF FINANCIAL ABUSE PATTERNS:")
#     print("\n1. SARAH JOHNSON (No Abuse):")
#     print("   - Regular biweekly paychecks")
#     print("   - Consistent spending across all categories")
#     print("   - Healthy discretionary spending (entertainment, fitness, beauty)")
#     print("   - Independent financial decisions")
    
#     print("\n2. MARIA RODRIGUEZ (Moderate Abuse):")
#     print("   - Phase 1: Normal behavior (months 1-3)")
#     print("   - Phase 2: Control begins - irregular deposits, reduced personal spending")
#     print("   - Phase 3: Punishment period - critical decline, only essentials")
#     print("   - Key signals: Missing deposits, declined discretionary spending, escalation")
    
#     print("\n3. JENNIFER LEE (Severe Abuse):")
#     print("   - Extreme financial restriction")
#     print("   - Irregular 'allowance' deposits only")
#     print("   - Survival spending only (bare minimum groceries, rare pharmacy)")
#     print("   - Zero discretionary spending - no autonomy")
#     print("   - Partner has complete financial control")
    
#     print("\n" + "=" * 80)


# if __name__ == "__main__":
#     main()