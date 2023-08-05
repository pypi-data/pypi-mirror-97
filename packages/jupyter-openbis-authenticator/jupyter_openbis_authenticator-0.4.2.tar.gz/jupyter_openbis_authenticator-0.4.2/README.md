# Jupyter-OpenBIS-Authenticator

## Description

This authenticator module for JupyterHub connects to a given openBIS instance, using the pyBIS module. It exports the environment variables
* OPENBIS_URL
* OPENBIS_TOKEN

to the user environment. Later, in a notebook, a user is then able to use pyBIS without any url, username or credentials:

```
from pybis import Openbis
o = Openbis()
```

## Compatibility

This Authenticator works only with Jupyterhub > 0.8.0. This module was tested with version 0.8.1

The authenticator uses the `spawner.environment` feature to modify the users environment variables during session creation. This feature was introduced in Jupyterhub by version 0.8.0.

## Installation

```
pip install jupyter_openbis_authenticator
```

## Jupyterhub Configuration

Edit your `jupyterhub_config.py` file and add the following to register `jupyter_openbis_authenticator` as a JupyterHub authenticator class:

```
c.JupyterHub.authenticator_class = 'jupyter_openbis_authenticator.auth.OpenbisAuthenticator'
c.JupyterHub.spawner = 'jupyter_openbis_authenticator.auth.KerberosSudoSpawner'

if 'JUPYTERHUB_CRYPT_KEY' not in os.environ:
    warnings.warn(
        "Need JUPYTERHUB_CRYPT_KEY env for persistent auth_state.\n"
        "    export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)"
    )
    c.CryptKeeper.keys = [ os.urandom(32) ]

# enable persisting auth_state, i.e. enable JupyterHub to change the environment variables of the user.
c.Authenticator.enable_auth_state = True

# openBIS settings
c.OpenbisAuthenticator.server_url = 'https://my_openbis_instance.ch'
c.OpenbisAuthenticator.verify_certificates = True
```

## RRPPersistentBinderSpawner

This spawner reads directories from a specified project folder and presents them to the logged-in user. The user then can
launch virtual machines (using kubernetes) with the given running environment that **repo2docker** detects in the chosen
project folder.


Changes in `jupyterhub_config.py` to enable this spawner:

```python
c.JupyterHub.spawner_class = 'jupyter_openbis_authenticator.spawner.RRPPersistentBinderSpawner'
c.JupyterHub.spawner_class = 'rrp_pbh_spawner'
c.RRPPersistentBinderSpawner.projects_dir = '/path/to/my/projects'

```
