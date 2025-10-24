import requests
from typing import Dict, List, Optional
from app.util import backoff

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "protein-service/1.0"})


@backoff()
def _get(url, timeout=15):
    return SESSION.get(url, timeout=timeout)


def fetch_uniprot_core(uniprot_id: str) -> Optional[Dict]:
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    r = _get(url)
    if r.status_code != 200:
        return None
    j = r.json()
    name = (
        j.get("proteinDescription", {})
        .get("recommendedName", {})
        .get("fullName", {})
        .get("value")
    )
    length = j.get("sequence", {}).get("length")
    organism = j.get("organism", {}).get("scientificName")
    return {"id": uniprot_id, "name": name, "length": length, "organism": organism}


def fetch_pdb_ids(uniprot_id: str, method: str = "") -> List[str]:
    """
    UniProt cross-references から PDB ID を抽出。
    method が指定されていれば（"X-ray" "EM" "NMR"）一致するもののみ。
    """
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    r = _get(url)
    if r.status_code != 200:
        return []
    j = r.json()
    xrefs = j.get("uniProtKBCrossReferences", [])
    out = []
    for x in xrefs:
        if x.get("database") != "PDB":
            continue
        props = {p["key"]: p.get("value") for p in x.get("properties", [])}
        meth = props.get("Method") or props.get("method")
        if not method or not meth or meth.lower() == method.lower():
            pid = x.get("id")
            if pid:
                out.append(pid)
    # 例: 1ABC_A のようにチェーン付きのことがあるので4文字を抜き出す
    out = [p[:4].upper() for p in out if len(p) >= 4]
    # 4文字以外のゴミを落とす
    out = [p for p in out if len(p) == 4 and p.isalnum()]
    return sorted(list(set(out)))
