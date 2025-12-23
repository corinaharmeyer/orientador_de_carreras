import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union

from .models import UserProfile, CareerScore



def save_run(user: UserProfile, recs: List[CareerScore], out_dir: Union[str, Path] = "runs") -> Path:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S")
    path = out_path / f"run_{ts}.json"

    payload: Dict[str, Any] = {
        "created_at": now.isoformat(),
        "user_profile": asdict(user),
        "recommendations": [
            {"career": r.career, "score": r.score, "reasons": r.reasons, "cautions": r.cautions}
            for r in recs
        ],
    }

    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
