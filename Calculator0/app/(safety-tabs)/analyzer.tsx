import { useState } from 'react';
import { StyleSheet, Button, ScrollView, ActivityIndicator, View } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { GoogleGenerativeAI } from '@google/generative-ai';

// Replace with your actual key or an environment variable
const GEMINI_API_KEY = "YOUR_API_KEY";

export default function Analyzer() {
  const [abuseAnalysis, setAbuseAnalysis] = useState('');
  const [savingsAdvice, setSavingsAdvice] = useState('');
  const [loading, setLoading] = useState(false);

  const transactionHistory = [
    { date: '2024-01-15', merchant: 'Grocery Store', amount: -45.32 },
    { date: '2024-01-16', merchant: 'Gas Station', amount: -52.10 },
    { date: '2024-01-17', merchant: 'Coffee Shop', amount: -6.50 },
    { date: '2024-01-18', merchant: 'Restaurant', amount: -78.25 },
  ];

  const analyzeFinances = async () => {
    setLoading(true);
    setAbuseAnalysis('');
    setSavingsAdvice('');

    try {
      const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

      const abusePrompt =  ` \
        Analyze a transaction history for signs of financial abuse.
        Look for common red flags, such as unusual gaps in spending, signs of an allowance and microtransactions,
        deliberate overdrafting, any other suspicious activity you think would signify financial abuse.
        Consider this transaction history: ${JSON.stringify(transactionHistory)} \
        List every red flag that applies, give an explanation of why it may point to financial abuse, and rate it from \
        low, medium, or high in terms of how likely it is that the activity is associated with financial abuse. \
        If there are no red flag, you can say that as well. Your response should be well-organized and easy to follow. \
        Make sure the bullet points are well-summarized, I don't want a wall of text. Give the overall risk level of the account at the top. \
        The response should have the format \
        Risk Level: High, Medium, or Low \n\
        Reasons for risk level: \n...
      `;

      const savingsPrompt = `\
        Provide a concise guide on how much money a person should save before moving to a new location. Include factors like deposits, first month's rent, and emergency buffers.`;

      // Parallel execution for better performance during demos
      const [abuseRes, savingsRes] = await Promise.all([
        model.generateContent(abusePrompt),
        model.generateContent(savingsPrompt)
      ]);

      setAbuseAnalysis(abuseRes.response.text());
      setSavingsAdvice(savingsRes.response.text());
    } catch (error) {
      setAbuseAnalysis('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemedView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <ThemedText type="title" style={styles.title}>Financial Insights</ThemedText>
        
        <View style={styles.buttonWrapper}>
          <Button 
            title="Analyze Finances with Gemini" 
            onPress={analyzeFinances}
            disabled={loading}
            color="#2196F3" // Nice blue button
          />
        </View>

        {loading && <ActivityIndicator size="large" color="#BB86FC" style={styles.loader} />}

        {/* Box 1: Financial Abuse Risk */}
        {abuseAnalysis !== '' && (
          <View style={styles.card}>
            <ThemedText style={styles.cardTitle}>Financial Abuse Risk</ThemedText>
            <View style={styles.divider} />
            <ThemedText style={styles.resultText}>{abuseAnalysis}</ThemedText>
          </View>
        )}

        {/* Box 2: Savings Advice */}
        {savingsAdvice !== '' && (
          <View style={[styles.card, styles.savingsCard]}>
            <ThemedText style={styles.cardTitle}>Emergency Moving Fund</ThemedText>
            <View style={[styles.divider, { backgroundColor: '#03DAC6' }]} />
            <ThemedText style={styles.resultText}>{savingsAdvice}</ThemedText>
          </View>
        )}
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212', // Dark background
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 10,
  },
  buttonWrapper: {
    marginVertical: 15,
    borderRadius: 8,
    overflow: 'hidden',
  },
  loader: {
    marginVertical: 20,
  },
  card: {
    backgroundColor: '#1E1E1E', // Dark grey card
    padding: 20,
    borderRadius: 12,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#333333',
    // Shadow for iOS
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    // Elevation for Android
    elevation: 6,
  },
  savingsCard: {
    borderColor: '#018786', // Subtle teal/blue border for the second box
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#BB86FC', // Soft purple/blue title
    marginBottom: 8,
  },
  divider: {
    height: 2,
    backgroundColor: '#BB86FC',
    width: '40%',
    marginBottom: 15,
    borderRadius: 1,
  },
  resultText: {
    fontSize: 15,
    lineHeight: 22,
    color: '#E0E0E0', // Light grey text for readability
  },
});