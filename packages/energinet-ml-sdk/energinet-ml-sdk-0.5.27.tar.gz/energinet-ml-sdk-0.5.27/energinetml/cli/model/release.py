import os
import click
import click_spinner
import zipfile
import tempfile
from azureml.core import (
    Run as AzRun,
    Experiment as AzExperiment,
)

from energinetml.backend import default_backend as backend
from energinetml.core.model import Model, TrainedModel
from energinetml.cli.utils import discover_model


# -- CLI Command -------------------------------------------------------------


@click.command()
@discover_model()
@click.option('--run-id', '-r', 'run_id',
              type=str, required=False, default=None,
              help='Run ID to release')
def release(run_id, model):
    """
    Release a model.
    \f

    :param str run_id:
    :param Model model:
    """
    project = model.project

    workspace = backend.get_workspace(
        name=project.workspace_name,
        subscription_id=project.subscription_id,
        resource_group=project.resource_group,
    )

    if run_id is None:
        run_id = _get_run_id_if_omitted(workspace, model)

    run = AzRun.get(
        workspace=workspace,
        run_id=run_id,
    )

    # -- Download files ------------------------------------------------------

    click.echo('Releasing model using Run ID: %s' % run_id)

    with tempfile.TemporaryDirectory() as temp_folder_path:

        # -- Download resources ----------------------------------------------

        # Download project snapshot (model.py, model.json, etc).
        # Snapshot is downloaded as a zip-archive.
        click.echo('Downloading model code snapshot')
        with click_spinner.spinner():
            snapshot_zip_path = run.restore_snapshot(path=temp_folder_path)

        # Download the trained model file (artifact).
        click.echo('Downloading trained model file')
        with click_spinner.spinner():
            # Trained model file path relative to model root
            trained_model_relative_path = \
                model.get_relative_file_path(model.trained_model_path)

            # Absolute path where trained model file is downloaded to
            trained_model_absolute_path = \
                os.path.join(temp_folder_path, trained_model_relative_path)

            # Download trained model file
            run.download_file(
                name=trained_model_relative_path,
                output_file_path=trained_model_absolute_path,
            )

        # -- Handle resources ------------------------------------------------

        # Instantiate TrainedModel object to test its existence and validity
        try:
            TrainedModel.load(trained_model_absolute_path)
        except:
            # TODO Error handling
            raise

        # Add trained model file to existing archive
        click.echo('Archiving files')
        with click_spinner.spinner():
            z = zipfile.ZipFile(snapshot_zip_path, 'a')
            z.write(
                filename=trained_model_absolute_path,
                arcname=trained_model_relative_path,
            )
            z.close()

        # -- Create Model ----------------------------------------------------

        # Can not use run.register_model() here, as its only able to copy
        # files from the Run's output folder, and we also want to package
        # the project files (from the restored snapshot).
        with click_spinner.spinner():
            model_tags = {k: v for k, v in run.tags.items()
                          if not k.startswith('_')}
            model_tags.update({'run_id': run_id})

            model = backend.release_model(
                workspace=workspace,
                model_path=snapshot_zip_path,
                model_name=project.name,
                properties=run.properties,
                description='TODO Describe me!',
                run_id=run_id,
                tags=model_tags,
            )

            click.echo('Released new model %s version %s' % (model.name, model.version))


# -- Helper functions --------------------------------------------------------

def _get_run_id_if_omitted(workspace, model):
    experiment = AzExperiment(
        workspace=workspace,
        name=model.experiment,
    )

    latest_runs = list(AzRun.list(experiment=experiment))

    if not latest_runs:
        click.echo('No runs exists for experiment %s' % model.experiment)
        raise click.Abort()

    latest_run_id = latest_runs[0].id

    use_latest_run = click.confirm((
        'You did not provide me with a Run ID. '
        'Would you like to use the latest (Run ID: %s)?'
    ) % latest_run_id)

    if use_latest_run is False:
        click.echo((
            'I do not know which run to release. Provide me with a '
            'Run ID using the -r/--run-id parameter.'
        ))
        raise click.Abort()

    return latest_run_id
