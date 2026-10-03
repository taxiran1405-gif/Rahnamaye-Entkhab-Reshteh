import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from corpus_coverage import report

class TestCorpusCoverage(unittest.TestCase):
    def test_separates_offering_and_admission(self):
        r=report(
            [{"admission_year":1403,"group":"math","choice_code":"123"}],
            [{"data_year":1404,"group":"math","program_id":"PF-CSE","university_id":"U-TEH-001","quota_type":"منطقه","region":"2"}]
        )
        self.assertEqual(r["1403"]["unique_choice_codes"],1)
        self.assertEqual(r["1404"]["admission_rows"],1)

if __name__=="__main__":
    unittest.main()
