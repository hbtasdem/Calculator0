import { useState } from 'react';
import { ScrollView, StyleSheet, TextInput, Button, Pressable, View, KeyboardAvoidingView, Platform, Alert } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';

type Category = {
  id: string;
  name: string;
  location: string;
  currentAmount: number;
  goalAmount: number;
};

export default function SafetyPlan() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [customAmountId, setCustomAmountId] = useState<string | null>(null);
  const [customAmount, setCustomAmount] = useState('');
  const [selectedCategoryType, setSelectedCategoryType] = useState('Cash');
  const [customCategoryName, setCustomCategoryName] = useState('');
  const [newCategory, setNewCategory] = useState({ location: '', goalAmount: '' });
  const [editForm, setEditForm] = useState({ name: '', location: '', goalAmount: '' });

  const categoryOptions = ['Cash', 'Personal Checking Account', 'Gift Cards', 'Custom'];

  const addCategory = () => {
    const categoryName = selectedCategoryType === 'Custom' ? customCategoryName : selectedCategoryType;

    if (categoryName && newCategory.goalAmount) {
      const category: Category = {
        id: Date.now().toString(),
        name: categoryName,
        location: newCategory.location,
        currentAmount: 0,
        goalAmount: parseFloat(newCategory.goalAmount),
      };
      setCategories([...categories, category]);
      setNewCategory({ location: '', goalAmount: '' });
      setSelectedCategoryType('Cash');
      setCustomCategoryName('');
      setShowAddForm(false);
    }
  };

  const startEditing = (category: Category) => {
    setEditingId(category.id);
    setEditForm({
      name: category.name,
      location: category.location,
      goalAmount: category.goalAmount.toString(),
    });
  };

  const saveEdit = (id: string) => {
    setCategories(categories.map(cat =>
      cat.id === id
        ? {
            ...cat,
            name: editForm.name,
            location: editForm.location,
            goalAmount: parseFloat(editForm.goalAmount),
          }
        : cat
    ));
    setEditingId(null);
  };

  const cancelEdit = () => {
    setEditingId(null);
  };

  const deleteCategory = (id: string) => {
    setCategories(categories.filter(cat => cat.id !== id));
  };

  const addMoney = (id: string, amount: number) => {
    setCategories(categories.map(cat => 
      cat.id === id 
        ? { ...cat, currentAmount: cat.currentAmount + amount }
        : cat
    ));
  };

  const addCustomAmount = (id: string) => {
    const amount = parseFloat(customAmount);
    if (!isNaN(amount) && amount > 0) {
      addMoney(id, amount);
      setCustomAmount('');
      setCustomAmountId(null);
    }
  };

  const subtractCustomAmount = (id: string) => {
    const amount = parseFloat(customAmount);
    if (!isNaN(amount) && amount > 0) {
      addMoney(id, -amount); // Negative amount to subtract
      setCustomAmount('');
      setCustomAmountId(null);
    }
  };

  const getProgress = (current: number, goal: number) => {
    return Math.min((current / goal) * 100, 100);
  };

  return (
    <KeyboardAvoidingView 
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView 
        style={styles.container}
        keyboardShouldPersistTaps="handled"
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        <ThemedView style={styles.content}>
          <ThemedText type="title" style={styles.title}>Safety Plan</ThemedText>
          
          <ThemedText style={styles.description}>
            Building financial independence is a crucial step in creating a safe exit strategy. 
            Track your progress toward financial goals in secure, private locations.
          </ThemedText>

          <ThemedView style={styles.strategiesBox}>
            <ThemedText style={styles.aiNote}>
              For personalized recommendations on building your plan, visit the Analyzer tool
            </ThemedText>
          </ThemedView>

          <ThemedText type="subtitle" style={styles.categoriesTitle}>Your Savings Categories</ThemedText>

          {categories.map((category) => (
            <ThemedView key={category.id} style={styles.categoryCard}>
              {editingId === category.id ? (
                // Edit Mode
                <View>
                  <TextInput
                    style={styles.input}
                    placeholder="Category name"
                    placeholderTextColor="#888"
                    value={editForm.name}
                    onChangeText={(text) => setEditForm({...editForm, name: text})}
                  />
                  <TextInput
                    style={styles.input}
                    placeholder="Location"
                    placeholderTextColor="#888"
                    value={editForm.location}
                    onChangeText={(text) => setEditForm({...editForm, location: text})}
                  />
                  <TextInput
                    style={styles.input}
                    placeholder="Goal amount"
                    placeholderTextColor="#888"
                    keyboardType="numeric"
                    value={editForm.goalAmount}
                    onChangeText={(text) => setEditForm({...editForm, goalAmount: text})}
                  />
                  <View style={styles.editButtons}>
                    <Button title="Cancel" onPress={cancelEdit} color="#888" />
                    <Button title="Save" onPress={() => saveEdit(category.id)} />
                    <Button title="Delete" onPress={() => deleteCategory(category.id)} color="#dc2626" />
                  </View>
                </View>
              ) : (
                // View Mode
                <View>
                  <View style={styles.categoryHeader}>
                    <View style={{ flex: 1 }}>
                      <ThemedText type="defaultSemiBold" style={styles.categoryName}>
                        {category.name}
                      </ThemedText>
                      <ThemedText style={styles.location}>{category.location}</ThemedText>
                    </View>
                    <Pressable 
                      style={styles.editButton}
                      onPress={() => startEditing(category)}
                    >
                      <ThemedText style={styles.editButtonText}>Edit</ThemedText>
                    </Pressable>
                  </View>

                  <View style={styles.amountRow}>
                    <ThemedText style={styles.amount}>
                      ${category.currentAmount.toFixed(2)} / ${category.goalAmount.toFixed(2)}
                    </ThemedText>
                  </View>

                  {/* Progress Bar */}
                  <View style={styles.progressBarContainer}>
                    <View 
                      style={[
                        styles.progressBar, 
                        { width: `${getProgress(category.currentAmount, category.goalAmount)}%` }
                      ]} 
                    />
                  </View>

                  <ThemedText style={styles.percentage}>
                    {getProgress(category.currentAmount, category.goalAmount).toFixed(0)}% of goal
                  </ThemedText>

                  {/* Quick Add Buttons */}
                  <View style={styles.quickAddContainer}>
                    <Pressable 
                      style={styles.quickAddButton}
                      onPress={() => addMoney(category.id, 10)}
                    >
                      <ThemedText style={styles.quickAddText}>+$10</ThemedText>
                    </Pressable>
                    <Pressable 
                      style={styles.quickAddButton}
                      onPress={() => addMoney(category.id, 20)}
                    >
                      <ThemedText style={styles.quickAddText}>+$20</ThemedText>
                    </Pressable>
                    <Pressable 
                      style={styles.quickAddButton}
                      onPress={() => setCustomAmountId(category.id)}
                    >
                      <ThemedText style={styles.quickAddText}>Custom</ThemedText>
                    </Pressable>
                  </View>

                  {/* Custom Amount Input */}
                  {customAmountId === category.id && (
                    <View style={styles.customAmountContainer}>
                      <TextInput
                        style={styles.customAmountInput}
                        placeholder="Enter amount"
                        placeholderTextColor="#888"
                        keyboardType="numeric"
                        value={customAmount}
                        onChangeText={setCustomAmount}
                        autoFocus
                      />
                      <View style={styles.customAmountButtons}>
                        <Button 
                          title="Cancel" 
                          onPress={() => {
                            setCustomAmountId(null);
                            setCustomAmount('');
                          }} 
                          color="#888" 
                        />
                        <Button 
                          title="Subtract" 
                          onPress={() => subtractCustomAmount(category.id)} 
                          color="#dc2626"
                        />
                        <Button 
                          title="Add" 
                          onPress={() => addCustomAmount(category.id)} 
                        />
                      </View>
                    </View>
                  )}
                </View>
              )}
            </ThemedView>
          ))}

          {/* Add New Category */}
          {!showAddForm ? (
            <Pressable 
              style={styles.addButton}
              onPress={() => setShowAddForm(true)}
            >
              <ThemedText style={styles.addButtonText}>+ Add New Category</ThemedText>
            </Pressable>
          ) : (
            <ThemedView style={styles.addForm}>
              <ThemedText style={styles.label}>Category Type:</ThemedText>
              
              <View style={styles.categoryTypeButtons}>
                {categoryOptions.map((option) => (
                  <Pressable
                    key={option}
                    style={[
                      styles.categoryTypeButton,
                      selectedCategoryType === option && styles.categoryTypeButtonSelected
                    ]}
                    onPress={() => setSelectedCategoryType(option)}
                  >
                    <ThemedText style={[
                      styles.categoryTypeButtonText,
                      selectedCategoryType === option && styles.categoryTypeButtonTextSelected
                    ]}>
                      {option}
                    </ThemedText>
                  </Pressable>
                ))}
              </View>

              {selectedCategoryType === 'Custom' && (
                <TextInput
                  style={styles.input}
                  placeholder="Enter custom category name"
                  placeholderTextColor="#888"
                  value={customCategoryName}
                  onChangeText={setCustomCategoryName}
                />
              )}

              <TextInput
                style={styles.input}
                placeholder="Location (e.g., Hidden at home, Bank XYZ)"
                placeholderTextColor="#888"
                value={newCategory.location}
                onChangeText={(text) => setNewCategory({...newCategory, location: text})}
              />
              <TextInput
                style={styles.input}
                placeholder="Goal amount"
                placeholderTextColor="#888"
                keyboardType="numeric"
                value={newCategory.goalAmount}
                onChangeText={(text) => setNewCategory({...newCategory, goalAmount: text})}
              />
              <View style={styles.formButtons}>
                <Button title="Cancel" onPress={() => setShowAddForm(false)} color="#888" />
                <Button title="Add Category" onPress={addCategory} />
              </View>
            </ThemedView>
          )}
        </ThemedView>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 20,
  },
  title: {
    marginBottom: 15,
  },
  description: {
    fontSize: 15,
    lineHeight: 22,
    marginBottom: 20,
  },
  strategiesBox: {
    backgroundColor: '#f0f9ff',
    padding: 15,
    borderRadius: 8,
    marginBottom: 25,
  },
  strategiesTitle: {
    marginBottom: 10,
  },
  strategyItem: {
    fontSize: 14,
    marginBottom: 6,
    lineHeight: 20,
  },
  aiNote: {
    fontSize: 13,
    marginTop: 10,
    fontStyle: 'italic',
    color: '#0a7ea4',
  },
  categoriesTitle: {
    marginBottom: 15,
  },
  categoryCard: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
  },
  categoryHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  categoryName: {
    fontSize: 18,
    marginBottom: 4,
  },
  location: {
    fontSize: 13,
    color: '#666',
  },
  editButton: {
    backgroundColor: '#0a7ea4',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  editButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  amountRow: {
    marginBottom: 8,
  },
  amount: {
    fontSize: 16,
    fontWeight: '600',
  },
  progressBarContainer: {
    height: 20,
    backgroundColor: '#e5e5e5',
    borderRadius: 10,
    overflow: 'hidden',
    marginBottom: 5,
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#22c55e',
    borderRadius: 10,
  },
  percentage: {
    fontSize: 12,
    color: '#666',
    marginBottom: 10,
  },
  quickAddContainer: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 5,
  },
  quickAddButton: {
    flex: 1,
    backgroundColor: '#0a7ea4',
    padding: 8,
    borderRadius: 6,
    alignItems: 'center',
  },
  quickAddText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
  customAmountContainer: {
    marginTop: 10,
    padding: 10,
    backgroundColor: '#f5f5f5',
    borderRadius: 6,
  },
  customAmountInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 6,
    padding: 10,
    fontSize: 16,
    backgroundColor: '#fff',
    marginBottom: 8,
  },
  customAmountButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 5,
  },
  addButton: {
    backgroundColor: '#0a7ea4',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  addButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 16,
  },
  addForm: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    padding: 15,
    marginTop: 10,
  },
  label: {
    fontSize: 14,
    marginBottom: 10,
    fontWeight: '500',
  },
  categoryTypeButtons: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 15,
  },
  categoryTypeButton: {
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#ddd',
    backgroundColor: '#fff',
  },
  categoryTypeButtonSelected: {
    backgroundColor: '#0a7ea4',
    borderColor: '#0a7ea4',
  },
  categoryTypeButtonText: {
    fontSize: 14,
    color: '#333',
  },
  categoryTypeButtonTextSelected: {
    color: '#fff',
    fontWeight: '600',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 6,
    padding: 10,
    marginBottom: 10,
    fontSize: 16,
    backgroundColor: '#fff',
  },
  formButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
  },
  editButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
    marginTop: 10,
  },
});