from invoke import task
from tabulate import tabulate

from metrics import BuildsCollector


@task
def setup(ctx):
    """ Setup the project and install dependencies """
    ctx.run('pip3 install -r requirements.txt')


@task
def lint(ctx):
    """ Perform linting of the source code """
    print('Running linting...')
    ctx.run('pylint metrics')


@task
def test(ctx):
    """ Perform unit tests """
    print('Running unit tests...')
    ctx.run('pytest --disable-pytest-warnings --cov metrics --cov-report term-missing')


@task
def metrics(_):
    """ Print the build metrics """
    collector = BuildsCollector()
    build_metrics, headers = collector.get_metrics_table()
    print(tabulate(build_metrics, headers=headers))


@task(default=True, pre=[lint], post=[test])
def build(_):
    """ Perform the general build for the metrics project """
