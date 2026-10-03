"""Validate annual choice-offering exports before canonical loading."""
import argparse, json
from pathlib import Path

REQUIRED={"offering_id","admission_year","group","choice_code","program_id","university_id","course_type","selection_method","source_id","status"}

def load(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def validate(rows):
    errors=[]; seen=set()
    for i,row in enumerate(rows,1):
        missing=sorted(REQUIRED-set(row))
        if missing: errors.append({"row":i,"error":"missing_fields","fields":missing})
        key=(row.get("admission_year"),row.get("group"),row.get("choice_code"))
        if key in seen: errors.append({"row":i,"error":"duplicate_choice_code","key":key})
        seen.add(key)
        if row.get("status")=="verified" and not row.get("source_locator"):
            errors.append({"row":i,"error":"verified_without_locator"})
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    args=ap.parse_args()
    rows=load(args.input)
    errors=validate(rows)
    print(json.dumps({"ok":not errors,"rows":len(rows),"errors":errors},ensure_ascii=False,indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":
    main()
