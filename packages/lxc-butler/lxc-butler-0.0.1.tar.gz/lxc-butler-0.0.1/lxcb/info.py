from os import readlink
from os.path import expanduser, isfile, relpath
from getpass import getuser

# package info
__version__ = '0.0.1'
__author__ = 'Kobus van Schoor'
__author_email__ = 'v.schoor.kobus@gmail.com'
__url__ = 'https://github.com/kobus-v-schoor/lxc-butler'
__license__ = 'MIT License'

# user info
username = getuser()
home = expanduser('~')
timezone = relpath(readlink('/etc/localtime'), '/usr/share/zoneinfo')

# try and figure out the distro name and release
# TODO add methods for other distros
distro = None
release = None
arch = 'amd64'

if isfile('/etc/os-release'):
    with open('/etc/os-release', 'r') as f:
        for line in f.readlines():
            key, value = line.strip().split('=', maxsplit=1)
            if key == 'ID':
                distro = value.strip('"')
            elif key == 'VERSION_CODENAME':
                release = value.strip('"')
