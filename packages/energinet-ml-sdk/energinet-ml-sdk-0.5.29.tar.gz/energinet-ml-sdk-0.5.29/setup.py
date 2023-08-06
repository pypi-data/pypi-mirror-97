"""
Example setup.py from https://github.com/activescott/python-package-example/blob/master/package-project/src/setup.py.
"""
# Always prefer setuptools over distutils
import os
import codecs
import setuptools
from distutils.command.sdist import sdist


class sdist_hg(sdist):
    """Add git short commit hash to version.
    Based on https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/specification.html
    """

    user_options = sdist.user_options + [("dev", None, "Add a dev marker")]

    def initialize_options(self):
        sdist.initialize_options(self)
        self.dev = 0

    def run(self):
        if self.dev:
            suffix = f".dev{self.get_timestamp()}"
            self.distribution.metadata.version += suffix
            print(self.distribution.metadata.version)
        sdist.run(self)

    def get_tip_revision(self):
        import git
        repo = git.Repo()
        sha = repo.head.commit.hexsha
        short_sha = repo.git.rev_parse(sha, short=True)
        return short_sha

    def get_timestamp(self):
        from datetime import datetime
        now = datetime.now()
        stamp = now.strftime("%Y%m%d%H%M%S")
        return stamp


here = os.path.abspath(os.path.dirname(__file__))


def __read_meta(fn):
    with open(os.path.join(here, 'energinetml', 'meta', fn)) as f:
        return f.read().strip()


name = __read_meta('PACKAGE_NAME')
version = __read_meta('PACKAGE_VERSION')
python_requires = __read_meta('PYTHON_VERSION')
command = __read_meta('COMMAND_NAME')


setuptools.setup(
    name=name,
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,
    description="Energinet Machine Learning",
    author="Koncern Digitalisering Advanced Analytics Team",
    author_email="mny@energinet.dk, xjakk@energinet.dk",
    # Choose your license
    license="Apache Software License 2.0",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.8",
    ],
    # What does your project relate to?
    keywords=[],
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=setuptools.find_packages(),  # Required
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # TODO SPECIFIC VERSION OF REQUIREMENTS!
    install_requires=[
        'pandas==1.1.4',
        'packaging',
        'pyjwt==1.7.1',
        'click==7.1.2',
        'click-spinner==0.1.10',
        'fastapi==0.63.0',
        'uvicorn==0.13.3',
        'pydantic==1.7.3',
        'azure-cli-core==2.18.0',
        'azure-identity==1.2.0',
        'azureml-sdk==1.21.0',
        'opencensus-ext-azure==1.0.7',
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": [],
        "test": [],
    },
    cmdclass={"sdist": sdist_hg},

    python_requires=">=3.8",

    include_package_data=True,
    package_data={'': [
        'meta/*',
        'static/*',
        'static/model-template/*',
    ]},

    entry_points={
        'console_scripts': ['%s=energinetml.cli:main' % command],
    }
)
