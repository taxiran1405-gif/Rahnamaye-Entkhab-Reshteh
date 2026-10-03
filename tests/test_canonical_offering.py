import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from build_canonical_offering import stable_id, COURSE_TYPES

class TestCanonicalOffering(unittest.TestCase):
    def test_course_type_mapping(self):
        self.assertEqual(COURSE_TYPES["روزانه"],"CT-DAILY")
        self.assertEqual(COURSE_TYPES["شبانه"],"CT-SECOND")

    def test_id_is_deterministic(self):
        row={"admission_year":1402,"group":"math","choice_code":"12345"}
        self.assertEqual(stable_id(row),stable_id(row))

if __name__=="__main__":
    unittest.main()
