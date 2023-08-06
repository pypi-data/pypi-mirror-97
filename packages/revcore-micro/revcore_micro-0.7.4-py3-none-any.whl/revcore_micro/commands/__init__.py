import os
import pkgutil
from importlib import import_module


def main():
    return


def find_commands():
    command_dir = os.path.join('revcore', 'commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
                if not is_pkg and not name.startswith('_')]


if __name__ == '__main__':
    return
