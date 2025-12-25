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

# =================================================
# FLIPKART FAQ CHATBOT (NO CSV, EMBEDDED DATA)
# =================================================
st.markdown("---")
st.header("🤖 Flipkart FAQ Chatbot")

st.write(
    "Ask questions related to **delivery, refund, return, payment** "
    "based on public Flipkart FAQ information."
)

FLIPKART_FAQ_TEXT = [
    "You can return most items within 7 days of delivery.",
    "Refunds are initiated once the returned item is received.",
    "Refunds are credited to the original payment method.",
    "Delivery usually takes 3 to 5 business days.",
    "Cash on Delivery is available for eligible products.",
    "Orders can be cancelled before shipment.",
    "Replacement is available for damaged or defective items.",
    "Refunds for prepaid orders take 5 to 7 working days.",
    "You can track your shipment using the tracking ID.",
    "Items must be returned in original condition with packaging.",
    "Shipping charges may apply to certain products.",
    "Payment options include UPI, credit card, debit card and net banking.",
    "Refund timelines depend on the payment method used.",
    "Partial refunds may be issued for promotional offers.",
    "If your order is delayed, check the order status in your account."
]

faq_df = pd.DataFrame(FLIPKART_FAQ_TEXT, columns=["text"])

vectorizer = TfidfVectorizer(stop_words="english")
faq_vectors = vectorizer.fit_transform(faq_df["text"])

def get_faq_answer(question):
    user_vec = vectorizer.transform([question])
    similarity = cosine_similarity(user_vec, faq_vectors)

    best_index = similarity.argmax()
    best_score = similarity[0][best_index]

    if best_score < 0.25:
        return "Sorry, I couldn't find a relevant answer. Please rephrase your question."

    return faq_df.iloc[best_index]["text"]

# =================================================
# CHAT UI
# =================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input(
    "Ask a question (example: How will I get my refund?)"
)

if st.button("Ask FAQ"):
    if user_input:
        reply = get_faq_answer(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", reply))

for role, message in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
