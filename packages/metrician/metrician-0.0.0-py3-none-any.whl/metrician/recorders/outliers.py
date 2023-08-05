
from .interface import BaseSignal
from torch import Tensor
import math
class MomentOutlierSignal(BaseSignal):
    '''
        Real time outlier detection for metrics

        This class records moments in order to estimate the likelihood of an outlier when data is passed to it. 
        If data may be an outlier, such as something that causes a really high error, this will record the index so you can view it later
    '''

    def __init__(self):
        self._index = self._eta = self._rho = self._tau = self._phi = 0.0
        self._min   = self._max = float('nan')

    def __call__(self, x : Tensor) -> int:
        if self._index == 0.0:
            self._min = x
            self._max = x
        else:
            # TODO: abstract for multidimensional input
            self._min = min(self._min, x)
            self._max = max(self._max, x)
        
        outlier = self._is_outlier(x) if self._index > 5 else False
        if not outlier: # don't include the outliers
            delta = x - self._eta
            delta_n = delta / (self._index + 1)
            delta_n2 = delta_n * delta_n
            term = delta * delta_n * self._index

            self._eta += delta_n
            self._phi += (
                term * delta_n2 * (self._index ** 2 - 3 * self._index + 3)
                + 6 * delta_n2 * self._rho
                - 4 * delta_n * self._tau
            )
            self._tau += (
                term * delta_n * (self._index - 2) - 3 * delta_n * self._rho
            )
            self._rho += term
        self._index += 1
        return 1 if outlier else 0

    def _is_outlier(self, x : Tensor) -> bool:
        '''
            weight the amount of standard deviation to use based on kurtosis of the data
        '''
        m = self.mean
        std = math.sqrt( self.var )
        k = self.kurtosis
        #            Above the threshold           |         Below the threshold
        return ( x > ( m + (std*(3.5 - k ) ) )  ) or ( x < ( m - (std*(3.5 - k ) ) )  )


    @property
    def mean(self) -> Tensor: return self._eta

    @property
    def var(self) -> Tensor: return self._rho / (self._index - 1)

    @property
    def skewness(self) -> Tensor: return (self._index ** 0.5) * self._tau / pow(self._rho, 1.5)

    @property
    def kurtosis(self) -> Tensor: return (self._index * self._phi / (self._rho * self._rho) - 3.0)/2.


    