"""Map raw offering titles to seeded canonical entities only when exact enough."""
import argparse,json,re
from pathlib import Path

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def norm(s):
    s=str(s or "").replace("ي","ی").replace("ك","ک")
    return re.sub(r"[\s\u200c]+","",s)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--raw",required=True)
    ap.add_argument("--programs",required=True)
    ap.add_argument("--universities",required=True)
    ap.add_argument("--mapped-output",required=True)
    ap.add_argument("--review-output",required=True)
    args=ap.parse_args()

    raw=[json.loads(x) for x in Path(args.raw).read_text(encoding="utf-8").splitlines() if x.strip()]
    programs=load_json(args.programs)["records"]
    universities=load_json(args.universities)["records"]

    pmap={}
    for x in programs:
        pmap[norm(x["name_fa"])]=x["id"]
        for alias in x.get("aliases",[]):
            pmap[norm(alias)]=x["id"]
    umap={norm(x["name_fa"]):x["id"] for x in universities}

    mapped=[]; review=[]
    for row in raw:
        pid=pmap.get(norm(row["raw_program_title"]))
        uid=umap.get(norm(row["raw_university_title"]))
        valid=pid and uid and row["raw_course_type"]!="نیازمندبررسی" and row["raw_selection_method"]!="نیازمندبررسی"
        row=dict(row)
        if not valid:
            row["status"]="needs-review"
            review.append(row)
            continue
        row["program_id"]=pid
        row["university_id"]=uid
        row["course_type"]=row["raw_course_type"]
        row["selection_method"]=row["raw_selection_method"]
        row["status"]="mapped"
        mapped.append(row)

    Path(args.mapped_output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.review_output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.mapped_output).write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in mapped)+"\n",encoding="utf-8")
    Path(args.review_output).write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in review)+"\n",encoding="utf-8")
    print(json.dumps({"mapped":len(mapped),"needs_review":len(review)},ensure_ascii=False))

if __name__=="__main__":
    main()
