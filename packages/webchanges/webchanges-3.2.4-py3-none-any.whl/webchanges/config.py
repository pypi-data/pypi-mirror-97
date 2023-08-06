"""Command-line configuration. For program config files, see storage.py"""

import argparse
import os.path

import webchanges as project


class BaseConfig(object):

    def __init__(self, project_name, config_dir, config, jobs, cache, hooks, verbose):
        self.project_name = project_name
        self.config_dir = config_dir
        self.config = config
        self.jobs = jobs
        self.cache = cache
        self.hooks = hooks
        self.verbose = verbose


class CommandConfig(BaseConfig):

    def __init__(self, project_name, config_dir, bindir, prefix, config, jobs, hooks, cache, verbose):
        super().__init__(project_name, config_dir, config, jobs, cache, hooks, verbose)
        self.bindir = bindir
        self.prefix = prefix

        if self.bindir == 'bin':
            # Installed system-wide
            self.examples_dir = os.path.join(prefix, 'share', self.project_name, 'examples')
        else:
            # Assume we are not yet installed
            self.examples_dir = os.path.join(prefix, bindir, 'share', self.project_name, 'examples')

        # self.urls_yaml_example = os.path.join(self.examples_dir, 'jobs-example.yaml')
        # self.hooks_py_example = os.path.join(self.examples_dir, 'hooks.rst')

        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description=project.__doc__.replace('\n\n', '--par--').replace('\n', ' ')
                                         .replace('--par--', '\n\n'),
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', version=f'{project.__project_name__}'
                                                                         f' {project.__version__}')
        parser.add_argument('-v', '--verbose', action='store_true', help='show debug output')

        group = parser.add_argument_group('override file defaults')
        group.add_argument('--jobs', '--urls', dest='jobs', metavar='FILE',
                           help='read job list (URLs) from FILE', default=self.jobs)
        group.add_argument('--config', metavar='FILE', help='read configuration from FILE', default=self.config)
        group.add_argument('--hooks', metavar='FILE', help='use FILE as hooks.py module', default=self.hooks)
        group.add_argument('--cache', metavar='FILE', help=('use FILE as cache database or directory, '
                                                            'alternatively can accept a redis URI'), default=self.cache)
        group = parser.add_argument_group('job management')
        group.add_argument('--list', action='store_true', help='list jobs')
        group.add_argument('--test', '--test-filter', dest='test_job', metavar='JOB',
                           help='test job and its filter (by URL/command or index)')
        group.add_argument('--test-diff', '--test-diff-filter', dest='test_diff', metavar='JOB',
                           help="test job's diff filter (up to 10 historical snapshots) (by URL/command or index)")
        group.add_argument('--errors', action='store_true', help='list jobs with errors or no data captured')
        group.add_argument('--add', metavar='JOB', help='add job (key1=value1,key2=value2,...) (obsolete; use --edit)')
        group.add_argument('--delete', metavar='JOB',
                           help='delete job by URL/command or index number. WARNING: all remarks are deleted from file '
                                '(obsolete; use --edit)')

        group = parser.add_argument_group('reporters')
        group.add_argument('--test-reporter', metavar='REPORTER', help='send a test notification')
        group.add_argument('--smtp-login', action='store_true',
                           help='enter or check password for SMTP email (stored in keyring)')
        group.add_argument('--telegram-chats', action='store_true', help='list telegram chats program is joined to')
        group.add_argument('--xmpp-login', action='store_true',
                           help='enter or check password for XMPP (stored in keyring)')

        group = parser.add_argument_group('launch editor ($EDITOR/$VISUAL)')
        group.add_argument('--edit', action='store_true', help='edit job (URL/command) list')
        group.add_argument('--edit-config', action='store_true', help='edit configuration file')
        group.add_argument('--edit-hooks', action='store_true', help='edit hooks script')

        group = parser.add_argument_group('miscellaneous')
        group.add_argument('--gc-cache', action='store_true',
                           help='garbage collect the cache database by removing old snapshots plus all data of old jobs'
                                ' now deleted')
        group.add_argument('--clean-cache', action='store_true', help='remove old snapshots from the cache database')
        group.add_argument('--rollback-cache', metavar='TIMESTAMP', type=int,
                           help='delete recent snapshots > timestamp; backup the database before using!')
        group.add_argument('--database-engine', choices=['sqlite3', 'minidb', 'textfiles'], default='sqlite3',
                           help='database engine to use (default: %(default)s)')
        group.add_argument('--features', action='store_true', help='list supported job types, filters and reporters')

        # workaround for avoiding triggering error when invoked by pytest
        if parser.prog != '_jb_pytest_runner.py':
            args = parser.parse_args()

            for arg in vars(args):
                argval = getattr(args, arg)
                setattr(self, arg, argval)

        return parser
