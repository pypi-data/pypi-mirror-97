from torch.utils import data
from typing import Union
class Dataset:

    def __init__(
                    self,
                    dataset : data.Dataset,
                    callbacks : list = []
                ):
        self.dataset = dataset
        self.callbacks = callbacks

    def __getitem__(self,index : Union[slice,int]):
        return self.dataset[index]