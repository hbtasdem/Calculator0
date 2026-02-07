import { initializeApp, getApps, type FirebaseApp } from 'firebase/app';
import * as FirebaseAuth from '@firebase/auth';
import ReactNativeAsyncStorage from '@react-native-async-storage/async-storage';

// getReactNativePersistence is in the RN build of @firebase/auth (not in main typings)
const { getAuth, initializeAuth, createUserWithEmailAndPassword: firebaseCreateUser, signInWithEmailAndPassword: firebaseSignIn, signOut: firebaseSignOut } = FirebaseAuth;
const getReactNativePersistence = (FirebaseAuth as typeof FirebaseAuth & { getReactNativePersistence: (s: typeof ReactNativeAsyncStorage) => unknown }).getReactNativePersistence;
type Auth = FirebaseAuth.Auth;
type UserCredential = FirebaseAuth.UserCredential;

// Web config for Firebase JS SDK (works in Expo Go).
// Add a Web app in Firebase Console to get your own config if needed.
const firebaseConfig = {
  apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY ?? 'AIzaSyBRpd3b7dBB1XyybBNVpPs85lLUXy7WBfE',
  authDomain: process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN ?? 'calculator0-74b81.firebaseapp.com',
  projectId: process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID ?? 'calculator0-74b81',
  storageBucket: process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET ?? 'calculator0-74b81.firebasestorage.app',
  messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID ?? '315299082291',
  appId: process.env.EXPO_PUBLIC_FIREBASE_APP_ID ?? '1:315299082291:web:default',
};

let app: FirebaseApp;
let authInstance: Auth;

if (getApps().length === 0) {
  app = initializeApp(firebaseConfig);
  authInstance = initializeAuth(app, {
    persistence: getReactNativePersistence(ReactNativeAsyncStorage) as FirebaseAuth.Persistence,
  });
} else {
  app = getApps()[0] as FirebaseApp;
  authInstance = getAuth(app);
}

/**
 * Auth wrapper that matches @react-native-firebase/auth API
 * so existing code (authService) works unchanged. Uses Firebase JS SDK
 * so the app runs in Expo Go without native modules.
 */
function auth() {
  return {
    createUserWithEmailAndPassword(email: string, password: string): Promise<UserCredential> {
      return firebaseCreateUser(authInstance, email, password);
    },
    signInWithEmailAndPassword(email: string, password: string): Promise<UserCredential> {
      return firebaseSignIn(authInstance, email, password);
    },
    signOut(): Promise<void> {
      return firebaseSignOut(authInstance);
    },
    get currentUser() {
      return authInstance.currentUser;
    },
  };
}

export { auth };

export const testFirebase = async () => {
  try {
    const user = authInstance.currentUser;
    console.log('Firebase initialized. Current user:', user?.email ?? 'None');
    return true;
  } catch (error) {
    console.error('Firebase error:', error);
    return false;
  }
};
