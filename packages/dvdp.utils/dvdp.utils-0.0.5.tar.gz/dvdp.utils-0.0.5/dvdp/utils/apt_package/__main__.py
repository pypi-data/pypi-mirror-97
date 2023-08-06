from argparse import ArgumentParser
from pathlib import Path

from dvdp.utils.apt_package.apt_package import *


def main():
    parser = ArgumentParser()
    parser.add_argument(
        'filelist',
        help='File containing list of files to install. Structure of files '
             'in this list is used for the filetree in the package.',
        type=Path,
    )
    parser.add_argument(
        'packagename',
        help='Name of the debian package to create. e.g. cmake',
        type=str,
    )
    parser.add_argument(
        'version',
        help='Package version number',
        type=str
    )

    args = parser.parse_args()
    filelist = args.filelist
    name = args.packagename.lower()
    version = args.version

    paths = parse_log_for_paths(filelist)
    size = create_package_tree(Path('.'), name, paths)
    create_control_file(Path('.'), name, version, 'EAE', size)
    create_package(Path('.'), name, version)


if __name__ == '__main__':
    main()
