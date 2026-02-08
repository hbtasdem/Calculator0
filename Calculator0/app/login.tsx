import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';
import { useState } from 'react';
import { router } from 'expo-router';
import { authService } from '@/services/authService';

export default function LoginScreen() {
    // ---------- SIGN UP ----------
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [customerId, setCustomerId] = useState('');
    const [isSignUp, setIsSignUp] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSignUp = async () => {
        if (!email || !password || !customerId) {
            Alert.alert('Error', 'Please fill all fields');
            return;
        }

        if (password.length < 6) {
            Alert.alert('Error', 'Password must be at least 6 characters');
            return;
        }

        setLoading(true);
        const result = await authService.signUp(email, password, customerId);
        setLoading(false);

        if (result.success) {
            Alert.alert('Success', 'Account created! Welcome to Cipher.', [
                { text: 'OK', onPress: () => router.replace('/(safety-tabs)/safety-plan') }
            ]);
        } else {
            Alert.alert('Signup Failed', result.error || 'Could not create account');
        }
    };

    // ---------- SIGN IN ----------
    const handleSignIn = async () => {
        if (!email || !password) {
            Alert.alert('Error', 'Please enter email and password');
            return;
        }

        setLoading(true);
        const result = await authService.signIn(email, password);
        setLoading(false);

        if (result.success) {
            if (result.isDecoy) {
                Alert.alert('Decoy Mode', 'Showing safe fake data');
            }
            router.replace('/(safety-tabs)/safety-plan');
        } else {
            Alert.alert('Login Failed', result.error || 'Could not sign in');
        }
    };

    return (
        <View style={styles.container}>
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                style={styles.keyboardView}
            >
                <ScrollView
                    contentContainerStyle={styles.scrollContent}
                    keyboardShouldPersistTaps="handled"
                >
                    {/* Header */}
                    <View style={styles.header}>
                        <View style={styles.logoContainer}>
                            <View style={styles.logo}>
                                <Text style={styles.logoText}>C</Text>
                            </View>
                        </View>
                        <Text style={styles.title}>Cipher</Text>
                        <Text style={styles.subtitle}>Your financial safety, encrypted</Text>
                    </View>

                    {/* Form */}
                    <View style={styles.form}>
                        <View style={styles.inputContainer}>
                            <Text style={styles.label}>Email</Text>
                            <TextInput
                                style={styles.input}
                                placeholder="Enter your email"
                                placeholderTextColor="#94a3b8"
                                value={email}
                                onChangeText={setEmail}
                                autoCapitalize="none"
                                keyboardType="email-address"
                                editable={!loading}
                            />
                        </View>

                        <View style={styles.inputContainer}>
                            <Text style={styles.label}>Password</Text>
                            <TextInput
                                style={styles.input}
                                placeholder="At least 6 characters"
                                placeholderTextColor="#94a3b8"
                                value={password}
                                onChangeText={setPassword}
                                secureTextEntry
                                editable={!loading}
                            />
                        </View>

                        {isSignUp && (
                            <View style={styles.inputContainer}>
                                <Text style={styles.label}>Customer ID</Text>
                                <TextInput
                                    style={styles.input}
                                    placeholder="Nessie Customer ID"
                                    placeholderTextColor="#94a3b8"
                                    value={customerId}
                                    onChangeText={setCustomerId}
                                    editable={!loading}
                                />
                            </View>
                        )}

                        <TouchableOpacity
                            style={[styles.button, loading && styles.buttonDisabled]}
                            onPress={isSignUp ? handleSignUp : handleSignIn}
                            disabled={loading}
                            activeOpacity={0.8}
                        >
                            <Text style={styles.buttonText}>
                                {loading ? 'Processing...' : (isSignUp ? 'Create Account' : 'Sign In')}
                            </Text>
                        </TouchableOpacity>

                        <TouchableOpacity
                            style={styles.switchButton}
                            onPress={() => setIsSignUp(!isSignUp)}
                            disabled={loading}
                            activeOpacity={0.6}
                        >
                            <Text style={styles.switchText}>
                                {isSignUp ? 'Already have an account? ' : "Don't have an account? "}
                                <Text style={styles.switchTextBold}>
                                    {isSignUp ? 'Sign In' : 'Sign Up'}
                                </Text>
                            </Text>
                        </TouchableOpacity>
                    </View>

                    {/* Info Cards */}
                    <View style={styles.infoSection}>
                        {isSignUp && (
                            <View style={styles.infoCard}>
                                <View style={styles.infoIconContainer}>
                                    <Text style={styles.infoIcon}>ℹ️</Text>
                                </View>
                                <View style={styles.infoContent}>
                                    <Text style={styles.infoTitle}>Need a Customer ID?</Text>
                                    <Text style={styles.infoText}>Run POST /api/demo/setup to create demo customers</Text>
                                </View>
                            </View>
                        )}

                        <View style={styles.infoSection}>
                            {isSignUp && (
                                <View style={styles.infoCard}>
                                    <View style={styles.infoIconContainer}>
                                        <Text style={styles.infoIcon}>ℹ️</Text>
                                    </View>
                                    <View style={styles.infoContent}>
                                        <Text style={styles.infoTitle}>Need a Customer ID?</Text>
                                        <Text style={styles.infoText}>Run POST /api/demo/setup to create demo customers</Text>
                                    </View>
                                </View>
                            )}

                            <TouchableOpacity
                                style={styles.calculatorButton}
                                onPress={() => router.push('/(tabs)')}
                                activeOpacity={0.8}
                            >
                                <Text style={styles.calculatorButtonText}>Calculator</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
        </View>
    );
}

const styles = StyleSheet.create({
    calculatorButton: {
        height: 56,
        backgroundColor: '#1e293b',
        borderRadius: 12,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#334155',
    },
    calculatorButtonText: {
        color: '#3b82f6',
        fontSize: 17,
        fontWeight: '600',
    },
    container: {
        flex: 1,
        backgroundColor: '#0f172a',
    },
    keyboardView: {
        flex: 1,
    },
    scrollContent: {
        flexGrow: 1,
        paddingHorizontal: 24,
        paddingTop: 60,
        paddingBottom: 40,
    },
    header: {
        alignItems: 'center',
        marginBottom: 48,
    },
    logoContainer: {
        marginBottom: 20,
    },
    logo: {
        width: 80,
        height: 80,
        borderRadius: 20,
        backgroundColor: '#3b82f6',
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: '#3b82f6',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.3,
        shadowRadius: 16,
        elevation: 8,
    },
    logoText: {
        fontSize: 42,
        fontWeight: '700',
        color: '#fff',
    },
    title: {
        fontSize: 36,
        fontWeight: '700',
        color: '#fff',
        marginBottom: 8,
        letterSpacing: 1,
    },
    subtitle: {
        fontSize: 16,
        color: '#94a3b8',
        textAlign: 'center',
    },
    form: {
        marginBottom: 32,
    },
    inputContainer: {
        marginBottom: 20,
    },
    label: {
        fontSize: 14,
        fontWeight: '600',
        color: '#e2e8f0',
        marginBottom: 8,
        marginLeft: 4,
    },
    input: {
        height: 56,
        backgroundColor: '#1e293b',
        borderRadius: 12,
        paddingHorizontal: 16,
        fontSize: 16,
        color: '#fff',
        borderWidth: 1,
        borderColor: '#334155',
    },
    button: {
        height: 56,
        backgroundColor: '#3b82f6',
        borderRadius: 12,
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 8,
        shadowColor: '#3b82f6',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 4,
    },
    buttonDisabled: {
        backgroundColor: '#475569',
        shadowOpacity: 0,
    },
    buttonText: {
        color: '#fff',
        fontSize: 17,
        fontWeight: '600',
        letterSpacing: 0.5,
    },
    switchButton: {
        marginTop: 24,
        padding: 12,
        alignItems: 'center',
    },
    switchText: {
        color: '#94a3b8',
        fontSize: 15,
    },
    switchTextBold: {
        color: '#3b82f6',
        fontWeight: '600',
    },
    infoSection: {
        gap: 12,
    },
    infoCard: {
        flexDirection: 'row',
        backgroundColor: '#1e293b',
        borderRadius: 12,
        padding: 16,
        borderWidth: 1,
        borderColor: '#334155',
    },
    infoIconContainer: {
        marginRight: 12,
    },
    infoIcon: {
        fontSize: 24,
    },
    infoContent: {
        flex: 1,
    },
    infoTitle: {
        fontSize: 14,
        fontWeight: '600',
        color: '#e2e8f0',
        marginBottom: 4,
    },
    infoText: {
        fontSize: 13,
        color: '#94a3b8',
        lineHeight: 18,
    },
});