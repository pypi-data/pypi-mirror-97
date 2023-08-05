
# import abc
from torch import Tensor
from enum import Enum
class ConfigType(Enum):
    unknown         =   -1
    classification  =   0
    regression      =   1
    reinforcement   =   2

class DefaultConfigInterface():#metaclass=abc.ABCMeta
    """
        Listen, I know that the class name says "Interface" and then I'm making an Abstract Class, but it's Python, give me a break.
    """
    config_type = ConfigType.unknown

    @staticmethod
    # @abc.abstractmethod
    def auto_config(model:object) -> 'DefaultConfigInterface':
        """
            Autogenerate a default config from an arbitrary model.
        """
        from metrician.src.configs.defaults import SimpleClf,SimpleRgr
        final_layer = list(model.children())[-1]
        return SimpleClf if final_layer.out_features > 1 else SimpleRgr
        

    # @abc.abstractmethod
    def sanitize_inputs(self, output : Tensor, labels : Tensor) -> (Tensor,Tensor):
        """
            For different types of models, you'll need to coerce the data differently. 
            Regression Models:
                Convert to numpy arrays and return
            Classification Models:
                Take the ArgMax (for right now), convert to a numpy array and return
        """
        return {
            ConfigType.unknown: lambda a,b : (a.clone().detach(),b.clone().detach()),#(raise ValueError('Config Type has not been set. Unable to determine how to sanitize inputs!')),
            ConfigType.classification: lambda a,b : (
                                                        a.clone().detach().argmax(dim=-1).numpy() if len( a.size() ) > 1 else a.clone().detach().numpy(),
                                                        b.clone().detach().argmax(dim=-1).numpy() if len( b.size() ) > 1 else b.clone().detach().numpy()
                                                    ),
            ConfigType.regression: lambda a,b : (a.clone().detach(),b.clone().detach())
        }[ self.config_type ]( output,labels )




    