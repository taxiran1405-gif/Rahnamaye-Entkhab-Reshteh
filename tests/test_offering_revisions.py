import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from apply_offering_revisions import materialize

class TestOfferingRevisions(unittest.TestCase):
    def test_change_then_delete(self):
        base=[{"admission_year":1402,"group":"math","choice_code":"123","capacity":20}]
        rev=[
            {"revision_id":"1","admission_year":1402,"group":"math","choice_code":"123","operation":"CHANGE","fields_after":{"capacity":10},"effective_date":"2023-09-01"},
            {"revision_id":"2","admission_year":1402,"group":"math","choice_code":"123","operation":"DELETE","fields_after":{},"effective_date":"2023-09-02"}
        ]
        out,_=materialize(base,rev)
        self.assertEqual(out,[])

    def test_add_new_code(self):
        out,_=materialize([],[
            {"revision_id":"1","admission_year":1403,"group":"math","choice_code":"999","operation":"ADD","fields_after":{"program_id":"PF-CSE"}}
        ])
        self.assertEqual(out[0]["choice_code"],"999")

if __name__=="__main__":
    unittest.main()
