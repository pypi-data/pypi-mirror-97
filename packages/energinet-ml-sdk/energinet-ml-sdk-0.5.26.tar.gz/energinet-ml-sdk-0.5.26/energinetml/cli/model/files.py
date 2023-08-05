import click

from energinetml.cli.utils import discover_model


@click.command()
@discover_model()
def files(model):
    """
    List files that are copied to the cloud when submitting.
    \f

    :param Model model:
    """
    for file_path in sorted(model.files):
        click.echo(file_path)
