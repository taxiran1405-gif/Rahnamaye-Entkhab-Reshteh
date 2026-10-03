"""Deterministic recommendation composition primitives for v0."""
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass(frozen=True)
class Candidate:
    option_id: str
    program_id: str
    university_id: str
    cell_group_id: str
    role_hint: str
    admission_midpoint: float
    confidence: float
    preference_scores: Dict[str, float] = field(default_factory=dict)
    evidence_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class RankedCandidate:
    option_id: str
    score: float
    admission_midpoint: float
    confidence: float
    role: str
    evidence_ids: List[str]

@dataclass(frozen=True)
class RecommendationCell:
    cell_group_id: str
    primary: RankedCandidate
    parallel: List[RankedCandidate]
    cover: List[RankedCandidate]

DEFAULT_WEIGHTS = {
    "major_interest": 25,
    "university_interest": 15,
    "city_interest": 10,
    "admission_probability": 25,
    "course_type": 10,
    "cost": 5,
    "job_market": 5,
    "distance": 3,
    "quality": 2,
}

def utility_score(candidate: Candidate, weights: Dict[str, float] | None = None) -> float:
    w = weights or DEFAULT_WEIGHTS
    total_w = sum(w.values()) or 1.0
    weighted = sum((w.get(k, 0.0) * candidate.preference_scores.get(k, 0.0)) for k in w)
    return weighted / total_w

def composite_score(candidate: Candidate, weights: Dict[str, float] | None = None) -> float:
    # admission_midpoint and preference inputs are both normalized to [0,1].
    utility = utility_score(candidate, weights)
    return 0.60 * utility + 0.40 * candidate.admission_midpoint

def rank_candidates(candidates: List[Candidate], weights: Dict[str, float] | None = None) -> List[RankedCandidate]:
    ranked = sorted(candidates, key=lambda c: (-composite_score(c, weights), -c.confidence, c.option_id))
    return [
        RankedCandidate(
            option_id=c.option_id,
            score=composite_score(c, weights),
            admission_midpoint=c.admission_midpoint,
            confidence=c.confidence,
            role=c.role_hint,
            evidence_ids=c.evidence_ids,
        )
        for c in ranked
    ]

def compose_cell(candidates: List[Candidate], weights: Dict[str, float] | None = None, max_parallel: int = 3, max_cover: int = 1) -> RecommendationCell:
    if not candidates:
        raise ValueError("cell requires at least one candidate")
    ranked = rank_candidates(candidates, weights)
    primary = ranked[0]
    rest = ranked[1:]
    parallel = [x for x in rest if x.role != "cover"][:max_parallel]
    cover = [x for x in rest if x.role == "cover"][:max_cover]
    return RecommendationCell(candidates[0].cell_group_id, primary, parallel, cover)
