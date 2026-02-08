import { useState, useEffect } from 'react';
import { StyleSheet, Button, ScrollView, ActivityIndicator, View, TextInput, Alert } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { auth, db } from '@/config/firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';

const GEMINI_API_KEY = process.env.EXPO_PUBLIC_GEMINI_API_KEY || "";
const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

export default function Analyzer() {
  const [abuseAnalysis, setAbuseAnalysis] = useState('');
  const [savingsAdvice, setSavingsAdvice] = useState('');
  const [savingsPlan, setSavingsPlan] = useState<any>(null); // Store structured plan
  const [loading, setLoading] = useState(false);
  const [dataLoading, setDataLoading] = useState(true);
  const [generatingPlan, setGeneratingPlan] = useState(false);
  
  const [location, setLocation] = useState('');
  const [dependents, setDependents] = useState('');
  const [userFinanceData, setUserFinanceData] = useState<any>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const user = auth.currentUser;
        if (!user) {
          setDataLoading(false);
          return;
        }

        const docRef = doc(db, 'users', user.uid);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
          const data = docSnap.data();
          if (data.transactionData) {
            setUserFinanceData(data.transactionData);
            console.log("✅ Custom transaction data loaded");
          }
        }
      } catch (error) {
        console.error("Error fetching transaction data:", error);
      } finally {
        setDataLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const analyzeFinances = async () => {
    if (!userFinanceData) {
      Alert.alert("No Data", "No transaction data found for this user in Firestore.");
      return;
    }

    setLoading(true);
    setAbuseAnalysis('');
    setSavingsAdvice('');
    setSavingsPlan(null);

    try {
      const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

      // PROMPT 1: Abuse analysis
      const abusePrompt = `
        Analyze a transaction history for signs of financial abuse.
        Look for red flags like unusual gaps, microtransactions, or signs of an allowance.
        Consider this REAL transaction data: ${JSON.stringify(userFinanceData)}
        
        List red flags, explain the suspicion, and rate risk (Low/Medium/High).
        Format:
        Risk Level: [Level]
        Reasons for risk level:
        - [Point]
      `;

      // PROMPT 2: Savings advice with structured output
      const savingsPrompt = `
        Act as a financial safety expert. Create an Exit Strategy for ${location || 'a generic city'} with ${dependents || '0'} children.
        Target 1 month of living costs.
        
        Respond with TWO parts:
        
        PART 1 - Human readable summary:
        For [area] with [number] children, it is recommended to save: $[total]
        Breakdown:
        - Cash: $[amount]
        - Checking Account: $[amount]
        - Gift Cards: $[amount]
        
        PART 2 - JSON structure (put this at the END, after "JSON_START:"):
        JSON_START:
        {
          "categories": [
            {"name": "Emergency Cash", "location": "Hidden at home", "goalAmount": 500},
            {"name": "Personal Checking Account", "location": "Bank of America", "goalAmount": 1000},
            {"name": "Gift Cards", "location": "Walmart gift cards", "goalAmount": 300}
          ]
        }
      `;

      const abuseRes = await model.generateContent(abusePrompt);
      setAbuseAnalysis(abuseRes.response.text());

      await delay(2000);

      const savingsRes = await model.generateContent(savingsPrompt);
      const fullResponse = savingsRes.response.text();
      
      // Split response into readable part and JSON
      const parts = fullResponse.split('JSON_START:');
      setSavingsAdvice(parts[0].trim());
      
      if (parts[1]) {
        try {
          const jsonStr = parts[1].trim().replace(/```json/g, '').replace(/```/g, '');
          const parsed = JSON.parse(jsonStr);
          setSavingsPlan(parsed);
        } catch (e) {
          console.error('Failed to parse JSON from Gemini:', e);
        }
      }

    } catch (error: any) {
      console.error(error);
      setAbuseAnalysis('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const generatePlanToFirestore = async () => {
    if (!savingsPlan) {
      Alert.alert("No Plan", "Please analyze finances first to generate a savings plan.");
      return;
    }

    setGeneratingPlan(true);
    try {
      const user = auth.currentUser;
      if (!user) {
        Alert.alert("Error", "You must be logged in");
        return;
      }

      // Add unique IDs to each category
      const categoriesWithIds = savingsPlan.categories.map((cat: any) => ({
        id: Date.now().toString() + Math.random(),
        name: cat.name,
        location: cat.location || "",
        currentAmount: 0,
        goalAmount: cat.goalAmount
      }));

      // Save to Firestore
      await setDoc(doc(db, 'users', user.uid), {
        categories: categoriesWithIds,
        updatedAt: new Date().toISOString()
      }, { merge: true });

      Alert.alert(
        "Plan Generated!", 
        "Your safety plan has been created. Go to the Safety Plan tab to view it.",
        [{ text: "OK" }]
      );

    } catch (error) {
      console.error('Error generating plan:', error);
      Alert.alert('Error', 'Failed to generate plan');
    } finally {
      setGeneratingPlan(false);
    }
  };

  if (dataLoading) {
    return (
      <ThemedView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#BB86FC" />
        <ThemedText>Loading your secure data...</ThemedText>
      </ThemedView>
    );
  }

  return (
    <ThemedView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <ThemedText type="title" style={styles.title}>Financial Insights</ThemedText>
        
        <View style={styles.inputSection}>
          <ThemedText style={styles.label}>Current Location (Zip Code)</ThemedText>
          <TextInput 
            style={styles.input} 
            value={location}
            onChangeText={setLocation}
            placeholder="e.g. 78701"
            placeholderTextColor="#666"
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
            disabled={loading || !userFinanceData}
            color="#2196F3"
          />
        </View>

        {loading && <ActivityIndicator size="large" color="#BB86FC" style={styles.loader} />}

        {!userFinanceData && !loading && (
          <ThemedText style={styles.warningText}>⚠️ No transaction data linked to account.</ThemedText>
        )}

        {abuseAnalysis !== '' && (
          <View style={styles.card}>
            <ThemedText style={styles.cardTitle}>Financial Abuse Risk</ThemedText>
            <View style={styles.divider} />
            <ThemedText style={styles.resultText}>{abuseAnalysis}</ThemedText>
          </View>
        )}

        {savingsAdvice !== '' && (
          <View style={[styles.card, styles.savingsCard]}>
            <ThemedText style={styles.cardTitle}>Exit Plan Recommendations</ThemedText>
            <View style={[styles.divider, { backgroundColor: '#03DAC6' }]} />
            <ThemedText style={styles.resultText}>{savingsAdvice}</ThemedText>
            
            {savingsPlan && (
              <View style={styles.generateButtonWrapper}>
                <Button 
                  title={generatingPlan ? "Generating..." : "Generate Plan"}
                  onPress={generatePlanToFirestore}
                  disabled={generatingPlan}
                  color="#03DAC6"
                />
              </View>
            )}
          </View>
        )}
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#242e24' },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#121212' },
  scrollContent: { padding: 20, paddingBottom: 40 },
  title: { color: '#ecfad4', marginBottom: 15 },
  inputSection: {
    backgroundColor: '#141a14',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  label: { color: '#ecfad4', fontSize: 14, marginBottom: 5, fontWeight: '600' },
  input: {
    backgroundColor: '#242e24',
    color: '#FFF',
    padding: 10,
    borderRadius: 8,
    marginBottom: 15,
  },
  buttonWrapper: { marginVertical: 15, borderRadius: 8, overflow: 'hidden' },
  generateButtonWrapper: { marginTop: 15, borderRadius: 8, overflow: 'hidden' },
  loader: { marginVertical: 20 },
  warningText: { color: '#FFA000', textAlign: 'center', marginVertical: 10 },
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
  cardTitle: { fontSize: 20, fontWeight: '700', color: '#ecfad4', marginBottom: 8 },
  divider: { height: 2, backgroundColor: '#ecfad4', width: '40%', marginBottom: 15 },
  resultText: { fontSize: 15, lineHeight: 22, color: '#ebf5f3' },
});