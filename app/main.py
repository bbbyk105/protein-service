from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

from app.services.uniprot import fetch_uniprot_core, fetch_pdb_ids
from app.services.alphafold import fetch_alphafold_models
from app.services.pdb import download_mmCIF_batch
from app.compute import analyze_structures
from app.util import uniq

app = FastAPI(title="Protein Analysis Service")


@app.get("/health")
def health():
    return {"ok": True}


class AnalyzeReq(BaseModel):
    uniprot_ids: List[str] = Field(..., description="UniProt accession list")
    method: str = Field("X-ray", description="X-ray|EM|NMR")
    seq_ratio: int = Field(20, ge=1, le=100)
    negative_pdbids: Optional[List[str]] = Field(default_factory=list)


class AnalyzeRes(BaseModel):
    results: list
    warnings: List[str] = []


@app.post("/analyze", response_model=AnalyzeRes)
def analyze(req: AnalyzeReq):
    warnings = []
    out = []

    ids = uniq([s.strip() for s in req.uniprot_ids if s and s.lower() != "undefined"])
    for uid in ids:
        # 1) UniProt 概要
        core = fetch_uniprot_core(uid)
        if not core:
            warnings.append(f"{uid}: UniProt entry not found")
            out.append({"uniprot_id": uid, "status": "not_found"})
            continue

        # 2) UniProt cross-ref から PDB ID を収集（method で絞る）
        pdb_ids = fetch_pdb_ids(uid, method=req.method)
        # 除外
        negset = set(map(str.upper, req.negative_pdbids or []))
        pdb_ids = [p for p in pdb_ids if p.upper() not in negset]

        # 3) PDB mmCIF をDL（キャッシュ）
        cif_paths = download_mmCIF_batch(pdb_ids)

        # 4) PDB が乏しい場合は AlphaFold をフォールバック取得
        af_models = []
        if len(cif_paths) < 2:
            af_models = fetch_alphafold_models(uid)

        # 5) 解析（現状は雛形）
        analysis = analyze_structures(
            uniprot_id=uid,
            method=req.method,
            seq_ratio=req.seq_ratio,
            cif_paths=cif_paths,
            alphafold=af_models,
        )

        out.append(
            {
                "uniprot_id": uid,
                "core": core,
                "pdb_ids": pdb_ids,
                "analysis": analysis,
                "status": "ok",
            }
        )

        if not pdb_ids and not af_models:
            warnings.append(f"{uid}: no PDB/AlphaFold models available")

    return {"results": out, "warnings": warnings}
