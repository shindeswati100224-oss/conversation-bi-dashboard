import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ================= CONFIG ================= #
st.set_page_config(
    page_title="Conversation BI + Chatbot",
    layout="wide"
)

API_BASE_URL = "http://localhost:8000"  
# 🔁 Change to deployed FastAPI URL later

# ================= PAGE TITLE ================= #
st.title("📊 E-commerce Customer Support Insights")

# ================= FETCH SUMMARY ================= #
with st.spinner("Connecting to API..."):
    try:
        summary = requests.get(f"{API_BASE_URL}/summary").json()
    except:
        st.error("❌ Cannot connect to FastAPI")
        st.stop()

if summary.get("status") != "success":
    st.error("⚠️ API Error")
    st.json(summary)
    st.stop()

# ================= METRICS ================= #
st.subheader("📌 Key Metrics")

c1, c2, c3 = st.columns(3)
c1.metric("Total Conversations", summary["total_rows"])
c2.metric("Issue Types", len(summary["issue_type_counts"]))
c3.metric("Sources", len(summary["source_counts"]))

# ================= SENTIMENT ================= #
sentiment_df = pd.DataFrame(
    summary["sentiment_counts"].items(),
    columns=["Sentiment", "Count"]
)

fig1 = px.pie(sentiment_df, names="Sentiment", values="Count", title="Sentiment Analysis")
st.plotly_chart(fig1, use_container_width=True)

# ================= ISSUE TYPES ================= #
issue_df = pd.DataFrame(
    summary["issue_type_counts"].items(),
    columns=["Issue Type", "Count"]
)

fig2 = px.bar(issue_df, x="Issue Type", y="Count", title="Customer Issues")
st.plotly_chart(fig2, use_container_width=True)

# ================= SOURCE ================= #
source_df = pd.DataFrame(
    summary["source_counts"].items(),
    columns=["Source", "Count"]
)

fig3 = px.bar(source_df, x="Source", y="Count", title="Conversation Sources")
st.plotly_chart(fig3, use_container_width=True)

# ================= SAMPLE DATA ================= #
st.subheader("📄 Sample Records")

records = requests.get(f"{API_BASE_URL}/data?limit=20").json()
st.dataframe(pd.DataFrame(records))

# ==================================================
# 🤖 CHATBOT SECTION (API-BASED)
# ==================================================
st.markdown("---")
st.header("🤖 E-commerce FAQ Chatbot")

# Chat memory
if "chat" not in st.session_state:
    st.session_state.chat = []

def chatbot_api(question: str):
    """Simulated chatbot API logic"""
    q = question.lower()

    if "refund" in q and "upi" in q:
        return "UPI refunds are credited to the same bank account within 3–5 working days."
    if "refund" in q and "shipping" in q:
        return "Shipping charges are non-refundable unless the product was damaged or incorrect."
    if "refund" in q:
        return "Refunds are processed after pickup as per return policy."
    if "where is my order" in q or "track" in q:
        return "You can track your order from My Orders → Track Order."
    if "emi" in q:
        return "EMI options are available on select credit cards."
    if "payment" in q:
        return "We support UPI, credit card, debit card and net banking."
    if "large appliance" in q:
        return "Large appliances are delivered with scheduled installation support."

    return "Sorry, I couldn't understand. Please rephrase."

# Display chat
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_q = st.chat_input("Ask about refund, delivery, payment...")

if user_q:
    st.session_state.chat.append({"role": "user", "content": user_q})

    bot_reply = chatbot_api(user_q)

    st.session_state.chat.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
