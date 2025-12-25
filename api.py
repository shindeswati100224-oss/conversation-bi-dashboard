from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Conversation BI API")

# SAFE CSV LOAD
try:
    df = pd.read_csv("conversation_bi_ai_output.csv", encoding="utf-8")
except Exception as e:
    df = pd.DataFrame()
    load_error = str(e)
else:
    load_error = None


@app.get("/")
def home():
    return {"message": "Conversation BI API is running"}


@app.get("/summary")
def summary():
    # If CSV failed to load
    if load_error:
        return {
            "status": "error",
            "reason": "CSV could not be loaded",
            "error": load_error
        }

    # If CSV loaded but empty
    if df.empty:
        return {
            "status": "error",
            "reason": "CSV loaded but DataFrame is empty",
            "columns": []
        }

    # SAFE SUMMARY (NO CRASH POSSIBLE)
    return {
        "status": "success",
        "total_rows": int(len(df)),
        "columns": list(df.columns),
        "sentiment_counts": df["sentiment"].fillna("Unknown").value_counts().to_dict(),
        "issue_type_counts": df["issue_type"].fillna("Unknown").value_counts().to_dict(),
        "source_counts": df["source"].fillna("Unknown").value_counts().to_dict()
    }


@app.get("/data")
def data(limit: int = 20):
    if df.empty:
        return []
    return df.head(limit).to_dict(orient="records")
