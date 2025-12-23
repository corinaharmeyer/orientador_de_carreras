import json
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

# Ensure project package is importable when running tests directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from career_orientator.persistence import save_run
from career_orientator.models import UserProfile, CareerScore


def test_save_run_creates_file_and_payload(tmp_path):
    user = UserProfile(
        interests=["math"],
        skills=["python"],
        math=5,
        communication=4,
        creativity=3,
        people_work=2,
        teamwork=1,
    )

    recs = [CareerScore(career="Engineer", score=0.95, reasons=["good fit"], cautions=["long hours"]) ]

    out_dir = tmp_path / "runs"
    path = save_run(user, recs, out_dir=str(out_dir))

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["user_profile"] == asdict(user)
    assert len(data["recommendations"]) == 1

    rec = data["recommendations"][0]
    assert rec["career"] == "Engineer"
    assert abs(rec["score"] - 0.95) < 1e-6

    ts_from_filename = path.stem.split("_", 1)[1]
    created = datetime.fromisoformat(data["created_at"])
    assert created.strftime("%Y%m%d_%H%M%S") == ts_from_filename
