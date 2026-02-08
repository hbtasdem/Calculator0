import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User
} from 'firebase/auth';
import { auth } from '@/config/firebase';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthResult {
  success: boolean;
  error?: string;
  isDecoy?: boolean;
}

class AuthService {
  // Sign up with email, password, and customer ID
  async signUp(email: string, password: string, customerId: string): Promise<AuthResult> {
    try {
      // Create user with Firebase Auth
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);

      // Store customer ID in AsyncStorage linked to user UID
      await AsyncStorage.setItem(`customer_id_${userCredential.user.uid}`, customerId);

      return { success: true };
    } catch (error: any) {
      console.error('Sign up error:', error);
      return {
        success: false,
        error: this.getErrorMessage(error.code)
      };
    }
  }

  // Sign in with email and password
  async signIn(email: string, password: string): Promise<AuthResult> {
    try {
      // Check for decoy mode (password is "0000")
      if (password === '0000') {
        // Set decoy flag
        await AsyncStorage.setItem('decoy_mode', 'true');
        return { success: true, isDecoy: true };
      }

      // Regular sign in
      await signInWithEmailAndPassword(auth, email, password);
      await AsyncStorage.setItem('decoy_mode', 'false');

      return { success: true, isDecoy: false };
    } catch (error: any) {
      console.error('Sign in error:', error);
      return {
        success: false,
        error: this.getErrorMessage(error.code)
      };
    }
  }

  // Sign out
  async signOutUser(): Promise<void> {
    try {
      await signOut(auth);
      await AsyncStorage.removeItem('decoy_mode');
    } catch (error) {
      console.error('Sign out error:', error);
      throw error;
    }
  }

  // Get current user
  getCurrentUser(): User | null {
    return auth.currentUser;
  }

  // Listen to auth state changes
  onAuthStateChanged(callback: (user: User | null) => void) {
    return onAuthStateChanged(auth, callback);
  }

  // Get customer ID for current user
  async getCustomerId(): Promise<string | null> {
    const user = this.getCurrentUser();
    if (!user) return null;

    return await AsyncStorage.getItem(`customer_id_${user.uid}`);
  }

  // Check if in decoy mode
  async isDecoyMode(): Promise<boolean> {
    const mode = await AsyncStorage.getItem('decoy_mode');
    return mode === 'true';
  }

  // Get friendly error messages
  private getErrorMessage(errorCode: string): string {
    switch (errorCode) {
      case 'auth/email-already-in-use':
        return 'This email is already registered';
      case 'auth/invalid-email':
        return 'Invalid email address';
      case 'auth/weak-password':
        return 'Password is too weak';
      case 'auth/user-not-found':
        return 'No account found with this email';
      case 'auth/wrong-password':
        return 'Incorrect password';
      case 'auth/too-many-requests':
        return 'Too many failed attempts. Try again later';
      case 'auth/network-request-failed':
        return 'Network error. Check your connection';
      default:
        return 'An error occurred. Please try again';
    }
  }
}

export const authService = new AuthService();