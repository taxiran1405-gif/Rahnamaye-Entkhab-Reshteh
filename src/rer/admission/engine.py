"""Transparent, deterministic v0 admission heuristic."""
from dataclasses import dataclass
from math import exp
from statistics import median
from typing import Iterable, Optional

@dataclass(frozen=True)
class AdmissionObservation:
    year: int
    cutoff_rank: float
    source_confidence: float = 1.0
    sample_weight: float = 1.0

@dataclass(frozen=True)
class ProbabilityBand:
    lower: float
    upper: float
    midpoint: float
    n: int
    cutoff_median: Optional[float]
    cutoff_min: Optional[float]
    cutoff_max: Optional[float]
    calibration_status: str = "uncalibrated"

def _logistic(x: float) -> float:
    return 1.0 / (1.0 + exp(-x))

def estimate_probability_band(rank: float, observations: Iterable[AdmissionObservation]) -> ProbabilityBand:
    obs = list(observations)
    if not obs:
        return ProbabilityBand(0.0,0.0,0.0,0,None,None,None)
    scored=[]
    for o in obs:
        margin=(o.cutoff_rank-rank)/max(abs(o.cutoff_rank),1.0)
        p=_logistic(5.0*margin)
        w=max(o.source_confidence,0.0)*max(o.sample_weight,0.0)
        scored.append((p,w))
    denom=sum(w for _,w in scored) or 1.0
    midpoint=sum(p*w for p,w in scored)/denom
    vals=[p for p,_ in scored]
    spread=max(vals)-min(vals) if len(vals)>1 else 0.20
    half=min(0.45,max(0.08,spread/2.0))
    cuts=[o.cutoff_rank for o in obs]
    return ProbabilityBand(max(0.0,midpoint-half),min(1.0,midpoint+half),midpoint,len(obs),median(cuts),min(cuts),max(cuts))
