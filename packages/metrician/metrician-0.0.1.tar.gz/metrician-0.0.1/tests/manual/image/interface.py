
from ..interface import BaseTestInterface

class ImageTestInterface(BaseTestInterface):

    dataset_name = ''

    _t = None

    @classmethod
    def _get_dataset(cls):
        import torchvision.datasets as dset
        import torchvision.transforms as T
        return getattr(dset,cls.dataset_name)(root='./data', train=False, transform=T.Compose([ 
                T.ToTensor(),
                # T.Resize( (32,32) )
         ]), download=True)#[:500]

    def _preprocess(self,data): return self._t( data )

    @property
    def t(self):
        assert self._t is not None, 'Image Test Transform must be defined'
        return self._t