import unittest
from unittest import TestCase
import torch
from metrician.signals.outliers import MomentOutlierSignal
class MomentOutlierTest(TestCase):
    
    def setUp(self):
        
        self.eps = 1e-2 # threshold for differences in data evaluation
    
    def test_scalar_mean(self):
        
        Signal = MomentOutlierSignal()
        data = torch.randn( 100 )
        mean = data.mean()
        for d in data:Signal( d )
        self.assertTrue(
            torch.abs(Signal.mean - mean) < self.eps,
            'Outlier Scalar Mean not within threshold value'
        )
    def test_scalar_var(self):
        
        Signal = MomentOutlierSignal()
        data = torch.randn( 100 )
        var = data.var()
        for d in data:Signal( d )
        self.assertTrue(
            torch.abs(Signal.var - var) < self.eps,
            'Outlier Scalar Variance not within threshold value'
        )
    def test_scalar_skewness(self):
        from scipy.stats import norm, skew
        Signal = MomentOutlierSignal()
        data = torch.randn( 100 )
        s = skew(data)
        for d in data:Signal( d )
        self.assertTrue(
            torch.abs(Signal.skewness - s) < self.eps*10,
            'Outlier Scalar Skewness not within threshold value'
        )
    def test_scalar_kurtosis(self):
        from scipy.stats import norm, kurtosis
        Signal = MomentOutlierSignal()
        data = torch.randn( 100 )
        k = kurtosis(data)
        for d in data:Signal( d )
        self.assertTrue(
            torch.abs(Signal.kurtosis - k) < self.eps*10,
            'Outlier Scalar Kurtosis not within threshold value'
        )

if __name__ == '__main__':
    unittest.main()     
