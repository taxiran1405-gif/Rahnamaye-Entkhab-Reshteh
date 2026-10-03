import unittest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from rer.calibration.metrics import brier_score, log_loss, expected_calibration_error

class TestCalibrationMetrics(unittest.TestCase):
    def test_brier(self):
        self.assertAlmostEqual(brier_score([0.0,1.0],[0,1]),0.0)

    def test_log_loss_finite(self):
        self.assertGreaterEqual(log_loss([0.25,0.75],[0,1]),0.0)

    def test_ece_perfect(self):
        self.assertAlmostEqual(expected_calibration_error([0.0,1.0],[0,1]),0.0)

    def test_bad_lengths_rejected(self):
        with self.assertRaises(ValueError):
            brier_score([0.5],[0,1])

if __name__=="__main__":
    unittest.main()
