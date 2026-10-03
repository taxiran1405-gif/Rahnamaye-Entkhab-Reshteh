"""Coverage report for annual mathematics choice-offering and admission history."""
import argparse
import json
from pathlib import Path

def load(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def report(offering_rows, admission_rows):
    result={}
    years=sorted({r.get("admission_year") for r in offering_rows}|{r.get("data_year") for r in admission_rows})
    for year in years:
        o=[r for r in offering_rows if r.get("admission_year")==year and r.get("group")=="math"]
        a=[r for r in admission_rows if r.get("data_year")==year and r.get("group")=="math"]
        result[str(year)]={
            "offering_rows":len(o),
            "unique_choice_codes":len({r.get("choice_code") for r in o}),
            "admission_rows":len(a),
            "admission_programs":len({r.get("program_id") for r in a}),
            "admission_universities":len({r.get("university_id") for r in a}),
            "admission_quota_regions":len({(r.get("quota_type"),str(r.get("region"))) for r in a})
        }
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--offerings",required=True)
    ap.add_argument("--admissions",required=True)
    args=ap.parse_args()
    print(json.dumps(report(load(args.offerings),load(args.admissions)),ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
