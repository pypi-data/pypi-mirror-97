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
from ..appsocket import socketio


class HostListener(Service):
    """Kitica Device Hosts Listener Endpoint.

    Handles Device Hosts Update. [/hosts/listener]

    Methods
    ----------
    POST
        Handles POST Requests
        Updates the device status.
    """

    args = {
        'udid': fields.Str(),
        'status': fields.Str(validate=validate.OneOf(Service.STATUS)),
        'server': fields.String(required=True,
                                validate=validate.OneOf(Service.get_servers())),
    }

    @use_kwargs(args)
    def post(self,
             udid,
             status,
             server
             ):
        """Host Listener Interface.

        Handles POST Requests from [/hosts/listener] endpoint.

        Parameters
        ----------
        udid : str
            The Unique Device Identifier.
        status : str
            The status reported by the host listener client.
        """
        response = self._set_device_status(('udid=\"' +
                                            str(udid) +
                                            '\" AND server=\"' +
                                            str(server) + '\" '), status)
        socketio.emit('update', {'data': 'device status update'})
        return response
