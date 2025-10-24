import requests


def fetch_alphafold_model(uniprot_id: str):
    """AlphaFold モデル情報を取得"""
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    res = requests.get(url, timeout=10)
    if res.status_code != 200:
        return None
    data = res.json()
    if not data:
        return None
    return {
        "model_url": data[0].get("pdbUrl"),
        "confidence": data[0].get("plddt"),
    }
