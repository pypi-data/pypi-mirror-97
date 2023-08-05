# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List
import os

# Pip
from kdependencies import InstalledPackage
from kcu import strings, strio

# Local
from .core_texts import setup
from .utils import multi_replace

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def updated_setup(
    old_setup: str,
    dependencies: Optional[List[str]] = None,
    version_bump_type: int = 0
) -> str:
    if dependencies:
        try:
            old_dependencies_str = 'install_requires{}'.format(old_setup.split('install_requires')[-1].split(']')[0])

            old_setup = old_setup.replace(
                old_dependencies_str,
                'install_requires=[{}'.format(__dependencies_str(dependencies))
            )
        except Exception as e:
            print(e)

    try:
        old_version_str = __extract_current_version_number(old_setup)

        if old_version_str:
            old_setup = old_setup.replace(old_version_str, __bumped_version_number(old_version_str))
    except Exception as e:
        print(e)

    return old_setup

def current_version_number(setup_file_path: str) -> Optional[str]:
    if not os.path.exists(setup_file_path):
        return None

    try:
        return __extract_current_version_number(strio.load(setup_file_path))
    except:
        return None

def new_setup(
    package_name: str,
    min_python_version: Optional[float] = None,
    max_python_version: Optional[float] = None,
    package_version: Optional[str] = None,
    author: Optional[str] = None,
    git_url: Optional[str] = None,
    dependencies: Optional[List[InstalledPackage]] = None,
    short_description: Optional[str] = None,
    license_str: Optional[str] = None
) -> str:
    min_python_version = min_python_version or 3.4
    max_python_version = max_python_version or 3.9

    return multi_replace(setup, {
        '[PACKAGE_NAME]': package_name,
        '[AUTHOR]': author or '',
        '[GIT_URL]': git_url or '',
        '[PACKAGE_VERSION]': package_version or '0.0.0',
        '[DEPENDENCIES]': __dependencies_str(dependencies) if dependencies else '',
        '[SHORT_DESCRIPTION]': short_description or package_name,
        '[PYTHON_CLASSIFIERS]': __get_python_classifiers(min_python_version, max_python_version, license_str),
        '[MIN_PYTHON_VERSION]': min_python_version,
    })


# ----------------------------------------------------------- Private methods ------------------------------------------------------------ #

def __extract_current_version_number(setup_file_str: str) -> Optional[str]:
    try:
        return setup_file_str.split('version=')[-1].split('version =')[-1].split(',')[0].replace('"', '').replace("'", '')
    except:
        return None

def __get_python_classifiers(
    min_python_version: float,
    max_python_version: float,
    license_str: Optional[str] = 'License :: OSI Approved :: MIT License'
) -> str:
    current_version = min_python_version - 0.1
    classifiers = []

    while current_version < max_python_version:
        current_version += 0.1
        classifiers.append('Programming Language :: Python :: {}'.format(float(int(current_version*10))/10))

    if license_str:
        classifiers.append(license_str)

    return ',\n{}'.format(8*' ').join(['\'{}\''.format(c) for c in classifiers])

def __dependencies_str(dependencies: List[InstalledPackage]) -> str:
    return '\n{}{}\n{}'.format(
        8*' ',
        ',\n{}'.format(8*' ').join(
            ['\'{}{}\''.format(d.get_install_name(), '>={}'.format(d.version) if not d.private else '') for d in dependencies]
        ),
        4*' '
    ) if dependencies else ''

def __bumped_version_number(version_number: str, bump_type: int = 0) -> str:
    comps = version_number.split('.')
    bump_index = len(comps)-1-bump_type
    comps[bump_index] = str(int(comps[bump_index]) + 1)

    return '.'.join(comps)


# ---------------------------------------------------------------------------------------------------------------------------------------- #