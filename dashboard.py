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
# FILE UPLOAD (Conversation Data)
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload conversation_bi_ai_output.csv",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # -------------------------------------------------
    # BASIC CLEANUP (safe)
    # -------------------------------------------------
    df.columns = df.columns.str.lower()

    # -------------------------------------------------
    # KPI METRICS
    # -------------------------------------------------
    total_conversations = len(df)

    negative_count = len(df[df["sentiment"].str.lower() == "negative"])
    positive_count = len(df[df["sentiment"].str.lower() == "positive"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Conversations", total_conversations)
    col2.metric("Negative Sentiment", negative_count)
    col3.metric("Positive Sentiment", positive_count)

    st.markdown("---")

    # -------------------------------------------------
    # FILTERS
    # -------------------------------------------------
    st.subheader("🔍 Filters")

    category_filter = st.selectbox(
        "Select Issue Category",
        ["All"] + sorted(df["category"].dropna().unique().tolist())
    )

    if category_filter != "All":
        df = df[df["category"] == category_filter]

    # -------------------------------------------------
    # CATEGORY DISTRIBUTION
    # -------------------------------------------------
    st.subheader("📌 Issue Category Distribution")

    category_chart = px.bar(
        df,
        x="category",
        title="Issues by Category",
        color="category"
    )

    st.plotly_chart(category_chart, use_container_width=True)

    # -------------------------------------------------
    # SENTIMENT DISTRIBUTION
    # -------------------------------------------------
    st.subheader("😊 Sentiment Distribution")

    sentiment_chart = px.pie(
        df,
        names="sentiment",
        title="Customer Sentiment Breakdown"
    )

    st.plotly_chart(sentiment_chart, use_container_width=True)

    # -------------------------------------------------
    # DATA PREVIEW
    # -------------------------------------------------
    with st.expander("📄 View Raw Conversation Data"):
        st.dataframe(df)

# =================================================
# FAQ CHATBOT SECTION
# =================================================
st.markdown("---")
st.header("🤖 Flipkart FAQ Chatbot")

st.write(
    "Ask questions related to **delivery, refund, return, payments** "
    "based on public Flipkart FAQ pages."
)

# -------------------------------------------------
# LOAD SCRAPED FAQ DATA
# -------------------------------------------------
try:
    faq_df = pd.read_csv("flipkart_faq_scraped.csv")

    vectorizer = TfidfVectorizer(stop_words="english")
    faq_vectors = vectorizer.fit_transform(faq_df["scraped_text"])

    def get_chatbot_answer(user_question):
        user_vec = vectorizer.transform([user_question])
        similarity = cosine_similarity(user_vec, faq_vectors)

        best_index = similarity.argmax()
        best_score = similarity[0][best_index]

        if best_score < 0.25:
            return "Sorry, I couldn't find an exact answer. Please try rephrasing."

        return faq_df.iloc[best_index]["scraped_text"]

    # -------------------------------------------------
    # CHAT UI
    # -------------------------------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input(
        "Ask your question (example: How will I get my refund?)"
    )

    if st.button("Ask"):
        if user_input:
            answer = get_chatbot_answer(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", answer))

    for role, message in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 Bot:** {message}")

except FileNotFoundError:
    st.warning(
        "⚠️ FAQ data file `flipkart_faq_scraped.csv` not found. "
        "Please add it to the project folder."
    )


