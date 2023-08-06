import os
from functools import cached_property
from dataclasses import dataclass, field

from energinetml.settings import (
    DEFAULT_LOCATION,
    PACKAGE_NAME,
    PACKAGE_VERSION,
)

from .configurable import Configurable
from .requirements import RequirementList


@dataclass
class Project(Configurable):
    """
    TODO
    """
    name: str
    subscription_id: str
    resource_group: str
    workspace_name: str
    location: str = field(default=DEFAULT_LOCATION)

    # Constants
    CONFIG_FILE_NAME = 'project.json'
    REQUIREMENTS_FILE_NAME = 'requirements.txt'

    @property
    def vnet_resourcegroup_name(self):
        return self.resource_group

    @property
    def vnet_name(self):
        return 'vnet-eml'

    @property
    def subnet_name(self):
        return 'snet-compute-aml'

    @classmethod
    def create(cls, *args, **kwargs):
        """
        :rtype Project
        """
        project = super(Project, cls).create(*args, **kwargs)

        # Create requirements.txt file
        with open(project.requirements_file_path, 'w') as f:
            f.write('%s==%s\n' % (PACKAGE_NAME, PACKAGE_VERSION))

        return project

    @property
    def requirements_file_path(self):
        """
        Absolute path to requirements.txt file.

        :rtype: str
        """
        return self.get_file_path(self.REQUIREMENTS_FILE_NAME)

    @cached_property
    def requirements(self):
        """
        Returns a list of project requirements from requirements.txt.

        :rtype: RequirementList
        """
        if os.path.isfile(self.requirements_file_path):
            return RequirementList.from_file(self.requirements_file_path)
        else:
            return RequirementList()

    def default_model_path(self, model_name):
        """
        Returns default absolute path to folder where new models
        should be created at.

        :param str model_name:
        :rtype: str
        """
        return self.get_file_path(model_name)
