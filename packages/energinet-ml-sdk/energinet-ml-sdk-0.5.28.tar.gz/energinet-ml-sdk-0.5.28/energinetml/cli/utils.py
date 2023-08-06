import os
import click

from energinetml.core.project import Project
from energinetml.core.model import (
    Model,
    TrainedModel,
    import_model_class,
    ModelImportError,
    ModelNotClassError,
    ModelNotInheritModel,
)


def abort_if_false_callback(ctx, param, value):
    """
    TODO
    """
    if not value:
        ctx.abort()


def discover_project(required=True):
    """
    TODO
    """
    def _project_from_path_callback(ctx, param, value):
        try:
            return Project.from_directory(value)
        except Project.NotFound:
            if required:
                click.echo((
                    'Could not find a project in this folder '
                    '(or any of its parents): %s'
                ) % value)

                click.echo((
                    'I am looking for a folder which contains a file '
                    'named "%s" - either in the folder itself or in '
                    'one of its parent folders.'
                ) % Project.CONFIG_FILE_NAME)

                click.echo((
                    'Specify which project to use by providing the '
                    '-p/--path parameter.'
                ))

                raise click.Abort()

    return click.option(
        '--path', '-p', 'project',
        default='.',
        type=click.Path(dir_okay=True, resolve_path=True),
        help='Project directory path (default: current directory)',
        callback=_project_from_path_callback,
    )


def discover_model(required=True, load_model=True, param_name='model'):
    """
    TODO
    """
    def _model_from_path_callback(ctx, param, value):
        model_file_path = os.path.join(value, Model.SCRIPT_FILE_NAME)

        # Does model.py exist?
        if not os.path.isfile(model_file_path):
            click.echo((
                'Could not find a model in this folder '
                '(or any of its parents): %s'
            ) % value)

            click.echo((
                'I am looking for a folder which contains a file '
                'named "%s" - either in the folder itself or in '
                'one of its parent folders.'
            ) % Model.SCRIPT_FILE_NAME)

            click.echo((
                'Specify which model to use by providing the '
                '-p/--path parameter.'
            ))

            raise click.Abort()

        try:
            model_class = import_model_class(model_file_path)
        except ModelImportError:
            # Imported script does not have a "model" attribute
            click.echo('Failed to import your model class from file: %s'
                       % model_file_path)

            click.echo((
                'Make sure you refer your model class and name it "model". '
                'Do this by defining a global variable named "model" in your '
                'model script, and point it to your model class.'
            ))

            click.echo('')
            click.echo('Example:')
            click.echo('')
            click.echo('    class MyModel(Model):')
            click.echo('        ...')
            click.echo('')
            click.echo('    model = MyModel')
            click.echo('')

            raise click.Abort()
        except ModelNotClassError:
            # Imported "model" attribute is not a Class type
            click.echo('Failed to import your model class from file: %s'
                       % model_file_path)

            click.echo((
                'When you define the "model" object in your model script, '
                'make sure not to instantiate it.'
            ))

            click.echo('')
            click.echo('Example of doing it correct:')
            click.echo('')
            click.echo('    class MyModel(Model):')
            click.echo('        ...')
            click.echo('')
            click.echo('    model = MyModel')

            click.echo('')
            click.echo('Example of doing it WRONG:')
            click.echo('')
            click.echo('    class MyModel(Model):')
            click.echo('        ...')
            click.echo('')
            click.echo('    model = MyModel()  # Notice the instantiation')
            click.echo('')

            raise click.Abort()
        except ModelNotInheritModel:
            # Imported "model" attribute does not inherit from Model
            click.echo('Failed to import your model class from file: %s'
                       % model_file_path)

            click.echo((
                'The model you are referring to does not inherit from Model.'
            ))

            click.echo('')
            click.echo('Example of doing it correct:')
            click.echo('')
            click.echo('    from energinetml import Model')
            click.echo('')
            click.echo('    class MyModel(Model):  # Notice the inheritance')
            click.echo('        ...')
            click.echo('')
            click.echo('    model = MyModel')
            click.echo('')

            raise click.Abort()

        try:
            return model_class.from_directory(value)
        except Model.NotFound:
            if required:
                click.echo((
                    'Could not find a model in this folder '
                    '(or any of its parents): %s'
                ) % value)

                click.echo((
                    'I am looking for a folder which contains a file '
                    'named "%s" - either in the folder itself or in '
                    'one of its parent folders.'
                ) % Model.CONFIG_FILE_NAME)

                click.echo((
                    'Specify which model to use by providing the '
                    '-p/--path parameter.'
                ))

                raise click.Abort()

    return click.option(
        '--path', '-p', 'model',
        default='.',
        type=click.Path(dir_okay=True, resolve_path=True),
        help='Model directory path (default: current directory)',
        callback=_model_from_path_callback,
    )


def discover_trained_model(required=True, load_model=True, param_name='trained_model'):
    """
    TODO
    """
    def _project_from_path_callback(ctx, param, value):
        if value is not None:
            fp = value
        elif ctx.params.get('model'):
            fp = ctx.params['model'].trained_model_path
        elif required:
            click.echo((
                'Could not determine path to trained model file. '
                'Specify one by providing the -m/--model-file parameter.'
            ))
            # click.echo((
            #     'I am looking for a file named "%s" in your model folder (%s)'
            # ) % Model.path)
            raise click.Abort()
        else:
            return None

        if not os.path.isfile(fp):
            click.echo('Trained model not found: %s' % fp)
            if value is None:
                click.echo('Specify one by providing the -m/--model-file parameter.')
            raise click.Abort()

        if not load_model:
            return fp
        else:
            try:
                return TrainedModel.load(fp)
            except Project.NotFound:
                click.echo('Failed to load trained model: %s' % fp)
                raise click.Abort()

    return click.option(
        '--model-file', '-m', param_name,
        default=None,
        type=click.Path(file_okay=True, resolve_path=True),
        help='Trained model file',
        callback=_project_from_path_callback,
    )


def requires_parameter(name, type):
    """
    TODO
    """
