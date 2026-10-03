"""Build deterministic canonical annual offering rows from conservatively mapped raw rows."""
import argparse, json, hashlib
from pathlib import Path

COURSE_TYPES={
    "روزانه":"CT-DAILY",
    "نوبت دوم":"CT-SECOND",
    "شبانه":"CT-SECOND",
    "پردیس خودگردان":"CT-CAMPUS",
    "مجازی":"CT-OTHER",
    "غیرانتفاعی":"CT-OTHER",
    "پیام نور":"CT-OTHER",
}

def load_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def load_jsonl(path): return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def stable_id(row):
    raw=f'{row["admission_year"]}|{row["group"]}|{row["choice_code"]}'
    return "OFF-"+hashlib.sha1(raw.encode()).hexdigest()[:16]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mapped",required=True)
    ap.add_argument("--universities",required=True)
    ap.add_argument("--source-id",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()

    rows=load_jsonl(args.mapped)
    universities=load_json(args.universities)["records"]
    umap={x["id"]:x for x in universities}

    out=[]; review=[]
    for row in rows:
        ct=COURSE_TYPES.get(row.get("course_type",""))
        uni=umap.get(row.get("university_id"))
        if not ct or not uni:
            review.append({**row,"status":"needs-review","mapping_error":"course_type_or_university"})
            continue
        out.append({
            "offering_id":stable_id(row),
            "admission_year":int(row["admission_year"]),
            "group":row["group"],
            "choice_code":str(row["choice_code"]),
            "program_id":row["program_id"],
            "university_id":row["university_id"],
            "campus_id":None,
            "course_type":ct,
            "selection_method":row.get("selection_method","نیازمندبررسی"),
            "city_id":None,
            "province_id":None,
            "quota_eligible":None,
            "capacity":None,
            "gender_restriction":None,
            "native_selection_type":row.get("raw_native_selection"),
            "tuition_text":row.get("tuition_text"),
            "source_id":args.source_id,
            "source_locator":row.get("source_locator"),
            "source_snapshot_hash":row.get("source_snapshot_hash"),
            "status":"provisional",
            "notes":row.get("notes_raw")
        })

    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(
        "\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8"
    )
    Path(str(args.output).replace(".jsonl",".needs-review.jsonl")).write_text(
        "\n".join(json.dumps(x,ensure_ascii=False) for x in review)+"\n",encoding="utf-8"
    )
    print(json.dumps({"canonical":len(out),"needs_review":len(review)},ensure_ascii=False))

if __name__=="__main__":
    main()
