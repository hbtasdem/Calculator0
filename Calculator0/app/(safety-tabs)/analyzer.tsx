import { useState } from 'react';
import { StyleSheet, Button, ScrollView, ActivityIndicator } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { GoogleGenerativeAI } from '@google/generative-ai';

export default function Analyzer() {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  // Mock transaction data
  const transactionHistory = [
    { date: '2024-01-15', merchant: 'Grocery Store', amount: -45.32 },
    { date: '2024-01-16', merchant: 'Gas Station', amount: -52.10 },
    { date: '2024-01-17', merchant: 'Coffee Shop', amount: -6.50 },
    { date: '2024-01-18', merchant: 'Restaurant', amount: -78.25 },
  ];

  const analyzeWithGemini = async () => {
    setLoading(true);
    setResult('');

    try {
      // Initialize Gemini
      const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

      // Create prompt with transaction data
      const prompt = ` \
        Analyze a transaction history for signs of financial abuse.
        Look for common red flags, such as unusual gaps in spending, signs of an allowance and microtransactions,
        deliberate overdrafting, any other suspicious activity. 
        Consider this transaction history: ${JSON.stringify(transactionHistory)} \
        List every red flag, give an explanation of why it may point to financial abuse, and rate it from \
        low, medium, or high in terms of how likely it is that the activity is associated with financial abuse. \
        If there are no red flag, you can say that as well. Your response should be well-organized and easy to follow.
      `;

      // Generate response
      const response = await model.generateContent(prompt);
      const text = response.response.text();
      
      setResult(text);
    } catch (error) {
      setResult('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemedView style={styles.container}>
      <ThemedText type="title">Analyzer</ThemedText>
      
      <ThemedView style={styles.buttonContainer}>
        <Button 
          title="Analyze with Gemini" 
          onPress={analyzeWithGemini}
          disabled={loading}
        />
      </ThemedView>

      {loading && <ActivityIndicator size="large" style={styles.loader} />}

      {result !== '' && (
        <ScrollView style={styles.resultContainer}>
          <ThemedText style={styles.resultText}>{result}</ThemedText>
        </ScrollView>
      )}
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  buttonContainer: {
    marginTop: 20,
    marginBottom: 20,
  },
  loader: {
    marginTop: 20,
  },
  resultContainer: {
    flex: 1,
    marginTop: 10,
    padding: 10,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
  },
  resultText: {
    fontSize: 14,
  },
});