import { View, StyleSheet } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';

export default function SafetyPlan() {
  return (
    <ThemedView style={styles.container}>
      <ThemedText type="title">Safety Plan</ThemedText>
      <ThemedText style={styles.text}>
        Your safety plan content goes here
      </ThemedText>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    marginTop: 20,
    fontSize: 16,
    textAlign: 'center',
  },
});