"""Calibration metrics for binary admission outcomes.

All functions expect probabilities in [0, 1] and observed outcomes in {0, 1}.
No metric is a substitute for quota/region-aware data preparation.
"""
from math import log
from typing import Iterable, Sequence

def _validate(probabilities: Sequence[float], outcomes: Sequence[int]) -> None:
    if len(probabilities) != len(outcomes):
        raise ValueError("probabilities and outcomes must have equal length")
    if not probabilities:
        raise ValueError("at least one observation is required")
    if any(p < 0.0 or p > 1.0 for p in probabilities):
        raise ValueError("probabilities must be in [0,1]")
    if any(y not in (0, 1) for y in outcomes):
        raise ValueError("outcomes must be 0 or 1")

def brier_score(probabilities: Iterable[float], outcomes: Iterable[int]) -> float:
    p=list(probabilities); y=list(outcomes); _validate(p,y)
    return sum((pi-yi)**2 for pi,yi in zip(p,y))/len(p)

def log_loss(probabilities: Iterable[float], outcomes: Iterable[int], eps: float=1e-15) -> float:
    p=list(probabilities); y=list(outcomes); _validate(p,y)
    return -sum(yi*log(max(pi,eps))+(1-yi)*log(max(1-pi,eps)) for pi,yi in zip(p,y))/len(p)

def expected_calibration_error(probabilities: Iterable[float], outcomes: Iterable[int], bins: int=10) -> float:
    p=list(probabilities); y=list(outcomes); _validate(p,y)
    if bins < 1: raise ValueError("bins must be positive")
    total=len(p); ece=0.0
    for b in range(bins):
        lo=b/bins; hi=(b+1)/bins
        idx=[i for i,pi in enumerate(p) if (lo <= pi < hi) or (b==bins-1 and pi==hi)]
        if not idx: continue
        avg_p=sum(p[i] for i in idx)/len(idx)
        avg_y=sum(y[i] for i in idx)/len(idx)
        ece += len(idx)/total*abs(avg_p-avg_y)
    return ece

def calibration_summary(probabilities: Iterable[float], outcomes: Iterable[int]) -> dict:
    p=list(probabilities); y=list(outcomes); _validate(p,y)
    return {
        "n": len(p),
        "brier_score": brier_score(p,y),
        "log_loss": log_loss(p,y),
        "ece_10": expected_calibration_error(p,y,10),
        "outcome_rate": sum(y)/len(y),
        "status": "evaluated"
    }
