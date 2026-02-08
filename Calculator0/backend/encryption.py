from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import json
import base64
import csv
from typing import List, Dict

# ============================================================================
# AES-256-GCM ENCRYPTION
# ============================================================================

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 256-bit encryption key from password using PBKDF2
    
    Args:
        password: User's password/PIN
        salt: Random salt (16 bytes)
    
    Returns:
        32-byte encryption key
    """
    key = PBKDF2(
        password, 
        salt, 
        dkLen=32,      # 256 bits
        count=100000   # Iterations (higher = more secure but slower)
    )
    return key

def encrypt_data(data: dict, password: str) -> tuple[str, str]:
    """
    Encrypt data with AES-256-GCM
    
    Args:
        data: Dictionary to encrypt (will be JSON-encoded)
        password: User's password/PIN
    
    Returns:
        Tuple of (encrypted_base64, salt_base64)
    """
    try:
        # Generate random salt
        salt = get_random_bytes(16)
        
        # Derive encryption key from password
        key = derive_key(password, salt)
        
        # Convert data to JSON bytes
        plaintext = json.dumps(data).encode('utf-8')
        
        # Create AES-GCM cipher (authenticated encryption)
        cipher = AES.new(key, AES.MODE_GCM)
        
        # Encrypt and get authentication tag
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        
        # Combine: nonce (16 bytes) + tag (16 bytes) + ciphertext
        encrypted = cipher.nonce + tag + ciphertext
        
        # Return base64-encoded strings for storage
        return (
            base64.b64encode(encrypted).decode('utf-8'),
            base64.b64encode(salt).decode('utf-8')
        )
        
    except Exception as e:
        print(f"❌ Encryption error: {e}")
        raise Exception(f"Encryption failed: {str(e)}")

def decrypt_data(encrypted_data: str, salt: str, password: str) -> dict:
    """
    Decrypt AES-256-GCM encrypted data
    
    Args:
        encrypted_data: Base64-encoded encrypted data
        salt: Base64-encoded salt
        password: User's password/PIN
    
    Returns:
        Decrypted dictionary
    """
    try:
        # Decode from base64
        encrypted = base64.b64decode(encrypted_data)
        salt_bytes = base64.b64decode(salt)
        
        # Derive same key from password and salt
        key = derive_key(password, salt_bytes)
        
        # Extract components
        nonce = encrypted[:16]      # First 16 bytes
        tag = encrypted[16:32]      # Next 16 bytes
        ciphertext = encrypted[32:] # Rest is ciphertext
        
        # Create cipher with nonce
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        # Decrypt and verify authentication tag
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        # Parse JSON
        data = json.loads(plaintext.decode('utf-8'))
        
        return data
        
    except ValueError as e:
        # Authentication tag verification failed
        print(f"❌ Decryption failed - wrong password or corrupted data: {e}")
        raise Exception("Decryption failed: Invalid password or corrupted data")
    except Exception as e:
        print(f"❌ Decryption error: {e}")
        raise Exception(f"Decryption failed: {str(e)}")

# ============================================================================
# CSV-SPECIFIC FUNCTIONS
# ============================================================================

def encrypt_transaction_list(transactions: List[Dict], password: str) -> tuple[str, str]:
    """
    Encrypt a list of transaction dictionaries from CSV
    
    Args:
        transactions: List of transaction dicts with keys like:
                     {date, description, category, debit, credit, amount}
        password: User's password/PIN
    
    Returns:
        Tuple of (encrypted_base64, salt_base64)
    """
    try:
        transaction_data = {
            'transactions': transactions,
            'count': len(transactions),
            'uploaded_at': None  # Can add timestamp if needed
        }
        
        return encrypt_data(transaction_data, password)
        
    except Exception as e:
        print(f"❌ Transaction encryption error: {e}")
        raise

def decrypt_transaction_list(encrypted_data: str, salt: str, password: str) -> List[Dict]:
    """
    Decrypt transaction data and return list of transactions
    
    Args:
        encrypted_data: Base64-encoded encrypted data
        salt: Base64-encoded salt
        password: User's password/PIN
    
    Returns:
        List of transaction dictionaries
    """
    try:
        decrypted = decrypt_data(encrypted_data, salt, password)
        return decrypted.get('transactions', [])
        
    except Exception as e:
        print(f"❌ Transaction decryption error: {e}")
        raise

def parse_and_encrypt_csv(csv_content: str, password: str) -> tuple[str, str, int]:
    """
    Parse CSV content and encrypt transactions
    
    Args:
        csv_content: Raw CSV string
        password: User's password/PIN
    
    Returns:
        Tuple of (encrypted_base64, salt_base64, transaction_count)
    """
    try:
        # Parse CSV
        lines = csv_content.strip().split('\n')
        
        # Skip header
        reader = csv.DictReader(lines)
        transactions = []
        
        for row in reader:
            transaction = {
                'date': row.get('Transaction Date', '').strip(),
                'description': row.get('Description', '').strip(),
                'category': row.get('Category', '').strip(),
                'debit': float(row.get('Debit', '0').strip() or '0'),
                'credit': float(row.get('Credit', '0').strip() or '0'),
            }
            
            # Calculate amount (positive for expenses, negative for income)
            transaction['amount'] = transaction['debit'] if transaction['debit'] > 0 else -transaction['credit']
            
            transactions.append(transaction)
        
        # Encrypt
        encrypted, salt = encrypt_transaction_list(transactions, password)
        
        print(f"✅ Encrypted {len(transactions)} transactions")
        
        return encrypted, salt, len(transactions)
        
    except Exception as e:
        print(f"❌ CSV parsing/encryption error: {e}")
        raise

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def test_encryption():
    """Test encryption/decryption with sample transaction data"""
    print("\n" + "="*60)
    print("🧪 Testing Transaction Encryption...")
    print("="*60)
    
    # Sample transaction data (mimics CSV structure)
    test_transactions = [
        {
            "date": "2024-01-15",
            "description": "Grocery Store",
            "category": "Food & Dining",
            "debit": 45.99,
            "credit": 0,
            "amount": 45.99
        },
        {
            "date": "2024-01-16",
            "description": "Paycheck",
            "category": "Income",
            "debit": 0,
            "credit": 2500.00,
            "amount": -2500.00
        },
        {
            "date": "2024-01-17",
            "description": "Gas Station",
            "category": "Auto & Transport",
            "debit": 52.30,
            "credit": 0,
            "amount": 52.30
        }
    ]
    
    password = "test_password_123"
    
    try:
        # Test 1: Encrypt transactions
        print("\n1️⃣  Encrypting transactions...")
        encrypted, salt = encrypt_transaction_list(test_transactions, password)
        print(f"✅ Encrypted successfully")
        print(f"   Transaction count: {len(test_transactions)}")
        print(f"   Encrypted (first 50 chars): {encrypted[:50]}...")
        print(f"   Salt: {salt}")
        
        # Test 2: Decrypt transactions
        print("\n2️⃣  Decrypting transactions...")
        decrypted = decrypt_transaction_list(encrypted, salt, password)
        print(f"✅ Decrypted successfully")
        print(f"   Data matches: {decrypted == test_transactions}")
        print(f"   First transaction: {decrypted[0]}")
        
        # Test 3: Wrong password
        print("\n3️⃣  Testing wrong password...")
        try:
            decrypt_transaction_list(encrypted, salt, "wrong_password")
            print("❌ ERROR: Wrong password should fail!")
        except:
            print("✅ Correctly rejected wrong password")
        
        # Test 4: CSV parsing and encryption
        print("\n4️⃣  Testing CSV parsing and encryption...")
        csv_content = """Transaction Date,Post Date,Card No.,Description,Category,Debit,Credit
2024-01-15,2024-01-16,1234,Grocery Store,Food & Dining,45.99,
2024-01-16,2024-01-17,1234,Paycheck,Income,,2500.00
2024-01-17,2024-01-18,1234,Gas Station,Auto & Transport,52.30,"""
        
        encrypted_csv, salt_csv, count = parse_and_encrypt_csv(csv_content, password)
        print(f"✅ CSV parsed and encrypted")
        print(f"   Transactions parsed: {count}")
        
        decrypted_csv = decrypt_transaction_list(encrypted_csv, salt_csv, password)
        print(f"✅ CSV decrypted successfully")
        print(f"   First CSV transaction: {decrypted_csv[0]}")
        
        print("\n" + "="*60)
        print("✅ All transaction encryption tests passed!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Encryption test failed: {e}\n")
        return False

def test_with_sample_csv_file(csv_file_path: str, password: str):
    """
    Test encryption with an actual CSV file
    
    Args:
        csv_file_path: Path to CSV file
        password: Password for encryption
    """
    try:
        print(f"\nReading CSV file: {csv_file_path}")
        
        with open(csv_file_path, 'r') as f:
            csv_content = f.read()
        
        print("Encrypting...")
        encrypted, salt, count = parse_and_encrypt_csv(csv_content, password)
        
        print(f" Encrypted {count} transactions")
        print(f"   Encrypted data (first 100 chars): {encrypted[:100]}...")
        print(f"   Salt: {salt}")
        
        print("\n Decrypting...")
        decrypted = decrypt_transaction_list(encrypted, salt, password)
        
        print(f"Decrypted {len(decrypted)} transactions")
        print(f"\nFirst 3 transactions:")
        for i, txn in enumerate(decrypted[:3], 1):
            print(f"  {i}. {txn['date']} - {txn['description']}: ${txn['amount']:.2f}")
        
        return encrypted, salt
        
    except Exception as e:
        print(f"CSV file test failed: {e}")
        raise

# ============================================================================
# RUN TESTS IF EXECUTED DIRECTLY
# ============================================================================

if __name__ == '__main__':
    # Run encryption tests
    test_encryption()
    
    # Example: If you have a sample CSV file, uncomment and update path:
    # test_with_sample_csv_file('sample_transactions.csv', 'my_password')
    
    print("\nEncryption module ready for CSV transaction data!")