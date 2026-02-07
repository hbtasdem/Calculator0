import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { useEffect, useState } from 'react';
import { router } from 'expo-router';
import { authService } from '@/services/authService';

/**
 * Entry screen: redirects to login, biometric gate, or main app
 * based on auth state and Face ID preference.
 */
export default function IndexScreen() {
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function run() {
      const signedIn = await authService.isSignedIn();
      if (cancelled) return;

      if (!signedIn) {
        router.replace('/login');
        return;
      }

      const biometricsEnabled = await authService.isBiometricsEnabled();
      if (cancelled) return;

      if (biometricsEnabled) {
        router.replace('/biometric-gate');
      } else {
        router.replace('/(tabs)');
      }
    }

    run().finally(() => {
      if (!cancelled) setChecking(false);
    });

    return () => {
      cancelled = true;
    };
  }, []);

  if (!checking) return null;

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#0ea5e9" />
      <Text style={styles.text}>Loading…</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0f172a',
  },
  text: {
    marginTop: 12,
    fontSize: 16,
    color: '#94a3b8',
  },
});
