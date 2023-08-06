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
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_restful import Api, abort
from webargs.flaskparser import parser
from flask_cors import CORS
from KiticaAPI.utils import Constants
from KiticaAPI.api import (
    DeviceLending,
    Devices,
    DeviceUtils,
    HostListener,
    Servers,
    Service
)
from KiticaAPI.appsocket import create_app, socketio

app = create_app(debug=True)
# app.config['SECRET_KEY'] = 'secret!'

CORS(app)
api = Api(app)


@app.route('/config/device/platforms')
def device_platforms():
    return {
        'platforms': Constants.PLATFORMS
    }


@app.route('/config/device/types')
def device_types():
    return {
        'types': Constants.DEVICES_TYPES
    }


@app.route('/auth/allowed/hosts')
def allowed_hosts():
    return {
        Service.get_servers()
    }


# This error handler is necessary for usage with Flask-RESTful.
@parser.error_handler
def handle_request_parsing_error(err):
    abort(422, errors=err.messages)


# Add API RESTful Endpoints
# api.add_resource(Devices, '/devices', endpoint=Constants.DEVICES_ENDPOINT)
# api.add_resource(DeviceUtils, '/device/utils', endpoint=Constants.UTILS)
# api.add_resource(DeviceLending, '/device/lending', endpoint=Constants.LENDING)
# api.add_resource(HostListener, '/hosts/listener', endpoint=Constants.HOST_LISTENER)

api.add_resource(Devices, '/devices', endpoint=Constants.DEVICES_ENDPOINT)
api.add_resource(DeviceUtils, '/device/utils', endpoint=Constants.UTILS)
api.add_resource(DeviceLending, '/device/lending', endpoint=Constants.LENDING)
api.add_resource(HostListener, '/hosts/listener', endpoint=Constants.HOST_LISTENER)
api.add_resource(Servers, '/hosts/servers', endpoint=Constants.SERVERS)


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect')
def test_connect():
    print('connected!')
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


def server():
    """
    Kitica Devicepool API Service.
    """
    socketio.run(app, debug=True,
                 host='0.0.0.0')


if __name__ == '__main__':
    socketio.run(app, debug=True,
                 host='0.0.0.0')
