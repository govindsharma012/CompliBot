import streamlit as st
import datetime
import google.generativeai as genai

# ============ SETUP ============
# IMPORTANT: Apni Gemini API key yahan daalo (Google AI Studio se milti hai - free)
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(page_title="CompliBot", page_icon="🤖", layout="centered")

# ============ CUSTOM STYLING (colorful CSS) ============
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    .title-box {
        background: linear-gradient(90deg, #ff6a00, #ee0979);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .title-box h1 {
        color: white;
        font-size: 36px;
        margin: 0;
    }
    .title-box p {
        color: #ffe8d6;
        margin: 5px 0 0 0;
    }
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        border-left: 8px solid #2a5298;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ee0979, #ff6a00);
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        opacity: 0.85;
    }
    </style>
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("""
    <div class="title-box">
        <h1>🤖 CompliBot</h1>
        <p>Compliance Automation Robot — AI-Powered Trade Filing</p>
    </div>
""", unsafe_allow_html=True)

# ============ SESSION STATE (record ka storage) ============
if "history" not in st.session_state:
    st.session_state.history = []
if "ai_output" not in st.session_state:
    st.session_state.ai_output = ""
if "current_trade" not in st.session_state:
    st.session_state.current_trade = ""

# ============ INPUT SECTION ============
st.subheader("📝 Apni Trade Details Likhiye")
trade = st.text_area("Trade description:", placeholder="e.g. US client ne Europe ke bank se derivative kharida", height=80)

if st.button("🔍 AI Se Analyze Karo"):
    if trade.strip() == "":
        st.warning("⚠️ Pehle trade type karo!")
    else:
        with st.spinner("AI trade ko samajh raha hai... ⏳"):
            prompt = """Tum ek compliance expert ho. Neeche di gayi trade description padho aur batao kaunsa regulation lagu hota hai.
Options: Dodd-Frank Act (USA), MiFID II (Europe), EMIR (derivatives/swaps), ya Manual Review (agar clear na ho).
Sirf regulation ka naam batao, ek chhoti si wajah ke saath. Format:
Law: <regulation name>
Reason: <ek line mein wajah>

Trade: """ + trade

            try:
                response = model.generate_content(prompt)
                st.session_state.ai_output = response.text
                st.session_state.current_trade = trade
            except Exception as e:
                st.error(f"AI se connect nahi ho paya: {e}")
                st.session_state.ai_output = ""

# ============ RESULT + APPROVAL SECTION ============
if st.session_state.ai_output:
    filing_id = "FL-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    st.markdown(f"""
        <div class="result-card">
            <h4>📄 AI Analysis</h4>
            <p>{st.session_state.ai_output.replace(chr(10), '<br>')}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="result-card">
            <h4>🗂️ Filing Form</h4>
            <b>Filing ID:</b> {filing_id}<br>
            <b>Trade:</b> {st.session_state.current_trade}<br>
            <b>Status:</b> ⏳ PENDING (Human Review Needed)
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Submit Filing"):
            status = "SUBMITTED"
            st.session_state.history.append({
                "id": filing_id, "trade": st.session_state.current_trade,
                "ai": st.session_state.ai_output, "status": status
            })
            with open("filing_log.txt", "a", encoding="utf-8") as f:
                f.write("--- COMPLIBOT FILING ---\n")
                f.write("Filing ID: " + filing_id + "\n")
                f.write("Trade: " + st.session_state.current_trade + "\n")
                f.write(st.session_state.ai_output + "\n")
                f.write("Status: " + status + "\n")
                f.write("--------------------------\n\n")
            st.success("✅ Filing submitted to regulator!")
            st.session_state.ai_output = ""

    with col2:
        if st.button("❌ Reject Filing"):
            status = "REJECTED"
            st.session_state.history.append({
                "id": filing_id, "trade": st.session_state.current_trade,
                "ai": st.session_state.ai_output, "status": status
            })
            with open("filing_log.txt", "a", encoding="utf-8") as f:
                f.write("--- COMPLIBOT FILING ---\n")
                f.write("Filing ID: " + filing_id + "\n")
                f.write("Trade: " + st.session_state.current_trade + "\n")
                f.write(st.session_state.ai_output + "\n")
                f.write("Status: " + status + "\n")
                f.write("--------------------------\n\n")
            st.error("❌ Filing rejected by user.")
            st.session_state.ai_output = ""

# ============ HISTORY SECTION ============
if st.session_state.history:
    st.subheader("📚 Filing History (Is Session Ki)")
    for record in reversed(st.session_state.history):
        color = "#28a745" if record["status"] == "SUBMITTED" else "#dc3545"
        st.markdown(f"""
            <div class="result-card" style="border-left-color:{color};">
                <b>{record['id']}</b> — <span style="color:{color};"><b>{record['status']}</b></span><br>
                <i>{record['trade']}</i>
            </div>
        """, unsafe_allow_html=True)
