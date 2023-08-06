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
from KiticaAPI.utils import Constants
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from ..appsocket import socketio


class DeviceLending(Service):
    """kitica Device Lending Endpoint.

    Handles Request made to [/device/lending] endpoint.

    Methods
    ----------
    GET
        Handles the GET Requests.
        Useful for obtaining device by specifying parameters.
    POST
        Handles the POST Requests.
        Fetches a specific device through deviceId.
    """

    args = {
        'platformName': fields.Str(required=False,
                                   validate=validate.OneOf(Service.PLATFORMS)
                                   ),
        'teamName': fields.String(required=False,
                                  validate=validate.OneOf(Service.CONFIG['teams'])
                                  ),
        'platformVersion': fields.Str(required=False),
        'borrowerIp': fields.Str(required=False),
        'borrowerHostname': fields.Str(required=False),
        'deviceId': fields.Int(required=False),
        'deviceType': fields.String(required=False,
                                    validate=validate.OneOf(Service.DEVICES_TYPES)
                                    ),
        'forced': fields.Boolean(required=False)
    }

    @use_kwargs(args)
    def get(self,
            platformName,
            forced=False,
            platformVersion=None,
            teamName=None,
            deviceId=None,
            borrowerIp=None,
            borrowerHostname=None,
            deviceType=None
            ):
        """Device Lending GET Request Handler.

        Handles GET Requests from [/device/lending] endpoint.

        Parameters
        ----------
        platformName : str, optional
            Device's platform name, should be one of the supported devices
            listed in the config.yaml.
        forced : boolean, default(false)
            Denotes if the device should be returned whether the status is
            ACTIVE.defaults to False.
        deviceId : str
            The device's Id given by the database. When this is passed,
            all other arguments are ignored,
        borrowerIp : str, optional
            The borrower's IP Address used for logging.
        borrowerHostname : str, optional
            The borrower's Hostname used for logging.

        Returns
        ----------
        device : json
            Returns the device data in json format should the request be
            successful.
        """
        device = self.borrow_device(platformName,
                                    forced,
                                    platformVersion,
                                    deviceId,
                                    teamName,
                                    borrowerIp,
                                    borrowerHostname,
                                    deviceType
                                    )
        socketio.emit('update', {'data': 'device was updated'})
        return device

    @use_kwargs(args)
    def post(self, deviceId):
        """Device Lending POST Request Handler.

        Handles GET Requests from /device/lending endpoint.
        Accepts deviceId Parameter to fetch a specific device.

        Parameters
        ----------
        deviceId : str
            The device's Id given by the database.

        Returns
        ----------
        device : json
            Returns the device data in json format should the request be
            successful.
        """
        response = self.return_device(deviceId)
        socketio.emit('update', {'data': 'device was updated'})
        return response
