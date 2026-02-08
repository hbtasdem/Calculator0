import { useState, useEffect } from 'react';
import { StyleSheet, Button, ScrollView, ActivityIndicator, View, TextInput, Alert } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { auth, db } from '@/config/firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import * as DocumentPicker from 'expo-document-picker';

const GEMINI_API_KEY = process.env.EXPO_PUBLIC_GEMINI_API_KEY || "";
const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

export default function Analyzer() {
  const [abuseAnalysis, setAbuseAnalysis] = useState('');
  const [savingsAdvice, setSavingsAdvice] = useState('');
  const [savingsPlan, setSavingsPlan] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [dataLoading, setDataLoading] = useState(true);
  const [generatingPlan, setGeneratingPlan] = useState(false);
  const [uploadingCsv, setUploadingCsv] = useState(false);
  
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
            console.log("✅ Transaction data loaded");
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

  const handleCsvUpload = async () => {
    setUploadingCsv(true);
    try {
      const result = await DocumentPicker.getDocumentAsync({ 
        type: ['text/csv', 'text/comma-separated-values', 'application/csv']
      });
      
      if (result.canceled) {
        setUploadingCsv(false);
        return;
      }

      const response = await fetch(result.assets[0].uri);
      const csvText = await response.text();
      
      // Parse CSV - assumes format: Transaction Date,Post Date,Card No.,Description,Category,Debit,Credit
      const lines = csvText.trim().split('\n');
      const headers = lines[0].split(',');
      
      const transactions: any[] = [];
      
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        if (values.length < 6) continue; // Skip invalid lines
        
        const transaction = {
          date: values[0]?.trim(),
          description: values[3]?.trim(),
          category: values[4]?.trim(),
          debit: values[5]?.trim() ? parseFloat(values[5].trim()) : 0,
          credit: values[6]?.trim() ? parseFloat(values[6].trim()) : 0,
        };
        
        // Calculate amount (positive for expenses, negative for income)
        transaction.amount = transaction.debit > 0 ? transaction.debit : -transaction.credit;
        
        transactions.push(transaction);
      }
      
      if (transactions.length === 0) {
        Alert.alert('Error', 'No valid transactions found in CSV');
        setUploadingCsv(false);
        return;
      }

      // Save to Firestore
      const user = auth.currentUser;
      if (!user) {
        Alert.alert('Error', 'You must be logged in');
        setUploadingCsv(false);
        return;
      }
      
      await setDoc(doc(db, 'users', user.uid), {
        transactionData: transactions,
        updatedAt: new Date().toISOString()
      }, { merge: true });
      
      setUserFinanceData(transactions);
      Alert.alert('Success', `Uploaded ${transactions.length} transactions`);
      
    } catch (error: any) {
      console.error('CSV upload error:', error);
      Alert.alert('Error', 'Failed to parse CSV: ' + error.message);
    } finally {
      setUploadingCsv(false);
    }
  };

  const analyzeFinances = async () => {
    if (!userFinanceData) {
      Alert.alert("No Data", "Please upload transaction data first.");
      return;
    }

    setLoading(true);
    setAbuseAnalysis('');
    setSavingsAdvice('');
    setSavingsPlan(null);

    try {
      const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

      // PROMPT 1: Abuse analysis using actual transaction data
      const abusePrompt = `
        You are a financial abuse detection expert. Analyze this transaction history for signs of financial abuse or control.
        
        Transaction Data:
        ${JSON.stringify(userFinanceData, null, 2)}
        
        Look for red flags such as:
        - Unusual spending patterns or restrictions
        - Frequent small withdrawals (possible allowance system)
        - Lack of access to certain merchants or categories
        - Suspicious gaps in transaction history
        - Evidence of financial monitoring or control
        - Microtransactions that could indicate limited access
        
        Provide:
        1. Risk Level (Low/Medium/High)
        2. Specific red flags found in the data
        3. Brief explanation of concerns
        
        Format your response clearly with sections.
      `;

      // PROMPT 2: Savings advice with structured output
      const savingsPrompt = `
        Act as a financial safety expert. Create an Exit Strategy savings plan for someone in ${location || 'a mid-sized US city'} with ${dependents || '0'} children.
        
        Target: 1 month of living expenses for emergency exit.
        
        Provide TWO parts in your response:
        
        PART 1 - Human-readable summary:
        Recommend total savings amount and breakdown by category (Cash, Checking Account, Gift Cards).
        Explain why each category is important for financial safety.
        
        PART 2 - Structured plan (put this at the END after "JSON_START:"):
        JSON_START:
        {
          "categories": [
            {"name": "Emergency Cash", "location": "Hidden at home", "goalAmount": 500},
            {"name": "Personal Checking Account", "location": "Separate bank", "goalAmount": 1500},
            {"name": "Gift Cards", "location": "Grocery/gas cards", "goalAmount": 300}
          ]
        }
        
        Adjust amounts based on location and dependents provided.
      `;

      // Execute prompts sequentially
      console.log('Analyzing for financial abuse...');
      const abuseRes = await model.generateContent(abusePrompt);
      setAbuseAnalysis(abuseRes.response.text());

      await delay(2000);

      console.log('Generating savings recommendations...');
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
          console.log('Savings plan parsed successfully');
        } catch (e) {
          console.error('Failed to parse JSON from Gemini:', e);
        }
      }

    } catch (error: any) {
      console.error('Analysis error:', error);
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
        
        {/* Upload Section */}
        <View style={styles.uploadSection}>
          <ThemedText style={styles.sectionTitle}>Step 1: Upload Transaction Data</ThemedText>
          
          <View style={styles.buttonWrapper}>
            <Button 
              title={uploadingCsv ? "Uploading..." : "Upload CSV File"} 
              onPress={handleCsvUpload}
              disabled={uploadingCsv}
              color="#03DAC6"
            />
          </View>
          
          {userFinanceData && (
            <ThemedText style={styles.successText}>
              ✅ {userFinanceData.length} transactions loaded
            </ThemedText>
          )}
        </View>

        {/* Analysis Section */}
        <View style={styles.inputSection}>
          <ThemedText style={styles.sectionTitle}>Step 2: Provide Context</ThemedText>
          
          <ThemedText style={styles.label}>Current Location (City or Zip)</ThemedText>
          <TextInput 
            style={styles.input} 
            value={location}
            onChangeText={setLocation}
            placeholder="e.g. Austin, TX or 78701"
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
            title="Analyze with Gemini" 
            onPress={analyzeFinances}
            disabled={loading || !userFinanceData}
            color="#2196F3"
          />
        </View>

        {loading && <ActivityIndicator size="large" color="#BB86FC" style={styles.loader} />}

        {!userFinanceData && !loading && (
          <ThemedText style={styles.warningText}>
            ⚠️ Upload transaction data to begin analysis
          </ThemedText>
        )}

        {/* Results */}
        {abuseAnalysis !== '' && (
          <View style={styles.card}>
            <ThemedText style={styles.cardTitle}>🔍 Financial Abuse Risk Assessment</ThemedText>
            <View style={styles.divider} />
            <ThemedText style={styles.resultText}>{abuseAnalysis}</ThemedText>
          </View>
        )}

        {savingsAdvice !== '' && (
          <View style={[styles.card, styles.savingsCard]}>
            <ThemedText style={styles.cardTitle}>💰 Exit Strategy Recommendations</ThemedText>
            <View style={[styles.divider, { backgroundColor: '#03DAC6' }]} />
            <ThemedText style={styles.resultText}>{savingsAdvice}</ThemedText>
            
            {savingsPlan && (
              <View style={styles.generateButtonWrapper}>
                <Button 
                  title={generatingPlan ? "Generating..." : "Generate Safety Plan"}
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
    marginBottom: 10,
  },
  buttonWrapper: { marginVertical: 8, borderRadius: 8, overflow: 'hidden' },
  generateButtonWrapper: { marginTop: 15, borderRadius: 8, overflow: 'hidden' },
  loader: { marginVertical: 20 },
  successText: { color: '#03DAC6', textAlign: 'center', marginTop: 10, fontSize: 14 },
  warningText: { color: '#FFA000', textAlign: 'center', marginVertical: 15, fontSize: 14 },
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