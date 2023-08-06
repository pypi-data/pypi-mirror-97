import json
import click
import pydantic

from energinetml.core.predicting import PredictionController
from energinetml.cli.utils import discover_model, discover_trained_model


@click.command()
@click.option('--json', '-j', 'json_str',
              required=False, type=str,
              help='Input JSON string')
@click.option('--json-file', '-f', 'json_file',
              type=click.File('r'),
              help='Input JSON filepath')
@discover_model()
@discover_trained_model()
def predict(json_str, json_file, model, trained_model):
    """
    Predict using a model.
    \f

    :param str json_str:
    :param typing.TextIO json_file:
    :param Model model:
    :param TrainedModel trained_model:
    """
    controller = PredictionController(model, trained_model)

    if not json_str and not json_file:
        click.echo((
            'You must provide me with either the -j/--json or the '
            '-f/--json-file parameter.'
        ))
        raise click.Abort()
    elif json_str and json_file:
        click.echo((
            'Do not provide me with both the -j/--json and the '
            '-f/--json-file parameter, I only need one.'
        ))
        raise click.Abort()

    if json_file:
        json_str = json_file.read()

    # Parse input JSON
    try:
        input_json = json.loads(json_str)
    except json.decoder.JSONDecodeError as e:
        click.echo('Failed to parse input json: %s' % str(e))
        raise click.Abort()

    # Load data model from JSON
    try:
        request = pydantic.parse_obj_as(controller.request_model, input_json)
    except pydantic.error_wrappers.ValidationError as e:
        click.echo('Invalid input JSON provided. Error description follows:')
        click.echo(str(e.json(indent=4)))
        raise click.Abort()

    # Predict
    try:
        predictions = controller.predict(request)
    except NotImplementedError:
        click.echo('Prediction script needs an implementation!')
        click.echo((
            'The predict() method of your model raised a NotImplementedError '
            'which indicates that you have not yet implemented it.'
        ))
        click.echo('Stacktrace follows:')
        click.echo('-' * 79)
        raise

    click.echo(json.dumps(predictions.dict(), indent=4))
