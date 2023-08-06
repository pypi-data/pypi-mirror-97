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
# Date          : February 4 2020 14:55 UTC-8
# Company       : Spiralworks Technologies Inc.
#
from flask import Flask
from flask_restful import Api, abort
from webargs.flaskparser import parser
from flask_cors import CORS
from KiticaAPI.utils import Constants
from KiticaAPI.api import (
    DeviceLending,
    Devices,
    DeviceUtils,
    HostListener
)

app = Flask(__name__)
CORS(app)
api = Api(app)


# This error handler is necessary for usage with Flask-RESTful.
@parser.error_handler
def handle_request_parsing_error(err):
    abort(422, errors=err.messages)


# Add API RESTful Endpoints
api.add_resource(Devices, '/devices', endpoint=Constants.DEVICES_ENDPOINT)
api.add_resource(DeviceUtils, '/device/utils', endpoint=Constants.UTILS)
api.add_resource(DeviceLending, '/device/lending', endpoint=Constants.LENDING)
api.add_resource(HostListener, '/hosts/listener', endpoint=Constants.HOST_LISTENER)


def api():
    """
    Kitica Devicepool API Service.
    """
    app.run(debug=True,
            host='localhost'
            )
