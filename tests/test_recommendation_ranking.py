import unittest
from rer.recommendation.ranking import Candidate, compose_cell, utility_score

class TestRecommendationRanking(unittest.TestCase):
    def test_interest_and_probability_are_combined(self):
        a=Candidate("A","PF-CSE","U1","C1","primary",0.80,1.0,{"major_interest":1.0})
        b=Candidate("B","PF-EE","U2","C1","parallel",0.90,1.0,{"major_interest":0.2})
        cell=compose_cell([a,b])
        self.assertEqual(cell.primary.option_id,"A")
        self.assertEqual(len(cell.parallel),1)

    def test_cover_role_is_separate_even_with_high_score(self):
        a=Candidate("A","PF-CSE","U1","C2","primary",0.5,1.0,{"major_interest":1.0})
        b=Candidate("B","PF-CSE","U2","C2","cover",0.99,1.0,{"major_interest":1.0})
        cell=compose_cell([a,b])
        self.assertEqual(cell.primary.option_id,"A")
        self.assertEqual(cell.cover[0].option_id,"B")

    def test_legacy_0_to_100_preferences_are_supported(self):
        a=Candidate("A","PF-CSE","U1","C3","primary",0.0,1.0,{"major_interest":100})
        self.assertAlmostEqual(utility_score(a),0.25)

if __name__=="__main__":
    unittest.main()
