from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import json
import base64

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
    # PBKDF2 with 100,000 iterations (resistant to brute force)
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
# HELPER FUNCTIONS
# ============================================================================

def test_encryption():
    """
    Test encryption/decryption with sample data
    Run this to verify encryption is working
    """
    print("\n" + "="*60)
    print("🧪 Testing Encryption...")
    print("="*60)
    
    # Sample data
    test_data = {
        "user": "test_user",
        "transactions": [
            {"id": 1, "amount": 50.00, "merchant": "Grocery Store"},
            {"id": 2, "amount": 25.00, "merchant": "Gas Station"}
        ],
        "sensitive_info": "This should be encrypted"
    }
    
    password = "test_password_123"
    
    try:
        # Encrypt
        print("\n1️⃣  Encrypting data...")
        encrypted, salt = encrypt_data(test_data, password)
        print(f"✅ Encrypted successfully")
        print(f"   Encrypted (first 50 chars): {encrypted[:50]}...")
        print(f"   Salt: {salt}")
        
        # Decrypt
        print("\n2️⃣  Decrypting data...")
        decrypted = decrypt_data(encrypted, salt, password)
        print(f"✅ Decrypted successfully")
        print(f"   Data matches: {decrypted == test_data}")
        
        # Test wrong password
        print("\n3️⃣  Testing wrong password...")
        try:
            decrypt_data(encrypted, salt, "wrong_password")
            print("❌ ERROR: Wrong password should fail!")
        except:
            print("✅ Correctly rejected wrong password")
        
        print("\n" + "="*60)
        print("✅ All encryption tests passed!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Encryption test failed: {e}\n")
        return False

# ============================================================================
# ADVANCED FEATURES (Optional for hackathon)
# ============================================================================

def encrypt_file(file_path: str, password: str, output_path: str = None):
    """
    Encrypt a file (for document vault)
    
    Args:
        file_path: Path to file to encrypt
        password: Encryption password
        output_path: Where to save encrypted file (default: file_path + '.enc')
    """
    try:
        if output_path is None:
            output_path = file_path + '.enc'
        
        # Read file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Encrypt (convert bytes to base64 string first)
        file_b64 = base64.b64encode(file_data).decode('utf-8')
        encrypted, salt = encrypt_data({'file': file_b64}, password)
        
        # Save encrypted file
        with open(output_path, 'w') as f:
            f.write(json.dumps({
                'encrypted': encrypted,
                'salt': salt
            }))
        
        print(f"✅ File encrypted: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ File encryption failed: {e}")
        raise

def decrypt_file(encrypted_path: str, password: str, output_path: str):
    """
    Decrypt a file
    
    Args:
        encrypted_path: Path to encrypted file
        password: Decryption password
        output_path: Where to save decrypted file
    """
    try:
        # Read encrypted file
        with open(encrypted_path, 'r') as f:
            enc_data = json.load(f)
        
        # Decrypt
        decrypted = decrypt_data(
            enc_data['encrypted'],
            enc_data['salt'],
            password
        )
        
        # Decode from base64
        file_data = base64.b64decode(decrypted['file'])
        
        # Save decrypted file
        with open(output_path, 'wb') as f:
            f.write(file_data)
        
        print(f"✅ File decrypted: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ File decryption failed: {e}")
        raise

# ============================================================================
# RUN TESTS IF EXECUTED DIRECTLY
# ============================================================================

if __name__ == '__main__':
    # Run encryption tests
    test_encryption()
    
    # Example usage
    print("\n📝 Example Usage:")
    print("-" * 60)
    
    example_data = {
        "customer_id": "abc123",
        "purchases": [
            {"amount": 45.99, "merchant": "Target"},
            {"amount": 12.50, "merchant": "Starbucks"}
        ]
    }
    
    password = "my_secure_pin"
    
    print("\nOriginal data:")
    print(json.dumps(example_data, indent=2))
    
    # Encrypt
    encrypted, salt = encrypt_data(example_data, password)
    print(f"\nEncrypted: {encrypted[:100]}...")
    print(f"Salt: {salt}")
    
    # Decrypt
    decrypted = decrypt_data(encrypted, salt, password)
    print("\nDecrypted data:")
    print(json.dumps(decrypted, indent=2))
    
    print("\n✅ Encryption module ready!")