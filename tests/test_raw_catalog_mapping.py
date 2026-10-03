import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from map_raw_choice_catalog import norm

class TestRawCatalogMapping(unittest.TestCase):
    def test_persian_normalization(self):
        self.assertEqual(norm("مهندسی‌ کامپیوتر"),norm("مهندسی کامپیوتر"))
        self.assertEqual(norm("كشاورزي"),norm("کشاورزی"))

    def test_raw_contract_is_lossless(self):
        row={"raw_program_title":"مهندسی برق","raw_university_title":"دانشگاه تهران","notes_raw":"اصل متن"}
        self.assertIn("notes_raw",row)
        self.assertEqual(row["notes_raw"],"اصل متن")

if __name__=="__main__":
    unittest.main()
