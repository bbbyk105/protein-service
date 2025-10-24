import os, requests


def download_pdb(pdb_id: str, out_dir="data/pdb"):
    os.makedirs(out_dir, exist_ok=True)
    url = f"https://files.rcsb.org/download/{pdb_id}.cif"
    out_path = os.path.join(out_dir, f"{pdb_id}.cif")
    res = requests.get(url, timeout=10)
    if res.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(res.content)
        return out_path
    return None
