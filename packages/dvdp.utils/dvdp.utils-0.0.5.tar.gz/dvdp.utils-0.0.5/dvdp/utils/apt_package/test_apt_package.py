from dvdp.utils.apt_package.apt_package import *


INSTALL_LOG_FILE = '../install_log_cmake.txt'
DESTINATION = '/tmp/test'
NAME = 'cmake'
VERSION = '3.15.7'


def test_parse_log_for_paths():
    paths = parse_log_for_paths(Path(__file__).parent / INSTALL_LOG_FILE)
    assert len(paths) > 0


def test_create_package_tree():
    paths = parse_log_for_paths(Path(__file__).parent / INSTALL_LOG_FILE)
    create_package_tree(DESTINATION, NAME, paths)


def test_create_control_file():
    paths = parse_log_for_paths(Path(__file__).parent / INSTALL_LOG_FILE)
    size = create_package_tree(DESTINATION, NAME, paths)
    create_control_file(DESTINATION, NAME, VERSION, 'EAE', size)


def test_create_package():
    paths = parse_log_for_paths(Path(__file__).parent / INSTALL_LOG_FILE)
    size = create_package_tree(DESTINATION, NAME, paths)
    create_control_file(DESTINATION, NAME, VERSION, 'EAE', size)
    create_package(DESTINATION, NAME, VERSION)