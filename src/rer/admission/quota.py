"""Quota-aware rank selection.

National rank and final quota rank are separate dimensions.
"""
from dataclasses import dataclass
from typing import Iterable, Optional

REGION_QUOTA="منطقه"

@dataclass(frozen=True)
class QuotaRank:
    quota_type: str
    rank: int
    region: Optional[str] = None
    is_final: bool = True
    verification_status: str = "provisional"

@dataclass(frozen=True)
class RankContext:
    national_rank: int
    final_quota_type: str
    final_quota_rank: Optional[int]
    region: Optional[str]
    quota_ranks: tuple[QuotaRank, ...] = ()

@dataclass(frozen=True)
class ComparisonDecision:
    comparable: bool
    rank: Optional[int]
    reason_code: str

def _same_region(a: Optional[str], b: Optional[str]) -> bool:
    return a is not None and b is not None and str(a) == str(b)

def select_candidate_rank(ctx: RankContext, candidate_quota_type: str,
                          candidate_region: Optional[str]) -> ComparisonDecision:
    if ctx.final_quota_rank is None:
        return ComparisonDecision(False, None, "NO_FINAL_QUOTA_RANK")
    if candidate_quota_type != ctx.final_quota_type:
        return ComparisonDecision(False, None, "QUOTA_TYPE_MISMATCH")
    if candidate_quota_type == REGION_QUOTA and not _same_region(ctx.region, candidate_region):
        return ComparisonDecision(False, None, "REGION_MISMATCH")
    return ComparisonDecision(True, ctx.final_quota_rank, "EXACT_FINAL_QUOTA_RANK")

def filter_comparable_observations(ctx: RankContext, observations: Iterable[dict]) -> list[dict]:
    result=[]
    for obs in observations:
        if obs.get("quota_type") != ctx.final_quota_type:
            continue
        if ctx.final_quota_type == REGION_QUOTA and not _same_region(ctx.region, str(obs.get("region"))):
            continue
        if obs.get("rank_basis") not in {"quota_rank","regional_rank","special_quota_rank","final_quota_rank"}:
            continue
        result.append(obs)
    return result
