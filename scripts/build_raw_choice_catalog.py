"""Convert extracted candidate rows into lossless raw choice-offering records."""
import argparse,json,re,hashlib
from pathlib import Path

def load(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def first_code(cells):
    for c in cells:
        s=str(c).strip()
        if re.fullmatch(r"\d{4,6}",s):
            return s
    return None

def find_course_type(cells):
    t=" ".join(map(str,cells))
    for k in ("پردیس خودگردان","نوبت دوم","شبانه","روزانه","مجازی","غیرانتفاعی","پیام نور"):
        if k in t:
            return k
    return "نیازمندبررسی"

def find_selection(cells):
    t=" ".join(map(str,cells))
    if "سوابق تحصیلی" in t or "صرفاً با سوابق" in t:
        return "صرفاً با سوابق تحصیلی"
    if "با آزمون" in t:
        return "با آزمون"
    return "نیازمندبررسی"

def extract_title_candidates(cells):
    texts=[str(c).strip() for c in cells if str(c).strip()]
    code=first_code(texts)
    return [x for x in texts if x!=code][:12]

def make_id(year,page,table,row,code):
    raw=f"{year}:{page}:{table}:{row}:{code}"
    return "RAW-"+hashlib.sha1(raw.encode()).hexdigest()[:16]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    rows=load(args.input)
    out=[]
    for r in rows:
        cells=r.get("cells") or []
        code=first_code(cells)
        if not code:
            continue
        texts=extract_title_candidates(cells)
        out.append({
            "raw_id":make_id(r["year"],r["page"],r["table_index"],r["raw_row_index"],code),
            "admission_year":int(r["year"]),
            "group":"math",
            "choice_code":code,
            "raw_program_title":texts[0] if texts else "نیازمندبررسی",
            "raw_university_title":texts[1] if len(texts)>1 else "نیازمندبررسی",
            "raw_campus_title":None,
            "raw_city_title":None,
            "raw_course_type":find_course_type(cells),
            "raw_selection_method":find_selection(cells),
            "raw_native_selection":None,
            "capacity_text":None,
            "gender_text":None,
            "notes_raw":" | ".join(texts),
            "source_id":"S001_OR_MIRROR",
            "source_locator":None,
            "source_snapshot_hash":None,
            "status":"raw"
        })
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    print(json.dumps({"rows":len(out),"status":"raw_only"},ensure_ascii=False))

if __name__=="__main__":
    main()
