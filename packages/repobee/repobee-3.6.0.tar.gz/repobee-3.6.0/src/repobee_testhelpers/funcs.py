"""Helper functions for tests."""
import tempfile
import pathlib
import shutil
import shlex
import contextlib
from typing import Mapping, List, Union, Iterator

import repobee
import git  # type: ignore

import repobee_plug as plug

from repobee_testhelpers import localapi
from repobee_testhelpers import const


def initialize_repo(
    path: pathlib.Path, default_branch: str = "master"
) -> git.Repo:
    """Initialize the directory to a Git repo and commit all files in it.

    Args:
        path: Path to the directory to turn into a Git repository.
        default_branch: Name of the default branch to use.
    Returns:
        A repo.
    """
    repo = git.Repo.init(path)
    repo.git.config("user.name", const.TEACHER)
    repo.git.config("user.email", f"{const.TEACHER}@repobee.org")
    repo.git.checkout("-b", default_branch)
    repo.git.add(".", "--force")
    repo.git.commit("-m", "Initial commit")
    return repo


def hash_directory(dirpath: Union[str, pathlib.Path]) -> str:
    """Compute the directory hash using Git.

    Args:
        dirpath: Path to a directory.
    Returns:
        The hash of the root tree of the directory.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        target_dir = pathlib.Path(tmpdir) / "repo"
        shutil.copytree(dirpath, target_dir)

        if (target_dir / ".git").exists():
            shutil.rmtree(target_dir / ".git")

        repo = initialize_repo(target_dir)
        return repo.head.commit.tree.hexsha


def run_repobee(
    cmd: Union[str, List[str]], **kwargs
) -> Mapping[str, List[plug.Result]]:
    """Helper function to call :py:class:`repobee.run` when using the
    :py:class:`fakeapi.FakeAPI` platform API.

    This function will by default use a config file that sets appropriate
    values for ``students_file``, ``user``, ``org_name`` and
    ``template_org_name`` for use with the :py:class:`~fakeapi.FakeAPI`
    platform API. If you wish to use a different config, simply pass
    ``config_file="/path/to/your/config"`` to the function, or
    ``config_file=""`` to not use a config file at all.

    The :py:class:`~fakeapi.FakeAPI` plugin is always loaded last, so it is the
    not possible to use another platform API with this function. If you wish
    to do so, you should use :py:class`repobee.run` directly instead.

    Args:
        cmd: A string or list of strings with a RepoBee command.
        kwargs: Keyword arguments for :py:func:`repobee.run`.
    Returns:
        The results mapping returned by :py:func:`repobee.run`
    """
    cmd = shlex.split(cmd) if isinstance(cmd, str) else cmd
    kwargs = dict(kwargs)  # copy to not mutate input
    plugins = (kwargs.get("plugins") or []) + [localapi]
    kwargs["plugins"] = plugins

    students_file = (
        pathlib.Path(__file__).parent / "resources" / "students.txt"
    )

    with tempfile.NamedTemporaryFile() as tmp:
        config_file = pathlib.Path(tmp.name)
        config_file.write_text(
            f"""[repobee]
students_file = {students_file}
org_name = {const.TARGET_ORG_NAME}
user = {const.TEACHER}
template_org_name = {const.TEMPLATE_ORG_NAME}
token = {const.TOKEN}
"""
        )
        kwargs.setdefault("config_file", config_file)

        return repobee.run(cmd, **kwargs)


def template_repo_hashes() -> Mapping[str, str]:
    """Get hashes for the template repos.

    Returns:
        A mapping (template_repo_name -> hash)
    """
    return {
        path.name: hash_directory(path)
        for path in map(
            lambda name: const.TEMPLATE_REPO_DIR / name,
            const.TEMPLATE_REPO_NAMES,
        )
    }


def tree_hash(repo_root: pathlib.Path) -> str:
    """Get the hash of the HEAD tree object of this repository.

    Args:
        repo_root: Path to the root of a Git repository.
    Returns:
        The hash of the root tree object.
    """
    repo = git.Repo(repo_root)
    return repo.head.commit.tree.hexsha


def get_api(
    platform_url: str,
    org_name: str = const.TARGET_ORG_NAME,
    user: str = const.TEACHER,
    token: str = const.TOKEN,
) -> localapi.LocalAPI:
    """Return an instance of the :py:class:`fakeapi.FakeAPI`,
    configured for the tests.
    """
    return localapi.LocalAPI(
        base_url=platform_url, user=user, org_name=org_name, token=token
    )


def get_repos(
    platform_url: str, org_name: str = const.TARGET_ORG_NAME
) -> List[localapi.Repo]:
    """Get all repos from the given platform and organization.

    Args:
        platform_url: URL to the directory used by the
            :py:class:`fakeapi.FakeAPI`.
        org_name: The organization to get repos from.
    Returns:
        A list of fake repos.
    """
    api = get_api(platform_url, org_name=org_name)
    return list(api._repos[org_name].values())


def get_teams(
    platform_url: str, org_name: str = const.TARGET_ORG_NAME
) -> List[localapi.Team]:
    """Get all of the teams from the given platform and organization.
    Note that this returns the actual platform implementation of
    :py:class:`~repobee_plug.Team`.

    Args:
        platform_url: URL to the directory used by the
            :py:class:`fakeapi.FakeAPI`.
        org_name: The organization to get repos from.
    Returns:
        A list of platform teams.
    """
    api = get_api(platform_url, org_name=org_name)
    return list(api._teams[org_name].values())


def get_student_teams(
    platform_url: str, org_name: str = const.TARGET_ORG_NAME
) -> List[plug.StudentTeam]:
    """Like :py:func:`get_platform_teams`, but converts each team to a
    :py:class:`~repobee_plug.StudentTeam`. for easier comparison.

    Args:
        platform_url: URL to the directory used by the
            :py:class:`fakeapi.FakeAPI`.
        org_name: The organization to get repos from.
    Returns:
        A list of student teams.
    """
    api = get_api(platform_url, org_name=org_name)
    return [
        plug.StudentTeam(members=[usr.username for usr in team.members])
        for team in api._teams[org_name].values()
    ]


@contextlib.contextmanager
def update_repository(repo_url: str) -> Iterator[pathlib.Path]:
    """Context manager for updating a Git repository. Clones the repository
    from the given url, yields the path to the cloned directory, and then
    commits and pushes any changes after the context has been exited.

    Args:
        repo_url: URL to a Git repository.
    Returns:
        A context manager that yields a path to the local repository.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = pathlib.Path(tmpdir) / "repo"
        repo = git.Repo.clone_from(repo_url, to_path=repo_path)
        yield repo_path
        repo.git.add(".")
        repo.git.commit("-m", "Update repo")
        repo.git.push()
