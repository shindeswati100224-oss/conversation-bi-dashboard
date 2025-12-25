import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="E-commerce Customer Support Insights",
    layout="wide"
)

st.title("📊 E-commerce Customer Support Insights")
st.caption("Upload conversation data to analyze customer support performance")

# --------------------------------------------------
# File Upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload conversation_bi_ai_output.csv",
    type=["csv"]
)

if uploaded_file is None:
    st.info("⬆️ Please upload the CSV file to continue")
    st.stop()

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = pd.read_csv(uploaded_file)

# Safety check
required_columns = {"sentiment", "issue_type"}
if not required_columns.issubset(df.columns):
    st.error("❌ CSV must contain 'sentiment' and 'issue_type' columns")
    st.stop()

# --------------------------------------------------
# Metrics
# --------------------------------------------------
total_rows = len(df)
sentiment_counts = df["sentiment"].value_counts()

col1, col2, col3 = st.columns(3)
col1.metric("Total Conversations", total_rows)
col2.metric("Negative Sentiment", sentiment_counts.get("NEGATIVE", 0))
col3.metric("Positive Sentiment", sentiment_counts.get("POSITIVE", 0))

st.divider()

# --------------------------------------------------
# Filters
# --------------------------------------------------
st.subheader("🎛 Filters")
col_f1, col_f2 = st.columns(2)

sentiment_filter = col_f1.multiselect(
    "Sentiment",
    df["sentiment"].unique(),
    default=df["sentiment"].unique()
)

issue_filter = col_f2.multiselect(
    "Issue Type",
    df["issue_type"].unique(),
    default=df["issue_type"].unique()
)

filtered_df = df[
    (df["sentiment"].isin(sentiment_filter)) &
    (df["issue_type"].isin(issue_filter))
]

# --------------------------------------------------
# Charts
# --------------------------------------------------
st.subheader("😊 Sentiment Distribution")
fig_sentiment = px.bar(
    filtered_df["sentiment"].value_counts().reset_index(),
    x="index",
    y="sentiment",
    labels={"index": "Sentiment", "sentiment": "Count"},
    height=300
)
st.plotly_chart(fig_sentiment, use_container_width=True)

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

# --------------------------------------------------
# Data Table
# --------------------------------------------------
st.subheader("📄 Filtered Conversations")
st.dataframe(filtered_df, use_container_width=True)

# --------------------------------------------------
# Download
# --------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Filtered CSV",
    csv,
    "filtered_conversations.csv",
    "text/csv"
)

st.caption("🚀 Built with Streamlit | Conversation BI Project")
