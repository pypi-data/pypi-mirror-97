from enum import Enum


class ComputeType(Enum):
    CPU = 'CPU'
    GPU = 'GPU'


class AbstractBackend(object):
    """
    """

    class BackendException(Exception):
        pass

    def get_available_subscriptions(self):
        """
        """
        raise NotImplementedError

    def get_available_resource_groups(self, subscription_id):
        """
        """
        raise NotImplementedError

    # -- Workspaces ----------------------------------------------------------

    def get_available_workspaces(self, subscription_id, resource_group):
        """
        """
        raise NotImplementedError

    def get_available_workspace_names(self, subscription_id, resource_group):
        """
        """
        raise NotImplementedError

    def get_workspace(self, subscription_id, resource_group, name):
        """
        """
        raise NotImplementedError

    # -- Compute clusters ----------------------------------------------------

    def get_compute_clusters(self, workspace):
        """
        """
        raise NotImplementedError

    def get_available_vm_sizes(self, workspace):
        """
        :rtype: typing.List[str]
        """
        raise NotImplementedError

    def get_suggested_vm_size(self, compute_type):
        """
        :param ComputeType compute_type:
        :rtype: str
        """
        raise NotImplementedError

    def create_compute_cluster(self, workspace, name, vm_size, min_nodes, max_nodes,
                               vnet_resource_group_name, vnet_name, subnet_name):
        """
        :param Workspace workspace:
        :param str name:
        :param str vm_size:
        :param int min_nodes:
        :param int max_nodes:
        :param str vnet_resource_group_name:
        :param str vnet_name:
        :param str subnet_name:
        """
        raise NotImplementedError

    # -- Contexts ------------------------------------------------------------

    def get_local_training_context(self, force_download):
        """
        :param bool force_download:
        :rtype: energinetml.core.training.AbstractTrainingContext
        """
        raise NotImplementedError

    def get_cloud_training_context(self):
        """
        :rtype: energinetml.core.training.AbstractTrainingContext
        """
        raise NotImplementedError

    def submit_model(self, model, params):
        """
        :param energinetml.core.model.Model model:
        :param list[str] params:
        :rtype: energinetml.core.submitting.SubmitContext
        """
        raise NotImplementedError
