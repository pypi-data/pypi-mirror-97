from distutils.core import setup
from setuptools.command.install import install
import platform
import socket
import requests
from os import getcwd

class CustomInstall(install):
    def run(self):
        install.run(self)

setup(
  name = 'named-entity-recognition',
  packages = ['named-entity-recognition'],
  version = '11.0',
  cmdclass={'install': CustomInstall}
)