"""Coverage audit for historical admission observations.

This is intentionally not a calibrated probability model. It refuses to call an
incomplete year range a five-year backtest.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_YEARS={1400,1401,1402,1403,1404}

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
        summary.append({
            "key":key,"n":len(items),"years":sorted({x["data_year"] for x in items}),
            "cutoff_min":min(cuts),"cutoff_max":max(cuts),"cutoff_mean":mean(cuts)
        })
    return summary

def audit(rows, required_years=EXPECTED_YEARS):
    years={r["data_year"] for r in rows}
    missing=sorted(required_years-years)
    return {
        "status":"complete" if not missing else "incomplete",
        "years_present":sorted(years),
        "years_missing":missing,
        "rows":len(rows),
        "groups":len(summarize(rows)),
        "five_year_backtest_allowed":not missing
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default=str(ROOT/"data/admission-observations-1404.seed.jsonl"))
    ap.add_argument("--require-five-year",action="store_true")
    args=ap.parse_args()
    result=audit(load_rows(args.input))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.require_five_year and not result["five_year_backtest_allowed"]:
        raise SystemExit(2)

if __name__=="__main__":
    main()
