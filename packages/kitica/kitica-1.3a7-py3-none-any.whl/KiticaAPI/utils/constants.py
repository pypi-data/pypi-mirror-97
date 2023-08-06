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
from pathlib import Path
from os.path import join


class Constants():
    """
    Constants Class.
    """
    DEVICES_ENDPOINT = 'devices'
    HOST_LISTENER = 'hosts/listener'
    LENDING = 'device/lending'
    UTILS = 'device/utils'
    SERVERS = 'hosts/servers'
    DEVICES_TYPES = [
        'Real Device',
        'Emulator',
        'Simulator'
    ]
    PLATFORMS = [
        'Android',
        'iOS'
    ]
    STATUS = [
        'FREE',
        'ACTIVE',
        'UNPLUGGED',
        'DISABLED'
    ]
    CONFIG_DEFAULT = {
        'admin': ['Admin'],
        'hosts': {'allowed': []},
        'teams': ['']
    }
    KITICA_API_HOME = join(str(Path.home()), 'kitica', 'api')
    DATABASE_COMMANDS = [
        'create'
    ]
    DATABASE_PATH = join(KITICA_API_HOME, 'kitica.db')
