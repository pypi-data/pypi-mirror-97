#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Created by Swen Vermeul on Feb 26th 2018
Copyright (c) 2018 ETH Zuerich All rights reserved.
"""

import os
import re

from jupyterhub.auth import Authenticator
from sudospawner import SudoSpawner
import pamela
from tornado import gen
from traitlets import Unicode, Bool

from pybis.pybis import Openbis



class OpenbisAuthenticator(Authenticator):
    server_url = Unicode(
        config=True,
        help='URL of openBIS server to contact'
    )

    kerberos_domain = Unicode(
        config=True,
        help='The domain to authenticate against to obtain a kerberso ticket'
    )

    default_username = Unicode(
        config=True,
        help='the username which should be used within jupyterhub/binderhub instead of the real username, usually jovyan'
    )

    verify_certificates = Bool(
        config=True,
        default_value=True,
        help='Should certificates be verified? Normally True, but maybe False for debugging.'
    )

    valid_username_regex = Unicode(
        r'^[a-zA-Z][.a-zA-Z0-9_-]*$',
        config=True,
        help="""Regex to use to validate usernames before sending to openBIS."""
    )

    @gen.coroutine
    def authenticate(self, handler, data):
        """Checks username and password against the given openBIS instance.
        If authentication is successful, it not only returns the username but
        a data structure:
        {
            "name": username,
            "auth_state": {
                "token": openBIS.token,
                "url"  : openBIS.url
            }
        }
        """
        username = data['username']
        password = data['password']

        # Protect against invalid usernames as well as LDAP injection attacks
        if not re.match(self.valid_username_regex, username):
            self.log.warn('Invalid username')
            return None

        # No empty passwords!
        if password is None or password.strip() == '':
            self.log.warn('Empty password')
            return None


        openbis = Openbis(self.server_url, verify_certificates=self.verify_certificates)
        try:
            # authenticate against openBIS and store the token (if possible)
            openbis.login(username, password)

            # instead of just returning the username, we return a dict
            # containing the auth_state as well
            kerberos_username = username
            if getattr(self, 'kerberos_domain', None):
               kerberos_username = username + '@' + self.kerberos_domain

            if getattr(self, 'default_username', None):
                kerberos_username = self.default_username
            return {
                "name": kerberos_username,
                "auth_state": {
                    "token": openbis.token,
                    "url": openbis.url,
                    "kerberos_username": kerberos_username,
                    "username": username,
                    "kerberos_password": password,

                }
            }
        except ValueError as err:
            self.log.warn(str(err))
            return None


    @gen.coroutine
    def pre_spawn_start(self, user, spawner):
        """Pass openbis token to spawner via environment variable"""
        auth_state = yield user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return

        # Write the openBIS token to the users' environment variables
        spawner.environment['OPENBIS_URL']       = auth_state['url']
        spawner.environment['OPENBIS_TOKEN']     = auth_state['token']
        spawner.environment['KERBEROS_USERNAME'] = auth_state['kerberos_username']
        spawner.environment['KERBEROS_PASSWORD'] = auth_state['kerberos_password']
        spawner.environment['USERNAME']          = auth_state['username']


    def get_new_uid_for_home(self, os_home):
        id_sequence = 999; # Linux uids start at 1000
        for file in next(os.walk(os_home))[1]:
            home_info = os.stat(os_home + file)
            if home_info.st_uid > id_sequence:
                id_sequence = home_info.st_uid
            if home_info.st_gid > id_sequence:
                id_sequence = home_info.st_gid
        if id_sequence is None:
            return None
        else:
            return { "uid" : id_sequence + 1 }


class KerberosSudoSpawner(SudoSpawner):
    """Specialized SudoSpawner which defines KERBEROS_USERNAME and KERBEROS_PASSWORD
    for the global environment variables. These variables are later used by the
    sudospawner-singleuser script to log in to Active Director to obtain a valid Kerberos ticket
    """

    def get_env(self):
        env = super().get_env()

        spawner_env = getattr(self.user.spawner, 'environment', None)
        if not spawner_env:
            # auth_state was probably not enabled
            return env
        env['KERBEROS_USERNAME'] = spawner_env['KERBEROS_USERNAME']
        env['KERBEROS_PASSWORD'] = spawner_env['KERBEROS_PASSWORD']
        return env

    @gen.coroutine
    def do(self, action, **kwargs):
        """Before we spawn the notebook server, we need to obtain a Kerberos ticket
        otherwise we'll get a PID error as we cannot access the (SMB mounted) user home
        without a valid Kerberos ticket.
        """

        if os.getenv('KERBEROS_USERNAME') and os.getenv('KERBEROS_PASSWORD'):
            pamela.authenticate(
                os.getenv('KERBEROS_USERNAME'),
                os.getenv('KERBEROS_PASSWORD'),
                resetcred=0x0002
            )

        return super().do(action, **kwargs)
