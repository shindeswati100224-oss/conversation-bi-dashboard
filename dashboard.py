import streamlit as st
import pandas as pd

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

# Validate required columns
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
    sorted(df["sentiment"].unique()),
    default=sorted(df["sentiment"].unique())
)

issue_filter = col_f2.multiselect(
    "Issue Type",
    sorted(df["issue_type"].unique()),
    default=sorted(df["issue_type"].unique())
)

filtered_df = df[
    (df["sentiment"].isin(sentiment_filter)) &
    (df["issue_type"].isin(issue_filter))
]

st.divider()

# --------------------------------------------------
# Sentiment Distribution (SAFE)
# --------------------------------------------------
st.subheader("😊 Sentiment Distribution")

if filtered_df.empty:
    st.warning("⚠️ No data available for selected filters")
else:
    sentiment_chart = (
        filtered_df["sentiment"]
        .value_counts()
        .to_frame(name="Count")
    )
    st.bar_chart(sentiment_chart)

# --------------------------------------------------
# Issue Type Distribution (SAFE)
# --------------------------------------------------
st.subheader("📦 Issue Type Distribution")

if filtered_df.empty:
    st.warning("⚠️ No data available for selected filters")
else:
    issue_chart = (
        filtered_df["issue_type"]
        .value_counts()
        .to_frame(name="Count")
    )
    st.bar_chart(issue_chart)

st.divider()

# --------------------------------------------------
# Data Table
# --------------------------------------------------
st.subheader("📄 Filtered Conversations")

if filtered_df.empty:
    st.info("No records to display")
else:
    st.dataframe(filtered_df, use_container_width=True)

# --------------------------------------------------
# Download
# --------------------------------------------------
if not filtered_df.empty:
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Filtered CSV",
        csv,
        "filtered_conversations.csv",
        "text/csv"
    )

st.caption("🚀 Built with Streamlit | Conversation BI Project")
