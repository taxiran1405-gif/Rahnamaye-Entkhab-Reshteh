import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from import_library_contract import validate_rows, validate_sheet_names
from backtest_admission import audit

class TestLibraryContracts(unittest.TestCase):
    def test_required_sheets_contract(self):
        result=validate_sheet_names(["منابع","قواعد_AI"])
        self.assertFalse(result["ok"])
        self.assertIn("داده_اولیه_قبولی",result["missing"])

    def test_lineage_is_required(self):
        rows=[{"raw_sheet":"منابع","raw_row":1,"import_batch_id":"B1","imported_at":"2026-10-03"}]
        errors=validate_rows(rows)
        self.assertTrue(any(e["error"]=="missing_lineage" for e in errors))

    def test_duplicate_requires_conflict(self):
        base={"raw_sheet":"آخرین_رتبه_قبولی","raw_row":1,"import_batch_id":"B1","imported_at":"2026-10-03","canonical_key":["1404","x"]}
        errors=validate_rows([base,dict(base,raw_row=2)])
        self.assertTrue(any(e["error"]=="duplicate_canonical_key_without_conflict" for e in errors))

    def test_current_seed_is_not_five_year(self):
        rows=[json.loads(x) for x in (ROOT/"data/admission-observations-1404.seed.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        result=audit(rows)
        self.assertFalse(result["five_year_backtest_allowed"])
        self.assertEqual(result["years_missing"],[1400,1401,1402,1403])

if __name__=="__main__":
    unittest.main()
