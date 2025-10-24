import os, pathlib, requests
from typing import List
from app.util import backoff

CACHE = pathlib.Path("data/pdb")
CACHE.mkdir(parents=True, exist_ok=True)


@backoff()
def _get(url, timeout=20):
    return requests.get(url, timeout=timeout)


def download_mmCIF(pdb_id: str) -> str | None:
    fn = CACHE / f"{pdb_id}.cif"
    if fn.exists() and fn.stat().st_size > 0:
        return str(fn)
    url = f"https://files.rcsb.org/download/{pdb_id}.cif"
    r = _get(url)
    if r.status_code == 200 and r.content:
        fn.write_bytes(r.content)
        return str(fn)
    return None


def download_mmCIF_batch(pdb_ids: List[str]) -> List[str]:
    out = []
    for pid in pdb_ids:
        p = download_mmCIF(pid)
        if p:
            out.append(p)
    return out
