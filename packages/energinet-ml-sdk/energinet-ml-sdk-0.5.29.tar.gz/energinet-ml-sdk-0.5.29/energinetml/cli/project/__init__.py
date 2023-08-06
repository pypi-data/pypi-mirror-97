import click

from .init import init_project


@click.group()
def project_group():
    """
    Manage machine learning projects
    """
    pass


project_group.add_command(init_project, 'init')
