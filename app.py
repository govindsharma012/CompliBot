import datetime
import google.generativeai as genai

# IMPORTANT: Apni Gemini API key yahan daalo (Google AI Studio se milti hai - free)
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-3.6-flash")

print("=== CompliBot - Compliance Automation Robot ===\n")

while True:
    trade = input("Apni trade likhiye (ya 'exit' type karo band karne ke liye): ")

    if trade.lower() == "exit":
        print("\nCompliBot band ho raha hai. Dhanyawad!")
        break

    prompt = """Tum ek compliance expert ho. Neeche di gayi trade description padho aur batao kaunsa regulation lagu hota hai.
Options: Dodd-Frank Act (USA), MiFID II (Europe), EMIR (derivatives/swaps), ya Manual Review (agar clear na ho).
Sirf regulation ka naam batao, ek chhoti si wajah ke saath. Format:
Law: <regulation name>
Reason: <ek line mein wajah>

Trade: """ + trade

    try:
        response = model.generate_content(prompt)
        ai_output = response.text
    except Exception as e:
        print("\n⚠️ AI se connect nahi ho paya. Error:", e)
        print("Manual review karo is trade ka.\n")
        continue

    filing_id = "FL-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    print("\n--- AI ANALYSIS ---")
    print(ai_output)
    print("-------------------")

    print("\n--- FILING FORM ---")
    print("Filing ID:", filing_id)
    print("Trade:", trade)
    print(ai_output)
    print("Status: PENDING")
    print("-------------------")

    approval = input("\nSubmit this filing? (yes/no): ")

    if approval.lower() == "yes":
        status = "SUBMITTED"
        print("Filing submitted to regulator!")
    else:
        status = "REJECTED"
        print("Filing rejected by user.")

    with open("filing_log.txt", "a", encoding="utf-8") as f:
        f.write("--- COMPLIBOT FILING ---\n")
        f.write("Filing ID: " + filing_id + "\n")
        f.write("Trade: " + trade + "\n")
        f.write(ai_output + "\n")
        f.write("Status: " + status + "\n")
        f.write("--------------------------\n\n")

    print("Filing record 'filing_log.txt' mein add ho gaya.\n")
