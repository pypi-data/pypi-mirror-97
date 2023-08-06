import inspect
from typing import Union
from tensorboardX import GlobalSummaryWriter
BaseInterface=None
class BaseInterface(object):

    callbacks       = {}
    callback_kwargs = {}

    dtype           = None

    # @classmethod
    def _write_fn(cls) -> callable:
        from metrician import DatasetType
        writer = GlobalSummaryWriter.getSummaryWriter()
        return {
            # 'audio':writer.add_audio,
            DatasetType.text:writer.add_text,
            # 'tabular':writer.add_histogram,
            DatasetType.image:writer.add_image
        }[ cls.dtype ]

    def __call__(cls,*args,**kwargs) -> 'Data':
        output = cls.forward(*args,**kwargs)

        # check the number or arguments required for the function. 
        # if its more than 1, pass this object as well
        for f_name,clbk in cls.callbacks.items():
            nargs = clbk.__code__.co_argcount
            if len( nargs ) > 1: cblk( output,cls,**cls.callback_kwargs[fname] )
            else: cblk( output,**cls.callback_kwargs[fname]  )
        return output
    @classmethod
    def register_callback(cls,fn : callable,**kwargs ) -> BaseInterface:
        cls.callbacks[fn.__name__] = fn
        cls.callback_kwargs[fn.__name__] = kwargs
        return cls
    @classmethod
    def unregister_callback(cls,fn : Union[callable,str]) -> BaseInterface:
        name = fn if isinstance( fn, str ) else fn.__name__
        del cls.callbacks[name]
        del cls.callback_kwargs[name]
        return cls
    @classmethod
    def forward(cls,*args,**kwargs) -> 'Data':raise NotImplementedError(f'the "__call__" method for {cls.__class__.__name__} has not been implemented!')