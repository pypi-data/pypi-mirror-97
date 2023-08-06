from typing import List
from packaging import version
from pkg_resources import Requirement, parse_requirements


class RequirementList(List[Requirement]):

    @classmethod
    def from_file(cls, filepath):
        """
        :param str filepath:
        :rtype: RequirementList
        """
        with open(filepath) as f:
            return cls(parse_requirements(f.read()))

    def __contains__(self, package_name):
        """
        :param str package_name:
        :rtype: bool
        """
        return self.get(package_name) is not None

    def get(self, package_name):
        """
        :param str package_name:
        :rtype: Requirement
        """
        for requirement in self:
            if requirement.key == package_name:
                return requirement

    def get_specs(self, package_name):
        """
        :param str package_name:
        """
        requirement = self.get(package_name)
        if requirement is not None:
            return requirement.specs

    def get_version(self, package_name):
        """
        :param str package_name:
        """
        specs = self.get_specs(package_name)
        if specs is not None:
            if specs:
                return version.parse(specs[0][1])
