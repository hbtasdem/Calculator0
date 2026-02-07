from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow React Native to call this API

# ============================================================================
# DATABASE SETUP
# ============================================================================

def init_db():
    """Initialize SQLite database with users table only"""
    conn = sqlite3.connect('secure_data.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id TEXT PRIMARY KEY, 
                  password_hash TEXT, 
                  customer_id TEXT,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

init_db()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def verify_user(user_id, password):
    """Verify user credentials"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect('secure_data.db')
    c = conn.cursor()
    c.execute('SELECT password_hash, customer_id FROM users WHERE id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == password_hash:
        return True, result[1]  # Return (is_valid, customer_id)
    return False, None

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/auth/setup', methods=['POST'])
def setup_account():
    """
    Initial account setup - create new user
    
    Request:
    {
        "firebase_uid": "abc123" (or any user_id),
        "password": "user_pin",
        "customer_id": "nessie_customer_id"
    }
    """
    try:
        data = request.json
        firebase_uid = data.get('firebase_uid') or data.get('user_id')
        password = data.get('password')
        customer_id = data.get('customer_id')
        
        if not all([firebase_uid, password, customer_id]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: firebase_uid, password, customer_id'
            }), 400
        
        # Hash password for storage
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Store in database
        conn = sqlite3.connect('secure_data.db')
        c = conn.cursor()
        
        # Check if user already exists
        c.execute('SELECT id FROM users WHERE id = ?', (firebase_uid,))
        existing = c.fetchone()
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'User already exists'
            }), 409
        
        c.execute('INSERT INTO users (id, password_hash, customer_id) VALUES (?, ?, ?)', 
                  (firebase_uid, password_hash, customer_id))
        conn.commit()
        conn.close()
        
        print(f"✅ User created: {firebase_uid}")
        
        return jsonify({
            'success': True,
            'user_id': firebase_uid,
            'customer_id': customer_id,
            'message': 'Account setup complete'
        })
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Login with PIN/password
    Supports both real PIN and decoy PIN
    
    Request:
    {
        "user_id": "firebase_uid",
        "password": "user_pin"
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            return jsonify({
                'success': False,
                'error': 'Missing credentials'
            }), 400
        
        # Check for decoy PIN first (0000)
        if password == '0000':
            print(f"⚠️  Decoy PIN used by: {user_id}")
            return jsonify({
                'success': True,
                'is_decoy': True,
                'message': 'Decoy mode activated'
            })
        
        # Verify real credentials
        is_valid, customer_id = verify_user(user_id, password)
        
        if is_valid:
            print(f"✅ Login successful: {user_id}")
            return jsonify({
                'success': True,
                'is_decoy': False,
                'customer_id': customer_id,
                'message': 'Login successful'
            })
        else:
            print(f"❌ Login failed: {user_id}")
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/verify', methods=['POST'])
def verify_password():
    """
    Verify password without full login (for sensitive operations)
    
    Request:
    {
        "user_id": "firebase_uid",
        "password": "user_pin"
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            return jsonify({
                'success': False,
                'error': 'Missing credentials'
            }), 400
        
        is_valid, customer_id = verify_user(user_id, password)
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'customer_id': customer_id if is_valid else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/update-password', methods=['POST'])
def update_password():
    """
    Update user password
    
    Request:
    {
        "user_id": "firebase_uid",
        "old_password": "current_pin",
        "new_password": "new_pin"
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not all([user_id, old_password, new_password]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Verify old password
        is_valid, _ = verify_user(user_id, old_password)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Invalid current password'
            }), 401
        
        # Update to new password
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        conn = sqlite3.connect('secure_data.db')
        c = conn.cursor()
        c.execute('UPDATE users SET password_hash = ? WHERE id = ?',
                  (new_password_hash, user_id))
        conn.commit()
        conn.close()
        
        print(f"✅ Password updated: {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Password updated successfully'
        })
        
    except Exception as e:
        print(f"❌ Password update error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/delete-account', methods=['POST'])
def delete_account():
    """
    Delete user account
    
    Request:
    {
        "user_id": "firebase_uid",
        "password": "user_pin",
        "confirm": "DELETE"
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        password = data.get('password')
        confirm = data.get('confirm')
        
        if confirm != "DELETE":
            return jsonify({
                'success': False,
                'error': 'Confirmation required. Must send "confirm": "DELETE"'
            }), 400
        
        # Verify password
        is_valid, _ = verify_user(user_id, password)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Invalid password'
            }), 401
        
        # Delete account
        conn = sqlite3.connect('secure_data.db')
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        print(f"✅ Account deleted: {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Account deleted successfully'
        })
        
    except Exception as e:
        print(f"❌ Account deletion error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0-auth-only'
    })

@app.route('/api/users/list', methods=['GET'])
def list_users():
    """List all users (for testing only - remove in production!)"""
    try:
        conn = sqlite3.connect('secure_data.db')
        c = conn.cursor()
        c.execute('SELECT id, customer_id, created_at FROM users')
        users = c.fetchall()
        conn.close()
        
        user_list = [
            {
                'user_id': user[0],
                'customer_id': user[1],
                'created_at': user[2]
            }
            for user in users
        ]
        
        return jsonify({
            'success': True,
            'users': user_list,
            'count': len(user_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔒 Cipher API Server (Auth Only) Starting...")
    print("="*60)
    print("📍 Running on: http://localhost:5000")
    print("🔥 Hot reload enabled")
    print("🌐 CORS enabled for React Native")
    print("💾 Database: secure_data.db")
    print("\n🚀 Available endpoints:")
    print("   POST /api/auth/setup")
    print("   POST /api/auth/login")
    print("   POST /api/auth/verify")
    print("   POST /api/auth/update-password")
    print("   POST /api/auth/delete-account")
    print("   GET  /api/health")
    print("   GET  /api/users/list")
    print("="*60 + "\n")
    
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )