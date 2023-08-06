"""Create apt packages from a file list"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import List

from dvdp.utils import system


def parse_log_for_paths(log_file: str):
    if system.is_windows():
        raise Exception('Cannot parse log on a windows system.')
    paths = []
    with open(log_file, 'r') as file:
        for line in file:
            splitted = line.split('/', maxsplit=1)
            if len(splitted) == 2:
                path_candidate = Path('/' + splitted[1].replace(
                    '\n', ''
                ).replace(
                    '\r', ''
                ))
                if path_candidate.exists():
                    paths.append(path_candidate)
                else:
                    print(f'path {path_candidate} does not exist.')
    return paths


def create_package_tree(
        destination: Path,
        name: str,
        paths: List[Path]
) -> float:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    nr_files = 0
    size = 0
    for path in paths:
        dest_sub = destination / name / str(path)[1:]
        dest_sub.parent.mkdir(parents=True, exist_ok=True)
        if path.is_dir():
            print(f'Skipping dir {path}')
            continue
        print(f'Copying {path} to {dest_sub}')
        shutil.copy(path, dest_sub)
        size += os.stat(dest_sub).st_size
        nr_files += 1
    print(f'Copied {nr_files} files together {size} bytes.')
    return size / 1024


def create_control_file(
        destination: Path,
        name,
        version,
        maintainer,
        size,
        description='N/A',

):
    info = {
        'Package': name,
        'Version': version,
        'Section': 'custom',
        'Priority': 'optional',
        'Architecture': 'all',
        'Essential': 'no',
        'Installed-Size': round(size),
        'Maintainer': maintainer,
        'Description': description,
    }
    lines = [f'{key}: {val}\n' for key, val in info.items()]
    dir = Path(destination) / name / 'DEBIAN'
    dir.mkdir(parents=True, exist_ok=True)
    with open(dir / 'control', 'w') as file:
        file.writelines(lines)


def create_package(
    destination: Path,
    name,
    version,
):
    destination = Path(destination)
    source = destination / name
    cmd = ['dpkg-deb', '--build', str(source)]
    subprocess.run(cmd)
    package_source_loc = destination / (name + '.deb')
    package_dest_loc = destination / (name + '-' + version + '.deb')
    shutil.move(str(package_source_loc), str(package_dest_loc))
    print(f'Saved debain package to {str(package_dest_loc)}')
