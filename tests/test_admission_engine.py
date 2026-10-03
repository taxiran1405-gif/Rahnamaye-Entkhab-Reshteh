import unittest
from rer.admission.engine import AdmissionObservation, estimate_probability_band

class TestAdmissionEngine(unittest.TestCase):
    def test_empty(self):
        p=estimate_probability_band(100,[])
        self.assertEqual(p.n,0)
        self.assertEqual(p.midpoint,0.0)

    def test_rank_direction(self):
        obs=[AdmissionObservation(1400,150),AdmissionObservation(1401,170),AdmissionObservation(1402,160,.9)]
        better=estimate_probability_band(80,obs)
        worse=estimate_probability_band(220,obs)
        self.assertGreater(better.midpoint,worse.midpoint)
        self.assertGreaterEqual(better.lower,0.0)
        self.assertLessEqual(better.upper,1.0)

if __name__=="__main__":
    unittest.main()
