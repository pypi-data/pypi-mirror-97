import click

# Hack OS version to avoid licencing problems in azureml
# TODO How else to get azureml Datasets working?
# TODO Move to somewhere else?
from dotnetcore2 import runtime
runtime.version = ("18", "10", "0")

from energinetml.settings import PACKAGE_VERSION

from .project import project_group
from .model import model_group
from .cluster import cluster_group


@click.command()
def version():
    """
    Prints SDK version.
    """
    click.echo(PACKAGE_VERSION)


@click.group()
def main():
    pass


main.add_command(project_group, 'project')
main.add_command(model_group, 'model')
main.add_command(cluster_group, 'cluster')
main.add_command(version)
