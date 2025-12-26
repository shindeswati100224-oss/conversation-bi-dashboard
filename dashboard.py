import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Conversation BI + Chatbot", layout="wide")
st.title("📊 E-commerce Customer Support Insights")

API_BASE_URL = "https://conversation-bi-api.up.railway.app"


# ---------------- FETCH SUMMARY ----------------
with st.spinner("Loading analytics..."):
    try:
        summary = requests.get(f"{API_BASE_URL}/summary", timeout=10).json()
    except:
        st.error("❌ Backend API not reachable")
        st.stop()

if summary.get("status") != "success":
    st.error("API error")
    st.json(summary)
    st.stop()

# ---------------- METRICS ----------------
c1, c2, c3 = st.columns(3)
c1.metric("Total Conversations", summary["total_rows"])
c2.metric("Issue Types", len(summary["issue_type_counts"]))
c3.metric("Sources", len(summary["source_counts"]))

# ---------------- CHARTS ----------------
sentiment_df = pd.DataFrame(summary["sentiment_counts"].items(), columns=["Sentiment", "Count"])
st.plotly_chart(px.pie(sentiment_df, names="Sentiment", values="Count"), use_container_width=True)

issue_df = pd.DataFrame(summary["issue_type_counts"].items(), columns=["Issue", "Count"])
st.plotly_chart(px.bar(issue_df, x="Issue", y="Count"), use_container_width=True)

# ---------------- TABLE ----------------
data = requests.get(f"{API_BASE_URL}/data?limit=20").json()
st.dataframe(pd.DataFrame(data))

# ---------------- CHATBOT ----------------
st.markdown("---")
st.header("🤖 FAQ Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

def chatbot(q):
    q = q.lower()
    if "upi" in q and "refund" in q:
        return "UPI refunds are credited within 3–5 working days."
    if "refund" in q:
        return "Refunds are processed after pickup as per policy."
    if "track" in q or "order" in q:
        return "Track order from My Orders section."
    if "emi" in q:
        return "EMI options are available on select cards."
    return "Please rephrase your question."

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

q = st.chat_input("Ask your question...")
if q:
    st.session_state.chat.append({"role": "user", "content": q})
    a = chatbot(q)
    st.session_state.chat.append({"role": "assistant", "content": a})
    with st.chat_message("assistant"):
        st.markdown(a)

