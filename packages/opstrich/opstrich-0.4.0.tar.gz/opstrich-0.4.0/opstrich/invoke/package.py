import os

from invoke import Exit, task


def _get_package_version(c):
    return c.run('poetry version --no-ansi | cut -d" " -f2').stdout.strip()


def _get_pyproject_filename(c):
    git_root = c.run("git rev-parse --show-toplevel").stdout.strip()
    return os.path.join(git_root, "pyproject.toml")


def _is_git_dirty(c):
    dirty_files = c.run("git status --porcelain").stdout.strip()
    return bool(dirty_files)


@task(
    help={
        "rule": "A valid semver string or a valid bump rule (eg. patch, minor, major, etc.)"
    }
)
def bump(c, rule):
    """
    Bumps the version of the package in pyproject.toml. Then commits, tags, and pushes the new version.
    """
    if _is_git_dirty(c):
        raise Exit("This repo has uncommitted changes. Aborting...")

    previous_version = _get_package_version(c)
    c.run(f"poetry version {rule}")
    pyproject_filename = _get_pyproject_filename(c)
    c.run(f"git add {pyproject_filename}")
    updated_version = _get_package_version(c)
    c.run(f"git commit -m 'Bump version from {previous_version} to {updated_version}'")
    c.run(f"git tag -a '{updated_version}' -m 'version {updated_version}'")
    c.run("git push --follow-tags")
