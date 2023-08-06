import click
import click_spinner

from energinetml.core.model import Model, TrainedModel
from energinetml.backend import default_backend as backend
from energinetml.settings import PACKAGE_VERSION, PACKAGE_NAME
from energinetml.cli.utils import discover_model


# -- CLI Command -------------------------------------------------------------


@click.command()
@discover_model()
@click.argument('parameters', nargs=-1)
@click.option('--cloud-mode', '-c', 'cloud_mode',
              default=False, is_flag=True,
              help='Run training in cloud mode (do not use locally)')
@click.option('--force-download', '-f', 'force_download',
              default=True, is_flag=True,
              help='Force download of datasets (ignore locally cached files)')
@click.option('--seed', '-s',
              required=False, default=None, type=str,
              help='Seed value')
def train(parameters, cloud_mode, force_download, seed, model):
    """
    Train a model locally.
    \f

    :param list[str] parameters:
    :param bool cloud_mode:
    :param bool force_download:
    :param str seed:
    :param Model model:
    """

    # -- Train Parameters ----------------------------------------------------

    params = model.parameters.copy()
    params.update(dict(param.split(':') for param in parameters))
    params['seed'] = seed \
        if seed is not None \
        else model.generate_seed()

    # -- Tags ----------------------------------------------------------------

    tags = model.default_tags.copy()
    tags[PACKAGE_NAME] = str(PACKAGE_VERSION)
    tags.update(params)

    # -- Training context ----------------------------------------------------

    if cloud_mode:
        # Training is running in the cloud
        context = backend.get_cloud_training_context()
    else:
        # Training is running locally
        context = backend.get_local_training_context(force_download)

    # -- Training ------------------------------------------------------------

    click.echo('Training model...')

    try:
        trained_model = context.train_model(model=model, tags=tags, **params)
    except NotImplementedError:
        click.echo('Training script needs an implementation!')
        click.echo((
            'The train() method of your model raised a NotImplementedError '
            'which indicates that you have not yet implemented it.'
        ))
        click.echo('Stacktrace follows:')
        click.echo('-' * 79)
        raise

    # -- Verify returned object ----------------------------------------------

    click.echo('-' * 79)
    click.echo('Training complete')
    click.echo('Verifying trained model...')

    # Must be of type TrainedModel
    if not isinstance(trained_model, TrainedModel):
        click.echo('-' * 79)
        click.echo((
            'The object returned by your train()-method must be of type '
            'TrainedModel (or inherited classes). You gave me something '
            'of type %s instead.'
        ) % str(type(trained_model)))
        raise click.Abort()

    # Verify object properties
    try:
        trained_model.verify()
    except trained_model.Invalid as e:
        click.echo('-' * 79)
        click.echo('%s is INVALID: %s' % (trained_model.__class__.__name__, str(e)))
        raise click.Abort()

    # -- Dump output to disk -------------------------------------------------

    click.echo('Dumping trained model to: %s' % model.trained_model_path)

    trained_model.params.update(params)
    trained_model.dump(model.trained_model_path)

    # -- Upload output files -------------------------------------------------

    click.echo('Uploading output files...')

    with click_spinner.spinner():
        context.save_output_files(model)

    # -- Print portal link ---------------------------------------------------

    click.echo('Portal link: %s' % context.get_portal_url())
