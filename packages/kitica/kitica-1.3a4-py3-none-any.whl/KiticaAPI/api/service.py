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
from flask_restful import Resource
from flask_socketio import SocketIO, emit
from KiticaAPI.utils import (
    Database,
    Configurations,
    Constants
)


class Service(Resource,
              Database,
              Constants
              ):
    """
    Base API Service Class
    """
    CONFIG = Configurations()._load_config_file()

    def __init__(self):
        pass

    @staticmethod
    def get_servers():
        db = Database()
        return db._fetch_column_list('SELECT serverAddress FROM servers')
