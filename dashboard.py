import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="E-commerce Customer Support Insights",
    page_icon="📊",
    layout="wide"
)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    return pd.read_csv("conversation_bi_ai_output.csv")

df = load_data()

# ------------------ SIDEBAR FILTERS ------------------
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

# ------------------ HEADER ------------------
st.title("📊 E-commerce Customer Support Insights")
st.markdown("Interactive BI dashboard for customer issue & sentiment analysis")

# ------------------ KPI METRICS ------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Conversations", len(filtered_df))
col2.metric("Negative Sentiment", (filtered_df["sentiment"] == "NEGATIVE").sum())
col3.metric("Positive Sentiment", (filtered_df["sentiment"] == "POSITIVE").sum())

st.divider()

# ------------------ CHARTS ------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("😊 Sentiment Distribution")
    sentiment_counts = filtered_df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    fig1 = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        height=350,
        color="Sentiment",
        text="Count"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("📦 Issue Type Distribution")
    issue_counts = filtered_df["issue_type"].value_counts().reset_index()
    issue_counts.columns = ["Issue Type", "Count"]

    fig2 = px.pie(
        issue_counts,
        names="Issue Type",
        values="Count",
        height=350
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ------------------ DATA TABLE ------------------
st.subheader("📄 Filtered Conversations")
st.dataframe(filtered_df, use_container_width=True, height=300)

# ------------------ CSV DOWNLOAD ------------------
st.download_button(
    label="📥 Download Filtered CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_conversations.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Built with Streamlit • Conversation BI Project")
