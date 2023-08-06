import copy
import getpass
import logging
import os
import shutil
import sqlite3
import stat
import threading
from abc import ABCMeta, abstractmethod
from datetime import datetime

import msgpack

try:
    import pwd
except ImportError:
    pwd = None

try:
    import redis
except ImportError:
    redis = None

import yaml

import webchanges as project

from .filters import FilterBase
from .jobs import JobBase, ShellJob, UrlJob
from .util import atomic_rename, edit_file

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'display': {  # select whether the report include the categories below
        'new': True,
        'error': True,
        'unchanged': False,
    },

    'report': {
        # text, html and markdown are three content types of reports
        'html': {
            'diff': 'unified',  # 'unified' or 'table'
            'diff_numlines': None,  # default if None
        },

        'text': {
            'line_length': 75,
            'details': True,
            'footer': True,
            'minimal': False,
        },

        'markdown': {
            'details': True,
            'footer': True,
            'minimal': False,
        },

        # the keys below control where a report is displayed and/or sent

        'stdout': {  # the console / command line display
            'enabled': True,
            'color': True,
        },

        'browser': {  # the system's default browser
            'enabled': False,
            'title': f'[{project.__project_name__}] {{count}} changes: {{jobs}}'
        },

        'email': {  # email (except mailgun)
            'enabled': False,
            'html': True,
            'to': '',
            'from': '',
            'subject': f'[{project.__project_name__}] {{count}} changes: {{jobs}}',
            'method': 'smtp',  # either 'smtp' or 'sendmail'
            'smtp': {
                'host': 'localhost',
                'user': '',
                'port': 25,
                'starttls': True,
                'auth': True,
                'insecure_password': '',
            },
            'sendmail': {
                'path': 'sendmail',
            }
        },
        'pushover': {
            'enabled': False,
            'app': '',
            'device': None,
            'sound': 'spacealarm',
            'user': '',
            'priority': 'normal',
        },
        'pushbullet': {
            'enabled': False,
            'api_key': '',
        },
        'telegram': {
            'enabled': False,
            'bot_token': '',
            'chat_id': '',
        },
        'webhook': {
            'enabled': False,
            'webhook_url': '',
            'max_message_length': '',
        },
        'webhook_markdown': {
            'enabled': False,
            'webhook_url': '',
            'max_message_length': '',
        },
        'matrix': {
            'enabled': False,
            'homeserver': '',
            'access_token': '',
            'room_id': '',
        },
        'mailgun': {
            'enabled': False,
            'region': 'us',
            'api_key': '',
            'domain': '',
            'from_mail': '',
            'from_name': '',
            'to': '',
            'subject': '{count} changes: {jobs}'
        },
        'ifttt': {
            'enabled': False,
            'key': '',
            'event': '',
        },
        'xmpp': {
            'enabled': False,
            'sender': '',
            'recipient': '',
        },
    },

    'job_defaults': {  # default settings for jobs
        'all': {},
        'url': {},  # these are used for url jobs without use_browser
        'browser': {},  # these are used for url jobs with use_browser: true
        # TODO rename 'shell' to 'command' for clarity
        'shell': {},  # these are used for 'command' jobs
    }
}


def merge(source, destination):
    # https://stackoverflow.com/a/20666342
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def load(self, *args):
        ...

    @abstractmethod
    def save(self, *args):
        ...


class BaseFileStorage(BaseStorage, metaclass=ABCMeta):
    def __init__(self, filename: str) -> None:
        self.filename = filename


class BaseTextualFileStorage(BaseFileStorage, metaclass=ABCMeta):
    def __init__(self, filename):
        super().__init__(filename)
        self.config = {}
        self.load()

    @classmethod
    @abstractmethod
    def parse(cls, *args):
        ...

    def edit(self, example_file=None):
        fn_base, fn_ext = os.path.splitext(self.filename)
        file_edit = fn_base + '.edit' + fn_ext

        if os.path.exists(self.filename):
            shutil.copy(self.filename, file_edit)
        elif example_file is not None and os.path.exists(example_file):
            shutil.copy(example_file, file_edit)

        while True:
            try:
                edit_file(file_edit)
                # Check if we can still parse it
                if self.parse is not None:
                    self.parse(file_edit)
                break  # stop if no exception on parser
            except SystemExit:
                raise
            except Exception as e:
                print()
                print('Errors in file:')
                print('======')
                print(e)
                print('======')
                print('')
                print('The file', file_edit, 'was NOT updated.')
                user_input = input('Do you want to retry the same edit? (Y/n)')
                if not user_input or user_input.lower()[0] == 'y':
                    continue
                print('Your changes have been saved in', file_edit)
                return 1

        atomic_rename(file_edit, self.filename)
        print('Saving edit changes in', self.filename)

    @classmethod
    def write_default_config(cls, filename):
        config_storage = cls(None)
        config_storage.filename = filename
        config_storage.save()


class JobsBaseFileStorage(BaseTextualFileStorage, metaclass=ABCMeta):
    def __init__(self, filename):
        super().__init__(filename)
        self.filename = filename

    def shelljob_security_checks(self):

        if os.name == 'nt':
            return []

        shelljob_errors = []
        current_uid = os.getuid()

        dirname = os.path.dirname(self.filename) or '.'
        dir_st = os.stat(dirname)
        if (dir_st.st_mode & (stat.S_IWGRP | stat.S_IWOTH)) != 0:
            shelljob_errors.append(f'{dirname} is group/world-writable')
        if dir_st.st_uid != current_uid:
            shelljob_errors.append(f'{dirname} not owned by {getpass.getuser()}')

        file_st = os.stat(self.filename)
        if (file_st.st_mode & (stat.S_IWGRP | stat.S_IWOTH)) != 0:
            shelljob_errors.append(f'{self.filename} is group/world-writable')
        if file_st.st_uid != current_uid:
            shelljob_errors.append(f'{self.filename} not owned by {getpass.getuser()}')

        return shelljob_errors

    def load_secure(self):
        jobs = self.load()

        def is_shell_job(job):
            if isinstance(job, ShellJob):
                return True

            for filter_kind, subfilter in FilterBase.normalize_filter_list(job.filter):
                if filter_kind == 'shellpipe':
                    return True

                if job.diff_tool is not None:
                    return True

            return False

        # Security checks for shell jobs - only execute if the current UID
        # is the same as the file/directory owner and only owner can write
        shelljob_errors = self.shelljob_security_checks()
        if shelljob_errors and any(is_shell_job(job) for job in jobs):
            print(f"Removing 'command' job(s) because {' and '.join(shelljob_errors)} (see "
                  f'https://webchanges.readthedocs.io/en/stable/jobs.html#important-note-for-command-jobs)')
            jobs = [job for job in jobs if not is_shell_job(job)]

        return jobs


class BaseTxtFileStorage(BaseTextualFileStorage, metaclass=ABCMeta):
    @classmethod
    def parse(cls, *args):
        filename = args[0]
        if filename is not None and os.path.exists(filename):
            with open(filename) as fp:
                for line in fp:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if line.startswith('|'):
                        yield ShellJob(command=line[1:])
                    else:
                        args = line.split(None, 2)
                        if len(args) == 1:
                            yield UrlJob(url=args[0])
                        elif len(args) == 2:
                            yield UrlJob(url=args[0], post=args[1])
                        else:
                            raise ValueError(f'Unsupported line format: {line}')


class BaseYamlFileStorage(BaseTextualFileStorage, metaclass=ABCMeta):
    @classmethod
    def parse(cls, *args):
        filename = args[0]
        if filename is not None and os.path.exists(filename):
            with open(filename) as fp:
                return yaml.safe_load(fp)


class YamlConfigStorage(BaseYamlFileStorage):
    def load(self, *args):
        self.config = merge(self.parse(self.filename) or {}, copy.deepcopy(DEFAULT_CONFIG))

    def save(self, *args):
        with open(self.filename, 'w') as fp:
            yaml.safe_dump(self.config, fp, default_flow_style=False, sort_keys=False, allow_unicode=True)


class JobsYaml(BaseYamlFileStorage, JobsBaseFileStorage):
    @classmethod
    def parse(cls, *args):
        filename = args[0]
        if filename is not None and os.path.exists(filename):
            with open(filename) as fp:
                return [JobBase.unserialize(job) for job in yaml.safe_load_all(fp)
                        if job is not None]

    def save(self, *args):
        jobs = args[0]
        print(f'Saving updated list to {self.filename}')

        with open(self.filename, 'w') as fp:
            yaml.safe_dump_all([job.serialize() for job in jobs], fp, default_flow_style=False, sort_keys=False,
                               allow_unicode=True)

    def load(self, *args):
        with open(self.filename) as fp:
            return [JobBase.unserialize(job) for job in yaml.safe_load_all(fp) if job is not None]


class CacheStorage(BaseFileStorage, metaclass=ABCMeta):
    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def get_guids(self):
        ...

    @abstractmethod
    def load(self, guid):
        ...

    @abstractmethod
    def save(self, guid, data, timestamp, tries, etag):
        ...

    @abstractmethod
    def delete(self, guid):
        ...

    @abstractmethod
    def clean(self, guid):
        ...

    @abstractmethod
    def rollback(self, guid):
        ...

    def backup(self):
        for guid in self.get_guids():
            data, timestamp, tries, etag = self.load(guid)
            yield guid, data, timestamp, tries, etag

    def restore(self, entries):
        for guid, data, timestamp, tries, etag in entries:
            self.save(guid, data, timestamp, tries, etag)

    def gc(self, known_guids):
        for guid in set(self.get_guids()) - set(known_guids):
            print(f'Deleting: {guid} (no longer being tracked)')
            self.delete(guid)
        self.clean_cache(known_guids)

    def clean_cache(self, known_guids):
        if hasattr(self, 'clean_all'):
            count = self.clean_all()
            if count:
                print(f'Deleted {count} old snapshots')
        else:
            for guid in known_guids:
                count = self.clean(guid)
                if count > 0:
                    print(f'Deleted {count} old snapshots of {guid}')

    def rollback_cache(self, timestamp):
        count = self.rollback(timestamp)
        try:
            timestamp_date = datetime.fromtimestamp(timestamp).astimezone().isoformat()
        except OSError:
            timestamp_date = datetime.fromtimestamp(timestamp).isoformat()
        if count:
            print(f'Deleted {count} snapshots taken after {timestamp_date}')
        else:
            print(f'No snapshots taken after {timestamp_date} found to delete')


class CacheDirStorage(CacheStorage):
    """Stores the information in individual files in a directory 'filename'"""
    def __init__(self, filename):
        super().__init__(filename)
        if not os.path.exists(filename):
            os.makedirs(filename)

    def close(self):
        """No need to close"""

    def _get_filename(self, guid):
        return os.path.join(self.filename, guid)

    def get_guids(self):
        return os.listdir(self.filename)

    def load(self, guid):
        filename = self._get_filename(guid)
        if not os.path.exists(filename):
            return None, None, None, None

        try:
            with open(filename) as fp:
                data = fp.read()
        except UnicodeDecodeError:
            with open(filename, 'rb') as fp:
                data = fp.read().decode(errors='ignore')

        timestamp = os.stat(filename)[stat.ST_MTIME]

        return data, timestamp, None, None

    def save(self, guid, data, timestamp, tries, etag):
        # Timestamp is not saved as is read from the file's timestamp; ETag is ignored
        filename = self._get_filename(guid)
        with open(filename, 'w+') as fp:
            fp.write(data)

    def delete(self, guid):
        filename = self._get_filename(guid)
        if os.path.exists(filename):
            os.unlink(filename)

    def clean(self, guid):
        """We only store the latest version, no need to clean"""

    def rollback(self, timestamp: float) -> None:
        raise NotImplementedError("'textfiles' databases cannot be rolled back as new snapshots overwrite old ones")


class CacheSQLite3Storage(CacheStorage):
    """
    Handles storage of the snapshot in a SQLite database in the 'filename' file using Python's built-in sqlite3 module
    and the msgpack package.

    The database contains the 'webchanges' table with the following columns:
    * uuid: unique hash of the "location", i.e. the URL; indexed
    * timestamp: the Unix timestamp of when then the snapshot was taken
    * msgpack_data: a msgpack blob containing 'data' 'tries' and 'etag' in a dict of keys 'd', 't' and 'e'
    """
    def __init__(self, filename: str) -> None:
        """Opens the database file and, if new, creates a table and index

        :param filename: The full filename of the database file
        """
        super().__init__(filename)

        dirname = os.path.dirname(filename)
        if dirname and not os.path.isdir(dirname):
            os.makedirs(dirname)
        # if os.path.isfile(filename):
        #     import shutil
        #     _ = shutil.copy2(filename, f'{filename}.{int(time.time())}.bak')

        # https://stackoverflow.com/questions/26629080
        self.lock = threading.RLock()

        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.db.cursor()
        tables = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchone()
        if tables == ('CacheEntry',):
            # found a minidb legacy database; rename it for migration and create new one
            self.db.close()
            os.rename(filename, filename + '.minidb')
            self.db = sqlite3.connect(filename, check_same_thread=False)
            self.cur = self.db.cursor()
        if tables != ('webchanges',):
            # not yet initialized
            self.cur.execute('CREATE TABLE webchanges (uuid TEXT, timestamp REAL, msgpack_data BLOB)')
            self.cur.execute('CREATE INDEX idx_uuid ON webchanges (uuid)')
            self.db.commit()
        if tables == ('CacheEntry',):
            # migrate the minidb legacy database renamed above
            self.migrate_from_minidb(filename + '.minidb')

    def close(self) -> None:
        """Cleans up the database and closes the connection to it"""
        with self.lock:
            self.cur.execute('VACUUM')
            self.db.commit()
            self.db.close()
            del self.db
            del self.cur

    def get_guids(self) -> list:
        """Lists the unique 'guid's contained in the database

        :returns: A list of guids
        """
        with self.lock:
            self.cur.row_factory = lambda cursor, row: row[0]
            guids = self.cur.execute('SELECT DISTINCT uuid FROM webchanges').fetchall()
            self.cur.row_factory = None
        return guids

    def load(self, guid: str) -> (str, float, int, str):  # TODO handle NoneType
        """return the most recent entry matching a 'guid'

        :param guid: The guid

        :returns: A tuple (data, timestamp, tries, etag)
            WHERE
            data is the data
            timestamp is the timestamp
            tries is the number of tries
            etag is the ETag
        """
        with self.lock:
            row = self.cur.execute('SELECT msgpack_data, timestamp FROM webchanges WHERE uuid = ? '
                                   'ORDER BY timestamp DESC LIMIT 1', (guid,)).fetchone()
        if row:
            msgpack_data, timestamp = row
            r = msgpack.unpackb(msgpack_data)
            return r['d'], timestamp, r['t'], r['e']

        return None, None, 0, None

    def get_history_data(self, guid: str, count: int = 1) -> dict:
        """Return some data from the last 'count' entries matching a 'guid'

        :param guid: The guid
        :param count: The maximum number of entries to return

        :returns: A dict (key: value)
            WHERE
            key is the data
            value is the timestamp
        """
        history = {}
        if count < 1:
            return history

        with self.lock:
            rows = self.cur.execute('SELECT msgpack_data, timestamp FROM webchanges WHERE uuid = ? '
                                    'ORDER BY timestamp DESC', (guid,)).fetchall()
        if rows:
            for msgpack_data, timestamp in rows:
                r = msgpack.unpackb(msgpack_data)
                if not r['t']:
                    if r['d'] not in history:
                        history[r['d']] = timestamp
                        if len(history) >= count:
                            break
        return history

    def save(self, guid: str, data: str, timestamp: float, tries: int, etag: str) -> None:
        """Save the data from a job

        :param guid: The guid
        :param data: The data
        :param timestamp: The timestamp
        :param tries: The number of tries
        :param etag: The ETag
        """
        c = {
            'd': data,
            't': tries,
            'e': etag,
        }
        msgpack_data = msgpack.packb(c)
        with self.lock:
            self.cur.execute('INSERT INTO webchanges VALUES (?, ?, ?)', (guid, timestamp, msgpack_data))
            self.db.commit()

    def delete(self, guid: str) -> None:
        """Delete all entries matching a 'guid'

        :param guid: The guid
        """
        with self.lock:
            self.cur.execute('DELETE FROM webchanges WHERE uuid = ?', (guid,))
            self.db.commit()

    def clean(self, guid: str, keep_entries: int = 1) -> int:
        """For the given 'guid', keep only the latest 'keep_entries' entries and delete all other (older) ones
        Use clean_all() if you want to remove all older entries

        :param guid: The guid
        :param keep_entries: Number of entries to keep after deletion

        :returns: Number of records deleted
        """
        with self.lock:
            self.cur.execute('''
                DELETE FROM webchanges
                WHERE ROWID IN (
                    SELECT ROWID FROM webchanges
                    WHERE uuid = ?
                    ORDER BY timestamp DESC
                    LIMIT -1 OFFSET ?
                )''', (guid, keep_entries))
            num_del = self.cur.execute('SELECT changes()').fetchone()[0]
            self.db.commit()
        return num_del

    def clean_all(self) -> int:
        """Delete all older entries for each 'guid' (keep only last one)

        :returns: Number of records deleted
        """
        with self.lock:
            self.cur.execute('''
                DELETE FROM webchanges
                WHERE EXISTS (
                    SELECT 1 FROM webchanges w
                    WHERE w.uuid = webchanges.uuid AND w.timestamp < webchanges.timestamp
                )''')
            num_del = self.cur.execute('SELECT changes()').fetchone()[0]
            self.db.commit()
        return num_del

    def rollback(self, timestamp: float) -> int:
        """Rollback database to timestamp

        :returns: Number of records deleted
        """
        with self.lock:
            self.cur.execute('''
                DELETE FROM webchanges
                WHERE EXISTS (
                     SELECT 1 FROM webchanges w
                     WHERE w.uuid = webchanges.uuid AND webchanges.timestamp > ? AND w.timestamp > ?
                )''', (timestamp, timestamp))
            num_del = self.cur.execute('SELECT changes()').fetchone()[0]
            self.db.commit()
        return num_del

    def migrate_from_minidb(self, filename):
        print("Found 'minidb' database and upgrading it to the new engine (note: only the last snapshot is retained).")
        logger.info("Found legacy 'minidb' database and converting it to 'sqlite3' and new schema. "
                    "Package 'minidb' needs to be installed for the conversion.")

        from .storage_minidb import CacheMiniDBStorage

        legacy_db = CacheMiniDBStorage(filename)
        for guid in legacy_db.get_guids():
            data, timestamp, tries, etag = legacy_db.load(guid)
            self.save(guid, data, timestamp, tries, etag)
        legacy_db.close()
        print(f'Database upgrade finished; the following backup file can be safely deleted: {filename}')
        print("and the 'minidb' package can be removed (unless used by another program): $ pip uninstall minidb")
        print('-' * 80)


class CacheRedisStorage(CacheStorage):
    def __init__(self, filename):
        super().__init__(filename)

        if redis is None:
            raise ImportError("Python package 'redis' is missing")

        self.db = redis.from_url(filename)

    @staticmethod
    def _make_key(guid):
        return 'guid:' + guid

    def close(self):
        self.db.connection_pool.disconnect()
        self.db = None

    def get_guids(self):
        guids = []
        for guid in self.db.keys(b'guid:*'):
            guids.append(str(guid[len('guid:'):]))
        return guids

    def load(self, guid):
        key = self._make_key(guid)
        data = self.db.lindex(key, 0)

        if data:
            r = msgpack.unpackb(data)
            return r['data'], r['timestamp'], r['tries'], r['etag']

        return None, None, 0, None

    def get_history_data(self, guid, count=1):
        history = {}
        if count < 1:
            return history

        key = self._make_key(guid)
        for i in range(0, self.db.llen(key)):
            r = self.db.lindex(key, i)
            c = msgpack.unpackb(r)
            if c['tries'] == 0 or c['tries'] is None:
                if c['data'] not in history:
                    history[c['data']] = c['timestamp']
                    if len(history) >= count:
                        break
        return history

    def save(self, guid, data, timestamp, tries, etag):
        r = {
            'data': data,
            'timestamp': timestamp,
            'tries': tries,
            'etag': etag,
        }
        self.db.lpush(self._make_key(guid), msgpack.packb(r))

    def delete(self, guid):
        self.db.delete(self._make_key(guid))

    def clean(self, guid):
        key = self._make_key(guid)
        i = self.db.llen(key)
        if self.db.ltrim(key, 0, 0):
            return i - self.db.llen(key)

    def rollback(self, timestamp: float) -> None:
        raise NotImplementedError("'redis' databases cannot be rolled back as new snapshots overwrite old ones")
