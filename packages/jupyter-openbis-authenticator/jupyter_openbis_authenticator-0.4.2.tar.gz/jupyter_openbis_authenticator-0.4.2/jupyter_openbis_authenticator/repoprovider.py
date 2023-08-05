from binderhub.repoproviders import RepoProvider
from datetime import timedelta, datetime, timezone
import json
import os
import time
import urllib.parse
import re
import subproces
from tornado import gen


def tokenize_spec(spec):
    """Tokenize spec into parts, error if spec invalid."""

    spec_parts = spec.split('/')
    if len(spec_parts) != 4:
        msg = 'Spec is not of the form "group/user/repo/git_commit_hash", provided: "{spec}".'.format(spec=spec)
        raise ValueError(msg)

    return spec_parts


class LocalRepoProvider(RepoProvider):
    """Provider for local git repos
    """

    def __init__(self):
        """Takes the spec and divides it up in smaller parts and puts it into self:
        <group>/<user>/<branch>
        """
        self.group, self.user, self.repo, self.git_commit_hash = tokenize_spec(self.spec)


    @gen.coroutine
    def get_resolved_ref(self):
        print("LocalRepoProvider.get_resolved_ref")
        self.git_commit_hash = spec


    async def get_resolved_spec(self):
        return self.get_repo_url()

    def get_repo_url(self):
        """
        While called repo URL, the return value of this function is passed
        as argument to repo2docker
        hence we return the spec as is.
        """
        return self.spec

    async def get_resolved_ref_url(self):
        """Return the URL of repository at this commit in history
        We do not provide a history, resolve to repo url
        """
        return self.get_repo_url()

    def get_build_slug(self):
        """
        return a unique id for each machine image that is built by repo2docker.
        a unique build slug
        The slug is used for caching?
        """
        return f'{self.project}-{self.git_commit_hash}'

