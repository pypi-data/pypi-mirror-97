"""GitLab compatibility plugin.

This plugin allows RepoBee to be used with GitLab. If you want to use RepoBee
with GitLab, then you should first activate this plugin persistently. See
:ref:`activate_plugins` for details on how to do that.
"""
import os
import collections
import contextlib
import pathlib
import urllib.parse
import functools
from typing import List, Iterable, Optional, Generator

import gitlab  # type: ignore
import requests.exceptions

import repobee_plug as plug

from _repobee import exception

PLUGIN_DESCRIPTION = "Makes RepoBee compatible with GitLab"

ISSUE_GENERATOR = Generator[plug.Issue, None, None]


# see https://docs.gitlab.com/ee/api/issues.html for mapping details
_ISSUE_STATE_MAPPING = {
    plug.IssueState.OPEN: "opened",
    plug.IssueState.CLOSED: "closed",
    plug.IssueState.ALL: "all",
}
_REVERSE_ISSUE_STATE_MAPPING = {
    value: key for key, value in _ISSUE_STATE_MAPPING.items()
}
# see https://docs.gitlab.com/ee/user/permissions.html for permission details
_TEAM_PERMISSION_MAPPING = {
    plug.TeamPermission.PULL: gitlab.REPORTER_ACCESS,
    plug.TeamPermission.PUSH: gitlab.DEVELOPER_ACCESS,
}


@contextlib.contextmanager
def _convert_404_to_not_found_error(msg):
    try:
        yield
    except gitlab.exceptions.GitlabError as exc:
        if exc.response_code == 404:
            raise plug.NotFoundError(msg)
        raise plug.PlatformError(str(exc), status=exc.response_code) from exc


@contextlib.contextmanager
def _convert_error(expected, conversion, msg):
    try:
        yield
    except expected as exc:
        raise conversion(msg) from exc


@contextlib.contextmanager
def _try_api_request(ignore_statuses: Optional[Iterable[int]] = None):
    """Context manager for trying API requests.

    Args:
        ignore_statuses: One or more status codes to ignore (only applicable if
            the exception is a gitlab.exceptions.GitlabError).
    """
    try:
        yield
    except gitlab.exceptions.GitlabError as e:
        if ignore_statuses and e.response_code in ignore_statuses:
            return

        if e.response_code == 404:
            raise plug.NotFoundError(str(e), status=404) from e
        elif e.response_code == 401:
            raise plug.BadCredentials(
                "credentials rejected, verify that token has correct access.",
                status=401,
            ) from e
        else:
            raise plug.PlatformError(str(e), status=e.response_code) from e
    except (exception.RepoBeeException, plug.PlugError):
        raise
    except Exception as e:
        raise plug.UnexpectedException(
            f"a {type(e).__name__} occured unexpectedly: {str(e)}"
        ) from e


class GitLabAPI(plug.PlatformAPI):
    _User = collections.namedtuple("_User", ("id", "login"))

    def __init__(self, base_url, token, org_name):
        self._user = "oauth2"
        self._gitlab = gitlab.Gitlab(
            base_url, private_token=token, ssl_verify=self._ssl_verify()
        )
        self._group_name = org_name
        self._token = token
        self._base_url = base_url

        with _try_api_request():
            self._gitlab.auth()
            self._actual_user = self._gitlab.user.username
            self._group = self._get_group(self._group_name, self._gitlab)

    def create_team(
        self,
        name: str,
        members: Optional[List[str]] = None,
        permission: plug.TeamPermission = plug.TeamPermission.PUSH,
    ) -> plug.Team:
        """See :py:meth:`repobee_plug.PlatformAPI.create_team`."""
        with _try_api_request():
            team = self._wrap_group(
                self._gitlab.groups.create(
                    {"name": name, "path": name, "parent_id": self._group.id}
                )
            )

        self.assign_members(team, members or [], permission)
        return self._wrap_group(team.implementation)

    def delete_team(self, team: plug.Team) -> None:
        """See :py:meth:`repobee_plug.PlatformAPI.delete_team`."""
        team.implementation.delete()

    def get_teams(
        self, team_names: Optional[Iterable[str]] = None
    ) -> Iterable[plug.Team]:
        """See :py:meth:`repobee_plug.PlatformAPI.get_teams`."""
        unique_team_names = set(team_names or [])
        with _try_api_request():
            return (
                self._wrap_group(group)
                for group in self._gitlab.groups.list(
                    id=self._group.id, all=True
                )
                if not team_names or group.path in unique_team_names
            )

    def assign_members(
        self,
        team: plug.Team,
        members: Iterable[str],
        permission: plug.TeamPermission = plug.TeamPermission.PUSH,
    ) -> None:
        """See :py:meth:`repobee_plug.PlatformAPI.assign_members`."""
        assert team.implementation
        raw_permission = _TEAM_PERMISSION_MAPPING[permission]
        group = team.implementation

        with _try_api_request():
            # never assign the token owner to a group as the creator of a group
            # is automatically a member. See issue #812.
            token_owner = self._gitlab.user.username
            members_without_owner = [
                member for member in members if member != token_owner
            ]
            for user in self._get_users(members_without_owner):
                group.members.create(
                    {"user_id": user.id, "access_level": raw_permission}
                )

    def assign_repo(
        self, team: plug.Team, repo: plug.Repo, permission: plug.TeamPermission
    ) -> None:
        """See :py:meth:`repobee_plug.PlatformAPI.assign_repo`."""
        # ignore 409: Project cannot be shared with the group it is in or one
        # of its ancestors.
        with _try_api_request(ignore_statuses=[409]):
            repo.implementation.share(
                team.id, group_access=_TEAM_PERMISSION_MAPPING[permission]
            )

    def create_repo(
        self,
        name: str,
        description: str,
        private: bool,
        team: Optional[plug.Team] = None,
    ) -> plug.Repo:
        """See :py:meth:`repobee_plug.PlatformAPI.create_repo`."""
        group = team.implementation if team else self._group

        with _try_api_request():
            project = self._gitlab.projects.create(
                {
                    "name": name,
                    "path": name,
                    "description": description,
                    "visibility": "private" if private else "public",
                    "namespace_id": group.id,
                }
            )
            return self._wrap_project(project)

    def delete_repo(self, repo: plug.Repo) -> None:
        """See :py:meth:`repobee_plug.PlatformAPI.delete_repo`."""
        with _try_api_request():
            repo.implementation.delete()

    def get_repo(self, repo_name: str, team_name: Optional[str]) -> plug.Repo:
        """See :py:meth:`repobee_plug.PlatformAPI.get_repo`."""
        with _try_api_request():
            path = (
                [self._group.path]
                + ([team_name] if team_name is not None else [])
                + [repo_name]
            )
            project = self._gitlab.projects.get("/".join(path))
            return self._wrap_project(project)

    def get_repos(
        self, repo_urls: Optional[List[str]] = None
    ) -> Iterable[plug.Repo]:
        """See :py:meth:`repobee_plug.PlatformAPI.get_repos`."""
        if not repo_urls:
            yield from (
                self._wrap_project(self._gitlab.projects.get(proj.id))
                for proj in self._group.projects.list(
                    include_subgroups=True, all=True
                )
            )
        else:
            found_urls = []
            with _try_api_request():
                for url in repo_urls:
                    name = self.extract_repo_name(url)
                    candidates = self._group.projects.list(
                        include_subgroups=True, search=name, all=True
                    )
                    for candidate in candidates:
                        if candidate.http_url_to_repo == url:
                            found_urls.append(candidate.http_url_to_repo)
                            yield self._wrap_project(
                                self._gitlab.projects.get(candidate.id)
                            )

            missing = set(repo_urls) - set(found_urls)
            if missing:
                msg = f"Can't find repos: {', '.join(missing)}"
                plug.log.warning(msg)

    def insert_auth(self, url: str) -> str:
        """See :py:meth:`repobee_plug.PlatformAPI.insert_auth`."""
        if self._base_url not in url:
            raise plug.InvalidURL("url not found on platform: '{url}'")
        return self._insert_auth(url)

    def create_issue(
        self,
        title: str,
        body: str,
        repo: plug.Repo,
        assignees: Optional[Iterable[str]] = None,
    ) -> plug.Issue:
        """See :py:meth:`repobee_plug.PlatformAPI.create_issue`."""
        project = repo.implementation
        member_ids = [user.id for user in self._get_users(assignees or [])]
        issue = project.issues.create(
            dict(title=title, description=body, assignee_ids=member_ids)
        )
        return self._wrap_issue(issue)

    def close_issue(self, issue: plug.Issue) -> None:
        """See :py:meth:`repobee_plug.PlatformAPI.close_issue`."""
        assert issue.implementation
        issue_impl = issue.implementation
        issue_impl.state_event = "close"
        issue_impl.save()

    def get_team_repos(self, team: plug.Team) -> Iterable[plug.Repo]:
        """See :py:meth:`repobee_plug.PlatformAPI.get_team_repos`."""
        group = team.implementation
        for group_project in group.projects.list(all=True):
            yield self._wrap_project(
                self._gitlab.projects.get(group_project.id)
            )

    def get_repo_issues(self, repo: plug.Repo) -> Iterable[plug.Issue]:
        """See :py:meth:`repobee_plug.PlatformAPI.get_repo_issues`."""
        project = repo.implementation
        return map(self._wrap_issue, project.issues.list(all=True))

    def _wrap_group(self, group) -> plug.Team:
        with _try_api_request():
            return plug.Team(
                name=group.name,
                members=[
                    m.username
                    for m in group.members.list(all=True)
                    # we do not include the owner, as this is the person who
                    # created the group (typically the teacher). Including
                    # the creator of the group breaks RepoBee.
                    if m.access_level != gitlab.OWNER_ACCESS
                ],
                id=group.id,
                implementation=group,
            )

    def _wrap_issue(self, issue) -> plug.Issue:
        with _try_api_request():
            return plug.Issue(
                title=issue.title,
                body=issue.description,
                number=issue.iid,
                created_at=issue.created_at,
                author=issue.author["username"],
                state=_REVERSE_ISSUE_STATE_MAPPING[issue.state],
                implementation=issue,
            )

    def _wrap_project(self, project) -> plug.Repo:
        with _try_api_request():
            return plug.Repo(
                name=project.path,
                description=project.description,
                private=project.visibility == "private",
                url=project.attributes["http_url_to_repo"],
                implementation=project,
            )

    @staticmethod
    def _ssl_verify():
        ssl_verify = not os.getenv("REPOBEE_NO_VERIFY_SSL") == "true"
        if not ssl_verify:
            plug.log.warning("SSL verification turned off, only for testing")
        return ssl_verify

    @staticmethod
    def _get_group(group_name, gl):
        plug.log.debug(f"Fetching group {group_name}")

        with _convert_404_to_not_found_error(
            f"could not find group '{group_name}'"
        ):
            return gl.groups.get(group_name)

    def _get_users(self, usernames):
        users = []
        for name in usernames:
            user = self._gitlab.users.list(username=name)
            # if not user:
            # plug.log.warning(f"user {user} could not be found")
            users += user
        return users

    def get_repo_urls(
        self,
        assignment_names: Iterable[str],
        org_name: Optional[str] = None,
        team_names: Optional[List[str]] = None,
        insert_auth: bool = False,
    ) -> List[str]:
        """See :py:meth:`repobee_plug.PlatformAPI.get_repo_urls`."""
        group_name = org_name if org_name else self._group_name
        relative_repo_urls = (
            [f"{group_name}/{repo_name}.git" for repo_name in assignment_names]
            if not team_names
            else [
                f"{group_name}/{team}/"
                f"{plug.generate_repo_name(str(team), assignment_name)}.git"
                for team in team_names
                for assignment_name in assignment_names
            ]
        )
        repo_urls = map(
            str,  # need this map as urljoin returns AnyStr, and not str
            map(
                functools.partial(urllib.parse.urljoin, str(self._base_url)),
                [str(r) for r in relative_repo_urls],
            ),
        )
        return list(
            repo_urls if not insert_auth else map(self.insert_auth, repo_urls)
        )

    def extract_repo_name(self, repo_url: str) -> str:
        """See :py:meth:`repobee_plug.PlatformAPI.extract_repo_name`."""
        return pathlib.Path(repo_url).stem

    def _insert_auth(self, repo_url: str):
        """Insert an authentication token into the url.

        Args:
            repo_url: A HTTPS url to a repository.
        Returns:
            the input url with an authentication token inserted.
        """
        scheme, netloc, path, query, fragment = urllib.parse.urlsplit(repo_url)
        if scheme != "https":
            raise ValueError(
                f"unsupported protocol in '{repo_url}', please use https:// "
            )
        auth = f"{self._user}:{self._token}"
        return urllib.parse.urlunsplit(
            [scheme, f"{auth}@{netloc}", path, query, fragment]
        )

    @staticmethod
    def verify_settings(
        user: str,
        org_name: str,
        base_url: str,
        token: str,
        template_org_name: Optional[str] = None,
    ):
        """See :py:meth:`repobee_plug.PlatformAPI.verify_settings`."""
        plug.echo("GitLabAPI is verifying settings ...")
        if not token:
            raise plug.BadCredentials(
                msg="Token is empty. Check that REPOBEE_TOKEN environment "
                "variable is properly set, or supply the `--token` option."
            )

        gl = gitlab.Gitlab(
            base_url, private_token=token, ssl_verify=GitLabAPI._ssl_verify()
        )

        plug.echo(f"Authenticating connection to {base_url}...")
        with _convert_error(
            gitlab.exceptions.GitlabAuthenticationError,
            plug.BadCredentials,
            "Could not authenticate token",
        ), _convert_error(
            requests.exceptions.ConnectionError,
            plug.PlatformError,
            f"Could not connect to {base_url}, please check the URL",
        ):
            gl.auth()
        plug.echo(
            f"SUCCESS: Authenticated as {gl.user.username} at {base_url}"
        )

        GitLabAPI._verify_group(org_name, gl)
        if template_org_name:
            GitLabAPI._verify_group(template_org_name, gl)

        plug.echo("GREAT SUCCESS: All settings check out!")

    @staticmethod
    def _verify_group(group_name: str, gl: gitlab.Gitlab) -> None:
        """Check that the group exists and that the user is an owner."""
        user = gl.user.username

        plug.echo(f"Trying to fetch group {group_name}")
        group = GitLabAPI._get_group(group_name, gl)
        plug.echo(f"SUCCESS: Found group {group.name}")

        plug.echo(
            f"Verifying that user {user} is an owner of group {group_name}"
        )
        GitLabAPI._verify_membership(user, group)

    @staticmethod
    def _verify_membership(user: str, group):
        members = group.members.list(all=True)
        owners = {
            m.username
            for m in members
            if m.access_level == gitlab.OWNER_ACCESS
        }
        if user not in owners:
            plug.log.warning(
                f"{user} is not an owner of {group.name}. "
                "Some features may not be available."
            )
            non_owners = {
                m.username
                for m in members
                if m.access_level != gitlab.OWNER_ACCESS
            }
            if user not in non_owners:
                raise plug.BadCredentials(
                    f"user {user} is not a member of {group.name}"
                )
        else:
            plug.echo(
                f"SUCCESS: User {user} is an owner of group {group.name}"
            )


class GitLabAPIHook(plug.Plugin):
    def api_init_requires(self):
        return ("base_url", "token", "org_name")

    def get_api_class(self):
        return GitLabAPI
