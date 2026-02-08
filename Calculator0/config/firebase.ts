import { initializeApp, getApp, getApps } from "firebase/app";
import {
    initializeAuth,
    getReactNativePersistence,
    getAuth
} from "firebase/auth";
import AsyncStorage from "@react-native-async-storage/async-storage";

const firebaseConfig = {
    apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY,
    authDomain: process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN,
    projectId: process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID,
    storageBucket: process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.EXPO_PUBLIC_FIREBASE_APP_ID
};

// 1. Initialize Firebase App (checks if already initialized)
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

// 2. Initialize Auth with Persistence safely
// We use a try/catch or a singleton check to prevent the "Auth already initialized" error
let auth;

try {
    auth = initializeAuth(app, {
        persistence: getReactNativePersistence(AsyncStorage),
    });
} catch (e) {
    // If initializeAuth fails because it's already been called, 
    // we just get the existing instance
    auth = getAuth(app);
}

export { auth };
