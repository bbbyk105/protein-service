from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Protein Analysis Service")


@app.get("/health")
def health():
    return {"ok": True}


class AnalyzeReq(BaseModel):
    uniprot_ids: List[str]
    method: str = "X-ray"
    seq_ratio: int = 20
    negative_pdbids: Optional[List[str]] = []


@app.post("/analyze")
def analyze(req: AnalyzeReq):
    results = [
        {
            "uniprot_id": uid,
            "method": req.method,
            "seq_ratio": req.seq_ratio,
            "status": "ok",
        }
        for uid in req.uniprot_ids
        if uid and uid.lower() != "undefined"
    ]
    return {"results": results, "warnings": []}
