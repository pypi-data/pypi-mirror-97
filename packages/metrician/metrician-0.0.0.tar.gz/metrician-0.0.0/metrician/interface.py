import inspect
from typing import Union

BaseInterface=None
class BaseInterface(object):

    callbacks       = {}
    callback_kwargs = {}

    def __call__(self,*args,**kwargs) -> 'Data':
        output = self.forward(*args,**kwargs)

        # check the number or arguments required for the function. 
        # if its more than 1, pass this object as well
        for f_name,clbk in self.callbacks.items():
            nargs = clbk.__code__.co_argcount
            if len( nargs ) > 1: cblk( output,self,**self.callback_kwargs[fname] )
            else: cblk( output,**self.callback_kwargs[fname]  )
        return output

    def register_callback(self,fn : callable,**kwargs ) -> BaseInterface:
        self.callbacks[fn.__name__] = fn
        self.callback_kwargs[fn.__name__] = kwargs
        return self
    
    def unregister_callback(self,fn : Union[callable,str]) -> BaseInterface:
        name = fn if isinstance( fn, str ) else fn.__name__
        del self.callbacks[name]
        del self.callback_kwargs[name]
        return self

    def forward(self,*args,**kwargs) -> 'Data':raise NotImplementedError(f'the "__call__" method for {self.__class__.__name__} has not been implemented!')