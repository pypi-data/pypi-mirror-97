"""
 
 This module use twine for publishing packages.
 
"""

from invoke import run
from invoke import task


@task
def clean(ctxt):
    """
    Clean build directory.
    """
    run("rm dist/*")


@task
def build(ctxt):
    """
    Build package for publishing to PyPI
    """
    run("python3 setup.py sdist bdist_wheel")


@task
def publish(ctxt, repository):
    """
    Publish package and push to all remotes: --repository <pypi,gitlab>
    
    The mandtory `--repository` option expects repositories to be configured in `~/.pypirc`:
    
        [distutils]
        index-servers =
            pypi
            gitlab

        [pypi]
        username = __token__
        password = pypi-<token>

        [gitlab]
        repository = https://gitlab.dev.beat.no/api/v4/projects/229/packages/pypi
        username = __token__
        password = <token>
    """
    run(f"twine upload --repository {repository} dist/*")
    run("git remote | xargs -L 1 -I remote git push remote")
