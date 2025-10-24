import requests


def fetch_uniprot_core(uniprot_id: str):
    """UniProtの基本情報を取得"""
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()
    return {
        "id": uniprot_id,
        "protein_name": data.get("proteinDescription", {})
        .get("recommendedName", {})
        .get("fullName", {})
        .get("value"),
        "organism": data.get("organism", {}).get("scientificName"),
        "sequence_length": data.get("sequence", {}).get("length"),
    }
