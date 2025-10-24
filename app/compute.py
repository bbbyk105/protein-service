import os, json
from datetime import datetime
from typing import List, Dict, Any

ART_ROOT = "data/artifacts"


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def analyze_structures(
    uniprot_id: str,
    method: str,
    seq_ratio: int,
    cif_paths: List[str],
    alphafold: List[Dict],
) -> Dict[str, Any]:
    """
    解析の表面API。現段階ではダミーの集計と成果物の雛形生成のみ。
    後でノートのロジック（距離・cis検出）をここに差し込み。
    """
    outdir = os.path.join(ART_ROOT, uniprot_id)
    _ensure_dir(outdir)

    # --- ダミー成果物（雛形） ---
    # cis.csv
    cis_csv = os.path.join(outdir, "cis.csv")
    with open(cis_csv, "w") as f:
        f.write("res1,res2,dist,score,chains\n")
        f.write("45,46,3.05,2.7,A|B|C\n")

    # distance.csv
    distance_csv = os.path.join(outdir, "distance.csv")
    with open(distance_csv, "w") as f:
        f.write("i,j,mean_dist,std_dist\n")
        f.write("1,2,3.10,0.15\n")

    # results.json（KPIまとめ）
    results_json = os.path.join(outdir, "results.json")
    summary = {
        "uniprot_id": uniprot_id,
        "method": method,
        "seq_ratio": seq_ratio,
        "inputs": {
            "pdb_cifs": cif_paths,
            "alphafold_models": alphafold[:1],  # 要約
        },
        "kpi": {
            "cis_count": 1,
            "cis_per_length_pct": None,
            "avg_distance_score": None,
        },
        "artifacts": {
            "results_json": results_json,
            "cis_csv": cis_csv,
            "distance_csv": distance_csv,
            "heatmap_png": None,  # 後で追加
        },
        "ts": datetime.utcnow().isoformat() + "Z",
    }
    with open(results_json, "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return summary
