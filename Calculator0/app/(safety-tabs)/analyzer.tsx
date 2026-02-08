import { useState } from 'react';
import { StyleSheet, Button, ScrollView, ActivityIndicator, View, TextInput } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { GoogleGenerativeAI } from '@google/generative-ai';

const GEMINI_API_KEY = "API_KEY";

export default function Analyzer() {
  const [abuseAnalysis, setAbuseAnalysis] = useState('');
  const [savingsAdvice, setSavingsAdvice] = useState('');
  const [loading, setLoading] = useState(false);
  
  // User Inputs for Context
  const [location, setLocation] = useState('');
  const [dependents, setDependents] = useState('');

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

      const abusePrompt = `
        Analyze a transaction history for signs of financial abuse.
        Look for common red flags, such as unusual gaps in spending, signs of an allowance and microtransactions,
        deliberate overdrafting, any other suspicious activity you think would signify financial abuse.
        Consider this transaction history: ${JSON.stringify(transactionHistory)}
        List every red flag that applies, give an explanation of why it may point to financial abuse, and rate it from
        low, medium, or high in terms of how likely it is that the activity is associated with financial abuse.
        If there are no red flag, you can say that as well. Your response should be well-organized and easy to follow.
        Make sure the bullet points are well-summarized, I don't want a wall of text. Give the overall risk level of the account at the top.
        The response should have the format

        Risk Level: High, Medium, or Low

        Reasons for risk level:
        Well-summarized risk 1
        well-summarized risk 2...
      `;

      const savingsPrompt = `
        Act as a financial safety expert. Create a 'Financial Exit Strategy' for a user in ${location || 'a generic city'} with ${dependents || '0'} children.
        Provide a total target amount to save based on local cost of living for at least a month of living. Break down the money saved into categories of:
        Required: Cash (untraceable), Required: Personal Checking (private account), Optional: Gift Cards Creative Saving Methods: 3-4 discreet ways to save
        (e.g., cashback at registers). In the response, keep bullet points summarized. No walls of text.
        Format the response as:

        For (area based on zip code or generic USA city) and (number of children) children, and for at least one month of living costs, it is reccomended to save:
        $(amount of money)

        The breakdown of funds should be:

        Cash (Untraceable):  $
        Personal Checking (private account): $
        
        And creative saving methods:
        Gift Cards: $
        (specify other methods here too): $
      `;

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
        
        {/* User Input Section */}
        <View style={styles.inputSection}>
          <ThemedText style={styles.label}>Current Location (Zip Code)</ThemedText>
          <TextInput 
            style={styles.input} 
            value={location}
            onChangeText={setLocation}
          />
          <ThemedText style={styles.label}>Number of Dependents</ThemedText>
          <TextInput 
            style={styles.input} 
            placeholder="0" 
            placeholderTextColor="#666"
            keyboardType="numeric"
            value={dependents}
            onChangeText={setDependents}
          />
        </View>

        <View style={styles.buttonWrapper}>
          <Button 
            title="Analyze Finances with Gemini" 
            onPress={analyzeFinances}
            disabled={loading}
            color="#2196F3"
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

        {/* Box 2: Exit Plan */}
        {savingsAdvice !== '' && (
          <View style={[styles.card, styles.savingsCard]}>
            <ThemedText style={styles.cardTitle}>Exit Plan</ThemedText>
            <View style={[styles.divider, { backgroundColor: '#03DAC6' }]} />
            <ThemedText style={styles.resultText}>{savingsAdvice}</ThemedText>
          </View>
        )}
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#121212' },
  scrollContent: { padding: 20, paddingBottom: 40 },
  title: { color: '#FFFFFF', marginBottom: 15 },
  inputSection: {
    backgroundColor: '#1E1E1E',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  label: { color: '#BB86FC', fontSize: 14, marginBottom: 5, fontWeight: '600' },
  input: {
    backgroundColor: '#2A2A2A',
    color: '#FFF',
    padding: 10,
    borderRadius: 8,
    marginBottom: 15,
  },
  buttonWrapper: { marginVertical: 15, borderRadius: 8, overflow: 'hidden' },
  loader: { marginVertical: 20 },
  card: {
    backgroundColor: '#1E1E1E',
    padding: 20,
    borderRadius: 12,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#333333',
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  savingsCard: { borderColor: '#018786' },
  cardTitle: { fontSize: 20, fontWeight: '700', color: '#BB86FC', marginBottom: 8 },
  divider: { height: 2, backgroundColor: '#BB86FC', width: '40%', marginBottom: 15 },
  resultText: { fontSize: 15, lineHeight: 22, color: '#E0E0E0' },
});