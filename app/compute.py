from typing import List


def analyze_structures(
    uniprot_id: str, pdb_files: List[str], seq_ratio: int, method: str
):
    """
    ここにcis結合や距離スコア計算ロジックを入れる。
    今はダミーで返す。
    """
    # TODO: あなたのColabノートの処理をここに移植
    return {
        "uniprot_id": uniprot_id,
        "pdb_files": pdb_files,
        "seq_ratio": seq_ratio,
        "method": method,
        "avg_distance_score": 0.83,  # 仮データ
        "cis_bond_count": 4,
    }
