Jupyter-OpenBIS-Authenticator
=============================

Compatibility
-------------

This Authenticator works only with Jupyterhub > 0.8.0. This module was
tested with version 0.8.1

The authenticator uses the ``spawner.environment`` feature to modify the
users environment variables during session creation. This feature was
introduced in Jupyterhub by version 0.8.0.

Installation
------------

::

    pip install jupyter_openbis_authenticator

Jupyterhub Configuration
------------------------

Edit your ``jupyterhub_config.py`` file and add the following class for
authenticating against openBIS:

::

    c.JupyterHub.authenticator_class = 'jupyter_openbis_authenticator.auth.OpenbisAuthenticator'

    # enable persisting auth_state:
    c.Authenticator.enable_auth_state = True
