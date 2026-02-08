"""
Decrypt and verify encrypted customer data
Tests that encryption/decryption works correctly
"""

import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def decrypt_file(encrypted_file_path, encryption_key_base64):
    """
    Decrypt an encrypted JSON file
    
    Args:
        encrypted_file_path: Path to the encrypted JSON file
        encryption_key_base64: Base64-encoded encryption key (from encryption_key.txt)
    
    Returns:
        Decrypted data as dictionary
    """
    print(f"🔓 Decrypting: {encrypted_file_path}")
    
    # 1. Load encrypted package
    with open(encrypted_file_path, 'r') as f:
        encrypted_package = json.load(f)
    
    print(f"   Encryption method: {encrypted_package.get('encryption_method')}")
    
    # 2. Decode the key from base64
    key = base64.b64decode(encryption_key_base64)
    print(f"   Key size: {len(key)} bytes ({len(key)*8} bits)")
    
    # 3. Decode encrypted data and IV from base64
    encrypted_data = base64.b64decode(encrypted_package['encrypted_data'])
    iv = base64.b64decode(encrypted_package['iv'])
    
    print(f"   IV size: {len(iv)} bytes")
    print(f"   Encrypted data size: {len(encrypted_data)} bytes")
    
    # 4. Create cipher and decrypt
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # 5. Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    
    # 6. Parse JSON
    data = json.loads(plaintext.decode())
    
    print(f"   ✅ Decryption successful!")
    print(f"   Decrypted data size: {len(plaintext)} bytes")
    
    return data


def verify_customer_data(data):
    """Verify the decrypted data has expected structure"""
    print(f"\n📊 Verifying data structure...")
    
    required_fields = ['customer_id', 'customer_name', 'account', 'deposits', 'purchases', 'statistics']
    
    for field in required_fields:
        if field in data:
            print(f"   ✅ {field}: present")
        else:
            print(f"   ❌ {field}: MISSING!")
            return False
    
    # Check deposits and purchases are lists
    if not isinstance(data['deposits'], list):
        print(f"   ❌ deposits is not a list!")
        return False
    
    if not isinstance(data['purchases'], list):
        print(f"   ❌ purchases is not a list!")
        return False
    
    print(f"\n   ✅ Data structure is valid!")
    return True


def display_summary(data):
    """Display a summary of the decrypted customer data"""
    print(f"\n{'='*80}")
    print(f"CUSTOMER SUMMARY")
    print(f"{'='*80}")
    print(f"Customer ID: {data['customer_id']}")
    print(f"Customer Name: {data['customer_name']}")
    print(f"\nAccount:")
    print(f"  Type: {data['account']['type']}")
    print(f"  Balance: ${data['account']['balance']:,.2f}")
    print(f"  Rewards: {data['account']['rewards']}")
    print(f"\nStatistics:")
    print(f"  Total Deposits: {data['statistics']['total_deposits']}")
    print(f"  Total Purchases: {data['statistics']['total_purchases']}")
    print(f"  Total Deposited: ${data['statistics']['total_deposited']:,.2f}")
    print(f"  Total Spent: ${data['statistics']['total_spent']:,.2f}")
    print(f"  Categories Active: {data['statistics']['categories_active']}")
    print(f"  Date Range: {data['statistics']['date_range']}")
    
    # Show first few transactions
    print(f"\nFirst 3 Deposits:")
    for i, dep in enumerate(data['deposits'][:3], 1):
        print(f"  {i}. {dep.get('transaction_date')}: ${dep.get('amount', 0):,.2f} - {dep.get('description', 'N/A')}")
    
    print(f"\nFirst 3 Purchases:")
    for i, purch in enumerate(data['purchases'][:3], 1):
        merchant = purch.get('merchant_name', 'Unknown')
        print(f"  {i}. {purch.get('purchase_date')}: ${purch.get('amount', 0):,.2f} at {merchant}")
    
    print(f"{'='*80}\n")


def main():
    """Main execution - test decryption"""
    print("="*80)
    print("DECRYPTION VERIFICATION TOOL")
    print("="*80)
    
    # Load encryption key
    print("\n📂 Loading encryption key...")
    try:
        with open('encryption_key.txt', 'r') as f:
            encryption_key = f.read().strip()
        print(f"   ✅ Key loaded: {encryption_key[:10]}...{encryption_key[-10:]}")
        print(f"   Key length: {len(encryption_key)} characters (base64)")
    except FileNotFoundError:
        print("   ❌ encryption_key.txt not found!")
        print("   Make sure you ran the encryption script first.")
        return
    
    # Find encrypted files
    import os
    encrypted_files = []
    if os.path.exists('encrypted_data'):
        for filename in os.listdir('encrypted_data'):
            if filename.endswith('_encrypted.json'):
                encrypted_files.append(os.path.join('encrypted_data', filename))
    
    if not encrypted_files:
        print("\n❌ No encrypted files found in encrypted_data/")
        print("   Make sure you ran the encryption script first.")
        return
    
    print(f"\n📁 Found {len(encrypted_files)} encrypted file(s)")
    
    # Decrypt each file
    for encrypted_file in encrypted_files:
        print(f"\n{'='*80}")
        print(f"Testing: {encrypted_file}")
        print(f"{'='*80}")
        
        try:
            # Decrypt
            decrypted_data = decrypt_file(encrypted_file, encryption_key)
            
            # Verify structure
            if verify_customer_data(decrypted_data):
                # Display summary
                display_summary(decrypted_data)
                
                # Save decrypted version for inspection
                output_file = encrypted_file.replace('_encrypted.json', '_decrypted_test.json')
                with open(output_file, 'w') as f:
                    json.dump(decrypted_data, f, indent=2)
                print(f"💾 Decrypted data saved to: {output_file}")
                print(f"   (for your inspection - not needed for Gemini)")
            else:
                print(f"\n❌ Data verification failed!")
        
        except Exception as e:
            print(f"\n❌ Decryption failed: {e}")
            print(f"   The data may be corrupted or the key is wrong.")
    
    print(f"\n{'='*80}")
    print("VERIFICATION COMPLETE")
    print("="*80)
    print("""
If all files decrypted successfully:
✅ Your encryption is working correctly
✅ Data is not corrupted
✅ Gemini will be able to decrypt using the same key

Next steps:
1. Send encrypted files to your teammate
2. Include encryption_key.txt
3. They'll use these with Gemini for analysis
    """)


if __name__ == "__main__":
    main()