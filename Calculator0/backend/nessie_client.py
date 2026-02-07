import requests
import os
from dotenv import load_dotenv

load_dotenv()

NESSIE_API_KEY = os.getenv('NESSIE_API_KEY')
BASE_URL = 'http://api.nessieisreal.com'

class NessieClient:
    
    @staticmethod
    def create_customer(first_name, last_name, street_number, street_name, city, state, zip_code):
        """Create a new customer"""
        url = f'{BASE_URL}/customers?key={NESSIE_API_KEY}'
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "address": {
                "street_number": street_number,
                "street_name": street_name,
                "city": city,
                "state": state,
                "zip": zip_code
            }
        }
        response = requests.post(url, json=data)
        return response.json()
    
    @staticmethod
    def get_customer(customer_id):
        """Get customer details"""
        url = f'{BASE_URL}/customers/{customer_id}?key={NESSIE_API_KEY}'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_accounts(customer_id):
        """Get all accounts for a customer"""
        url = f'{BASE_URL}/customers/{customer_id}/accounts?key={NESSIE_API_KEY}'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_purchases(account_id):
        """Get purchases (transactions) for an account"""
        url = f'{BASE_URL}/accounts/{account_id}/purchases?key={NESSIE_API_KEY}'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_transfers(account_id):
        """Get transfers for an account"""
        url = f'{BASE_URL}/accounts/{account_id}/transfers?key={NESSIE_API_KEY}'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_deposits(account_id):
        """Get deposits for an account"""
        url = f'{BASE_URL}/accounts/{account_id}/deposits?key={NESSIE_API_KEY}'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_withdrawals(account_id):
        """Get withdrawals for an account"""
        url = f'{BASE_URL}/accounts/{account_id}/withdrawals?key={NESSIE_API_KEY}'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_bills(account_id):
        """Get bills for an account"""
        url = f'{BASE_URL}/accounts/{account_id}/bills?key={NESSIE_API_KEY}'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_all_financial_data(customer_id):
        """
        Get EVERYTHING - purchases, transfers, deposits, withdrawals, bills
        """
        accounts = NessieClient.get_accounts(customer_id)
        
        all_data = {
            'customer_id': customer_id,
            'accounts': accounts,
            'purchases': [],
            'transfers': [],
            'deposits': [],
            'withdrawals': [],
            'bills': []
        }
        
        for account in accounts:
            account_id = account['_id']
            
            # Get all transaction types
            all_data['purchases'].extend(NessieClient.get_purchases(account_id))
            all_data['transfers'].extend(NessieClient.get_transfers(account_id))
            all_data['deposits'].extend(NessieClient.get_deposits(account_id))
            all_data['withdrawals'].extend(NessieClient.get_withdrawals(account_id))
            all_data['bills'].extend(NessieClient.get_bills(account_id))
        
        return all_data


# Convenience function
def fetch_transactions(customer_id):
    """Main function to fetch all financial data"""
    return NessieClient.get_all_financial_data(customer_id)


# Demo data setup
def create_demo_customers():
    """Create demo customers with different abuse scenarios"""
    
    # Scenario 1: High abuse
    customer1 = NessieClient.create_customer(
        first_name="Sarah",
        last_name="Johnson",
        street_number="123",
        street_name="Main St",
        city="New York",
        state="NY",
        zip_code="10001"
    )
    
    # Scenario 2: Medium abuse
    customer2 = NessieClient.create_customer(
        first_name="Maria",
        last_name="Garcia",
        street_number="456",
        street_name="Oak Ave",
        city="Los Angeles",
        state="CA",
        zip_code="90001"
    )
    
    # Scenario 3: Normal
    customer3 = NessieClient.create_customer(
        first_name="Jane",
        last_name="Purdue",
        street_number="789",
        street_name="Pine Rd",
        city="Chicago",
        state="IL",
        zip_code="60601"
    )
    
    return {
        'high_abuse': customer3,
        'medium_abuse': customer2,
        'normal': customer1
    }