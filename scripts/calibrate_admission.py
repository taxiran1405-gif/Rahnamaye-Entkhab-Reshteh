"""Outcome-linked admission calibration runner.

Input JSONL requires:
  predicted_probability: number in [0,1]
  accepted: 0 or 1
and should carry quota_type, region, admission_year and candidate identifiers.
The runner refuses an empty input and records scope so metrics are reproducible.
"""
import argparse
import json
from pathlib import Path
from rer.calibration.metrics import calibration_summary

def load(path):
    rows=[json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    if not rows: raise ValueError("no outcome-linked rows")
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",default="-")
    args=ap.parse_args()
    rows=load(args.input)
    required={"predicted_probability","accepted"}
    missing=sorted(required-set(rows[0]))
    if missing: raise ValueError(f"missing fields: {missing}")
    probs=[float(r["predicted_probability"]) for r in rows]
    ys=[int(r["accepted"]) for r in rows]
    summary=calibration_summary(probs,ys)
    summary["scope"]={
        "years":sorted({r.get("admission_year") for r in rows if r.get("admission_year") is not None}),
        "quota_types":sorted({r.get("quota_type") for r in rows if r.get("quota_type") is not None}),
        "regions":sorted({str(r.get("region")) for r in rows if r.get("region") is not None})
    }
    text=json.dumps(summary,ensure_ascii=False,indent=2)
    if args.output=="-": print(text)
    else: Path(args.output).write_text(text,encoding="utf-8")

if __name__=="__main__":
    main()
