import os
import click

from energinetml.core.project import Project
from energinetml.backend import default_backend as backend
from energinetml.settings import DEFAULT_LOCATION, COMMAND_NAME


# Constants  TODO Move to Project class?
PROJECT_FILES = ('project.json', 'requirements.txt')


# -- Input parsing and validation --------------------------------------------


def _parse_input_path(ctx, param, value):
    """
    TODO
    """
    if value is None:
        value = os.path.abspath(click.prompt(
            text='Enter project location',
            default=os.path.abspath('.'),
            type=click.Path(dir_okay=True, resolve_path=True),
        ))

    # Path points to a file?
    if os.path.isfile(value):
        click.echo('Failed to init project.')
        click.echo((
            'The path you provided me with points to a file, and not a '
            'folder. I need a folder to put the project files in. '
            'Check your -p/--path parameter.'
        ))
        click.echo('You provided me with: %s' % value)
        raise click.Abort()

    # Confirm overwrite files if they exists
    for filename in PROJECT_FILES:
        if os.path.isfile(os.path.join(value, filename)):
            click.echo('File already exists: %s'
                       % os.path.join(value, filename))
            if not click.confirm('Really override existing %s?' % filename):
                raise click.Abort()

    return value


def _parse_input_project_name(ctx, param, value):
    """
    TODO
    """
    if value is None:
        default = os.path.split(ctx.params['path'])[1] \
            if 'path' in ctx.params \
            else None

        value = click.prompt(
            text='Please enter a project name',
            default=default,
            type=str,
        )

    return value


def _parse_input_subscription_id(ctx, param, value):
    """
    TODO
    """
    subscriptions = backend.get_available_subscriptions()
    subscriptions_mapped = {
        s.display_name: s.subscription_id
        for s in subscriptions
    }

    if value not in subscriptions_mapped:
        if value is not None:
            click.echo('Azure Subscription "%s" not found' % value)

        value = click.prompt(
            text='Please enter Azure Subscription',
            type=click.Choice(subscriptions_mapped.keys()),
        )

    return subscriptions_mapped[value]


def _parse_input_resource_group(ctx, param, value):
    """
    TODO
    """
    if 'subscription_id' not in ctx.params:
        raise RuntimeError('Requires a "subscription_id" parameter')

    subscription_id = ctx.params['subscription_id']
    resource_groups = backend.get_available_resource_groups(
        subscription_id)
    resource_group_names = [g.name for g in resource_groups]

    if value not in resource_group_names:
        if value is not None:
            click.echo('Azure Resource Group "%s" not found' % value)

        value = click.prompt(
            text='Please enter Azure Resource Group',
            type=click.Choice(resource_group_names),
        )

    return value


def _parse_input_workspace_name(ctx, param, value):
    """
    TODO
    """
    if 'subscription_id' not in ctx.params:
        raise RuntimeError('Requires a "subscription_id" parameter')
    if 'resource_group' not in ctx.params:
        raise RuntimeError('Requires a "resource_group" parameter')

    existing_workspaces = backend.get_available_workspace_names(
        subscription_id=ctx.params['subscription_id'],
        resource_group=ctx.params['resource_group'],
    )

    if not existing_workspaces:
        click.echo('No AzureML Workspaces exists in this resource group')
        raise click.Abort()

    if value is None:
        default = existing_workspaces[0] \
            if len(existing_workspaces) == 1 \
            else None

        value = click.prompt(
            text='Please enter AzureML Workspace name',
            default=default,
            type=click.Choice(existing_workspaces),
        )

    return value


# -- CLI Command -------------------------------------------------------------


@click.command()
@click.option('--path', '-p',
              default=None,
              type=click.Path(dir_okay=True, resolve_path=True),
              callback=_parse_input_path,
              help='Project path (default to current)')
@click.option('--name', '-n',
              required=False, default=None, type=str,
              callback=_parse_input_project_name,
              help='Project name')
@click.option('--subscription', '-s', 'subscription_id',
              required=False, default=None, type=str,
              callback=_parse_input_subscription_id,
              help='Azure subscription name')
@click.option('--resource-group', '-r', 'resource_group',
              required=False, default=None, type=str,
              callback=_parse_input_resource_group,
              help='Azure Resource Group')
@click.option('--workspace', '-w', 'workspace_name',
              required=False, default=None, type=str,
              callback=_parse_input_workspace_name,
              help='AzureML Workspace name')
@click.option('--location', '-l', 'location',
              default=DEFAULT_LOCATION,
              required=False, type=str,
              help='Azure location (default: %s)' % DEFAULT_LOCATION)
def init_project(path, name, subscription_id, resource_group,
                 workspace_name, location):
    """
    Create a new, empty machine learning project.
    """
    if not os.path.isdir(path):
        os.makedirs(path)

    Project.create(
        path=path,
        name=name,
        subscription_id=subscription_id,
        resource_group=resource_group,
        workspace_name=workspace_name,
        location=location,
    )

    click.echo('-' * 79)
    click.echo('Initialized the project at: %s' % path)
    click.echo('Type "%s model init" to add a new model to the project.'
               % COMMAND_NAME)
