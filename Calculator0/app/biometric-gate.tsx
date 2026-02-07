import { View, Text, TouchableOpacity, StyleSheet, Alert, Platform } from 'react-native';
import { useState } from 'react';
import { router } from 'expo-router';
import { authService } from '@/services/authService';
import { IconSymbol } from '@/components/ui/icon-symbol';

const biometricLabel = Platform.OS === 'ios' ? 'Face ID' : 'fingerprint';

export default function BiometricGateScreen() {
  const [loading, setLoading] = useState(false);

  const handleUnlock = async () => {
    setLoading(true);
    try {
      const success = await authService.authenticateWithBiometrics(
        `Unlock 0 with ${biometricLabel}`
      );
      if (success) {
        router.replace('/(tabs)');
      }
    } catch (e) {
      Alert.alert('Error', 'Authentication failed. Try again or use password.');
    } finally {
      setLoading(false);
    }
  };

  const handleUsePassword = () => {
    router.replace('/login');
  };

  return (
    <View style={styles.container}>
      <View style={styles.iconWrap}>
        <IconSymbol name="faceid" size={64} color="#e2e8f0" />
      </View>
      <Text style={styles.title}>Unlock 0</Text>
      <Text style={styles.subtitle}>
        Use {biometricLabel} to open the app
      </Text>

      <TouchableOpacity
        style={[styles.primaryButton, loading && styles.buttonDisabled]}
        onPress={handleUnlock}
        disabled={loading}
      >
        <Text style={styles.primaryButtonText}>
          {loading ? 'Checking…' : `Unlock with ${biometricLabel}`}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.secondaryButton}
        onPress={handleUsePassword}
        disabled={loading}
      >
        <Text style={styles.secondaryButtonText}>Use password instead</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  iconWrap: {
    marginBottom: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    color: '#f8fafc',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#94a3b8',
    marginBottom: 32,
    textAlign: 'center',
  },
  primaryButton: {
    backgroundColor: '#0ea5e9',
    paddingVertical: 14,
    paddingHorizontal: 28,
    borderRadius: 12,
    minWidth: 260,
    alignItems: 'center',
    marginBottom: 12,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 17,
    fontWeight: '600',
  },
  secondaryButton: {
    paddingVertical: 14,
    paddingHorizontal: 28,
    minWidth: 260,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: '#94a3b8',
    fontSize: 16,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
});
