from sys import platform


def is_linux() -> bool:
    if platform == 'linux' or platform == 'linux2':
        return True
    return False


def is_windows() -> bool:
    if platform == 'win32':
        return True
    return False