import click

from energinetml.core.http import run_predict_api
from energinetml.cli.utils import discover_model, discover_trained_model


@click.command()
@discover_model()
@discover_trained_model()
@click.option('--host', default='127.0.0.1', type=str,
              help='Host to serve on (default: 127.0.0.1)')
@click.option('--port', default=8080, type=int,
              help='Port to serve on (default: 8080)')
@click.option('--model-version', 'model_version', default=None, type=str,
              help='Model version (used for logging)')
def serve(host, port, model, trained_model, model_version):
    """
    Serve a HTTP web API for model prediction.
    \f

    :param str host:
    :param int port:
    :param Model model:
    :param TrainedModel trained_model:
    :param typing.Optional[str] model_version:
    """
    run_predict_api(
        model=model,
        trained_model=trained_model,
        model_version=model_version,
        host=host,
        port=port,
    )
