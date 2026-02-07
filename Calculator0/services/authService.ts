import { auth } from '@/config/firebase';
import * as SecureStore from 'expo-secure-store';
import * as LocalAuthentication from 'expo-local-authentication';

const API_BASE = 'http://localhost:5000/api';
const BIOMETRICS_ENABLED_KEY = 'biometrics_enabled';

export const authService = {
  /**
   * Sign up new user with Firebase + link to backend
   */
  signUp: async (email: string, password: string, customerId: string) => {
    try {
      // 1. Create user in Firebase
      console.log('📝 Creating Firebase user...');
      const userCredential = await auth().createUserWithEmailAndPassword(email, password);
      const firebaseUid = userCredential.user.uid;

      console.log('✅ Firebase user created:', firebaseUid);

      // 2. Link Firebase UID to backend
      console.log('🔗 Linking to backend...');
      const response = await fetch(`${API_BASE}/auth/setup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          firebase_uid: firebaseUid,
          password: password,  // User's PIN for encryption
          customer_id: customerId
        })
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || 'Backend setup failed');
      }

      console.log('✅ Backend linked');

      // 3. Store credentials securely
      await SecureStore.setItemAsync('user_id', firebaseUid);
      await SecureStore.setItemAsync('password', password);
      await SecureStore.setItemAsync('customer_id', customerId);
      await SecureStore.setItemAsync('email', email);

      return {
        success: true,
        user: userCredential.user,
        firebaseUid: firebaseUid
      };

    } catch (error: any) {
      console.error('❌ Signup error:', error);

      // Parse Firebase error messages
      let errorMessage = error.message;
      if (error.code === 'auth/email-already-in-use') {
        errorMessage = 'This email is already registered';
      } else if (error.code === 'auth/weak-password') {
        errorMessage = 'Password must be at least 6 characters';
      } else if (error.code === 'auth/invalid-email') {
        errorMessage = 'Invalid email address';
      }

      return {
        success: false,
        error: errorMessage
      };
    }
  },

  /**
   * Sign in with Firebase
   */
  signIn: async (email: string, password: string) => {
    try {
      console.log('🔐 Signing in with Firebase...');
      const userCredential = await auth().signInWithEmailAndPassword(email, password);
      const firebaseUid = userCredential.user.uid;

      console.log('✅ Firebase login successful:', firebaseUid);

      // Verify with backend and get customer_id
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: firebaseUid,
          password: password
        })
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || 'Backend login failed');
      }

      // Store credentials
      await SecureStore.setItemAsync('user_id', firebaseUid);
      await SecureStore.setItemAsync('password', password);
      await SecureStore.setItemAsync('email', email);

      if (data.customer_id) {
        await SecureStore.setItemAsync('customer_id', data.customer_id);
      }

      return {
        success: true,
        user: userCredential.user,
        isDecoy: data.is_decoy || false,
        customerId: data.customer_id
      };

    } catch (error: any) {
      console.error('❌ Login error:', error);

      let errorMessage = error.message;
      if (error.code === 'auth/user-not-found' || error.code === 'auth/wrong-password') {
        errorMessage = 'Invalid email or password';
      } else if (error.code === 'auth/too-many-requests') {
        errorMessage = 'Too many failed attempts. Try again later.';
      }

      return {
        success: false,
        error: errorMessage
      };
    }
  },

  /**
   * Sign out
   */
  signOut: async () => {
    try {
      await auth().signOut();

      // Clear stored credentials and biometric preference
      await SecureStore.deleteItemAsync('user_id');
      await SecureStore.deleteItemAsync('password');
      await SecureStore.deleteItemAsync('customer_id');
      await SecureStore.deleteItemAsync('email');
      await SecureStore.deleteItemAsync(BIOMETRICS_ENABLED_KEY);

      console.log('✅ Signed out');
      return { success: true };

    } catch (error: any) {
      console.error('❌ Signout error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  },

  /**
   * Get current Firebase user
   */
  getCurrentUser: () => {
    return auth().currentUser;
  },

  /**
   * Check if user is signed in
   */
  isSignedIn: async () => {
    const user = auth().currentUser;
    const storedUserId = await SecureStore.getItemAsync('user_id');
    return user !== null && storedUserId !== null;
  },

  /**
   * Get stored credentials for API calls
   */
  getCredentials: async () => {
    const userId = await SecureStore.getItemAsync('user_id');
    const password = await SecureStore.getItemAsync('password');
    const customerId = await SecureStore.getItemAsync('customer_id');
    const email = await SecureStore.getItemAsync('email');

    return { userId, password, customerId, email };
  },

  // --- Face ID / Touch ID (after initial sign-in) ---

  /** Whether user chose to use biometrics for app unlock */
  isBiometricsEnabled: async (): Promise<boolean> => {
    const value = await SecureStore.getItemAsync(BIOMETRICS_ENABLED_KEY);
    return value === 'true';
  },

  /** Turn on/off "unlock with Face ID" for this device */
  setBiometricsEnabled: async (enabled: boolean): Promise<void> => {
    if (enabled) {
      await SecureStore.setItemAsync(BIOMETRICS_ENABLED_KEY, 'true');
    } else {
      await SecureStore.deleteItemAsync(BIOMETRICS_ENABLED_KEY);
    }
  },

  /** Device supports and has biometrics enrolled */
  isBiometricsAvailable: async (): Promise<boolean> => {
    const hasHardware = await LocalAuthentication.hasHardwareAsync();
    const isEnrolled = await LocalAuthentication.isEnrolledAsync();
    return hasHardware && isEnrolled;
  },

  /** Prompt Face ID / Touch ID; returns true if user authenticated */
  authenticateWithBiometrics: async (reason?: string): Promise<boolean> => {
    const options: LocalAuthentication.LocalAuthenticationOptions = {
      promptMessage: reason ?? 'Unlock 0',
      cancelLabel: 'Cancel',
    };
    const result = await LocalAuthentication.authenticateAsync(options);
    return result.success;
  },
};