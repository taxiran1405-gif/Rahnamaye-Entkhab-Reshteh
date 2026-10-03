"""Validate anonymized outcome records before calibration."""
import argparse,json
from pathlib import Path

REQUIRED={"candidate_anonymous_id","admission_year","quota_type","actual_quota_rank","accepted"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    args=ap.parse_args()
    rows=[json.loads(x) for x in Path(args.input).read_text(encoding="utf-8").splitlines() if x.strip()]
    errors=[]
    for i,row in enumerate(rows,1):
        missing=sorted(REQUIRED-set(row))
        if missing: errors.append({"row":i,"error":"missing_required","fields":missing})
        if row.get("accepted") and not row.get("choice_code"):
            errors.append({"row":i,"error":"accepted_without_choice_code"})
        if row.get("actual_quota_rank") is None:
            errors.append({"row":i,"error":"missing_actual_quota_rank"})
    print(json.dumps({"ok":not errors,"rows":len(rows),"errors":errors},ensure_ascii=False,indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":
    main()
