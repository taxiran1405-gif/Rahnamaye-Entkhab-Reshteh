import unittest
from scripts.backtest_admission import summarize

class TestBacktest(unittest.TestCase):
    def test_groups_preserve_course_and_region(self):
        rows=[
          {"program_id":"P","university_id":"U","course_type":"روزانه","quota_type":"منطقه","region":"1","data_year":1404,"cutoff_rank":100},
          {"program_id":"P","university_id":"U","course_type":"روزانه","quota_type":"منطقه","region":"2","data_year":1404,"cutoff_rank":200},
        ]
        result=summarize(rows)
        self.assertEqual(len(result),2)

if __name__=="__main__":
    unittest.main()
