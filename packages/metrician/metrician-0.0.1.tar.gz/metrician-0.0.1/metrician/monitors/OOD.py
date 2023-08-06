
from torch.utils.data import Dataset
from typing import Union,Iterable
from metrician.signals.outliers import MomentOutlierSignal as MOS
from metrician.signals.interface import BaseSignal
from .interface import BaseMonitorInterface
from torch import Tensor
import metrician

class OutOfDistributionMonitor(BaseMonitorInterface):

    '''
        Default monitor for out of distribution losses.

        Basically this sets up a monitor that calculates whether some output is an outlier and records the input so you can evaluate it later on
    '''

    def __init__(   
                    self,
                    dataset : Union[Dataset,Iterable],
                    data_type : Union[str,metrician.DatasetType] = None,
                    signal  : BaseSignal = MOS(),
                    slug : str = 'Out Of Distribution Sample'
                ):
        assert data_type is None and dataset.__class__.__name__ in metrician.DATASET_INPUT_TYPES, 'If your dataset is not a torch dataset you have to specify the input data type [image,audio,text,tabular] '
        self.dataset_length = len(dataset)
        self.dtype = data_type if data_type is not None else metrician.DATASET_INPUT_TYPES[dataset.__class__.__name__]
        self.signal = signal
        self.index = 0
        self.dataset = dataset
        self.slug = slug
        self.testing = False
        self.oods = []
        self.writer = self._write_fn()


    def forward(
                    self,
                    x : Tensor
                ) -> None:
        ood = self.signal( x )
        if ood > 0:
            self.writer(
                self.slug,
                self.dataset[ self.index % self.dataset_length ][0], # take the first index since it's the input
                self.index
            )
            if self.testing:self.oods.append( self.index )
        self.index += 1

