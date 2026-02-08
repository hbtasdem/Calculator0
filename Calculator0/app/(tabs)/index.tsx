import { useState } from 'react';
import { StyleSheet, View, Text, Pressable } from 'react-native';
import { router } from 'expo-router';

export default function HomeScreen() {
  const [input, setInput] = useState('0');

  const buttons = [
    ['C', '±', '%', '÷'],
    ['7', '8', '9', '×'],
    ['4', '5', '6', '−'],
    ['1', '2', '3', '+'],
    [' ', '0', '.', '='],
  ];

  const handleButtonPress = (button: string) => {
    if (button === 'C') {
      setInput('0');
      return;
    }

    // Update display
    if (input === '0') {
      setInput(button);
    } else {
      setInput(input + button);
    }

    // Check if user entered "123"
    const newInput = input === '0' ? button : input + button;
    if (newInput === '123') {
      router.push('/login');
    }
  };

  return (
    <View style={styles.container}>
      {/* Display */}
      <View style={styles.display}>
        <Text style={styles.displayText}>{input}</Text>
      </View>

      {/* Buttons */}
      <View style={styles.buttonContainer}>
        {buttons.map((row, rowIndex) => (
          <View key={rowIndex} style={styles.row}>
            {row.map((button) => {
              if (button === ' ') {
                // Empty space
                return <View key="space" style={styles.button} />;
              }

              const isOperator = ['÷', '×', '−', '+', '='].includes(button);
              const isTopRow = ['C', '±', '%'].includes(button);

              return (
                <Pressable
                  key={button}
                  style={[
                    styles.button,
                    isOperator && styles.operatorButton,
                    isTopRow && styles.topRowButton,
                  ]}
                  onPress={() => handleButtonPress(button)}
                >
                  <Text
                    style={[
                      styles.buttonText,
                      isOperator && styles.operatorText,
                    ]}
                  >
                    {button}
                  </Text>
                </Pressable>
              );
            })}
          </View>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    justifyContent: 'flex-end',
  },
  display: {
    padding: 20,
    alignItems: 'flex-end',
    justifyContent: 'flex-end',
    minHeight: 120,
  },
  displayText: {
    color: '#fff',
    fontSize: 64,
    fontWeight: '300',
  },
  buttonContainer: {
    padding: 10,
  },
  row: {
    flexDirection: 'row',
    marginBottom: 10,
  },
  button: {
    flex: 1,
    aspectRatio: 1,
    backgroundColor: '#333',
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 5,
  },
  operatorButton: {
    backgroundColor: '#ff9500',
  },
  topRowButton: {
    backgroundColor: '#a5a5a5',
  },
  buttonText: {
    color: '#fff',
    fontSize: 32,
    fontWeight: '400',
  },
  operatorText: {
    fontWeight: '500',
  },
});