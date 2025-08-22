from fastapi import FastAPI
from pydantic import BaseModel
from app.qa_engine import ask_question
import re

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(req: QueryRequest):
    try:
        response, grouped = ask_question(req.query)

        references = [
            f"{k} — {v['summary']}" if v["summary"] else k
            for k, v in sorted(
                grouped.items(),
                key=lambda x: int(re.findall(r'\d+', x[0])[0]) if re.search(r'\d+', x[0]) else 9999
            )
        ]

        return {
            "response": response,
            "references": references
        }

    except Exception as e:
        return {
            "response": f"⚠️ Internal error: {str(e)}",
            "references": []
        }
