import click

from .init import init_model
from .train import train
from .predict import predict
from .build import build
from .serve import serve
from .submit import submit
from .release import release
from .files import files


@click.group()
def model_group():
    """
    Manage machine learning models
    """
    pass


model_group.add_command(init_model, 'init')
model_group.add_command(train)
model_group.add_command(predict)
model_group.add_command(build)
model_group.add_command(serve)
model_group.add_command(submit)
model_group.add_command(release)
model_group.add_command(files)
