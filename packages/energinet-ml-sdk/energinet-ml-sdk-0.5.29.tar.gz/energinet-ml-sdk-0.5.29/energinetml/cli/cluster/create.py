import click
import click_spinner

from energinetml.cli.utils import discover_model
from energinetml.backend import default_backend as backend
from energinetml.settings import DEFAULT_VM_CPU, DEFAULT_VM_GPU


@click.command()
@discover_model()
def create(model):
    """
    Build a Docker image with a HTTP web API for model prediction.
    \f

    :param energinetml.Model model:
    """
    workspace = backend.get_workspace(
        subscription_id=model.project.subscription_id,
        resource_group=model.project.resource_group,
        name=model.project.workspace_name,
    )

    new_or_existing_cluster = click.prompt(
        text='Would you like to setup a new compute cluster, or use an existing one?',
        type=click.Choice(['new', 'existing']),
    )

    if new_or_existing_cluster == 'new':
        cluster, vm_size = _create_new_compute_cluster(model.project, workspace)
    elif new_or_existing_cluster == 'existing':
        cluster, vm_size = _use_existing_compute_cluster(workspace)
    else:
        raise RuntimeError('')

    model.compute_target = cluster
    model.vm_size = vm_size
    model.save()


# -- Helper functions --------------------------------------------------------


def _create_new_compute_cluster(project, workspace):
    """
    Executes CLI-flow for setting up a new compute cluster.

    :param energinetml.Project project:
    :param azureml.core.Workspace workspace:
    """
    available_vm_sizes = backend.get_available_vm_sizes(workspace)
    available_vm_size_mapped = {vm['name']: vm for vm in available_vm_sizes}

    click.echo((
        'You can either specific an exact VM Size, or use a default '
        'VM Size for either CPU or GPU computation.'
    ))
    vm_size_or_gpu_or_cpu = click.prompt(
        text='How would you like to specify VM Size?',
        type=click.Choice(['vmsize', 'cpu', 'gpu']),
    )

    vm_size = None
    cluster = None

    if vm_size_or_gpu_or_cpu == 'vmsize':
        vm_size = click.prompt(
            text='Please enter a VM size',
            type=click.Choice(available_vm_size_mapped),
        )
    elif vm_size_or_gpu_or_cpu == 'cpu':
        vm_size = DEFAULT_VM_CPU
        cluster = 'CPU-Cluster'
    elif vm_size_or_gpu_or_cpu == 'gpu':
        vm_size = DEFAULT_VM_GPU
        cluster = 'GPU-Cluster'

    if vm_size not in available_vm_size_mapped:
        click.echo('VM Size unavailable: %s' % vm_size)
        vm_size = click.prompt(
            text='Please enter a VM size',
            type=click.Choice(available_vm_size_mapped),
        )

    if cluster is None:
        cluster = vm_size.replace('_', '-')

    min_nodes = click.prompt(
        text='Please enter minimum nodes available',
        default=0,
        type=int,
    )

    max_nodes = click.prompt(
        text='Please enter maximum nodes available',
        default=1,
        type=int,
    )

    cluster = click.prompt(
        text='Please enter a name for the compute cluster',
        default=cluster,
        type=str,
    )

    existing_clusters = backend.get_compute_clusters(workspace)
    existing_cluster_names = [c.name for c in existing_clusters]

    while cluster in existing_cluster_names:
        click.echo('Cluster already exists: %s' % cluster)
        cluster = click.prompt(
            text='Please enter a name for the compute cluster',
            default=cluster,
            type=str,
        )

    click.echo('Creating compute cluster "%s" using VM Size: %s'
               % (cluster, vm_size))

    with click_spinner.spinner():
        backend.create_compute_cluster(
            workspace=workspace,
            name=cluster,
            vm_size=vm_size,
            min_nodes=min_nodes,
            max_nodes=max_nodes,
            vnet_resource_group_name=project.resource_group,
            vnet_name=project.vnet_name,
            subnet_name=project.subnet_name,
        )

    return cluster, vm_size


def _use_existing_compute_cluster(workspace):
    """
    Executes CLI-flow for using an existing compute cluster.
    
    :param azureml.core.Workspace workspace:
    """
    existing_clusters = backend.get_compute_clusters(workspace)
    existing_clusters_mapped = {c.name: c for c in existing_clusters}
    existing_cluster_names = [c.name for c in existing_clusters]

    if len(existing_clusters) == 0:
        click.echo('No compute clusters exists in workspace "%s"'
                   % workspace.name)
        raise click.Abort()

    default = existing_cluster_names[0] \
        if len(existing_cluster_names) == 1 \
        else None

    cluster = click.prompt(
        text='Please enter name of existing compute cluster',
        type=click.Choice(existing_cluster_names),
        default=default,
    )

    return cluster, existing_clusters_mapped[cluster].vm_size
