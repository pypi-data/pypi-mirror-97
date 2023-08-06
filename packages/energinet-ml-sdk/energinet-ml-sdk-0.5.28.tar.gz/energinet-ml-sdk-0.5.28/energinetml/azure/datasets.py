import os
from typing import Dict
from azureml import exceptions
from azureml.core import Dataset


class MLDataSet(object):
    """
    TODO
    """
    def __init__(self, name, mount_path):
        """
        :param str name:
        :param str mount_path:
        """
        self.name = name
        self.mount_path = mount_path

    def __str__(self):
        """
        :rtype: str
        """
        return '%s<%s>' % (self.__class__.__name__, self.name)

    def path(self, *relative_path):
        """
        :param list[str] relative_path:
        :rtype: str
        """
        return os.path.join(self.mount_path, *relative_path)

    def open(self, relative_path, *args, **kwargs):
        """
        :param list[str] relative_path:
        :param args: *args for open()
        :param kwargs: **kwargs for open()
        :rtype: typing.IO
        """
        return open(self.path(*relative_path), *args, **kwargs)

    def contains(self, *relative_path):
        """
        :param list[str] relative_path:
        :rtype: bool
        """
        return os.path.exists(self.path(*relative_path))


class MLDataStore(Dict[str, MLDataSet]):
    """
    TODO
    """
    class DataSetNotFound(Exception):
        pass


class AzureMLDataStore(MLDataStore):
    """
    TODO
    """
    @classmethod
    def from_model(cls, model, workspace, force_download=False):
        """
        :param energinetml.Model model:
        :param azureml.core.Workspace workspace:
        :param bool force_download:
        """
        mounted_datasets = {}

        # TODO Load dataset depending on version ("name:version" format)

        for dataset_name, dataset_version in model.datasets_parsed:
            azureml_dataset = cls.load_azureml_dataset(
                workspace=workspace,
                dataset_name=dataset_name,
                dataset_version=dataset_version,
            )

            mounted_datasets[dataset_name] = cls.mount(
                model=model,
                azureml_dataset=azureml_dataset,
                force_download=force_download,
            )

        return cls(**mounted_datasets)

    @classmethod
    def load_azureml_dataset(cls, workspace, dataset_name, dataset_version):
        """
        :param azureml.core.Workspace workspace:
        :param str dataset_name:
        :param str dataset_version:
        :rtype: azureml.data.TabularDataset or azureml.data.FileDataset
        """

        # azureml wants 'latest'
        if dataset_version is None:
            dataset_version = 'latest'

        try:
            return Dataset.get_by_name(
                workspace=workspace,
                name=dataset_name,
                version=dataset_version,
            )
        except exceptions._azureml_exception.UserErrorException:
            raise  # TODO
            raise cls.DataSetNotFound(dataset_name)

    @classmethod
    def mount(cls, model, azureml_dataset, force_download):
        """
        :param energinetml.Model model:
        :param azureml.data.TabularDataset or azureml.data.FileDataset azureml_dataset:
        :param bool force_download:
        :rtype: MLDataSet
        """
        raise NotImplementedError


class MountedAzureMLDataStore(AzureMLDataStore):
    """
    TODO
    """
    @classmethod
    def mount(cls, model, azureml_dataset, force_download):
        mount_context = azureml_dataset.mount()
        mount_point = mount_context.mount_point
        mount_context.start()
        return MLDataSet(name=azureml_dataset.name, mount_path=mount_point)


class DownloadedAzureMLDataStore(AzureMLDataStore):
    """
    TODO
    """
    @classmethod
    def mount(cls, model, azureml_dataset, force_download):
        mount_point = os.path.join(model.data_folder_path, azureml_dataset.name)
        azureml_dataset.download(mount_point, overwrite=force_download)
        return MLDataSet(name=azureml_dataset.name, mount_path=mount_point)
