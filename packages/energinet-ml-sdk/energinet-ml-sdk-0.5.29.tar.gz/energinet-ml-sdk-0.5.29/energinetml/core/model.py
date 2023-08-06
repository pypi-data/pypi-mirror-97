import os
import shutil
import pickle
import random
import inspect
import importlib
from functools import cached_property
from typing import Any, List, Dict
from dataclasses import dataclass, field

from energinetml.settings import EMPTY_MODEL_TEMPLATE_DIR

from .project import Project
from .files import FileMatcher, temporary_folder
from .configurable import Configurable
from .requirements import RequirementList


# Constants
# TODO Move to settings.py?
DEFAULT_FILES_INCLUDE = ['**/*.py', 'model.json', 'requirements.txt']
DEFAULT_FILES_EXCLUDE = []


@dataclass
class Model(Configurable):
    """
    TODO
    """
    name: str
    experiment: str
    compute_target: str
    vm_size: str
    datasets: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    files_include: List[str] = field(default_factory=list)
    files_exclude: List[str] = field(default_factory=list)

    # Constants
    CONFIG_FILE_NAME = 'model.json'
    SCRIPT_FILE_NAME = 'model.py'
    TRAINED_MODEL_FILE_NAME = 'model.pkl'
    REQUIREMENTS_FILE_NAME = 'requirements.txt'

    @classmethod
    def create(cls, *args, **kwargs):
        """
        :param typing.List args:
        :param typing.Dict kwargs:
        :rtype Model
        """
        model = super(Model, cls).create(*args, **kwargs)

        # Copy template files
        for fn in os.listdir(EMPTY_MODEL_TEMPLATE_DIR):
            src = os.path.join(EMPTY_MODEL_TEMPLATE_DIR, fn)
            dst = os.path.join(model.path, fn)
            if os.path.isfile(src):
                shutil.copyfile(src, dst)

        return model

    @cached_property
    def project(self):
        """
        Returns the Project which this model belongs to.

        :rtype: Project
        """
        try:
            return Project.from_directory(self.path)
        except Project.NotFound:
            return None

    @property
    def trained_model_path(self):
        """
        Returns path to the trained model.

        :rtype: str
        """
        return self.get_file_path('outputs', self.TRAINED_MODEL_FILE_NAME)

    @property
    def data_folder_path(self):
        """
        Returns path to the data folder.

        :rtype: str
        """
        return self.get_file_path('data')

    @property
    def requirements_file_path(self):
        """
        Absolute path to requirements.txt file.

        :rtype: str
        """
        return self.get_file_path(self.REQUIREMENTS_FILE_NAME)

    @property
    def datasets_parsed(self):
        """
        Parses datasets and returns an iterable of (name, version),
        where version is optional and can be None.

        Datasets (from self.datasets) must be defined in the format
        of either "name" or "name:version"

        :rtype: typing.Iterable[typing.Tuple[str, str]]
        """
        for dataset in self.datasets:
            if dataset.count(':') > 1:
                raise ValueError('Invalid dataset "%s"' % dataset)
            colon_at = dataset.find(':')
            if colon_at != -1:
                yield dataset[:colon_at], dataset[colon_at+1:]
            else:
                yield dataset, None

    @cached_property
    def requirements(self):
        """
        :rtype: RequirementList
        """
        if os.path.isfile(self.requirements_file_path):
            return RequirementList.from_file(self.requirements_file_path)
        elif self.project:
            return self.project.requirements
        else:
            return RequirementList()

    @property
    def default_tags(self):
        """
        :rtype: typing.Dict[str, typing.Any]
        """
        tags = {}
        if self.datasets:
            tags['datasets'] = ', '.join(self.datasets)
        tags.update(self.extra_tags())
        return tags

    @property
    def files(self):
        """
        Returns an iterable of files to include when submitting a model to
        the cloud. These are the files necessary to run training in the cloud.

        File paths are relative to model root.

        NB: Does NOT include requirements.txt !!!

        :rtype: typing.Iterable[str]
        """
        return FileMatcher(
            root_path=self.path,
            include=self.files_include,
            exclude=self.files_exclude,
            recursive=True,
        )

    def temporary_folder(self, include_trained_model=False):
        """
        Returns a context manager which creates a temporary folder on the
        filesystem and copies all model's files into the folder including
        the project's requirements.txt file (if it exists).

        Usage example:

            with model.temporary_folder() as temp_path:
                # files are available in temp_path

        :param bool include_trained_model:
        :rtype: typing.ContextManager[str]
        """
        files_to_copy = []

        # Model-specific files (relative to model root)
        for relative_path in self.files:
            files_to_copy.append((
                self.get_file_path(relative_path),
                relative_path,
            ))

        # Trained model (model.pkl) if necessary
        if include_trained_model:
            files_to_copy.append((
                self.trained_model_path,
                self.get_relative_file_path(self.trained_model_path),
            ))

        # requirements.txt from this folder or project folder
        if os.path.isfile(self.requirements_file_path):
            files_to_copy.append((
                self.requirements_file_path,
                'requirements.txt',
            ))
        elif self.project and os.path.isfile(
                self.project.requirements_file_path):
            files_to_copy.append((
                self.project.requirements_file_path,
                'requirements.txt',
            ))

        return temporary_folder(files_to_copy)

    # -- Partially abstract interface ----------------------------------------

    # The following methods are meant to be overwritten by inherited classes
    # if necessary. Some can be omitted, and will return default values.

    def extra_tags(self):
        """
        :rtype: typing.Dict[str, typing.Any]
        """
        return {}

    def generate_seed(self):
        """
        :rtype: typing.Any
        """
        return random.randint(0, 10**9)

    def train(self, datasets, logger, seed, **params):
        """
        :param energinetml.MLDataStore datasets:
        :param energinetml.MetricsLogger logger:
        :param typing.Any seed:
        :param typing.Dict[str, typing.Any] params:
        :rtype: energinetml.TrainedModel
        """
        raise NotImplementedError

    def predict(self, trained_model, identifier, input_data):
        """
        :param energinetml.TrainedModel trained_model:
        :param energinetml.PredictionInput input_data:
        :param str identifier:
        :rtype: typing.List[typing.Any]
        """
        raise NotImplementedError


@dataclass
class TrainedModel(object):
    model: Any = field(default=None)
    models: Dict[str, Any] = field(default_factory=dict)
    features: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)

    class Invalid(Exception):
        pass

    def __new__(cls, **kwargs):
        # if 'model' not in kwargs and 'models' not in kwargs:
        #     raise ValueError((
        #         'Must provide either the "model" or "models" parameter '
        #         'when instantiating %s'
        #     ) % cls.__name__)

        if 'model' in kwargs and 'models' in kwargs:
            raise ValueError((
                'Can not instantiate %s using both "model" and "models" '
                'parameters. Either provide a default model to the "model" '
                'parameter, or provide a series of identifiable models '
                'to the "models" parameter.'
            ) % cls.__name__)

        return object.__new__(cls)

    @property
    def identifiers(self):
        """
        :rtype: list[str]
        """
        return list(self.models.keys())

    def has_model(self, identifier):
        """
        :rtype: bool
        """
        return identifier in self.models

    def get_model(self, identifier=None):
        """
        :param str identifier:
        :rtype: object
        """
        if identifier is None:
            return self.get_default_model()
        elif identifier in self.models:
            return self.models[identifier]
        else:
            raise ValueError('No model exists with identifier: %s' % identifier)

    def has_default_model(self):
        """
        :rtype: bool
        """
        return self.model is not None

    def get_default_model(self):
        """
        :rtype: object
        """
        if not self.has_default_model():
            raise ValueError((
                'No default model exists for this model. '
                'Use get_model() instead and provide a model identifier.'
            ))
        return self.model

    def verify(self):
        """
        TODO move to function outside class?
        """
        if not self.model and not self.models:
            raise self.Invalid((
                'Must provide either "model" or "models" parameters, '
                'otherwise it is of no use anyway.'
            ))

        # Validate features
        if not isinstance(self.features, list):
            raise self.Invalid((
                'Must provide a list of features. You gave me '
                'something of type %s'
            ) % str(type(self.features)))
        if not all(isinstance(s, str) for s in self.features):
            raise self.Invalid('All features must be of type str')
        if not [f.strip() for f in self.features if f.strip()]:
            raise self.Invalid((
                'No feature names provided. Instantiate %s with a list '
                'of features using the "features" parameter.'
            ) % self.__class__.__name__)

    def dump(self, file_path):
        """
        :param str file_path:
        """
        folder = os.path.split(file_path)[0]
        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(fp):
        """
        :rtype: TrainedModel
        """
        with open(fp, 'rb') as f:
            return pickle.load(f)


# -- Model importing ---------------------------------------------------------


class ModelError(Exception):
    pass


class ModelImportError(ModelError):
    """
    Raised if script does not contain a 'model' object
    in the global scope.
    """
    pass


class ModelNotClassError(ModelError):
    """
    Raised if imported 'model' object is not a class type.
    """
    pass


class ModelNotInheritModel(ModelError):
    """
    Raised if imported 'model' does not inherit from Model.
    """
    pass


def import_model_class(path):
    """
    Imports 'model' object from python-script at 'path'.
    Validates that its a class, and that it inherits from Model.

    :param str path:
    """
    spec = importlib.util.spec_from_file_location('model', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, 'model'):
        raise ModelImportError()

    model_class = getattr(module, 'model')

    if not inspect.isclass(model_class):
        raise ModelNotClassError()
    if not issubclass(model_class, Model):
        raise ModelNotInheritModel()

    return model_class
