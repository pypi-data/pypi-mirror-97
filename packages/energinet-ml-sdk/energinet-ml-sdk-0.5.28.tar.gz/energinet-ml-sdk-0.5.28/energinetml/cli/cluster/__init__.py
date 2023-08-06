import click

from .create import create


@click.group()
def cluster_group():
    """
    Manage compute clusters
    """
    pass


cluster_group.add_command(create)
