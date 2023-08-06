import os
import sys
import subprocess

from energinetml.settings import DOCKERFILE_PATH, PACKAGE_VERSION


def build_prediction_api_docker_image(
        path, tag, trained_model_file_path, model_version):
    """
    TODO Add package version when installing energinet-ml-sdk

    :param str path:
    :param str tag: Docker tag
    :param str trained_model_file_path:
    :param str model_version: Model version (for logging)
    """
    trained_model_file_real_path = os.path.realpath(
        trained_model_file_path)
    trained_model_file_relative_path = os.path.relpath(
        trained_model_file_path, path)
    model_real_path = os.path.realpath(path)

    if not trained_model_file_real_path.startswith(model_real_path):
        raise ValueError((
            'Trained model file must be located within the model folder. '
            'You are trying to add file "%s" which is not located within '
            'the model folder (%s). This is not supported by Docker.'
        ) % (trained_model_file_path, path))

    command = ['docker', 'build']
    command.extend(('--tag', tag))
    command.extend(('--file', DOCKERFILE_PATH))
    command.extend(('--build-arg', 'TRAINED_MODEL_PATH=%s' % trained_model_file_relative_path))
    command.extend(('--build-arg', 'PACKAGE_VERSION=%s' % PACKAGE_VERSION))
    command.extend(('--build-arg', 'MODEL_VERSION=%s' % model_version))

    command.append(path)

    subprocess.check_call(
        command, stdout=sys.stdout, stderr=subprocess.STDOUT)
