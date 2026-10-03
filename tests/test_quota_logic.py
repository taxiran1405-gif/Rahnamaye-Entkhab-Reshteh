import unittest
from rer.admission.quota import RankContext, select_candidate_rank, filter_comparable_observations

class TestQuotaLogic(unittest.TestCase):
    def setUp(self):
        self.ctx=RankContext(
            national_rank=12000,
            final_quota_type="منطقه",
            final_quota_rank=2400,
            region="2",
        )

    def test_region_exact_match_uses_quota_rank(self):
        d=select_candidate_rank(self.ctx,"منطقه","2")
        self.assertTrue(d.comparable)
        self.assertEqual(d.rank,2400)
        self.assertEqual(d.reason_code,"EXACT_FINAL_QUOTA_RANK")

    def test_national_rank_is_not_used_as_fallback(self):
        ctx=RankContext(12000,"منطقه",None,"2")
        d=select_candidate_rank(ctx,"منطقه","2")
        self.assertFalse(d.comparable)
        self.assertEqual(d.reason_code,"NO_FINAL_QUOTA_RANK")

    def test_other_region_is_not_directly_comparable(self):
        d=select_candidate_rank(self.ctx,"منطقه","3")
        self.assertFalse(d.comparable)
        self.assertEqual(d.reason_code,"REGION_MISMATCH")

    def test_special_quota_does_not_mix_with_region(self):
        d=select_candidate_rank(self.ctx,"5_percent_esaargar",None)
        self.assertFalse(d.comparable)
        self.assertEqual(d.reason_code,"QUOTA_TYPE_MISMATCH")

    def test_filter_keeps_exact_quota_region_only(self):
        rows=[
            {"quota_type":"منطقه","region":"2","rank_basis":"quota_rank","cutoff_rank":100},
            {"quota_type":"منطقه","region":"1","rank_basis":"quota_rank","cutoff_rank":90},
            {"quota_type":"5_percent_esaargar","region":None,"rank_basis":"special_quota_rank","cutoff_rank":50}
        ]
        got=filter_comparable_observations(self.ctx,rows)
        self.assertEqual(len(got),1)
        self.assertEqual(got[0]["cutoff_rank"],100)

if __name__=="__main__":
    unittest.main()
