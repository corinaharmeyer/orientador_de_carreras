from dataclasses import dataclass
from typing import List


@dataclass
class UserProfile:
    interests: List[str]
    skills: List[str]
    math: int
    communication: int
    creativity: int
    people_work: int
    teamwork: int


@dataclass
class CareerScore:
    career: str
    score: float
    reasons: List[str]
    cautions: List[str]
