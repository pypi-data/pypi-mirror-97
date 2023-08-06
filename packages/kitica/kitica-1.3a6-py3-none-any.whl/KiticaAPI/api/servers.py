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
from .service import Service
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from flask_socketio import emit


class Servers(Service):
    """ kitica Devices Endpoint.

    ...

    Methods
    ----------
    GET
        Handles the GET Requests.
        Returns specific device/devices specified by the parameter/parameters.
    """
    args = {
        'server': fields.String(required=False)
    }

    def get(self):
        return Service.get_servers()

    @use_kwargs(args)
    def post(self, server):
        servers = Service.get_servers()
        if server not in servers:
            query = f'INSERT INTO servers (serverAddress) VALUES(\"{server}\");'
            self._update(query)
            return {
                'message': f'Added {server} to allowed hosts.',
                'statusCode': 1
            }
        else:
            return {
                'message': 'Host already exists.',
                'statusCode': -1
            }
