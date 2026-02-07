import { StyleSheet, View, Text, Pressable } from 'react-native';
import { Link } from 'expo-router';

export default function HomeScreen() {
  const buttons = [
    ['C', '±', '%', '÷'],
    ['7', '8', '9', '×'],
    ['4', '5', '6', '−'],
    ['1', '2', '3', '+'],
    [' ', '0', '.', '='],
  ];

  return (
    <View style={styles.container}>
      {/* Display */}
      <View style={styles.display}>
        <Text style={styles.displayText}>0</Text>
      </View>

      {/* Buttons */}
      <View style={styles.buttonContainer}>
        {buttons.map((row, rowIndex) => (
          <View key={rowIndex} style={styles.row}>
            {row.map((button) => {
              // Special case for "0" button - make it link to login
              if (button === '0') {
                return (
                  <Link key={button} href="/login" asChild>
                    <Pressable style={styles.button}>
                      <Text style={styles.buttonText}>{button}</Text>
                    </Pressable>
                  </Link>
                );
              }
              // Regular buttons
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
  zeroButton: {
    flex: 2,
    aspectRatio: 2.2,
    backgroundColor: '#333',
    borderRadius: 50,
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