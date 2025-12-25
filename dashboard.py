import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="E-commerce Customer Support Insights",
    layout="wide"
)

st.title("📊 E-commerce Customer Support Insights")
st.write("Upload conversation data to analyze customer support performance")

# -------------------------------------------------
# FILE UPLOAD (Conversation BI Data)
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload conversation_bi_ai_output.csv",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    # ---------------- KPIs ----------------
    total_conversations = len(df)
    negative_count = len(df[df["sentiment"] == "negative"])
    positive_count = len(df[df["sentiment"] == "positive"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Conversations", total_conversations)
    col2.metric("Negative Sentiment", negative_count)
    col3.metric("Positive Sentiment", positive_count)

    st.markdown("---")

    # ---------------- FILTERS ----------------
    st.subheader("🔍 Filters")

    category_filter = st.selectbox(
        "Select Issue Category",
        ["All"] + sorted(df["category"].dropna().unique())
    )

    if category_filter != "All":
        df = df[df["category"] == category_filter]

    # ---------------- CHARTS ----------------
    st.subheader("📌 Issue Category Distribution")
    st.plotly_chart(
        px.bar(df, x="category", color="category"),
        use_container_width=True
    )

    st.subheader("😊 Sentiment Distribution")
    st.plotly_chart(
        px.pie(df, names="sentiment"),
        use_container_width=True
    )

    with st.expander("📄 View Raw Conversation Data"):
        st.dataframe(df)

# =================================================
# EMBEDDED FLIPKART FAQ CHATBOT (NO CSV)
# =================================================
st.markdown("---")
st.header("🤖 Flipkart FAQ Chatbot")

st.write(
    "Ask questions related to **delivery, refund, return, payment** "
    "based on Flipkart public FAQ information."
)

# -------------------------------------------------
# EMBEDDED FAQ DATA (NO FILE REQUIRED)
# -------------------------------------------------
FLIPKART_FAQ_TEXT = [
    "You can return most items within 7 days of delivery",
    "Refunds are initiated once the returned item is received",
    "Refunds are credited to the original payment method",
    "Delivery usually takes 3 to 5 business days",
    "Cash on Delivery is available for eligible products",
    "Orders can be cancelled before shipment",
    "Replacement is available for damaged or defective items",
    "Refunds for prepaid orders take 5 to 7
