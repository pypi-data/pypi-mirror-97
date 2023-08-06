import re
import azureml
from functools import cached_property
from azureml.core import ComputeTarget, Model
from azureml.core.compute import AmlCompute
from azureml.core.authentication import AzureCliAuthentication
from azure.mgmt.resource import SubscriptionClient, ResourceManagementClient
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core import (
    Workspace,
    Experiment,
    ScriptRunConfig,
    RunConfiguration,
    Environment,
)

from energinetml.core.backend import AbstractBackend
from energinetml.settings import PYTHON_VERSION, PACKAGE_NAME

from .submitting import AzureSubmitContext
from .training import AzureCloudTrainingContext, AzureLocalTrainingContext


class AzureBackend(AbstractBackend):

    def parse_azureml_exception(self, e):
        """
        Extracts error message from AzureMLException and
        returns a BackendException.

        :param azureml._common.exceptions.AzureMLException e:
        :rtype: AbstractBackend.BackendException
        """
        msg = str(e)
        matches = re.findall(r'"message":"([^"]+)"', msg)
        if matches:
            return self.BackendException(matches[0])
        else:
            return self.BackendException(msg)

    @cached_property
    def _credential(self):
        """
        :rtype: AzureCliAuthentication
        """
        return AzureCliAuthentication()

    def get_available_subscriptions(self):
        """
        """
        subscription_client = SubscriptionClient(self._credential)
        try:
            return list(subscription_client.subscriptions.list())
        except azureml._common.exceptions.AzureMLException as e:
            raise self.parse_azureml_exception(e)

    def get_available_resource_groups(self, subscription_id):
        """
        :param str subscription_id:
        """
        resource_client = ResourceManagementClient(
            self._credential, subscription_id)
        try:
            return list(resource_client.resource_groups.list())
        except azureml._common.exceptions.AzureMLException as e:
            raise self.parse_azureml_exception(e)

    # -- Workspaces ----------------------------------------------------------

    def get_available_workspaces(self, subscription_id, resource_group):
        """
        :param str subscription_id:
        :param str resource_group:
        :rtype: list[Workspace]
        """
        try:
            workspaces_mapped = Workspace.list(
                auth=self._credential,
                subscription_id=subscription_id,
                resource_group=resource_group,
            )
        except azureml._common.exceptions.AzureMLException as e:
            raise self.parse_azureml_exception(e)

        workspaces = []

        for workspace_list in workspaces_mapped.values():
            workspaces.extend(workspace_list)

        return workspaces

    def get_available_workspace_names(self, subscription_id, resource_group):
        """
        :param str subscription_id:
        :param str resource_group:
        :rtype: list[str]
        """
        available_workspaces = self.get_available_workspaces(
            subscription_id=subscription_id,
            resource_group=resource_group,
        )

        return [w.name for w in available_workspaces]

    def get_workspace(self, subscription_id, resource_group, name):
        """
        :param str subscription_id:
        :param str resource_group:
        :param str name:
        :rtype: Workspace
        """
        try:
            return Workspace.get(
                auth=self._credential,
                subscription_id=subscription_id,
                resource_group=resource_group,
                name=name,
            )
        except azureml._common.exceptions.AzureMLException as e:
            raise self.parse_azureml_exception(e)

    # -- Compute clusters ----------------------------------------------------

    def get_compute_clusters(self, workspace):
        """
        :param Workspace workspace:
        """
        try:
            return AmlCompute.list(workspace=workspace)
        except azureml._common.exceptions.AzureMLException as e:
            raise self.parse_azureml_exception(e)

    def get_available_vm_sizes(self, workspace):
        """
        :param Workspace workspace:
        :rtype: typing.List[str]
        """
        try:
            return AmlCompute.supported_vmsizes(workspace=workspace)
        except azureml._common.exceptions.AzureMLException as e:
            raise self.parse_azureml_exception(e)

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

        compute_config = AmlCompute.provisioning_configuration(
            vm_size=vm_size,
            min_nodes=min_nodes,
            max_nodes=max_nodes,
            vnet_resourcegroup_name=vnet_resource_group_name,
            vnet_name=vnet_name,
            subnet_name=subnet_name,
        )

        try:
            ComputeTarget \
                .create(workspace, name, compute_config) \
                .wait_for_completion(show_output=False)
        except azureml._common.exceptions.AzureMLException as e:
            raise self.parse_azureml_exception(e)

    # -- Contexts ------------------------------------------------------------

    def get_local_training_context(self, force_download):
        """
        :param bool force_download:
        :rtype: energinetml.core.AbstractTrainingContext
        """
        return AzureLocalTrainingContext(self, force_download)

    def get_cloud_training_context(self):
        """
        :rtype: energinetml.core.AbstractTrainingContext
        """
        return AzureCloudTrainingContext()

    def submit_model(self, model, params):
        """
        :param energinetml.core.model.Model model:
        :param list[str] params:
        :rtype: energinetml.core.SubmitContext
        """
        cd = CondaDependencies()
        cd.set_python_version(PYTHON_VERSION)

        # Project requirements (from requirements.txt)
        for requirement in model.requirements:
            cd.add_pip_package(str(requirement))

        # Python environment
        env = Environment(str(model.requirements.get(PACKAGE_NAME)))
        env.python.conda_dependencies = cd

        compute_config = RunConfiguration()
        compute_config.target = model.compute_target
        compute_config.environment = env

        workspace = self.get_workspace(
            name=model.project.workspace_name,
            subscription_id=model.project.subscription_id,
            resource_group=model.project.resource_group,
        )

        experiment = Experiment(
            workspace=workspace,
            name=model.experiment,
        )

        with model.temporary_folder() as path:
            config = ScriptRunConfig(
                source_directory=path,
                script=model.SCRIPT_FILE_NAME,
                arguments=['model', 'train', '--cloud-mode'] + list(params),
                run_config=compute_config,
            )

            try:
                run = experiment.submit(config)
            except azureml._common.exceptions.AzureMLException as e:
                raise self.parse_azureml_exception(e)

            return AzureSubmitContext(model, run)

    def release_model(self, workspace, model_path, model_name, **kwargs):
        """
        :rtype: Model
        """
        try:
            asset = Model._create_asset(
                workspace.service_context, model_path, model_name, None)

            return Model._register_with_asset(
                workspace=workspace,
                model_name=model_name,
                asset_id=asset.id,
                **kwargs,
            )
        except azureml._common.exceptions.AzureMLException as e:
            raise self.parse_azureml_exception(e)
