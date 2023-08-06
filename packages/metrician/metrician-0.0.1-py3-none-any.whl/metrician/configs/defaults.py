
from metrician.configs.interface import DefaultConfigInterface,ConfigType
from metrician.configs.cfg import AutoDict

class SimpleClf(DefaultConfigInterface):
    """
        Default metrics for classification are F1, Accuracy and AUC-ROC
    """

    main_tag        = 'Classifier'
    metrics         = [ AutoDict(name=fn) for fn in 'accuracy_score,f1_score,roc'.split(',') ]
    config_type     = ConfigType.classification

class SimpleRgr(DefaultConfigInterface):
    """
        Default metrics for regression are Explained Variance, R2, Mean Absolute Error and Median Absolute Error
    """

    main_tag        = 'Regressor'
    metrics         = [ AutoDict(name=fn) for fn in 'explained_variance_score,r2_score,median_absolute_error,mean_absolute_error'.split(',') ]
    config_type     = ConfigType.regression
