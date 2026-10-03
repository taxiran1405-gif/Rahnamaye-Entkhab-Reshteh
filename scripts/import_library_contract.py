"""Lossless import contract for the internal adviser workbook.

This module deliberately does not guess missing semantics. It validates raw exports
before normalization and keeps provenance on every row.
"""
import argparse
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REQUIRED_SHEETS={
    "منابع","داده_اولیه_قبولی","رتبه_دانشگاه","قواعد_AI",
    "آخرین_رتبه_قبولی","ردیابی_منابع_رتبه","داده_تازه_1404",
    "مدل_ترجیحات_داوطلب","وزن_عوامل","الگوریتم_مشاوره",
    "فرم_داوطلب","فرم_نتیجه_واقعی","فرم_ارزیابی"
}
REQUIRED_LINEAGE=("raw_sheet","raw_row","import_batch_id","imported_at")

def validate_sheet_names(sheet_names):
    missing=sorted(REQUIRED_SHEETS-set(sheet_names))
    return {"ok":not missing,"missing":missing,"expected_count":len(REQUIRED_SHEETS)}

def read_rows(path):
    path=Path(path)
    if path.suffix.lower()==".jsonl":
        return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    if path.suffix.lower() in {".csv",".tsv"}:
        with path.open("r",encoding="utf-8",newline="") as f:
            dialect="excel-tab" if path.suffix.lower()==".tsv" else "excel"
            return list(csv.DictReader(f,dialect=dialect))
    raise ValueError("unsupported input; use jsonl/csv/tsv")

def validate_rows(rows):
    errors=[]
    seen=set()
    for i,row in enumerate(rows,1):
        for field in REQUIRED_LINEAGE:
            if not row.get(field):
                errors.append({"row":i,"error":"missing_lineage","field":field})
        raw_row=row.get("raw_row")
        try:
            if int(raw_row) < 1: raise ValueError
        except (TypeError,ValueError):
            errors.append({"row":i,"error":"invalid_raw_row"})
        key=row.get("canonical_key")
        if key:
            key_tuple=tuple(key) if isinstance(key,list) else str(key)
            if key_tuple in seen and row.get("status")!="conflicting":
                errors.append({"row":i,"error":"duplicate_canonical_key_without_conflict"})
            seen.add(key_tuple)
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input")
    ap.add_argument("--sheets", nargs="*")
    ap.add_argument("--report", default="-")
    args=ap.parse_args()

    if not args.input:
        print(json.dumps({
            "ok":True,
            "required_sheets":sorted(REQUIRED_SHEETS),
            "rule":"Do not discard any source row during normalization; preserve raw_sheet/raw_row/source_locator."
        },ensure_ascii=False,indent=2))
        return

    rows=read_rows(args.input)
    errors=validate_rows(rows)
    result={"ok":not errors,"rows":len(rows),"errors":errors}
    payload=json.dumps(result,ensure_ascii=False,indent=2)
    if args.report=="-":
        print(payload)
    else:
        Path(args.report).write_text(payload,encoding="utf-8")
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":
    main()
