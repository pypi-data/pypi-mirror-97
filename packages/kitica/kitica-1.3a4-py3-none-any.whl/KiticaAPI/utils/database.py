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
import sqlite3
from sqlite3 import Error
from os import environ
from os.path import abspath, dirname, join, exists
from .constants import Constants
from .configurations import Configurations


class Database(Constants):

    def __init__(self):
        """Constructor Function
        """
        pass

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def _initialize_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.DATABASE_PATH)
            conn.row_factory = sqlite3.Row
        except Error as e:
            raise e
        return conn

    def get_random_free_device(self, platform=None):
        if platform is not None:
            query = 'SELECT * FROM device WHERE status="FREE" AND platformName=\"' + str(platform) + '\"'
        else:
            query = 'SELECT * FROM device WHERE status="FREE" ORDER BY RANDOM() LIMIT 1'
        device = self._fetch_one(query)
        return device

    def get_device_by_id(self, deviceId):
        return self._get_device('deviceId=' + str(deviceId))

    def get_device_by_udid(self, udid):
        return self._get_device('udid=\"' + str(udid) + '\"')

    def _get_device(self, query):
        device = self._fetch_one('SELECT * FROM device WHERE ' + query)
        if device is not None:
            device = self._process_data(device)
            return device
        else:
            return None

    def get_device_name(self, deviceId):
        device = self.get_device_by_id(deviceId)
        deviceName = device["deviceName"]
        return deviceName

    def _fetch(self, query):
        data = []
        conn = self._initialize_connection()
        cur = conn.cursor()
        cur.execute(query)
        columns = [column[0] for column in cur.description]
        for row in cur.fetchall():
            data.append(dict(zip(columns, row)))
        conn.close()
        return data

    def _fetch_column_list(self, query):
        conn = self._initialize_connection()
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        data = c.execute(query).fetchall()
        conn.close()
        return data

    def _fetch_one(self, query):
        conn = self._initialize_connection()
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchone()
        conn.close()
        return data

    def _update(self, query):
        conn = self._initialize_connection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()

    def _set_device_status(self, key, STATUS):
        device = self._get_device(key)
        if device is not None:
            version = device["version"]
            query = 'UPDATE device SET status=\"'\
                + STATUS + '\",version='\
                    + str(version + 1)\
                    + ',lastBorrowed=datetime(\"now\",\"localtime\")'\
                    + ' WHERE ' \
                    + str(key) \
                    + ' AND version=' + str(version)
            self._update(query)
        else:
            return "ERROR: No Device Found with such key."

    def _set_borrower_info(self, key,
                           ip,
                           hostname
                           ):
        device = self.get_device_by_id(key)
        query = 'UPDATE device SET borrowerIp=\"'\
            + str(ip) + '\"' + ', borrowerHostname=\"'\
                + str(hostname) + '\"'\
                + ' WHERE deviceId=' \
                + str(key)
        self._update(query)

    def _set_device_server(self,
                           deviceId,
                           udid,
                           server,
                           driverPath,
                           status='FREE'
                           ):
        query = 'UPDATE device SET server=\"' \
            + str(server) + '\",status=\"'\
                + str(status) + '\"'\
                + ',driverPath=\"' \
                + str(driverPath) + '\"' \
                + ' WHERE deviceId=' \
                + str(deviceId) \
                + ' AND deviceType=\"Real Device\"'
        self._update(query)

    def _process_data(self, rawData):
        keys = rawData.keys()
        index = 0
        data = {}
        for value in rawData:
            data.update({keys[index]: value})
            index += 1
        return data

    def borrow_device(self,
                      platformName,
                      forced,
                      platformVersion=None,
                      deviceId=None,
                      teamName=None,
                      borrowerIp=None,
                      borrowerHostname=None,
                      deviceType=None
                      ):
        if deviceId is not None:
            device = self.get_device_by_id(deviceId)
            if device is not None \
                    and device['status'] != 'UNPLUGGED'\
                    and forced:
                return device
            else:
                device = None
        else:
            query = 'SELECT * FROM device WHERE platformName=\"'\
                + platformName + '\" '
            if teamName is not None:
                query += 'AND teamName IN (\"'\
                    + str(teamName) + '\",\"\")'
            if deviceType is not None:
                query += 'AND deviceType=\"'\
                    + str(deviceType) + '\"'
            allowed = '("FREE","ACTIVE")' if forced else '("FREE")'
            query += (' AND STATUS IN ' + allowed
                      + ' ORDER BY RANDOM() LIMIT 1'
                      )
            device = self._fetch_one(query)
        if device == [] or device is None:
            return "No device available."
        else:
            key = device["deviceId"]
            self._set_device_status(('deviceId=\"' + str(key) + '\"'), "ACTIVE")
            if (borrowerIp is not None) and \
                    (borrowerHostname is not None):
                self._set_borrower_info(key, borrowerIp, borrowerHostname)
            device = self.get_device_by_id(key)
            return device

    def return_device(self, deviceId):
        device = self.get_device_by_id(deviceId)
        if device["status"] not in ['UNPLUGGED', 'FREE', 'DISABLED']:
            self._set_device_status(('deviceId=' + str(deviceId)), 'FREE')
            return "Device Returned."
        else:
            return "Operation Error: Device is already FREE or UNPLUGGED."
