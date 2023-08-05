import os
from packaging import version
from pkg_resources import Requirement


# -- Directories/paths -------------------------------------------------------

__current_file = os.path.abspath(__file__)
__current_folder = os.path.split(__current_file)[0]

SOURCE_DIR = os.path.abspath(__current_folder)
STATIC_DIR = os.path.join(SOURCE_DIR, 'static')
EMPTY_MODEL_TEMPLATE_DIR = os.path.join(STATIC_DIR, 'model-template')
DOCKERFILE_PATH = os.path.join(STATIC_DIR, 'Dockerfile')


def __read_meta(fn):
    with open(os.path.join(__current_folder, 'meta', fn)) as f:
        return f.read().strip()


# -- Cloud -------------------------------------------------------------------

DEFAULT_LOCATION = 'westeurope'
DEFAULT_VM_CPU = 'Standard_D1_v2'
DEFAULT_VM_GPU = 'Standard_NV6'


# -- Package details ---------------------------------------------------------

# TODO Rename "PACKAGE" to "SDK" (here and elsewhere in general)

PYTHON_VERSION = __read_meta('PYTHON_VERSION')
PACKAGE_NAME = __read_meta('PACKAGE_NAME')
COMMAND_NAME = __read_meta('COMMAND_NAME')
PACKAGE_VERSION = version.parse(__read_meta('PACKAGE_VERSION'))
PACKAGE_REQUIREMENT = Requirement('%s==%s' % (
    PACKAGE_NAME, PACKAGE_VERSION))


# -- Misc --------------------------------------------------------------------

APP_INSIGHT_INSTRUMENTATION_KEY = os.environ.get(
    'APP_INSIGHT_INSTRUMENTATION_KEY')
