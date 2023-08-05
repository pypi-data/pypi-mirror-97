#!/usr/bin/env python
#
#   Copyright 2017 EPAM Systems
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
Tool for updating version files
"""
import argparse
import json
import re
import time
from typing import Sequence

# Constants
import semver
import yaml

PROFILE_VERSION_KEYS = [
    "odahu_infra_version",
    "odahuflow_version",
    "mlflow_toolchain_version",
    "jupyterlab_version",
    "packager_version",
    "examples_version",
    "odahu_airflow_plugin_version",
    "odahu_automation_version",
    "odahu_ui_version",
]

PY_SEARCH_PATTERN = r'''^__version__\s+=\s+'([0-9\.\-]+\w*?)'$'''
ODAHUFLOW_CONNECTIONS_KEY = "odahuflow_connections"
ODAHUFLOW_EXAMPLE_CONNECTION_ID = "odahu-flow-examples"


# Version files API


class VersionFile:
    """
    Interface that should be implemented by VersionFile Implementations
    """

    def __init__(self, fp):
        if not self.check_valid_file(fp):
            raise RuntimeError('Initialization of version file with not a valid format')
        self.fp = fp

    @staticmethod
    def check_valid_file(fp: str) -> bool:
        """
        Check whether this file is version file that is handled by this class or not
        :param fp: filepath to version file
        :return: True – means that this file can be handled by class, False – otherwise
        """
        raise NotImplementedError

    def set_version(self, version: str, **extra) -> None:
        """
        Version
        :param version: version
        :param extra: insert meta data to version file (optionally supported by different implementations)
        could be ignored
        :return: None
        """
        raise NotImplementedError

    def get_version(self):
        """
        Extract version from file
        :return:
        """
        raise NotImplementedError


class PythonVersionFile(VersionFile):
    """
    Handler for python `version.py`
    """

    @staticmethod
    def check_valid_file(fp: str) -> bool:
        return fp.endswith('version.py') or fp.endswith('version.info') or fp.endswith('__version__.py')

    def set_version(self, version, **extra):
        with open(self.fp, 'r') as stream:
            content = stream.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')

        # Set new __version__
        content = re.sub(
            PY_SEARCH_PATTERN, '__version__ = \'{}\''.format(version), content, flags=re.MULTILINE
        )

        with open(self.fp, 'w') as stream:
            stream.write(content)

    def get_version(self) -> str:
        with open(self.fp, 'r') as stream:
            try:
                content = stream.read()
                base_version = re.search(PY_SEARCH_PATTERN, content, flags=re.MULTILINE)
            except Exception:
                raise Exception('Can\'t get version from version string')

        return base_version.group(1)


class ProfileVersionFile(VersionFile):
    """
    Handler for internal profiles repo
    """

    @staticmethod
    def check_valid_file(fp: str) -> bool:
        return fp.endswith('common.yaml')

    def set_version(self, version, **extra):
        with open(self.fp, 'r') as f:
            data = yaml.load(f)

        for key in PROFILE_VERSION_KEYS:
            data[key] = version

        # Profiles have to contain an Odahu-flow connection that points to the examples repository.
        # For every release, we create a tag with version name for the examples repository.
        # In addition to the main versions, we also change the reference of the connection.
        odahuflow_connections = data[ODAHUFLOW_CONNECTIONS_KEY]
        for conn in odahuflow_connections:
            if conn['id'] == ODAHUFLOW_EXAMPLE_CONNECTION_ID:
                conn['spec']['reference'] = version

        with open(self.fp, 'w') as f:
            yaml.dump(data, f)

    def get_version(self) -> str:
        with open(self.fp, 'r') as f:
            data = yaml.load(f)

        return data[PROFILE_VERSION_KEYS[0]]


class NpmVersionFile(VersionFile):
    """
    Handler for npm `package.json`
    """

    @staticmethod
    def check_valid_file(fp: str) -> bool:
        return fp.endswith('package.json')

    def set_version(self, version: str, **extra):
        with open(self.fp) as f:
            package = json.load(f)

        package['version'] = version

        with open(self.fp, 'w') as f:
            json.dump(package, f, indent=2, sort_keys=True)

    def get_version(self):
        with open(self.fp) as f:
            package = json.load(f)

        return package['version']


ver_file_classes = [PythonVersionFile, NpmVersionFile, ProfileVersionFile]


def look_version_file_cls(fp: str):
    """
    Looks `VersionClass` that can handle file at filepath `fp`
    :param fp: filepath
    :return: `VersionClass` implementation if found – None otherwise
    """
    for cls in ver_file_classes:
        if cls.check_valid_file(fp):
            return cls
    else:
        raise ValueError(f'Unknown type of the file: {fp}')


def init_ver_file(fp: str) -> VersionFile:
    """
    Looks appropriate `VersionFile` class for file at given filepath (`fp`)
    Raise `RuntimeException` if class was not found
    :param fp:
    :return:
    """

    cls = look_version_file_cls(fp)
    if not cls:
        raise RuntimeError(f'VersionFile class for file {fp} is not found')

    return cls(fp)


def get_version_files(fps: Sequence[str]) -> Sequence[VersionFile]:
    """
    Initialize `VersionFile` instances by file paths
    :param fps: file paths to version files
    :return: Sequence[VersionFile]
    """

    ver_files = []

    for fp in fps:
        ver_files.append(init_ver_file(fp))

    return ver_files


# Script Arguments


class ScriptArgs:

    def __init__(
            self, build_id: int, build_user: str, date_string: str,
            git_revision: str, build_version: str, fps: Sequence[str]
    ):
        """
        :param build_id: Build serial number that is assigned by Jenkins for each job build
        :param build_user: User who launch job build
        :param date_string: Date when build was launched
        :param git_revision: Git revision
        :param build_version: Explicitly defined build version
        :param fps: version file paths
        """
        self.build_id = build_id
        self.build_user = build_user
        self.date_string = date_string
        self.git_revision = git_revision
        self.build_version = build_version
        self.fps = fps


def set_defaults(script_args: ScriptArgs, ver_file_for_meta: VersionFile):
    """
    Set defaults to script args
    :param script_args: Script args
    :param ver_file_for_meta: version file from which some meta data about current version will be extracted
    :return: None
    """
    if not script_args.build_version:
        local_version_string = f'b{int(round(time.time() * 1000))}'
        finalized_version = semver.finalize_version(ver_file_for_meta.get_version())

        script_args.build_version = '{}-{}'.format(finalized_version, local_version_string)


# MAIN

def main(args) -> str:
    version_files = get_version_files(args.fps)

    if not version_files:
        print('At least one version file must be specified')
        exit(3)

    script_args = ScriptArgs(
        args.build_id, args.build_user, args.date_string,
        args.git_revision, args.build_version, args.fps
    )
    set_defaults(script_args, ver_file_for_meta=version_files[0])

    try:
        for version_file in version_files:
            version_file.set_version(
                version=script_args.build_version,
                build_id=script_args.build_id,
                git_revision=script_args.git_revision,
                build_user=script_args.build_user
            )

    except KeyboardInterrupt:
        print('Interrupt')
        exit(2)

    return script_args.build_version


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Version file updater (adds time, build id, commit id to version)')
    parser.add_argument('build_id', type=int, help='Set build id')
    parser.add_argument('build_user', type=str, help='Set build user')
    parser.add_argument('date_string', type=str, help='Set date string')
    parser.add_argument('git_revision', type=str, help='Set git revision')
    parser.add_argument('fps', nargs='+', help='Paths to version files')
    parser.add_argument('--build-version', type=str, help='Explicitly specify new Legion build version')

    args = parser.parse_args()

    res = main(args)
    print(res)
