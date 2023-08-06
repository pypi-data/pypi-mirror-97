"""
Command line interface.

Requires invoke (pip install invoke). For help run "invoke -h", to list
commands "invoke -l" (you can also run the shorthand command "inv")

Source code for simple commands can be included here, for large ones, save it
in the lib/ folder and import it here.
"""
from invoke import task
from lib import conda, versioneer


@task
def setup(c):
    """Setup development environment
    """
    print('Creating conda environment...')
    c.run('conda env create environment.yml --force')
    print('Installing package...')
    conda.run_in_env(c, 'pip install --editable .[dev]', env='package_name')
    print('Done! Activate your environment with: conda activate package_name')
    print('Then run the pipeline with: ploomber build')


@task(
    help={
        'inplace':
        'Runs tests in the current environment '
        '(calling pytest directly). Does not generate lock file'
    })
def test(c, inplace=False):
    """Run tests and generates lock file
    """
    if inplace:
        print('Running tests in the current environment...')
        c.run('pytest tests/', pty=True)
    else:
        c.run('nox', pty=True)


@task
def version(c):
    """
    Create a new version
    1. Set new stable version in package_name/__init__.py
    2. Update header in CHANGELOG file, and ask to review CHANGELOG
    3. Create commit for new version, create git tag, and push
    4. Set new development version in package_name/__init__.py and CHANGELOG
    5. Commit new development version, and push

    (more details in CONTRIBUTING.md)
    """
    versioneer.version(project_root='.', tag=True)
