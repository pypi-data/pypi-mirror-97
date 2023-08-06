# from unittest import TestCase
from abc import ABC

class BaseTestInterface(object):
    
    _loss       = None
    _model      = None
    _index      = 0
    _dataset    = None
    _optimizer  = None
    _task_type  = None
    _error_locs = None


    @classmethod
    def tearDownClass(cls):
        cls._loss       = None
        cls._model      = None
        cls._index      = 0
        cls._dataset    = None
        cls._optimizer  = None
        cls._task_type  = None
        cls._error_locs = None

    @classmethod
    def _preprocess(cls,data): raise NotImplementedError('You must create a custom dataset builder')

    @classmethod
    def _postprocess(cls,data): return data#raise NotImplementedError('You must create a custom dataset builder')

    @classmethod
    def _get_dataset(cls):raise NotImplementedError('You must create a custom dataset builder')

    @classmethod
    def _get_model(cls):raise NotImplementedError('You must create a custom model')

    @classmethod
    def _get_loss(cls):raise NotImplementedError('You must create a custom loss getter')

    @classmethod
    def _get_optimizer(cls):#raise NotImplementedError('You must create a custom optimizer getter')
        from torch.optim import SGD
        model = cls.model()
        return SGD( model.parameters(),lr=.01 )
    
    # @property
    @classmethod
    def dataset(cls): 
        if cls._dataset is None:cls._dataset=cls._get_dataset()
        return cls._dataset

    # @property
    @classmethod
    def loss(cls): 
        if cls._loss is None:cls._loss=cls._get_loss()
        return cls._loss

    # @property
    @classmethod
    def optimizer(cls): 
        if cls._optimizer is None:cls._optimizer=cls._get_optimizer()
        return cls._optimizer    

    # @property
    @classmethod
    def model(cls): 
        if cls._model is None:cls._model=cls._get_model(cls)
        return cls._model

    @classmethod
    def _init_outlier_detection(cls):
        from metrician import MetricWriter,SimpleClf,OutOfDistributionMonitor
        dataset = cls.dataset()
        ood = OutOfDistributionMonitor(dataset)
        ood.testing = True
        return MetricWriter( SimpleClf() ).register_monitor(
            ood
        )

    @classmethod
    def _check_outliers(cls):pass

            
        

    

