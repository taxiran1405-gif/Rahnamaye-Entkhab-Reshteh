import unittest
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestSeedIntegrity(unittest.TestCase):
    def test_province_count(self):
        rows=json.loads((ROOT/"data/provinces-capitals.seed.json").read_text(encoding="utf-8"))["records"]
        self.assertEqual(len(rows),31)

    def test_admission_rows_are_unique(self):
        rows=[json.loads(x) for x in (ROOT/"data/admission-observations-1404.seed.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        keys=[(r["data_year"],r["program_id"],r["university_id"],r["course_type"],r["quota_type"],r["region"]) for r in rows]
        self.assertEqual(len(keys),len(set(keys)))

    def test_no_seed_claimed_official_without_c4(self):
        rows=[json.loads(x) for x in (ROOT/"data/admission-observations-1404.seed.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        bad=[r for r in rows if r["data_kind"]=="official" and r["confidence"]!="C4"]
        self.assertEqual(bad,[])

if __name__=="__main__":
    unittest.main()
