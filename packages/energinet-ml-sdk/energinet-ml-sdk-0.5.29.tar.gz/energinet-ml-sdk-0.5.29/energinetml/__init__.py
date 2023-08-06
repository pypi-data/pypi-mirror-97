from .cli import main
from .core.project import Project
from .core.logger import MetricsLogger
from .core.model import Model, TrainedModel
from .core.predicting import PredictionInput
from .core.training import requires_parameter
from .core.insight import query_predictions, query_predictions_as_dataframe
from .settings import PACKAGE_NAME, PACKAGE_VERSION
# from .core.datasets import MLDataStore, MLDataSet


__name__ = PACKAGE_NAME
__version__ = PACKAGE_VERSION
