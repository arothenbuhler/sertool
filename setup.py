from setuptools import find_packages, setup
from setuptools.extern.packaging.version import Version, InvalidVersion
from setuptools import setup

import os
import subprocess
import sys

# Build version file
FILE_NAME_BUILD_VERSION = 'sertool/package_version'

class VersionError(Exception):
    pass

def get_version():
    tags = subprocess.check_output(['git', 'tag', '--points-at']).decode()
    tags = tags.split('\n')
    env_tag = os.environ.get('CI_BUILD_TAG', None)
    if env_tag in tags:
        return env_tag
    
    for opt in ('--exact-match', '--tags', '--all'):
        status, string = subprocess.getstatusoutput('git describe --dirty=-dirty ' + opt)
        print(string)
        if status == 0 and string:
            return string
    raise VersionError('Cannot describe current git workspace')

version = get_version()

try:
    normalized_ver = Version(version)
    if str(normalized_ver) != version:
        print(f'Cannot release as version {version} because setuptools would normalize it to somehting else.', file=sys.stderr)
        print(f'Try re-tagging with something like {normalized_ver}.', file=sys.stderr)
        sys.exit(1)
except InvalidVersion:
    pass

with open(FILE_NAME_BUILD_VERSION, 'w') as f:
    print(version, file=f)

setup(
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    name='sertool',
    version=version,
    author='Adrian Rothenbuhler',
    author_email='adrian@redhill-embedded.com',
    description='Serial Port Helper Tool',
    keywords='Serial port',
    url='https://dev.azure.com/redhill-embedded/VirtusSolis/_git/can_controller',
    packages=find_packages(),
    package_data={
        "sertool": [
            "package_version"
        ]
    },
    python_requires=">=3.8",
    install_requires=["pyserial"],
    entry_points={
        "console_scripts": [
            "sertool=sertool.__main__:main",
        ]
    },
)