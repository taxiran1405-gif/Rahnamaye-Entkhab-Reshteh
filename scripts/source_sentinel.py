"""Minimal source watcher.

Usage:
  python scripts/source_sentinel.py config/source-watchlist.json state/source-state.json
It writes a JSON report. A production deployment should store the state in a durable
object store or repository-managed state with review/commit controls.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

def fetch(url: str) -> tuple[str, str]:
    req=Request(url,headers={"User-Agent":"Rahnamaye-Entkhab-Reshteh-SourceSentinel/0.1"})
    with urlopen(req, timeout=30) as resp:
        body=resp.read()
        content_type=resp.headers.get("content-type","")
    return hashlib.sha256(body).hexdigest(), content_type

def main() -> int:
    if len(sys.argv)!=3:
        print("usage: source_sentinel.py WATCHLIST STATE", file=sys.stderr)
        return 2
    watchlist=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    state_path=Path(sys.argv[2])
    old=json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    now=datetime.now(timezone.utc).isoformat()
    report=[]
    new_state={}
    for src in watchlist["sources"]:
        try:
            digest,ctype=fetch(src["url"])
            previous=old.get(src["id"],{}).get("sha256")
            changed=previous is not None and previous != digest
            new_state[src["id"]]={"sha256":digest,"checked_at":now,"content_type":ctype}
            report.append({"source_id":src["id"],"changed":changed,"impact":src["impact"],"status":"ok"})
        except Exception as exc:
            new_state[src["id"]]=old.get(src["id"],{"checked_at":now})
            report.append({"source_id":src["id"],"changed":False,"impact":src["impact"],"status":"error","error":str(exc)})
    state_path.parent.mkdir(parents=True,exist_ok=True)
    state_path.write_text(json.dumps(new_state,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"checked_at":now,"events":report},ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
