import os
import sys

from invoke import task


def _get_pyupgrade_python_version_arg():
    python_version = sys.version_info
    for minor_version in (8, 7):
        if python_version >= (3, minor_version):
            return f"--py3{minor_version}-plus"
    else:
        return "--py36-plus"


def _is_django_installed():
    try:
        import django
    except ImportError:
        return False
    else:
        return True


def _is_django_project():
    return _is_django_installed() and os.path.exists("./manage.py")


@task
def pyupgrade(c):
    """
    Upgrade Python syntax using pyupgrade.
    Exits non-zero if any changes are made, so doubles as a check.
    """
    python_version_arg = _get_pyupgrade_python_version_arg()
    c.run(f"pyupgrade {python_version_arg} $(find . -name '*.py')")


@task
def isort(c):
    """
    Check Python code for incorrectly-sorted imports.
    """
    c.run("isort . --check")


@task
def black(c):
    """
    Check Python code for style errors.
    """
    c.run("black . --check")


@task
def migrations(c):
    """
    Check Django models for outstanding changes.
    """
    c.run("./manage.py makemigrations --check")


@task(default=True)
def all(c):
    """
    Perform all checks.
    """
    pyupgrade(c)
    isort(c)
    black(c)

    # It only makes sense to perform migration checks on Django projects
    if _is_django_project():
        migrations(c)
