#! /usr/bin/env python

from __future__ import print_function

import argparse
import collections
import os
import platform
import re
import shlex
import sys

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


_ROOT = os.path.abspath(os.path.dirname(__file__))
_CONF_DIR = os.path.join(_ROOT, 'configurations')
_FILES_DIR = os.path.join(_ROOT, 'files')

_SECTION = re.compile(r'^(?P<section_type>\w+):(?P<name>[a-zA-Z0-9\.-]+)$')
_LIST_OF_VALUES = re.compile(r'\s*,\s*')

_CURRENT_PLATFORM = platform.system().lower()
_PLATFORMS = set(['linux', 'darwin'])


class Status(object):
    INSTALLED = 'installed'
    NOT_AVAILABLE_FOR_PLATFORM = 'not available for platform'
    NOT_INSTALLED = 'not installed'
    SOURCE_NOT_FOUND = 'source not found'
    UNKNOWN_NOT_A_SYMLINK = 'unknown: not a symlink'
    UNKNOWN_NOT_LINKED_TO_SOURCE = 'unknown: not linked to source'


def _parse_platforms(value):
    if value is None:
        return _PLATFORMS
    if isinstance(value, (set, list)):
        return value
    values = _LIST_OF_VALUES.split(value)
    values = set([v for v in values if v.strip() != ''])
    for value in values:
        if value not in _PLATFORMS:
            _debug('Value {} is not a valid platform.'.format(value))
            return _PLATFORMS
    return values


def _debug(*a, **kw):
    if not _debug.enabled:
        return
    kw.setdefault('file', sys.stderr)
    print('[debug]', *a, **kw)


_debug.enabled = False


def _format_list(l):
    return ', '.join(sorted(l))


def _print(*a,  **kw):
    a, tabs = list(a), kw.pop('tabs', 0)
    if tabs:
        a.insert(0, ' ' * (4 * tabs - 1))
    a = [_format_list(v) if isinstance(v, (set, list)) else v for v in a]
    print(*a, **kw)


def _parse_bool(s):
    if isinstance(s, bool):
        return s
    val = s.lower().strip()
    if val in ['0', 'off', 'no', 'false']:
        return False
    if val in ['1', 'on', 'yes', 'true']:
        return True
    raise ValueError('value "{0}" is not a valid boolean'.format(s))


def _translate_configparser_to_dict(config):
    res = dict()
    for section_name in config.sections():
        res[section_name] = dict(config.items(section_name))
    return res


class PlatformsHolder(object):
    @property
    def platforms(self):
        if not hasattr(self, '_platforms'):
            self._platforms = _parse_platforms(None)
        return self._platforms

    @platforms.setter
    def platforms(self, value):
        self._platforms = _parse_platforms(value)




class ConfigurationFile(PlatformsHolder):
    def __init__(self, soft_conf, name, conf):
        self._soft_conf, self.name, self._conf = soft_conf, name, conf
        # generate filename
        self.platforms = self._conf.get('platforms')
        if self._conf.get('filename') is not None:
            self.source_filename = self._conf.get('filename')
            self.target_filename = self.source_filename
        else:
            self.source_filename = self._conf.get('source_filename', self.name)
            self.target_filename = self._conf.get('target_filename', self.source_filename)
        if not _parse_bool(self._conf.get('no_dot', False)):
            self.target_filename = '.{}'.format(self.target_filename)

    @property
    def target_path(self):
        return os.path.expanduser(os.path.join(
            self._soft_conf.base_path, self.target_filename))

    @property
    def source_path(self):
        return os.path.join(_FILES_DIR, self.source_filename)

    def can(self, action, force=False):
        _not_installable = [
            Status.INSTALLED,
            Status.NOT_AVAILABLE_FOR_PLATFORM,
            Status.SOURCE_NOT_FOUND,
        ]
        if action == 'install':
            if not force and self.status == Status.NOT_INSTALLED:
                return True
            if force and self.status not in _not_installable:
                return True
            return False
        if action == 'uninstall':
            return self.status == 'installed'
        return False

    @property
    def status(self):
        source_path, target_path = self.source_path, self.target_path
        if _CURRENT_PLATFORM not in self.platforms:
            return Status.NOT_AVAILABLE_FOR_PLATFORM
        if not os.path.exists(source_path):
            return Status.SOURCE_NOT_FOUND
        if not os.path.lexists(target_path):
            return Status.NOT_INSTALLED
        if not os.path.islink(target_path):
            return Status.UNKNOWN_NOT_A_SYMLINK
        if os.path.realpath(target_path) != source_path:
            return Status.UNKNOWN_NOT_LINKED_TO_SOURCE
        return Status.INSTALLED


class SoftwareConfiguration(PlatformsHolder):
    def __init__(self, filename):
        self.name = None
        self.files = collections.OrderedDict()
        self.platforms = None
        # Load the configuration file.
        config = configparser.ConfigParser()
        config.read(filename)
        config = _translate_configparser_to_dict(config)
        # Load the information contained in the configuration file.
        _debug('Parsing configuration file', filename)
        for section_name in config.keys():
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
                self.platforms = section.get('platforms')
                self.base_path = section.get('base_path', '~')
                self.setup_commands = section.get('setup-commands', '')
                self.setup_commands = self.setup_commands.strip().splitlines()
                self.teardown_commands = section.get('teardown-commands', '')
                self.teardown_commands = self.teardown_commands.strip().splitlines()
        # If there is no specific section for software in the file, then use
        # all the defaults.
        if self.name is None:
            self.name = os.path.basename(filename)[:-len('.ini')]
            self.base_path = '~'
            self.setup_commands = []
            self.teardown_commands = []
        # Global treatment of paths.
        self.base_path = os.path.expanduser(self.base_path)
        # Finalize platforms attributes.
        if self.platforms != _PLATFORMS:
            excluded_platforms = (_PLATFORMS - self.platforms)
            for conf_file in self.files.values():
                if conf_file.platforms != _PLATFORMS:
                    if not conf_file.platforms.issubset(self.platforms):
                        msg = 'Configuration file {0}\'s platforms is'
                        msg += ' not a subset of {1}\'s platforms.'
                        _debug(msg.format(conf_file.name, self.name))
                    conf_file.platforms = conf_file.platforms - excluded_platforms
                else:
                    conf_file.platforms = self.platforms


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
    forced = bool(args.software)
    soft_names = sorted(softwares.keys() if not forced else args.software)
    for soft_name in soft_names:
        try:
            soft = softwares[soft_name]
        except KeyError:
            warn = '[warn] Software `{}` does not exist.'
            _print(warn.format(soft_name), file=sys.stderr)
            continue
        if not args.ignore_platform and _CURRENT_PLATFORM not in soft.platforms:
            warn = 'Software `{}` is not available for this platform.'
            if forced:
                _print('[warn]', warn.format(soft_name), file=sys.stderr)
            else:
                _debug(warn.format(soft_name))
            continue
        yield soft_name, soft


def info_command(args, softwares):
    for soft_name, soft in _iter_softwares(args, softwares):
        _print('Software:', soft_name)
        _print('Base:', soft.base_path, tabs=1)
        _print('Platforms:', soft.platforms, tabs=1)
        for filename, conf_file in soft.files.items():
            _print('Configuration filename:', filename, tabs=1)
            _print('platforms:', conf_file.platforms, tabs=2)
            _print('source:', conf_file.source_path, tabs=2)
            _print('target:', conf_file.target_path, tabs=2)
            _print('status:', conf_file.status, tabs=2)


def install_command(args, softwares):
    for soft_name, soft in _iter_softwares(args, softwares):
        _print('Installing software', soft_name, 'in', soft.base_path)
        for command in soft.setup_commands:
            command = command.format(root=_ROOT, base_path=soft.base_path)
            _print('=>', 'Executing:', command, tabs=1)
            os.system(shlex.join(['/bin/sh', '-c', command]))
        for filename, conf_file in soft.files.items():
            try:
                if conf_file.can('install', force=args.force):
                    _print('=> Installing {0} as {1}'.format(
                        conf_file.source_path,
                        conf_file.target_path,
                    ), tabs=1)
                    if os.path.lexists(conf_file.target_path):
                        os.unlink(conf_file.target_path)
                    os.symlink(conf_file.source_path, conf_file.target_path)
                else:
                    _print('=> Skipping {0} because of status: {1}'.format(
                        conf_file.source_path,
                        conf_file.status,
                    ), tabs=1)
            except (IOError, OSError) as exc:
                msg = '/!\\ Could not install {0} [{1}]: {2}'.format(
                    conf_file.target_path, type(exc).__name__, exc,
                )
                _print(msg, tabs=2)


def uninstall_command(args, softwares):
    for soft_name, soft in _iter_softwares(args, softwares):
        _print('Uninstalling software', soft_name, 'from', soft.base_path)
        for filename, conf_file in soft.files.items():
            try:
                if conf_file.can('uninstall'):
                    _print('=> Uninstalling', conf_file.target_path, tabs=1)
                    os.unlink(conf_file.target_path)
                else:
                    _print('=> Skipping {0} because of status: {1}'.format(
                        conf_file.source_path,
                        conf_file.status
                    ), tabs=1)
            except (IOError, OSError) as exc:
                msg = '/!\\ Could not uninstall {0} [{1}]: {2}'.format(
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
        sparser.add_argument('-I', '--ignore-platform', action='store_true',
                             default=False, help='ignore platform')
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
    if 'func' in args:
        return args.func(args, softwares)
    else:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
