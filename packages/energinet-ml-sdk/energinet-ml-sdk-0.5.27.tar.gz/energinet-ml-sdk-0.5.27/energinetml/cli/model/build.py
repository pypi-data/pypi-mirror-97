import os
import click

from energinetml.core.docker import build_prediction_api_docker_image
from energinetml.cli.utils import discover_model, discover_trained_model


@click.command()
@click.option('--tag', '-t', required=True,
              help='Name and optionally a tag in the ‘name:tag’ format')
@click.option('--extra-index-url', 'extra_index_url',
              required=False, default=None,
              help='Extra URLs of PIP package indexes to use')
@click.option('--model-version', 'model_version',
              required=False, default=None, type=str,
              help='Model version (used for logging)')
@discover_model()
@discover_trained_model(load_model=False, param_name='trained_model_path')
def build(tag, extra_index_url, model_version, model, trained_model_path):
    """
    Build a Docker image with a HTTP web API for model prediction.
    \f

    :param str tag:
    :param typing.Optional[str] extra_index_url:
    :param typing.Optional[str] model_version:
    :param energinetml.Model model:
    :param str trained_model_path:
    """
    with model.temporary_folder(include_trained_model=True) as path:
        build_prediction_api_docker_image(
            path=path,
            trained_model_file_path=os.path.join(path, 'outputs/model.pkl'),
            extra_index_url=extra_index_url,
            model_version=model_version,
            tag=tag,
        )
