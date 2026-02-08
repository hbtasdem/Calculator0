# Calculator0

94% of domestic abuse cases involve financial abuse. Financial abuse is the control of another person through financial means. This control is one of the most insidious tactics abusers use to trap their victims. It is also one of the hardest forms of abuse to detect and one of the hardest to escape from. Some of the patterns include the victims wanting to leave but not being able to due to lack of funds. Their paychecks might be intercepted, spending might be monitored, and saving money might be impossible without raising suspicion.

We started with one question: What if victims could secretly analyze their financial situation and plan their escape without their abuser ever knowing?

Most financial tools fail here. Budgeting apps, banking apps, and finance trackers are obvious and easy to monitor.

Then we realized something simple. Everyone has a calculator app. No one questions it.

What it does
Calculator0 is a disguised calculator that hides powerful financial safety tools behind a familiar interface. It is designed to stay invisible while giving users clarity, security, and control.

1. AI-Powered Financial Abuse Detection
Connects securely to bank accounts via Capital One's Nessie API
Uses Gemini 2.5 to analyze 6 months of transaction history
Detects patterns like:
Missing or irregular deposits (partner intercepting paychecks)
Sudden spending restrictions (punishment cycles)
Category elimination (loss of autonomy over time)
"Allowance" patterns (severe financial control)
Provides risk assessment: LOW, MEDIUM, or HIGH

3. Secret Savings Planner
Calculates how much money victims need to leave safely
Considers: first month's rent, security deposits, emergency fund, moving costs
Tracks progress toward savings goals
All data encrypted and hidden behind biometric authentication
Community resources embedded in the app (shelters, legal aid, hotlines)

5. Encrypted Data Protection
Secure storage for photos, documents, bank statements
AES-256 encryption protects all files
Face ID/email authentication required
Panic button that instantly closes app and clears from recent apps
If discovered, appears as a normal calculator


How we built it

Frontend
React Native + Expo for cross-platform mobile development
Expo Router for navigation
TypeScript for type safety
Expo SecureStore for encrypted local storage
AI & Backend
Google Gemini 2.5 Flash for transaction pattern analysis
Capital One Nessie API for realistic financial data
Python for mock data generation (5 distinct abuse profiles)
AES-256-CBC encryption for sensitive data
AI Prompt Engineering
We crafted specific prompts for Gemini to detect:

Accomplishments that we're proud of
1. Real-World Impact Potential
We are proud of our work because we didn't just build a tech demo, we built something that could actually create impact for potentially millions of victims of financial abuse. We made our design decision with real survivors in mind: from the disguise to the encryption to the AI patterns. Calculator0 answers real problems that keep people trapped in abusive relationships.

2. Novel AI Application
We believe that using Gemini to detect financial abuse patterns is an innovative use case. We're not just analyzing spending habits, we're detecting coercive control, punishment cycles, and economic isolation. This is pattern recognition that could help millions of people who don't even realize they're being abused.

What we learned
Technical Skills
Expo ecosystem: SecureStore, Constants, Local Authentication, Document Picker
AI prompt engineering: Crafting effective prompts for financial pattern detection
Encryption best practices: AES-256 implementation
API integration: REST APIs, error handling, response parsing
React Native: Cross-platform mobile development, biometric authentication
Domain Knowledge
Data privacy: Importance of encryption and local-first storage
UX for sensitive apps: Balancing security with accessibility
Financial abuse patterns: How abusers use money as a control mechanism
