import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="E-commerce Customer Support Insights",
    layout="wide"
)

st.title("📊 E-commerce Customer Support Insights")
st.write("Upload conversation data to analyze customer support performance")

# =================================================
# FILE UPLOAD
# =================================================
uploaded_file = st.file_uploader(
    "Upload conversation_bi_ai_output.csv",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    # =================================================
    # AUTO-DETECT COLUMNS (NO HARD CODING)
    # =================================================
    sentiment_col = None
    category_col = None

    for col in df.columns:
        if "sentiment" in col:
            sentiment_col = col
        if "category" in col or "issue" in col:
            category_col = col

    # =================================================
    # KPIs
    # =================================================
    total_conversations = len(df)

    if sentiment_col:
        negative_count = len(df[df[sentiment_col].astype(str).str.lower() == "negative"])
        positive_count = len(df[df[sentiment_col].astype(str).str.lower() == "positive"])
    else:
        negative_count = 0
        positive_count = 0
        st.warning("⚠️ Sentiment column not found in CSV")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Conversations", total_conversations)
    col2.metric("Negative Sentiment", negative_count)
    col3.metric("Positive Sentiment", positive_count)

    st.markdown("---")

    # =================================================
    # FILTERS
    # =================================================
    st.subheader("🔍 Filters")

    if category_col:
        category_filter = st.selectbox(
            "Select Issue Category",
            ["All"] + sorted(df[category_col].dropna().unique())
        )

        if category_filter != "All":
            df = df[df[category_col] == category_filter]
    else:
        st.info("ℹ️ Category column not found. Filters disabled.")

    # =================================================
    # CHARTS
    # =================================================
    if category_col:
        st.subheader("📌 Issue Category Distribution")
        st.plotly_chart(
            px.bar(df, x=category_col, color=category_col),
            use_container_width=True
        )

    if sentiment_col:
        st.subheader("😊 Sentiment Distribution")
        st.plotly_chart(
            px.pie(df, names=sentiment_col),
            use_container_width=True
        )

    with st.expander("📄 View Raw Data"):
        st.dataframe(df)

else:
    st.info("⬆️ Upload CSV file to view dashboard insights")

import streamlit as st
import re

st.set_page_config(page_title="E-commerce Support Chatbot", layout="centered")

st.title("🛍️ E-commerce FAQ Chatbot")

# ---------------- FAQ KNOWLEDGE BASE ---------------- #
FAQS = {
    "refund_upi": "If you paid using UPI, the refund will be credited back to the same UPI-linked bank account within 3–5 business days.",
    "refund_card": "For credit/debit card payments, refunds are processed back to the same card within 5–7 business days.",
    "refund_wallet": "If paid via wallet, the refund will be credited to your wallet balance.",
    "refund_shipping": "Shipping charges are usually non-refundable unless the product was defective or incorrect.",
    "refund_general": "Yes, refunds are available as per the return policy after the product is picked up.",
    "order_tracking": "You can track your order by going to **My Orders → Order Details → Track Order** in your account.",
    "order_delay": "If your order is delayed, please check the latest delivery date in your order details.",
    "emi": "Yes, EMI payment options are available on select credit cards during checkout.",
    "payment_methods": "We support UPI, credit card, debit card, net banking, and wallet payments.",
    "account_update": "You can update your account details from **My Account → Profile Settings**.",
    "large_appliance": "Large appliances are delivered by trained professionals with scheduled doorstep delivery and installation.",
    "default": "Sorry, I couldn't find an exact answer. Please try rephrasing your question."
}

# ---------------- INTENT DETECTION ---------------- #
def detect_intent(user_input):
    text = user_input.lower()

    if "refund" in text:
        if "upi" in text:
            return "refund_upi"
        elif "card" in text or "debit" in text or "credit" in text:
            return "refund_card"
        elif "wallet" in text or "bank" in text:
            return "refund_wallet"
        elif "shipping" in text:
            return "refund_shipping"
        else:
            return "refund_general"

    if "where is my order" in text or "track" in text:
        return "order_tracking"

    if "delayed" in text or "late" in text:
        return "order_delay"

    if "emi" in text:
        return "emi"

    if "payment" in text or "pay" in text:
        return "payment_methods"

    if "account" in text or "update" in text:
        return "account_update"

    if "large appliance" in text or "washing machine" in text or "refrigerator" in text:
        return "large_appliance"

    return "default"

# ---------------- CHAT UI ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    intent = detect_intent(user_input)
    bot_reply = FAQS.get(intent, FAQS["default"])

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
