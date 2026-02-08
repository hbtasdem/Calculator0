import { useState, useEffect } from 'react';
import { ScrollView, StyleSheet, TextInput, Button, Pressable, View, KeyboardAvoidingView, Platform, Alert,ActivityIndicator } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { auth, db } from '@/config/firebase';
import { doc, setDoc, getDoc } from 'firebase/firestore';

type Category = {
  id: string;
  name: string;
  location: string;
  currentAmount: number;
  goalAmount: number;
};

export default function SafetyPlan() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [customAmountId, setCustomAmountId] = useState<string | null>(null);
  const [customAmount, setCustomAmount] = useState('');
  const [selectedCategoryType, setSelectedCategoryType] = useState('Cash');
  const [customCategoryName, setCustomCategoryName] = useState('');
  const [newCategory, setNewCategory] = useState({ location: '', goalAmount: '' });
  const [editForm, setEditForm] = useState({ name: '', location: '', goalAmount: '' });

  const categoryOptions = ['Cash', 'Personal Checking Account', 'Gift Cards', 'Custom'];

  // ============================================================================
  // FIREBASE DATA PERSISTENCE
  // ============================================================================

  useEffect(() => {
    // Listen for auth state to handle the "blank screen" race condition
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        console.log("✅ User detected:", user.uid);
        loadCategories(user.uid);
      } else {
        console.log("⚠️ No user detected");
        setLoading(false);
      }
    });
    return unsubscribe;
  }, []);

  const loadCategories = async (userId: string) => {
    try {
      const docRef = doc(db, 'users', userId);
      const docSnap = await getDoc(docRef);

      if (docSnap.exists()) {
        const data = docSnap.data();
        if (data.categories) {
          setCategories(data.categories);
        }
      }
    } catch (error) {
      console.error('Error loading categories:', error);
      Alert.alert('Error', 'Failed to load your savings plan.');
    } finally {
      setLoading(false);
    }
  };

  const saveCategoriesToFirestore = async (updatedCategories: Category[]) => {
    try {
      const user = auth.currentUser;
      if (!user) return;

      await setDoc(doc(db, 'users', user.uid), {
        categories: updatedCategories,
        updatedAt: new Date().toISOString()
      }, { merge: true });
    } catch (error) {
      console.error('Error saving to Firestore:', error);
      Alert.alert('Cloud Sync Error', 'Changes saved locally but failed to sync.');
    }
  };

  // ============================================================================
  // LOGIC HANDLERS
  // ============================================================================

  const addCategory = async () => {
    const categoryName = selectedCategoryType === 'Custom' ? customCategoryName : selectedCategoryType;
    if (categoryName && newCategory.goalAmount) {
      const category: Category = {
        id: Date.now().toString(),
        name: categoryName,
        location: newCategory.location,
        currentAmount: 0,
        goalAmount: parseFloat(newCategory.goalAmount),
      };
      const updated = [...categories, category];
      setCategories(updated);
      await saveCategoriesToFirestore(updated);
      
      setNewCategory({ location: '', goalAmount: '' });
      setSelectedCategoryType('Cash');
      setCustomCategoryName('');
      setShowAddForm(false);
    }
  };

  const saveEdit = async (id: string) => {
    const updated = categories.map(cat =>
      cat.id === id ? { ...cat, name: editForm.name, location: editForm.location, goalAmount: parseFloat(editForm.goalAmount) } : cat
    );
    setCategories(updated);
    await saveCategoriesToFirestore(updated);
    setEditingId(null);
  };

  const deleteCategory = async (id: string) => {
    const updated = categories.filter(cat => cat.id !== id);
    setCategories(updated);
    await saveCategoriesToFirestore(updated);
  };

  const addMoney = async (id: string, amount: number) => {
    const updated = categories.map(cat => 
      cat.id === id ? { ...cat, currentAmount: cat.currentAmount + amount } : cat
    );
    setCategories(updated);
    await saveCategoriesToFirestore(updated);
  };

  const startEditing = (category: Category) => {
    setEditingId(category.id);
    setEditForm({ name: category.name, location: category.location, goalAmount: category.goalAmount.toString() });
  };

  const getProgress = (current: number, goal: number) => Math.min((current / goal) * 100, 100);

  // ============================================================================
  // RENDER
  // ============================================================================

  if (loading) {
    return (
      <ThemedView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0a7ea4" />
        <ThemedText style={{ marginTop: 10 }}>Syncing Safety Plan...</ThemedText>
      </ThemedView>
    );
  }

  return (
    <KeyboardAvoidingView 
      style={{ flex: 1, backgroundColor: '#121212' }} 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView 
        style={styles.container}
        contentContainerStyle={{ paddingBottom: 40 }}
        keyboardShouldPersistTaps="handled"
      >
        <ThemedView style={styles.content}>
          <ThemedText type="title" style={styles.title}>Safety Plan</ThemedText>
          
          <ThemedText style={styles.description}>
            Track your progress toward financial independence in secure, private locations.
          </ThemedText>

          {categories.length === 0 && !showAddForm && (
            <ThemedView style={styles.emptyState}>
                <ThemedText style={styles.emptyText}>No categories yet. Click below to start your plan.</ThemedText>
            </ThemedView>
          )}

          {categories.map((category) => (
            <ThemedView key={category.id} style={styles.categoryCard}>
              {editingId === category.id ? (
                <View>
                  <TextInput style={styles.input} placeholder="Name" value={editForm.name} onChangeText={(t) => setEditForm({...editForm, name: t})} placeholderTextColor="#888" />
                  <TextInput style={styles.input} placeholder="Location" value={editForm.location} onChangeText={(t) => setEditForm({...editForm, location: t})} placeholderTextColor="#888" />
                  <TextInput style={styles.input} placeholder="Goal" keyboardType="numeric" value={editForm.goalAmount} onChangeText={(t) => setEditForm({...editForm, goalAmount: t})} placeholderTextColor="#888" />
                  <View style={styles.editButtons}>
                    <Button title="Save" onPress={() => saveEdit(category.id)} />
                    <Button title="Delete" onPress={() => deleteCategory(category.id)} color="#dc2626" />
                    <Button title="Cancel" onPress={() => setEditingId(null)} color="#888" />
                  </View>
                </View>
              ) : (
                <View>
                  <View style={styles.categoryHeader}>
                    <View style={{ flex: 1 }}>
                      <ThemedText type="defaultSemiBold" style={styles.categoryName}>{category.name}</ThemedText>
                      <ThemedText style={styles.locationText}>{category.location}</ThemedText>
                    </View>
                    <Pressable style={styles.editBtn} onPress={() => startEditing(category)}>
                      <ThemedText style={styles.editBtnText}>Edit</ThemedText>
                    </Pressable>
                  </View>

                  <ThemedText style={styles.amountText}>${category.currentAmount.toFixed(2)} / ${category.goalAmount.toFixed(2)}</ThemedText>
                  
                  <View style={styles.progressBg}><View style={[styles.progressFill, { width: `${getProgress(category.currentAmount, category.goalAmount)}%` }]} /></View>
                  
                  <View style={styles.quickAddRow}>
                    <Pressable style={styles.quickBtn} onPress={() => addMoney(category.id, 10)}><ThemedText style={styles.quickBtnText}>+$10</ThemedText></Pressable>
                    <Pressable style={styles.quickBtn} onPress={() => addMoney(category.id, 50)}><ThemedText style={styles.quickBtnText}>+$50</ThemedText></Pressable>
                    <Pressable style={styles.quickBtn} onPress={() => setCustomAmountId(category.id)}><ThemedText style={styles.quickBtnText}>Custom</ThemedText></Pressable>
                  </View>

                  {customAmountId === category.id && (
                    <View style={styles.customInputRow}>
                      <TextInput style={styles.customInput} keyboardType="numeric" value={customAmount} onChangeText={setCustomAmount} autoFocus placeholder="0.00" placeholderTextColor="#888" />
                      <Button title="Add" onPress={async () => {
                        const amt = parseFloat(customAmount);
                        if (!isNaN(amt)) await addMoney(category.id, amt);
                        setCustomAmount(''); setCustomAmountId(null);
                      }} />
                    </View>
                  )}
                </View>
              )}
            </ThemedView>
          ))}

          {!showAddForm ? (
            <Pressable style={styles.addButton} onPress={() => setShowAddForm(true)}>
              <ThemedText style={styles.addButtonText}>+ Add New Category</ThemedText>
            </Pressable>
          ) : (
            <ThemedView style={styles.addForm}>
              <View style={styles.typeRow}>
                {categoryOptions.map(opt => (
                  <Pressable key={opt} style={[styles.typeBtn, selectedCategoryType === opt && styles.typeBtnActive]} onPress={() => setSelectedCategoryType(opt)}>
                    <ThemedText style={selectedCategoryType === opt ? {color: '#fff'} : {}}>{opt}</ThemedText>
                  </Pressable>
                ))}
              </View>
              {selectedCategoryType === 'Custom' && <TextInput style={styles.input} placeholder="Custom Name" value={customCategoryName} onChangeText={setCustomCategoryName} placeholderTextColor="#888" />}
              <TextInput style={styles.input} placeholder="Storage Location" value={newCategory.location} onChangeText={t => setNewCategory({...newCategory, location: t})} placeholderTextColor="#888" />
              <TextInput style={styles.input} placeholder="Goal Amount" keyboardType="numeric" value={newCategory.goalAmount} onChangeText={t => setNewCategory({...newCategory, goalAmount: t})} placeholderTextColor="#888" />
              <View style={styles.editButtons}>
                <Button title="Add" onPress={addCategory} />
                <Button title="Cancel" onPress={() => setShowAddForm(false)} color="#888" />
              </View>
            </ThemedView>
          )}
        </ThemedView>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#121212' },
  content: { padding: 20 },
  title: { marginBottom: 10, color: '#fff' },
  description: { marginBottom: 20, fontSize: 14, color: '#ccc' },
  emptyState: { padding: 40, alignItems: 'center' },
  emptyText: { color: '#666', textAlign: 'center' },
  categoryCard: { backgroundColor: '#1E1E1E', padding: 15, borderRadius: 12, marginBottom: 15, borderWidth: 1, borderColor: '#333' },
  categoryHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 10 },
  categoryName: { fontSize: 18, color: '#BB86FC' },
  locationText: { fontSize: 12, color: '#888' },
  editBtn: { backgroundColor: '#333', padding: 6, borderRadius: 4 },
  editBtnText: { color: '#fff', fontSize: 12 },
  amountText: { fontSize: 16, fontWeight: 'bold', marginVertical: 8, color: '#fff' },
  progressBg: { height: 10, backgroundColor: '#333', borderRadius: 5, overflow: 'hidden' },
  progressFill: { height: '100%', backgroundColor: '#03DAC6' },
  quickAddRow: { flexDirection: 'row', gap: 10, marginTop: 15 },
  quickBtn: { flex: 1, backgroundColor: '#0a7ea4', padding: 8, borderRadius: 6, alignItems: 'center' },
  quickBtnText: { color: '#fff', fontSize: 12, fontWeight: 'bold' },
  customInputRow: { flexDirection: 'row', marginTop: 10, gap: 10 },
  customInput: { flex: 1, backgroundColor: '#2A2A2A', color: '#fff', padding: 8, borderRadius: 6, borderWidth: 1, borderColor: '#444' },
  addButton: { backgroundColor: '#0a7ea4', padding: 15, borderRadius: 10, alignItems: 'center', marginTop: 10 },
  addButtonText: { color: '#fff', fontWeight: 'bold' },
  addForm: { backgroundColor: '#1E1E1E', padding: 15, borderRadius: 12, borderWidth: 1, borderColor: '#333' },
  input: { backgroundColor: '#2A2A2A', color: '#fff', padding: 10, borderRadius: 6, marginBottom: 10, borderWidth: 1, borderColor: '#444' },
  typeRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 15 },
  typeBtn: { padding: 8, borderRadius: 6, borderWidth: 1, borderColor: '#444', backgroundColor: '#2A2A2A' },
  typeBtnActive: { backgroundColor: '#0a7ea4', borderColor: '#0a7ea4' },
  editButtons: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 10 }
});
