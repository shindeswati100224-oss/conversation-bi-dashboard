import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Conversation BI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("conversation_bi_ai_output.csv")

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🎛 Filters")

sentiment_filter = st.sidebar.multiselect(
    "Select Sentiment",
    options=df["sentiment"].unique(),
    default=df["sentiment"].unique()
)

issue_filter = st.sidebar.multiselect(
    "Select Issue Type",
    options=df["issue_type"].unique(),
    default=df["issue_type"].unique()
)

filtered_df = df[
    (df["sentiment"].isin(sentiment_filter)) &
    (df["issue_type"].isin(issue_filter))
]

# ---------------- TITLE ----------------
st.title("📊 E-commerce Customer Support Insights")
st.caption("End-to-End Conversation BI Project")

# ---------------- KPI METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Conversations", len(filtered_df))
col2.metric("Negative", (filtered_df["sentiment"] == "NEGATIVE").sum())
col3.metric("Positive", (filtered_df["sentiment"] == "POSITIVE").sum())

st.divider()

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("😊 Sentiment Distribution")
    fig_sentiment = px.bar(
        filtered_df["sentiment"].value_counts().reset_index(),
        x="index",
        y="sentiment",
        labels={"index": "Sentiment", "sentiment": "Count"},
        height=300
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

with col2:
    st.subheader("📦 Issue Type Distribution")
    fig_issue = px.bar(
        filtered_df["issue_type"].value_counts().reset_index(),
        x="index",
        y="issue_type",
        labels={"index": "Issue Type", "issue_type": "Count"},
        height=300
    )
    st.plotly_chart(fig_issue, use_container_width=True)

st.divider()

# ---------------- DATA TABLE ----------------
st.subheader("📄 Filtered Conversations")
st.dataframe(filtered_df, height=300)

# ---------------- CSV DOWNLOAD ----------------
st.download_button(
    label="📥 Download Filtered CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_conversations.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Built with Streamlit • Conversation BI Project")
