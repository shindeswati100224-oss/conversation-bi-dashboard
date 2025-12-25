# 📊 Conversation BI Dashboard  
End-to-End E-commerce Customer Support Analytics

---

## 🔍 Project Overview
This project is an **end-to-end Conversation Business Intelligence (BI) system** that extracts, analyzes, and visualizes customer support conversations from e-commerce platforms.

It helps stakeholders understand:
- Customer sentiment trends  
- Common issue categories (Delivery, Refund, Payment, etc.)  
- Overall customer support health using an interactive dashboard  

---

## 🏗️ Architecture
Web Scraping (BeautifulSoup)
↓
Data Cleaning & NLP (Python, Pandas)
↓
Sentiment & Issue Classification
↓
FastAPI Backend (REST APIs)
↓
Streamlit Dashboard (Visualization)

yaml
Copy code

---

## 🛠️ Tech Stack
- Python 3.9+
- BeautifulSoup – Web scraping  
- Pandas – Data processing  
- NLP (Rule-based / ML-ready)  
- FastAPI – Backend API  
- Streamlit – Dashboard  
- GitHub & Streamlit Cloud – Deployment  

---

## 📁 Project Structure
conversation-bi-dashboard/
│
├── api.py
├── dashboard.py
├── conversation_bi_ai_output.csv
├── requirements.txt
├── README.md
└── .gitignore

yaml
Copy code

---

## 📊 Dashboard Features
- Total conversation count  
- Positive vs Negative sentiment metrics  
- Sentiment distribution charts  
- Filters by Sentiment and Issue Type  
- CSV download of filtered data  
- Clean and professional BI layout  

---

## 🚀 How to Run Locally

### Step 1: Clone Repository
```bash
git clone https://github.com/shindeswati100224-oss/conversation-bi-dashboard.git
cd conversation-bi-dashboard
Step 2: Create & Activate Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate
Step 3: Install Dependencies
bash
Copy code
pip install -r requirements.txt
Step 4: Run FastAPI Backend
bash
Copy code
uvicorn api:app --reload
API will be available at:

cpp
Copy code
http://127.0.0.1:8000
Step 5: Run Streamlit Dashboard
bash
Copy code
streamlit run dashboard.py
Dashboard will open at:

arduino
Copy code
http://localhost:8501
📈 Sample Insights (500 Records)
Total Conversations: 500

Negative Sentiment: 409

Positive Sentiment: 91

Top Issue Categories:

Other

Refund

Delivery

Payment

🌐 Live Deployment
The dashboard is deployed using Streamlit Cloud.

Live URL: (Add your Streamlit Cloud link here)

🎯 Use Cases
Customer Support Analytics

Customer Experience (CX) Improvement

Issue Trend Identification

Business Decision Support

🔮 Future Enhancements
Machine learning–based sentiment analysis

Time-series trend analysis

Multi-source data ingestion

Advanced BI dashboards

👩‍💻 Author
Swati Shinde
Python | Data Analytics | BI | AI

GitHub: https://github.com/shindeswati100224-oss

