#! /usr/bin/env python3

import argparse
import collections
import configparser
import os
import re
import sys


_ROOT = os.path.abspath(os.path.dirname(__file__))
_CONF_DIR = os.path.join(_ROOT, 'configurations')
_FILES_DIR = os.path.join(_ROOT, 'files')

_HOME = os.path.expanduser('~')

_SECTION = re.compile('^(?P<section_type>\w+):(?P<name>[a-zA-Z0-9\.-]+)$')

_PLATFORMS = ['linux', 'darwin']


def _debug(*a, **kw):
    if not _debug.enabled:
        return
    kw.setdefault('file', sys.stderr)
    print('[debug]', *a, **kw)


def _print(*a, tabs=0, **kw):
    a = list(a)
    if tabs:
        a.insert(0, ' ' * (4 * tabs - 1))
    print(*a, **kw)


_debug.enabled = False

class ConfigurationFile:
    def __init__(self, soft_conf, name, conf):
        self._soft_conf, self.name, self._conf = soft_conf, name, conf
        # generate filename
        self.source_filename = self._conf.get('filename', self.name)
        self.target_filename = self.source_filename
        if not self._conf.getboolean('no_dot', False):
            self.target_filename = '.{}'.format(self.target_filename)

    @property
    def target_path(self):
        return os.path.join(self._soft_conf.base_path, self.target_filename)

    @property
    def source_path(self):
        return os.path.join(_FILES_DIR, self.source_filename)

    @property
    def status(self):
        source_path, target_path = self.source_path, self.target_path
        if not os.path.exists(source_path):
            return 'source not found'
        if not os.path.lexists(target_path):
            return 'not installed'
        if not os.path.islink(target_path):
            return 'unkown: not a symlink'
        if os.path.realpath(target_path) != source_path:
            return 'unknown: not linked to source'
        return 'installed'


class SoftwareConfiguration:
    def __init__(self, filename):
        self.name, self.files = None, collections.OrderedDict()
        # Load the configuration file.
        config = configparser.ConfigParser()
        config.read(filename)
        # Load the information contained in the configuration file.
        _debug('Parsing configuration file', filename)
        for section_name in config.sections():
            match = _SECTION.match(section_name)
            if match is None:
                _debug('Could not parse section name `{0}`.'.format(section_name))
                continue
            section = config[section_name]
            section_type, name = match.group('section_type'), match.group('name')
            if section_type == 'file':
                conf_file = ConfigurationFile(self, name, section)
                self.files[conf_file.name] = conf_file
            if section_type == 'software':
                self.name = name
                self.base_path = section.get('base_path', _HOME)
                self.setup_commands = section.get('setup-commands', '')
                self.setup_commands = self.setup_commands.strip().splitlines()
                self.teardown_commands = section.get('teardown-commands', '')
                self.teardown_commands = self.teardown_commands.strip().splitlines()
        # If there is no specific section for software in the file, then use
        # all the defaults.
        if self.name is None:
            self.name = os.path.basename(filename)[:-len('.ini')]
            self.base_path = _HOME
            self.setup_commands = []


def load_software_configurations():
    softwares = dict()
    _debug('Loading configurations from conf directory', _CONF_DIR)
    for root, dirs, filenames in os.walk(_CONF_DIR):
        for filename in filenames:
            if filename.endswith('.ini'):
                soft_conf = SoftwareConfiguration(os.path.join(root, filename))
                softwares[soft_conf.name] = soft_conf
    return softwares


def _iter_softwares(args, softwares):
    soft_names = sorted(softwares.keys() if not args.software else args.software)
    for soft_name in soft_names:
        try:
            soft = softwares[soft_name]
        except KeyError:
            _print('[warn] Software `%s` does not exist.', soft_name, file=sys.stderr)
            continue
        yield soft_name, soft


def info_command(args, softwares):
    for soft_name, soft in _iter_softwares(args, softwares):
        _print('Software:', soft_name)
        _print('Base:', soft.base_path, tabs=1)
        for filename, conf_file in soft.files.items():
            _print('Configuration filename:', filename, tabs=1)
            _print('source:', conf_file.source_path, tabs=2)
            _print('target:', conf_file.target_path, tabs=2)
            _print('status:', conf_file.status, tabs=2)


def install_command(args, softwares):
    for soft_name, soft in _iter_softwares(args, softwares):
        _print('Installing software', soft_name, 'in', soft.base_path)
        for command in soft.setup_commands:
            command = command.format(root=_ROOT, base_path=soft.base_path)
            _print('=>', 'Executing:', command, tabs=1)
            os.system(command)
        for filename, conf_file in soft.files.items():
            should_install = (not args.force and conf_file.status == 'not installed')
            should_install = should_install or (args.force and conf_file.status not in ['installed', 'source not found'])
            try:
                if should_install:
                    _print('=>', 'Installing', conf_file.source_path, 'as', conf_file.target_path, tabs=1)
                    if os.path.lexists(conf_file.target_path):
                        os.unlink(conf_file.target_path)
                    os.symlink(conf_file.source_path, conf_file.target_path)
                else:
                    _print('=>', 'Skipping', conf_file.source_path, 'because of status:', conf_file.status, tabs=1)
            except (IOError, OSError) as exc:
                msg = '/!\ Could not install {0} [{1}]: {2}'.format(
                    conf_file.target_path, type(exc).__name__, exc,
                )
                _print(msg, tabs=2)


def uninstall_command(args, softwares):
    for soft_name, soft in _iter_softwares(args, softwares):
        _print('Uninstalling software', soft_name, 'from', soft.base_path)
        for filename, conf_file in soft.files.items():
            try:
                if conf_file.status == 'installed':
                    _print('=>', 'Uninstalling', conf_file.target_path, tabs=1)
                    os.unlink(conf_file.target_path)
                else:
                    _print('=>', 'Skipping', conf_file.source_path, 'because of status:', conf_file.status, tabs=1)
            except (IOError, OSError) as exc:
                msg = '/!\ Could not uninstall {0} [{1}]: {2}'.format(
                    conf_file.target_path, type(exc).__name__, exc,
                )
                _print(msg, tabs=2)
        for command in soft.teardown_commands:
            command = command.format(root=_ROOT, base_path=soft.base_path)
            _print('=>', 'Executing:', command, tabs=1)
            os.system(command)


_COMMANDS = [
    ('install', install_command, 'install or update the configurations for softwares'),
    ('uninstall', uninstall_command, 'uninstall the configurations for softwares'),
    ('info', info_command, 'show information for softwares'),
]


def main(args):
    parser = argparse.ArgumentParser(description='Configuration Manager')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='enable debugging output.')
    subcommands, subparsers = dict(), parser.add_subparsers()
    for name, func, _help in _COMMANDS:
        sparser = subparsers.add_parser(name, help=_help)
        sparser.add_argument('software', nargs='*', help='software list (empty = all)')
        sparser.set_defaults(func=func)
        subcommands[name] = sparser
    subcommands['install'].add_argument('-f', '--force', action='store_true', default=False,
                                        help='force install (overwrites anything)')
    args = parser.parse_args(args)
    _debug.enabled = args.verbose
    # Load all the configurations.
    softwares = load_software_configurations()
    # Apply the action requested.
    return args.func(args, softwares)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
