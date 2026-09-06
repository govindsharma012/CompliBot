🤖 CompliBot — Compliance Automation Robot
CompliBot ek AI-powered tool hai jo trading companies ke liye compliance filing automate karta hai. Ye ek trade description leta hai, Google Gemini AI se analyze karwata hai ki kaunsa financial regulation lagu hota hai (Dodd-Frank Act, MiFID II, ya EMIR), aur ek human approval step ke baad filing record save kar deta hai.
Features
🧠 AI-based reasoning (keyword matching nahi) using Google Gemini
✅ Human-in-the-loop approval before any filing is submitted
📝 Automatic filing log with unique Filing IDs
🎨 Colorful web interface (via Streamlit) alongside a simple command-line version
Files
app.py — Command-line version of CompliBot
compli_web.py — Web interface version (Streamlit) with colorful UI
filing_log.txt — Auto-generated log of all filings (created when you run the app)
Setup
Install dependencies:
Code
Get a free Gemini API key from Google AI Studio
Open app.py or compli_web.py and replace YOUR_API_KEY_HERE with your actual API key
Usage
Command-line version:
Code
Web interface version:
Code
How It Works
User types a trade description (e.g. "US client bought a derivative from a European bank")
Gemini AI analyzes it and suggests the applicable regulation with reasoning
A unique Filing ID is generated
The human user reviews and approves/rejects the filing
The result is saved to filing_log.txt
This human-in-the-loop design ensures AI suggestions are always verified by a person before being finalized — important for compliance-sensitive workflows.
