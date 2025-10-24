import requests
from typing import List, Dict
from app.util import backoff

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "protein-service/1.0"})


@backoff()
def _get(url, timeout=15):
    return SESSION.get(url, timeout=timeout)


def fetch_alphafold_models(uniprot_id: str) -> List[Dict]:
    """
    AlphaFold API からモデル一覧を取得。
    戻り値例: [{"pdbUrl": "...", "cifUrl": "...", "uniprot_id": "..."}]
    """
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    r = _get(url)
    if r.status_code != 200:
        return []
    try:
        arr = r.json()
    except Exception:
        return []
    if not isinstance(arr, list):
        return []
    out = []
    for m in arr:
        out.append(
            {
                "uniprot_id": m.get("uniprot_id"),
                "pdbUrl": m.get("pdbUrl"),
                "cifUrl": m.get("cifUrl"),
                "plddt": m.get("plddt") or m.get("pLDDT"),
            }
        )
    return out
