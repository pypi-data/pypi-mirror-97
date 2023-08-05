import json
import os
import re
from collections import namedtuple

from tools import update_version_files

BASE_VER = '1.0.0'
PY_SEARCH_PATTERN = r'''^__version__\s+=\s+'([0-9\.\-]+\w*?)'$'''

args_cls = namedtuple('args', 'build_id, build_user, date_string, build_version, git_revision, use_full_commit_id, fps')


def get_py_paths(main_path):

    return [
        f'{main_path}/legion/cli/legion/cli/',
        f'{main_path}/legion/sdk/legion/sdk/',
        f'{main_path}/legion/jupyterlab-plugin/legion/jupyterlab/',
    ]


def get_npm_paths(main_path):

    return [
        f'{main_path}/legion/jupyterlab-plugin/'
    ]


def get_info_paths(main_path):

    return [
        f'{main_path}/'
    ]


def get_fps(main_path):

    fps = []

    for py_fp in get_py_paths(main_path):
        fp = f'{py_fp}/version.py'
        fps.append(fp)

    for npm_fp in get_npm_paths(main_path):
        fp = f'{npm_fp}/package.json'
        fps.append(fp)

    for npm_fp in get_info_paths(main_path):
        fp = f'{npm_fp}/version.info'
        fps.append(fp)

    return fps


def create_structure(main_path):

    py_paths = get_py_paths(main_path)
    npm_paths = get_npm_paths(main_path)
    info_paths = get_info_paths(main_path)

    for path in py_paths:
        os.makedirs(path, exist_ok=True)
        with open(f'{path}/version.py', 'w') as f:
            f.write(f"__version__ = '{BASE_VER}'\n")

    for path in npm_paths:
        os.makedirs(path, exist_ok=True)
        package = {'version': f'{BASE_VER}'}
        with open(f'{path}/package.json', 'w') as f:
            json.dump(package, f)

    for path in info_paths:
        os.makedirs(path, exist_ok=True)
        with open(f'{path}/version.info', 'w') as f:
            f.write(f"__version__ = '{BASE_VER}'\n")


def assert_expected_version(version: str, expected_version: str, main_path: str):
    """
    Check that version was properly calculated and version files were updated
    :param version: version that is calculated by script
    :param expected_version: version that is expected
    :param main_path: project directory where version files should be updated
    :return:
    """

    assert version == expected_version

    for dir_ in get_npm_paths(main_path):
        fp = f'{dir_}/package.json'
        with open(fp) as f:
            package = json.load(f)
            assert package['version'] == expected_version

    for dir_ in get_py_paths(main_path):
        fp = f'{dir_}/version.py'
        with open(fp) as f:
            content = f.read()
            base_version = re.search(PY_SEARCH_PATTERN, content, flags=re.MULTILINE)
            ver = base_version.group(1)
            assert ver == expected_version

    for dir_ in get_info_paths(main_path):
        fp = f'{dir_}/version.info'
        with open(fp) as f:
            content = f.read()
            base_version = re.search(PY_SEARCH_PATTERN, content, flags=re.MULTILINE)
            ver = base_version.group(1)
            assert ver == expected_version


def test_update_version_id_stable(tmp_path):

    # Given

    create_structure(tmp_path)

    # When
    os.chdir(tmp_path)
    fps = get_fps(tmp_path)
    args = args_cls(17, 'null', '20190513113315', '2.0.0-rc1', '0000', False, fps)
    expected_version = args.build_version

    version = update_version_files.main(args)

    # Then
    assert_expected_version(version, expected_version, tmp_path)


def test_update_version_id_not_stable(tmp_path):

    # Given

    create_structure(tmp_path)

    # When
    os.chdir(tmp_path)
    fps = get_fps(tmp_path)
    args = args_cls(17, 'null', '20190513113315', None, '0000', False, fps)
    expected_version = f'{BASE_VER}-dev{args.build_id}'

    version = update_version_files.main(args)

    # Then
    assert_expected_version(version, expected_version, tmp_path)

