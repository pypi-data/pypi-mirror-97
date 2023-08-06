# -*- coding: utf-8 -*-
#  _     _       _
# | |   (_)  _  (_)
# | |  _ _ _| |_ _  ____ _____
# | |_/ ) (_   _) |/ ___|____ |
# |  _ (| | | |_| ( (___/ ___ |
# |_| \_)_|  \__)_|\____)_____|
#
# kitica DevicePool API
# Created by    : Joshua Kim Rivera
# Date          : September 23 2020 15:16 UTC-8
# Company       : Spiralworks Technologies Inc.
#
import yaml
import sqlite3
from sqlite3 import Error
from pathlib import Path
from os.path import join, exists, abspath, dirname
from .constants import Constants

CURDIR = dirname(abspath(__file__))


class Configurations(Constants):
    """
    Configurations Class.
    """
    def __init__(self):
        self._create_kitica_home()
        self.config = self._load_config_file()

    def _initialize_db_config(self):
        self.conn = sqlite3.connect(self.DATABASE_PATH)

    def _close_db_config(self):
        self.conn.close()

    def whitelistip(self, host):
        """
        Whitelist IP Argument Callback.

        -w, --whitelistip
        """
        if host not in self.config['hosts']['allowed']:
            print('Adding ' + host + ' to allowed hosts..')
            self.config['hosts']['allowed'].append(host)
            self._save_new_config()
        else:
            print('Host ' + host + ' already exists!')

    def teams(self, team):
        """
        Teams Argument Callback.

        -t, --teams
        """
        if team not in self.config['teams']:
            print('Adding ' + team + ' to device teams..')
            self.config['teams'].append(team)
            self._save_new_config()
        else:
            print('Team ' + team + ' already exists!')

    def database(self, command):
        """
        Database Argument Callback.

        -db, --database
        """
        if command not in self.DATABASE_COMMANDS:
            print('Invalid Database Command!')
        else:
            self._config_database_manager(command)

    def deletekey(self, delkey):
        """
        Delete Key Argument Callback Method.

        -del, --deletekey
        """
        if delkey not in self.config['admin']:
            print('Adding ' + delkey + ' to delete keys..')
            self.config['admin'].append(delkey)
            self._save_new_config()
        else:
            print('Delete Key ' + delkey + ' already exists!')

    def _config_database_manager(self, command):
        try:
            self._initialize_db_config()
            eval('self._' + command + '()')
        except Error as e:
            print(e)
        finally:
            if self.conn:
                self._close_db_config()

    def _create(self):
        cur = self.conn.cursor()
        with open(join(CURDIR, 'database.sql')) as fp:
            cur.executescript(fp.read())
        print('''
              Database Created.
              File Path: {db_path}
              Database Info: {db_ver}
              '''.format(db_ver=sqlite3.version,
                         db_path=self.DATABASE_PATH
                         )
              )

    def _open_config_file(self):
        """
        Opens the config file.
        """
        with open(join(self.KITICA_API_HOME, 'config.yaml'), 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        config = self.CONFIG_DEFAULT if config is None else config
        return config

    def _load_config_file(self):
        try:
            config = self._open_config_file()
        except Exception:
            open(join(self.KITICA_API_HOME, 'config.yaml'), 'a+')
            config = self._open_config_file()
        return config

    def _save_new_config(self):
        with open(join(self.KITICA_API_HOME, 'config.yaml'), 'w') as file:
            config = yaml.dump(self.config, file)

    def _create_kitica_home(self):
        Path(self.KITICA_API_HOME).mkdir(parents=True, exist_ok=True)
