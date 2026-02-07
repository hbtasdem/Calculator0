import { View, TextInput, Button, StyleSheet } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { router } from 'expo-router';

export default function Login() {
  return (
    <ThemedView style={styles.container}>
        <ThemedText type="title" style={styles.title}>Login</ThemedText>

        <TextInput
            style={styles.input}
            placeholder="Username"
            placeholderTextColor="#888"
        />

        <TextInput
            style={styles.input}
            placeholder="Password"
            secureTextEntry
            placeholderTextColor="#888"
        />

        <Button
            title="Login"
            onPress={() => router.push('/(safety-tabs)/safety-plan')}
        />
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    marginBottom: 30,
    textAlign: 'center',
  },
  input: {
    height: 50,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 15,
    fontSize: 16,
    backgroundColor: '#fff',
  },
});