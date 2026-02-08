"""
Secure Financial Abuse Detection - AES Encryption Pipeline (ID-based)
Fetches customer data by ID, encrypts it with AES, and prepares for Gemini analysis
"""

import requests
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# API Configuration
BASE_URL = "http://api.nessieisreal.com"
API_KEY = "9d787b27cf859b503a82cd83e58be1ec"


class SecureDataPipeline:
    def __init__(self, api_key, encryption_key=None):
        self.api_key = api_key
        self.base_url = BASE_URL
        
        # Generate or use provided AES key (256-bit)
        if encryption_key:
            self.key = encryption_key
        else:
            self.key = os.urandom(32)  # 256-bit key
        
        print(f" AES encryption key:")
        print(f"   {base64.b64encode(self.key).decode()}")
    
    
    def _make_request(self, endpoint):
        """Helper to make API GET requests"""
        url = f"{self.base_url}{endpoint}?key={self.api_key}"
        response = requests.get(url)
        return response.json()

    def _unwrap_list(self, resp, default=None):
        """Nessie API often returns a dict like {'customers': [...]}. Return the list."""
        if default is None:
            default = []
        if isinstance(resp, list):
            return resp
        if not isinstance(resp, dict):
            return default
        if "customers" in resp:
            return resp["customers"]
        if "results" in resp:
            return resp["results"]
        for v in resp.values():
            if isinstance(v, list) and (not v or isinstance(v[0], dict)):
                return v
        return default
    
    def list_all_customers(self):
        """
        Get all customers with their IDs
        Returns: List of customers with ID, name, and metadata
        """
        print("Fetching all customers\n")
        raw = self._make_request("/customers")
        customers = self._unwrap_list(raw)
        
        customer_list = []
        for idx, customer in enumerate(customers, 1):
            customer_info = {
                "index": idx,
                "customer_id": customer['_id'],
                "name": f"{customer['first_name']} {customer['last_name']}",
                "first_name": customer['first_name'],
                "last_name": customer['last_name'],
                "address": customer.get('address', {})
            }
            customer_list.append(customer_info)
            print(f"{idx}. ID: {customer['_id']}")
            print(f"   Name: {customer['first_name']} {customer['last_name']}")
            print(f"   Address: {customer.get('address', {}).get('city', 'N/A')}, {customer.get('address', {}).get('state', 'N/A')}\n")
        
        return customer_list
    
    def fetch_customer_data_by_id(self, customer_id):
        """
        Fetch all transaction data for a customer by ID
        Args:
            customer_id: The customer's unique ID from the API
        Returns: Dictionary with all customer data
        """
        print(f"Fetching data for customer ID: {customer_id}...")
        
        # 1. Get customer details
        customer = self._make_request(f"/customers/{customer_id}")
        customer_name = f"{customer['first_name']} {customer['last_name']}"
        
        # 2. Get customer's accounts
        accounts = self._unwrap_list(self._make_request(f"/customers/{customer_id}/accounts"))
        
        if not accounts:
            raise ValueError(f"No accounts found for customer {customer_id}")
        
        account = accounts[0]
        account_id = account['_id']
        
        # 3. Get purchases
        purchases = self._unwrap_list(self._make_request(f"/accounts/{account_id}/purchases"))
        
        # 4. Get deposits
        deposits = self._unwrap_list(self._make_request(f"/accounts/{account_id}/deposits"))
        
        # 5. Enrich purchases with merchant info
        enriched_purchases = []
        for purchase in purchases:
            merchant_id = purchase.get('merchant_id')
            if merchant_id:
                try:
                    merchant = self._make_request(f"/merchants/{merchant_id}")
                    purchase['merchant_name'] = merchant.get('name', 'Unknown')
                    purchase['merchant_category'] = merchant.get('category', 'Unknown')
                except:
                    purchase['merchant_name'] = 'Unknown'
                    purchase['merchant_category'] = 'Unknown'
            enriched_purchases.append(purchase)
        
        # 6. Build complete data structure
        customer_data = {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "customer_metadata": {
                "first_name": customer['first_name'],
                "last_name": customer['last_name'],
                "address": customer.get('address', {})
            },
            "account": {
                "account_id": account_id,
                "type": account.get('type'),
                "nickname": account.get('nickname'),
                "balance": account.get('balance'),
                "rewards": account.get('rewards')
            },
            "deposits": sorted(deposits, key=lambda x: x.get('transaction_date', '')),
            "purchases": sorted(enriched_purchases, key=lambda x: x.get('purchase_date', '')),
            "statistics": {
                "total_deposits": len(deposits),
                "total_purchases": len(purchases),
                "total_deposited": sum(d.get('amount', 0) for d in deposits),
                "total_spent": sum(p.get('amount', 0) for p in purchases),
                "date_range": "6 months",
                "categories_active": len(set(p.get('merchant_category', 'Unknown') for p in enriched_purchases))
            }
        }
        
        print(f"Fetched {len(deposits)} deposits and {len(purchases)} purchases")
        print(f"   Customer: {customer_name}")
        print(f"   Account: {customer_data}")
        return customer_data
    
    def aes_encrypt(self, data):
        """
        AES-256 CBC encryption
        Args:
            data: Dictionary or string to encrypt
        Returns:
            Dictionary with encrypted data and IV
        """
        # Convert data to JSON string
        if isinstance(data, dict):
            plaintext = json.dumps(data, indent=2)
        else:
            plaintext = str(data)
        
        # Generate random IV (Initialization Vector)
        iv = os.urandom(16)
        
        # Pad the data to AES block size (128 bits)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        
        # Encrypt
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return base64 encoded for easy transmission
        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "iv": base64.b64encode(iv).decode(),
            "encryption_method": "AES-256-CBC"
        }
    
    def aes_decrypt(self, encrypted_package, key=None):
        """
        AES-256 CBC decryption
        Args:
            encrypted_package: Dictionary with encrypted_data and iv
            key: Optional decryption key (uses instance key if not provided)
        Returns:
            Decrypted data as dictionary
        """
        if key is None:
            key = self.key
        
        # Decode from base64
        encrypted_data = base64.b64decode(encrypted_package['encrypted_data'])
        iv = base64.b64decode(encrypted_package['iv'])
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        
        # Parse JSON
        return json.loads(plaintext.decode())
    
    def process_customer_by_id(self, customer_id, output_dir="encrypted_data"):
        """
        Complete pipeline: Fetch → Encrypt → Save (using customer ID)
        """
        print(f"\n{'='*80}")
        print(f"Processing Customer ID: {customer_id}")
        print(f"{'='*80}\n")
        
        # 1. Fetch data
        customer_data = self.fetch_customer_data_by_id(customer_id)
        
        # 2. Save raw JSON (for reference)
        os.makedirs(output_dir, exist_ok=True)
        raw_filename = f"{output_dir}/customer_{customer_id}_raw.json"
        with open(raw_filename, 'w') as f:
            json.dump(customer_data, f, indent=2)
        print(f"💾 Raw data saved: {raw_filename}")
        
        # 3. Encrypt
        print(f"🔒 Encrypting data...")
        encrypted_package = self.aes_encrypt(customer_data)
        
        # 4. Save encrypted package
        encrypted_filename = f"{output_dir}/customer_{customer_id}_encrypted.json"
        with open(encrypted_filename, 'w') as f:
            json.dump(encrypted_package, f, indent=2)
        print(f"✅ Encrypted data saved: {encrypted_filename}")
        
        # 5. Test decryption
        print(f"🔓 Testing decryption...")
        decrypted = self.aes_decrypt(encrypted_package)
        assert decrypted['customer_id'] == customer_data['customer_id']
        print(f"✅ Decryption successful!")
        
        return {
            "customer_id": customer_id,
            "customer_name": customer_data['customer_name'],
            "customer_data": customer_data,
            "encrypted_package": encrypted_package,
            "raw_file": raw_filename,
            "encrypted_file": encrypted_filename
        }
    
    def generate_gemini_package(self, customer_id, output_dir="encrypted_data"):
        """
        Generate a complete package for Gemini with decryption instructions
        """
        result = self.process_customer_by_id(customer_id, output_dir)
        
        # Create Gemini instruction file
        instructions = f"""
# Gemini Analysis Package - Customer ID: {customer_id}

## 🔐 Encrypted Financial Data for Analysis

This package contains encrypted banking transaction data for financial abuse detection.

**Customer ID**: {customer_id}
**Customer Name**: {result['customer_name']} (for reference only)

### Decryption Details:
- **Encryption Method**: AES-256-CBC
- **Key (Base64)**: {base64.b64encode(self.key).decode()}

### Encrypted Package:
The encrypted data is in: {result['encrypted_file']}

### Your Task:
1. Decrypt the data using the provided AES key
2. Analyze the transaction patterns for signs of financial abuse
3. Provide a risk assessment (LOW / MEDIUM / HIGH)
4. Identify specific patterns and red flags
5. Recommend appropriate actions

### Decryption Code (Python):
```python
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Load encrypted package
with open('{result['encrypted_file']}', 'r') as f:
    encrypted_package = json.load(f)

# Decryption key
key = base64.b64decode("{base64.b64encode(self.key).decode()}")

# Decrypt
encrypted_data = base64.b64decode(encrypted_package['encrypted_data'])
iv = base64.b64decode(encrypted_package['iv'])

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

unpadder = padding.PKCS7(128).unpadder()
plaintext = unpadder.update(padded_data) + unpadder.finalize()

# Parse JSON
data = json.loads(plaintext.decode())
print(json.dumps(data, indent=2))
```

### Expected Analysis:
- **Customer ID**: {result['customer_id']}
- **Deposits**: {result['customer_data']['statistics']['total_deposits']}
- **Purchases**: {result['customer_data']['statistics']['total_purchases']}
- **Categories Active**: {result['customer_data']['statistics']['categories_active']}
- **Analysis Period**: {result['customer_data']['statistics']['date_range']}

Please analyze this customer's financial patterns for signs of abuse.
"""
        
        instructions_file = f"{output_dir}/customer_{customer_id}_gemini_instructions.txt"
        with open(instructions_file, 'w') as f:
            f.write(instructions)
        
        print(f"\n📋 Gemini instructions saved: {instructions_file}")
        
        # Also create a simple prompt
        prompt = f"""
I have encrypted banking transaction data that I need you to analyze for signs of financial abuse.

Customer ID: {customer_id}
Encryption: AES-256-CBC

Please help me:
1. Decrypt the attached data using the provided key
2. Analyze the transaction patterns
3. Identify any signs of financial abuse (irregular deposits, restricted spending, category elimination, etc.)
4. Provide a risk level: LOW / MEDIUM / HIGH
5. Explain your reasoning with specific evidence

The encrypted package and decryption key are in the attached file.
"""
        
        prompt_file = f"{output_dir}/customer_{customer_id}_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        print(f"📝 Prompt saved: {prompt_file}")
        
        return result
    
    def create_customer_mapping(self, output_dir="encrypted_data"):
        """
        Create a mapping file that shows which customer IDs correspond to which profiles
        """
        customers = self.list_all_customers()
        
        mapping = {
            "encryption_key": base64.b64encode(self.key).decode(),
            "customers": []
        }
        
        for customer in customers:
            mapping["customers"].append({
                "customer_id": customer["customer_id"],
                "name": customer["name"],
                "profile_type": "To be determined by analysis",
                "files": {
                    "raw": f"customer_{customer['customer_id']}_raw.json",
                    "encrypted": f"customer_{customer['customer_id']}_encrypted.json",
                    "instructions": f"customer_{customer['customer_id']}_gemini_instructions.txt",
                    "prompt": f"customer_{customer['customer_id']}_prompt.txt"
                }
            })
        
        os.makedirs(output_dir, exist_ok=True)
        mapping_file = f"{output_dir}/customer_mapping.json"
        with open(mapping_file, 'w') as f:
            json.dump(mapping, f, indent=2)
        
        print(f"\n📋 Customer mapping saved: {mapping_file}")
        return mapping


def main():
    """Main execution"""
    print("="*80)
    print("SECURE FINANCIAL ABUSE DETECTION - ID-BASED PIPELINE")
    print("="*80)
    
    # Initialize pipeline
    pipeline = SecureDataPipeline(API_KEY)
    
    # Save the encryption key
    key_file = "encryption_key.txt"
    with open(key_file, 'w') as f:
        f.write(base64.b64encode(pipeline.key).decode())
    print(f"🔑 Encryption key saved to: {key_file}\n")
    
    # List all customers and get their IDs
    customers = pipeline.list_all_customers()
    
    if not customers:
        print("No customers found! Please run generate_data.py first.")
        return
    
    # Process all customers by ID
    print("\n" + "="*80)
    print("PROCESSING ALL CUSTOMERS")
    print("="*80)
    
    results = {}
    for customer in customers:
        customer_id = customer['customer_id']
        try:
            result = pipeline.generate_gemini_package(customer_id)
            results[customer_id] = result
        except Exception as e:
            print(f"❌ Error processing customer {customer_id}: {e}")
    
#     # Create customer mapping file
#     print("\n" + "="*80)
#     print("CREATING CUSTOMER MAPPING")
#     print("="*80)
    mapping = pipeline.create_customer_mapping()
    
#     # Summary
#     print("\n" + "="*80)
#     print("PROCESSING COMPLETE")
#     print("="*80)
#     print("\n📦 Generated Files:")
#     for customer_id, result in results.items():
#         print(f"\nCustomer ID: {customer_id}")
#         print(f"Name: {result['customer_name']}")
#         print(f"  ├─ Raw JSON: {result['raw_file']}")
#         print(f"  ├─ Encrypted: {result['encrypted_file']}")
#         print(f"  ├─ Instructions: encrypted_data/customer_{customer_id}_gemini_instructions.txt")
#         print(f"  └─ Prompt: encrypted_data/customer_{customer_id}_prompt.txt")
    
#     print(f"\n🔐 Encryption Key: {key_file}")
#     print(f"📋 Customer Mapping: encrypted_data/customer_mapping.json")
    
#     print("\n" + "="*80)
#     print("NEXT STEPS")
#     print("="*80)
#     print("""
# 1. Check customer_mapping.json to see all customer IDs
# 2. Send encrypted files to Gemini by customer ID
# 3. Include the decryption instructions
# 4. Gemini will decrypt and analyze the data
# 5. You'll get a risk assessment with evidence

# Expected Profiles:
# • Customer with consistent patterns → LOW RISK (no abuse)
# • Customer with declining patterns → MEDIUM-HIGH RISK (escalating abuse)
# • Customer with minimal transactions → HIGH RISK (severe abuse)

# All references now use customer IDs instead of names for better data integrity.
#     """)


if __name__ == "__main__":
    main()