import * as SecureStore from 'expo-secure-store';
import { API_BASE } from '@/config/api';

export const api = {
  // Helper to get stored credentials
  getCredentials: async () => {
    const userId = await SecureStore.getItemAsync('user_id');
    const password = await SecureStore.getItemAsync('user_password');
    return { userId, password };
  },

  // Setup account (link Firebase to Nessie)
  setupAccount: async (firebaseUid: string, password: string, customerId: string) => {
    const response = await fetch(`${API_BASE}/auth/setup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        firebase_uid: firebaseUid, 
        password, 
        customer_id: customerId 
      })
    });
    return response.json();
  },

  // Sync transactions
  syncTransactions: async (customerId: string) => {
    const { userId, password } = await api.getCredentials();
    const response = await fetch(`${API_BASE}/transactions/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, password, customer_id: customerId })
    });
    return response.json();
  },

  // Get transactions
  getTransactions: async () => {
    const { userId, password } = await api.getCredentials();
    const response = await fetch(`${API_BASE}/transactions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, password })
    });
    return response.json();
  },

  // Run analysis
  runAnalysis: async () => {
    const { userId, password } = await api.getCredentials();
    const response = await fetch(`${API_BASE}/analysis/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, password })
    });
    return response.json();
  }
};