
from torch.utils.data import Dataset
from typing import Union,Iterable
from metrician.signals.outliers import MomentOutlierSignal as MOS
from metrician.signals.interface import BaseSignal
from metrician.interface import BaseInterface
from torch import Tensor

from metrician import DatasetType,DATASET_INPUT_TYPES
class OutOfDistribution(BaseInterface):

    '''
        Default monitor for out of distribution losses.

        Basically this sets up a monitor that calculates whether some output is an outlier and records the input so you can evaluate it later on
    '''

    def __init__(   
                    self,
                    dataset : Union[Dataset,Iterable],
                    data_type : Union[str,DatasetType] = None,
                    signal  : BaseSignal = MOS(),
                    slug : str = 'Out Of Distribution Sample'
                ):
        assert data_type is not None or data_type.__class__.__name__ in DATASET_INPUT_TYPES, 'If your dataset is not a torch dataset you have to specify the input data type [image,audio,text,tabular] '
        self.dataset_length = len(dataset)
        self.dtype = data_type if data_type is not None else DATASET_INPUT_TYPES[data_type.__class__.__name__]
        self.signal = signal
        self.index = 0
        self.dataset = dataset
        self.slug = slug


    def forward(
                    self,
                    x : Tensor
                ) -> None:
        ood = self.signal( x )
        if ood > 0:
            writer = self._write_fn()
            writer(
                self.slug,
                self.dataset[ self.index % self.dataset_length ],
                self.index
            )
        self.index += 1

