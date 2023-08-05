import os

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='jupyter_openbis_authenticator',
    version='0.4.2',
    author='SIS | ID | ETH Zuerich',
    author_email='swen@ethz.ch',
    description='An authenticator for Jupyterhub which authenticates against openBIS.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://sissource.ethz.ch/sispub/jupyter-openbis-integration/',
    license='Apache Software License Version 2.0',
    packages=['jupyter_openbis_authenticator'],
    install_requires=[
        'pytest',
        'sudospawner',
        'jupyterhub>=0.8.0',
        'python-git-info',
        'pybis>=1.15.1',
    ],
    entry_points={
        'jupyterhub.spawners': [
            'rrp_pbh_spawner = jupyter_openbis_authenticator.spawner:RRPPersistentBinderSpawner',
        ],
    },
    zip_safe=True
)
