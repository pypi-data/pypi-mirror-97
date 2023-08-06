
from typing import Union,Optional
from metrician.configs.cfg import DefaultCFG
from torch import Tensor
from metrician.writers.interface import BaseWriterInterface

MetricWriter = None
class MetricWriter(BaseWriterInterface):
    """
        Metric Writer is a lightweight class that will automatically log metrics during a training loop.
    """

    def __init__(   self,
                    cfg:Union[dict,DefaultCFG] = None
                ): 
        super(self.__class__,self).__init__()
        
        import sklearn.metrics as metrics
        from metrician.configs.interface import DefaultConfigInterface

        # check for user provided config, 
        # if not present fallback to default
        self.cfg = DefaultCFG( cfg if isinstance( cfg, dict ) else None ) if not issubclass(cfg.__class__,DefaultConfigInterface) else cfg
        
        self.metrics = metrics
        self.custom_functions = {}
        self.signals = {}
        self.montiors = {}
        self.index = 0

    def forward(   self,
                    _output : Tensor, 
                    _labels: Tensor, 
                    loss_fn: Optional[callable] = None,
                    index : Optional[int] = -1
                ) -> Union[ 'loss_fn',MetricWriter ]:

        """

        """
        self.index += 1
        output,labels = self.cfg.sanitize_inputs( _output, _labels )
        for metric in self.cfg.metrics:
            if hasattr( self.metrics,metric.name ): self.writer.add_scalar(
                self.cfg.main_tag+'_'+metric.name,
                getattr(self.metrics,metric.name)( output,labels ) if metric.name != 'f1_score' else getattr(self.metrics,metric.name)( output,labels, average='micro'),
            index if index > -1 else self.index
        )
        for name,func in self.custom_functions.items():
            self.writer.add_scalar(
                                    self.cfg.main_tag+'_'+name,
                                    func( output,labels ),
                                    index if index > -1 else self.index
            )
        if callable(loss_fn):
            loss = loss_fn( _output,_labels )
            self.writer.add_scalar(self.cfg.main_tag+'_loss',loss.item(),index if index > -1 else self.index)
            if len(self.montitors) > 0:
                l = loss.item()
                for k,v in self.montitors.items():v( l )
            return loss

        return self
