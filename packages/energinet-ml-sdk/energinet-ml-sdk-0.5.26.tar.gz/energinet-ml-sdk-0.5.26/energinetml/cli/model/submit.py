import click

from energinetml.cli.utils import discover_model
from energinetml.backend import default_backend as backend
from energinetml.settings import (
    PACKAGE_NAME,
    PACKAGE_VERSION,
    PACKAGE_REQUIREMENT,
)


@click.command()
@discover_model()
@click.argument('parameters', nargs=-1)
@click.option('--wait/--nowait', default=True,
              help='Wait for experiment to complete before exiting (default: yes)')
@click.option('--download', '-d', is_flag=True,
              help='Download output files after Run completed')
def submit(parameters, wait, download, model):
    """
    Submit a model to be trained in the cloud.
    \f

    TODO Describe how to create PAT (which access it requires etc.)

    :param list[str] parameters:
    :param bool wait:
    :param bool download:
    :param Model model:
    """
    if download and not wait:
        click.echo('Can not use -d/--download together with --nowait')
        raise click.Abort()

    # -- Verify SDK requirement ----------------------------------------------

    # Verify requirements.txt contains energinet-ml-sdk
    if PACKAGE_NAME not in model.requirements:
        click.echo((
            'Could not find "%s" in the project\'s '
            'requirements.txt file: %s'
        ) % (PACKAGE_NAME, model.project.requirements_file_path))
        click.echo('I suggest you add the following line:')
        click.echo('')
        click.echo('    %s' % PACKAGE_REQUIREMENT)
        click.echo('')
        raise click.Abort()

    required_sdk_version = model \
        .requirements \
        .get_version(PACKAGE_NAME)

    if required_sdk_version is None:
        click.echo('Using latest version of %s when training in the cloud.'
                   % PACKAGE_NAME)
    else:
        if required_sdk_version < PACKAGE_VERSION:
            click.echo('=' * 79)
            click.echo((
                'WARNING: Your requirements.txt file contains a version of '
                '%s (%s) which is older than your current installation (%s). '
                'I suggest you update your requirements.txt to match '
                'your current installation. '
            ) % (PACKAGE_NAME, required_sdk_version, PACKAGE_VERSION))
            click.echo('=' * 79)
        elif required_sdk_version > PACKAGE_VERSION:
            click.echo('=' * 79)
            click.echo((
                'WARNING: Your requirements.txt file contains a version of '
                '%s (%s) which is newer than your current installation (%s). '
                'I suggest you upgrade your installation using '
                '"pip install --upgrade %s ...". '
            ) % (PACKAGE_NAME, required_sdk_version,
                 PACKAGE_VERSION, PACKAGE_NAME))
            click.echo('=' * 79)

        click.echo('Using %s version %s when training in the cloud.' % (
            PACKAGE_NAME, required_sdk_version
        ))

    # -- Submit --------------------------------------------------------------

    context = backend.submit_model(
        model=model,
        params=parameters,
    )

    # Stream output to console?
    if wait:
        click.echo('-' * 79)
        click.echo('Streaming Run log...')
        click.echo('-' * 79)

        try:
            context.wait_for_completion()
        except context.FailedToWait as e:
            click.echo('-' * 79)
            click.echo(str(e))
            click.echo('')
            raise click.Abort()

    # -- Post-Run ------------------------------------------------------------

    # Download output files?
    if download:
        click.echo('-' * 79)
        click.echo('Downloading files...')
        context.download_files()
