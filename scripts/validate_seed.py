import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    provinces=load_json(ROOT/"data/provinces-capitals.seed.json")["records"]
    universities=load_json(ROOT/"data/universities-capitals.seed.json")["records"]
    programs=load_json(ROOT/"data/program-families.seed.json")["records"]
    course_types=load_json(ROOT/"data/course-types.seed.json")
    assert len(provinces)==31, f"expected 31 provinces, got {len(provinces)}"
    assert len({x["id"] for x in provinces})==31
    assert all(x.get("capital") for x in provinces)
    assert len({x["id"] for x in universities})==len(universities)
    assert len({x["id"] for x in programs})==len(programs)
    assert {"CT-DAILY","CT-SECOND","CT-CAMPUS"}.issubset({x["id"] for x in course_types})
    admissions=(ROOT/"data/admission-observations-1404.seed.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(admissions)>=1
    seen=set()
    for line in admissions:
        row=json.loads(line)
        key=(row["data_year"],row["program_id"],row["university_id"],row["course_type"],row["quota_type"],row["region"])
        assert key not in seen, f"duplicate admission key: {key}"
        seen.add(key)
        assert row["confidence"] in {"C4","C3","C2","C1","CX"}
        assert row["data_kind"]!="official" or row["confidence"]=="C4"
    print(f"OK provinces={len(provinces)} universities={len(universities)} programs={len(programs)} admissions={len(admissions)}")

if __name__=="__main__":
    main()
