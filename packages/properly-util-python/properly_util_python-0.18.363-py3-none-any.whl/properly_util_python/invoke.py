import os

from invoke import task


@task
def setup_environment(c):
    """
    Prepares the environment variables for running the tests
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "FakeID"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "FakeKey"
    os.environ["AWS_DEFAULT_REGION"] = "us-west-1"
    os.environ["PROPERLY_STAGE"] = "local"


@task
def black(c, fix=False):
    """
    Run python black
    --fix : run the auto-fixer
    """
    c.run(f"black {'--check ' if not fix else ''}.")


@task
def pycodestyle(c):
    """
    Run pycodestyle
    """
    c.run("pycodestyle ./src ./tests")


@task(setup_environment)
def test(c, k=None):
    """
    Run tests
    """
    c.run(
        f"python -m pytest -v --log-cli-level=INFO ./tests/ --color=yes {f'-k {k}' if k else ''}"
    )


@task(black, pycodestyle)
def lint(c):
    """
    Run all lint commands
    """
    print(
        """
        \033[0;32m==========================================================
        \033[0;32mNo Issues! More effective at de-linting than Scotch-Brite!
        \033[0;32m==========================================================\033[0m
    """
    )


@task
def typecheck(c):
    """
    Run python mypy
    """
    c.run("mypy src tests --config-file=mypy.ini")


@task(aliases=['format'])
def prettify(c):
    """
    Run the auto-formatter
    """
    black(c, fix=True)


@task()
def deploy(c, stage=None):
    """
    Run the serverless deploy
    --stage : stage to deploy to
    """
    if not stage:
        print("must supply a stage, one of dev, staging, prod")
        return

    c.run(f"./node_modules/serverless/bin/serverless deploy --stage {stage}")
