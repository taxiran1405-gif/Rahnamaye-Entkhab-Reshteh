"""Historical cutoff backtest utilities.

The current seed is reported-cutoff data, not official outcomes. The script therefore
measures directional ranking behavior and data coverage; it does not claim calibrated
real-world admission probabilities until outcome-linked data are available.
"""
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[1]

def load_rows(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

def group_key(row):
    return (row["program_id"],row["university_id"],row["course_type"],row["quota_type"],row["region"])

def summarize(rows):
    by=defaultdict(list)
    for row in rows:
        by[group_key(row)].append(row)
    summary=[]
    for key,items in sorted(by.items()):
        cuts=[x["cutoff_rank"] for x in items]
        years=sorted({x["data_year"] for x in items})
        summary.append({
            "key":key,
            "n":len(items),
            "years":years,
            "cutoff_min":min(cuts),
            "cutoff_max":max(cuts),
            "cutoff_mean":mean(cuts),
        })
    return summary

def main():
    path=ROOT/"data/admission-observations-1404.seed.jsonl"
    rows=load_rows(path)
    summary=summarize(rows)
    years=sorted({r["data_year"] for r in rows})
    print(json.dumps({
        "status":"coverage_audit_only",
        "rows":len(rows),
        "years":years,
        "groups":len(summary),
        "notes":[
            "Seed values are provisional reported cutoffs.",
            "Calibration requires historical outcomes or adequate outcome-linked observations.",
            "Five-year backtest is incomplete until 1400-1403 canonical observations are imported."
        ]
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
