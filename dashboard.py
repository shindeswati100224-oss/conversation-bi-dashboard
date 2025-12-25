import streamlit as st
import pandas as pd
import requests

# ---------------- CONFIG ----------------
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="E-commerce Customer Support Insights",
    layout="wide"
)

# ---------------- LOAD API DATA ----------------
summary = requests.get(f"{API_BASE}/summary").json()
data = requests.get(f"{API_BASE}/data?limit=20").json()

# ---------------- TITLE ----------------
st.title("📊 E-commerce Customer Support Insights")
st.markdown("Business Intelligence dashboard for customer issue & sentiment analysis")

st.divider()

# ---------------- KPI METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Conversations",
        summary["total_rows"]
    )

with col2:
    st.metric(
        "Negative Sentiment",
        summary["sentiment_counts"].get("NEGATIVE", 0)
    )

with col3:
    st.metric(
        "Positive Sentiment",
        summary["sentiment_counts"].get("POSITIVE", 0)
    )

st.divider()

# ---------------- SENTIMENT CHART ----------------
st.subheader("🙂 Sentiment Distribution")

sent_df = pd.DataFrame(
    summary["sentiment_counts"].items(),
    columns=["Sentiment", "Count"]
)

st.bar_chart(
    sent_df.set_index("Sentiment"),
    height=300
)

# ---------------- ISSUE TYPE CHART ----------------
st.subheader("📦 Issue Category Distribution")

issue_df = pd.DataFrame(
    summary["issue_type_counts"].items(),
    columns=["Issue Type", "Count"]
)

st.bar_chart(
    issue_df.set_index("Issue Type"),
    height=320
)

st.divider()

# ---------------- SAMPLE DATA ----------------
st.subheader("🗂 Sample Conversations (Top 20)")
st.dataframe(
    pd.DataFrame(data),
    height=300
)

st.divider()

# ---------------- BUSINESS INSIGHTS ----------------
st.subheader("📌 Key Business Insights")

st.info(
    """
    • Majority of conversations carry negative sentiment  
    • Delivery and refund issues dominate customer complaints  
    • Payment-related issues appear less frequent but impactful  
    • Improving logistics and faster refunds can significantly improve customer satisfaction
    """
)
