from influxdb import InfluxDBClient
from libra_core import *


class InfluxDBClinet(object):

    def __init__(self, host, port, username, password, database, timeout=3):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self._timeout = timeout
        self._connected = False
        self._connect()

    def _connect(self):
        if not self._connected:
            try:
                self._influx_client = InfluxDBClient(host=self._host, 
                                                    port=self._port, 
                                                    username=self._username,
                                                    database=self._database,
                                                    timeout=self._timeout)
                self._connected = True
            except Exception as e:
                log_error('Fail to connect {}:{} influxdb error msg({})'.format(self._host,
                                                                                self._port, e))
                self._connected = False
        return self._connected

    def query(self, sql_str):
        while not self._connect():
            sleep(0.1)
        items = []
        for item in self._influx_client.query(query=sql_str):
            items.append(item)
        if len(items):
            return items[0]
        return []
