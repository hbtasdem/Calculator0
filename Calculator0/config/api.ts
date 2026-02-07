import { Platform } from 'react-native';

/**
 * Backend API base URL.
 * - Set EXPO_PUBLIC_API_URL in .env (e.g. http://192.168.1.5:5000) when using a physical device.
 * - iOS simulator: localhost works (it’s your Mac).
 * - Android emulator: 10.0.2.2 is the host machine.
 */
function getApiBase(): string {
  const env = process.env.EXPO_PUBLIC_API_URL;
  if (env) return env.replace(/\/$/, '');
  if (Platform.OS === 'android') {
    return 'http://10.0.2.2:5000';
  }
  return 'http://localhost:5000';
}

export const API_BASE = `${getApiBase()}/api`;
