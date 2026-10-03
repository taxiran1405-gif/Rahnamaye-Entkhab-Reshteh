"""Fetch and extract the four mathematics selection booklets."""
import argparse, hashlib, json, re
from pathlib import Path
from urllib.request import Request, urlopen
import pdfplumber
import yaml

ROOT=Path(__file__).resolve().parents[1]

def fetch(url):
    req=Request(url,headers={"User-Agent":"Rahnamaye-Entkhab-Reshteh-HistoricalCorpus/0.1"})
    with urlopen(req,timeout=90) as r:
        return r.read()

def sha256(data): return hashlib.sha256(data).hexdigest()

def norm(x):
    return re.sub(r"\\s+"," ",str(x or "")).strip()

def looks_like_offering(rows):
    joined=" ".join(norm(c) for row in rows[:4] for c in row)
    return sum(k in joined for k in ("کد رشته","کدرشته","عنوان رشته","دوره تحصیلی","نحوه پذیرش")) >= 2

def extract(pdf_path,year,outdir):
    yd=outdir/str(year); yd.mkdir(parents=True,exist_ok=True)
    pagesf=yd/f"{year}-pages.jsonl"; tablesf=yd/f"{year}-tables.jsonl"; candf=yd/f"{year}-candidate-rows.jsonl"
    settings_list=[
        {"vertical_strategy":"lines","horizontal_strategy":"lines","snap_tolerance":3,"join_tolerance":3,"edge_min_length":3},
        {"vertical_strategy":"text","horizontal_strategy":"text","snap_tolerance":3,"join_tolerance":3}
    ]
    table_count=0; cand_count=0
    with pdfplumber.open(pdf_path) as pdf, pagesf.open("w",encoding="utf-8") as pf, tablesf.open("w",encoding="utf-8") as tf, candf.open("w",encoding="utf-8") as cf:
        for page_no,page in enumerate(pdf.pages,1):
            pf.write(json.dumps({"year":year,"page":page_no,"text":page.extract_text() or ""},ensure_ascii=False)+"\n")
            tables=[]
            for st in settings_list:
                try:
                    got=page.extract_tables(table_settings=st) or []
                    if len(got)>len(tables): tables=got
                except Exception:
                    pass
            for ti,table in enumerate(tables,1):
                clean=[[norm(c) for c in row] for row in table]
                flag=looks_like_offering(clean)
                tf.write(json.dumps({"year":year,"page":page_no,"table_index":ti,"rows":clean,"looks_like_offering_table":flag},ensure_ascii=False)+"\n")
                table_count += 1
                if flag:
                    for ri,row in enumerate(clean,1):
                        cf.write(json.dumps({"year":year,"page":page_no,"table_index":ti,"raw_row_index":ri,"cells":row},ensure_ascii=False)+"\n")
                        cand_count += 1
    return {"pages":len(pdf.pages),"tables":table_count,"candidate_rows":cand_count,"sha256":sha256(pdf_path.read_bytes())}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default=str(ROOT/"config/historical-booklets.yaml"))
    ap.add_argument("--output",default=str(ROOT/"artifacts/historical_booklets"))
    ap.add_argument("--year",type=int,action="append")
    args=ap.parse_args()
    cfg=yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    years=args.year or [1400,1401,1402,1403]
    outdir=Path(args.output); outdir.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for year in years:
        targets=[cfg["booklets"][year]["primary"]]+cfg["booklets"][year].get("fallback",[])
        data=None; used=None; errors=[]
        for t in targets:
            try:
                data=fetch(t["url"]); used=t; break
            except Exception as e:
                errors.append({"url":t["url"],"error":str(e)})
        if data is None:
            manifest.append({"year":year,"status":"fetch_failed","errors":errors})
            continue
        yd=outdir/str(year); yd.mkdir(parents=True,exist_ok=True)
        pdf=yd/f"math-selection-{year}.pdf"; pdf.write_bytes(data)
        item={"year":year,"status":"downloaded","source_used":used,"bytes":len(data),"fetch_errors":errors}
        try:
            item.update(extract(pdf,year,outdir)); item["status"]="extracted"
        except Exception as e:
            item["status"]="extract_failed"; item["extract_error"]=str(e)
        manifest.append(item)
    (outdir/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
    if any(x["status"]=="fetch_failed" for x in manifest): raise SystemExit(2)

if __name__=="__main__": main()
