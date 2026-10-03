"""Build the final annual offering catalog from base rows plus revision events.

This is a pure, deterministic materialization step. DELETE removes an offering only
from the materialized snapshot; the revision event remains in the audit ledger.
"""
import argparse,json,hashlib
from pathlib import Path

def load(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def key(r):
    return (int(r["admission_year"]),r["group"],str(r["choice_code"]))

def materialize(base, revisions):
    state={key(r):dict(r) for r in base}
    ordered=sorted(revisions,key=lambda r:(r.get("effective_date") or "",r.get("revision_id","")))
    audit=[]
    for rev in ordered:
        k=(int(rev["admission_year"]),rev["group"],str(rev["choice_code"]))
        op=rev["operation"]
        if op=="ADD":
            if k in state:
                audit.append({"key":k,"status":"conflict_add_existing"})
            else:
                state[k]=dict(rev.get("fields_after") or {})
                audit.append({"key":k,"status":"added"})
        elif op=="CHANGE":
            if k not in state:
                audit.append({"key":k,"status":"conflict_change_missing"})
            else:
                state[k].update(rev.get("fields_after") or {})
                audit.append({"key":k,"status":"changed"})
        elif op=="DELETE":
            state.pop(k,None)
            audit.append({"key":k,"status":"deleted"})
    return sorted(state.values(),key=lambda r:(r.get("admission_year"),r.get("group"),str(r.get("choice_code")))),audit

def sha256_json(rows):
    payload="\n".join(json.dumps(r,ensure_ascii=False,sort_keys=True) for r in rows)
    return hashlib.sha256(payload.encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--base",required=True)
    ap.add_argument("--revisions",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--audit",required=True)
    args=ap.parse_args()
    out,audit=materialize(load(args.base),load(args.revisions))
    Path(args.output).write_text("\n".join(json.dumps(r,ensure_ascii=False) for r in out)+"\n",encoding="utf-8")
    Path(args.audit).write_text(json.dumps({"rows":len(out),"snapshot_hash":sha256_json(out),"events":audit},ensure_ascii=False,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
