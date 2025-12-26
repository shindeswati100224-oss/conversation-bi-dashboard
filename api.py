from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Conversation BI API")

# Load CSV
try:
    df = pd.read_csv("conversation_bi_ai_output.csv")
except Exception as e:
    df = pd.DataFrame()
    load_error = str(e)
else:
    load_error = None

@app.get("/")
def root():
    return {"message": "Conversation BI API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/summary")
def summary():
    if load_error:
        return {"status": "error", "error": load_error}

    if df.empty:
        return {"status": "error", "reason": "Data empty"}

    return {
        "status": "success",
        "total_rows": int(len(df)),
        "sentiment_counts": df["sentiment"].fillna("Unknown").value_counts().to_dict(),
        "issue_type_counts": df["issue_type"].fillna("Unknown").value_counts().to_dict(),
        "source_counts": df["source"].fillna("Unknown").value_counts().to_dict(),
    }

@app.get("/data")
def data(limit: int = 20):
    if df.empty:
        return []
    return df.head(limit).to_dict(orient="records")


