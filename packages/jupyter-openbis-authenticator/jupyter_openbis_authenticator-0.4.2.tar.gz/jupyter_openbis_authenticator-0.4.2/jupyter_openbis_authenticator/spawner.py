#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import pwd
import re
import time
#from persistent_bhub_config import PersistentBinderSpawner
from jupyterhub.spawner import LocalProcessSpawner
from traitlets import Unicode, Bool
import git
from git import Repo

def list_repos():
    return [{"path": repo} for repo in all_volumes()]

def all_volumes():
    projects_dir = "/var/rrp-projects"
    return (o for o in os.listdir(projects_dir)
                if os.path.isdir(os.path.join(projects_dir, o)))

def volumes(kube_spawner):
    """Builds a list of tuples (`display name`, `folder name`, `locked`)
    """
    pods = kube_spawner.pod_reflector.pods.values()
    consumed_vols = set(filter(None, (pod.metadata.annotations.get("rrp-vol")
                                      for pod in pods)))
    return ((vol, vol, vol in consumed_vols) for vol in all_volumes())


def get_lockfile(path):
    is_locked = False
    locked_by = ""
    locked_when = ""

    lockfile_path = os.path.join(path, '.lockfile')
    if os.path.isfile(lockfile_path):
        is_locked = True
        with open(lockfile_path, 'r') as fh:
            locked_by = fh.readline().strip()
        locked_when = time.ctime(os.path.getmtime(lockfile_path))

    return (is_locked, locked_by, locked_when)

def get_git_commit(path):
    try:
        repo = Repo(path)
    except git.NoSuchPathError:
        repo = None
        pass
    except git.InvalidGitRepositoryError:
        repo = None
        pass
        
    commit = repo.commit()
    git_commit = {
        "commit_hash": commit.hexsha,
        "commit_date": time.ctime(commit.committed_date),
        "commit_name": commit.committer.name,
        "commit_message": commit.message,
        "active_branch": repo.active_branch.name,
    }
    return git_commit


def vol_name(folder_name: str):
    """Volume names only may container lower case alphanumeric chars.
    To prevent collisions, we build a hex representation of the original
    name"""
    return "vol-" + folder_name.encode().hex().lower()

def get_project_dirs(project_dir):
    def _get_project_dirs():
        project_dirs = [] 
        for f in os.scandir(project_dir):
            if f.is_dir():
                (is_locked, locked_by, locked_when) = get_lockfile(f.path) 
                print('-------------------------------')
                print(f.path)
                git_commit = get_git_commit(f.path) or {}
                project_dirs.append(
                    {
                        "repo_url": f.path,
                        "display_name": f.name,
                        "image": "",
                        "ref": git_commit.get('commit_hash'),
                        "git_commit": git_commit,
                        "is_locked": is_locked,
                        "locked_by": locked_by,
                        "locked_when": locked_when,
                    }
                )
        return project_dirs
    return _get_project_dirs

class RRPPersistentBinderSpawner(LocalProcessSpawner):
    # the main project dir can be defined in the jupyterhub_config.py
    # c.RRPPersistentBinderSpawner.projects_dir = '/path/to/projects'

    projects_dir = Unicode(
        config=True,
        help='Directory of projects'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user.project_dirs = get_project_dirs(self.projects_dir)
        return
        
    def get_state(self):
        _state = self.orm_spawner.state
        state = super().get_state()
        return state
