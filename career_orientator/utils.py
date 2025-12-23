import re
from typing import List


def normalize(text: str) -> str:
    """
    Normaliza texto para matching:
    - minúsculas
    - espacios -> _
    - quita acentos/símbolos dejando [a-z0-9_]
    """
    text = (text or "").lower().strip()
    text = re.sub(r"\s+", "_", text)
    return re.sub(r"[^a-z0-9_]", "", text)


def split_pipe(text: str) -> List[str]:
    """Convierte 'a|b|c' a ['a','b','c'] normalizado."""
    if not text:
        return []
    return [normalize(x) for x in text.split("|") if x.strip()]


def parse_csv_list(text: str) -> List[str]:
    """Convierte 'a, b, c' a lista normalizada."""
    if not text:
        return []
    out = []
    for x in text.split(","):
        nx = normalize(x)
        if nx:
            out.append(nx)
    return out


def clamp_1_3(x: int) -> int:
    return max(1, min(3, int(x)))


def yes_no_to_int(x: str) -> int:
    return 1 if (x or "").strip().lower() in {"s", "si", "sí", "y", "yes"} else 0
