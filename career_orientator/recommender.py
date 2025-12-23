from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import UserProfile, CareerScore
from .utils import normalize, split_pipe


# ─────────────────────────────────────────────────────────────
# Ruta robusta al CSV (funciona desde cualquier punto de ejecución)
# ─────────────────────────────────────────────────────────────
DATA_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "careers.csv"
).as_posix()


# ─────────────────────────────────────────────────────────────
# Carga y validación del dataset
# ─────────────────────────────────────────────────────────────
def load_careers(data_path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(data_path)

    expected = {
        "career", "interests", "skills",
        "math", "communication", "creativity",
        "people_work", "teamwork",
    }
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en {data_path}: {sorted(missing)}")

    # Normalización consistente
    df["interests_list"] = df["interests"].apply(split_pipe)
    df["skills_list"] = df["skills"].apply(split_pipe)

    return df


# ─────────────────────────────────────────────────────────────
# Similitud numérica (0 a 1)
# ─────────────────────────────────────────────────────────────
def _numeric_similarity(user: UserProfile, df: pd.DataFrame) -> np.ndarray:
    user_vec = np.array(
        [
            user.math,
            user.communication,
            user.creativity,
            user.people_work,
            user.teamwork,
        ],
        dtype=float,
    )

    career_vecs = df[
        ["math", "communication", "creativity", "people_work", "teamwork"]
    ].astype(float).values

    dist = np.linalg.norm(career_vecs - user_vec, axis=1)

    # normalización conservadora
    return 1.0 - (dist / np.sqrt(45))


# ─────────────────────────────────────────────────────────────
# Recomendador principal
# ─────────────────────────────────────────────────────────────
def recommend(
    user: UserProfile,
    top_k: int = 5,
    data_path: str = DATA_PATH,
    w_interests: float = 0.45,
    w_skills: float = 0.45,
    w_numeric: float = 0.10,
) -> List[CareerScore]:

    df = load_careers(data_path)

    if df.empty:
        return []

    # límite lógico
    top_k = min(top_k, len(df))

    # vocabularios globales
    interests_vocab = sorted({x for row in df["interests_list"] for x in row})
    skills_vocab = sorted({x for row in df["skills_list"] for x in row})

    vec_int = CountVectorizer(vocabulary=interests_vocab, binary=True)
    vec_skl = CountVectorizer(vocabulary=skills_vocab, binary=True)

    user_interests = [normalize(x) for x in user.interests]
    user_skills = [normalize(x) for x in user.skills]

    Xc_int = vec_int.transform(df["interests_list"].apply(" ".join))
    Xu_int = vec_int.transform([" ".join(user_interests)])

    Xc_skl = vec_skl.transform(df["skills_list"].apply(" ".join))
    Xu_skl = vec_skl.transform([" ".join(user_skills)])

    s_int = cosine_similarity(Xu_int, Xc_int)[0]
    s_skl = cosine_similarity(Xu_skl, Xc_skl)[0]
    s_num = _numeric_similarity(user, df)

    score = (
        w_interests * s_int
        + w_skills * s_skl
        + w_numeric * s_num
    )

    results: List[CareerScore] = []
    top_idx = np.argsort(score)[::-1][:top_k]

    for i in top_idx:
        row = df.iloc[i]

        shared_int = sorted(set(user_interests) & set(row["interests_list"]))
        shared_skl = sorted(set(user_skills) & set(row["skills_list"]))

        reasons: List[str] = []
        cautions: List[str] = []

        if shared_int:
            reasons.append(f"Intereses en común: {', '.join(shared_int[:6])}")
        else:
            cautions.append("Pocos intereses en común (podría no motivarte).")

        if shared_skl:
            reasons.append(f"Habilidades en común: {', '.join(shared_skl[:6])}")
        else:
            cautions.append("Pocas habilidades en común (podrías necesitar aprender más).")

        def flag(name: str, u: int, c: int):
            if abs(u - c) >= 2:
                cautions.append(
                    f"Diferencia fuerte en {name} (vos: {u}, carrera: {c})."
                )

        flag("matemática", user.math, int(row["math"]))
        flag("comunicación", user.communication, int(row["communication"]))
        flag("creatividad", user.creativity, int(row["creativity"]))

        results.append(
            CareerScore(
                career=str(row["career"]),
                score=float(score[i]),
                reasons=reasons,
                cautions=cautions,
            )
        )

    return results
