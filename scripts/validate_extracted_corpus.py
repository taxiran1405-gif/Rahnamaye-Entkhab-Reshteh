"""Validate one yearly historical booklet extraction artifact."""
import argparse
import json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--year",required=True,type=int)
    args=ap.parse_args()

    data=json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    matches=[x for x in data if int(x.get("year",-1))==args.year]
    if len(matches)!=1:
        raise SystemExit(f"expected exactly one manifest row for {args.year}, got {len(matches)}")

    row=matches[0]
    required={"year","status","source_used","sha256","bytes","pages","tables","candidate_rows"}
    missing=sorted(required-set(row))
    if missing:
        raise SystemExit(f"manifest missing fields: {missing}")
    if row["status"]!="extracted":
        raise SystemExit(f"extraction status for {args.year}: {row['status']}")

    year_dir=Path(args.manifest).parent/str(args.year)
    required_files=[
        year_dir/f"{args.year}-pages.jsonl",
        year_dir/f"{args.year}-tables.jsonl",
        year_dir/f"{args.year}-candidate-rows.jsonl",
        year_dir/f"math-selection-{args.year}.pdf",
    ]
    missing_files=[str(p) for p in required_files if not p.exists()]
    if missing_files:
        raise SystemExit(f"missing artifact files: {missing_files}")

    print(json.dumps({
        "ok":True,
        "year":args.year,
        "pages":row["pages"],
        "tables":row["tables"],
        "candidate_rows":row["candidate_rows"],
        "sha256":row["sha256"]
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
