# -*- coding: utf-8 -*-
#  _     _       _
# | |   (_)  _  (_)
# | |  _ _ _| |_ _  ____ _____
# | |_/ ) (_   _) |/ ___|____ |
# |  _ (| | | |_| ( (___/ ___ |
# |_| \_)_|  \__)_|\____)_____|
#
#            _ _           _  _
#           | | |         | |(_)             _
#  _____  __| | |__   ____| | _ _____ ____ _| |_
# (____ |/ _  |  _ \ / ___) || | ___ |  _ (_   _)
# / ___ ( (_| | |_) | (___| || | ____| | | || |_
# \_____|\____|____/ \____)\_)_|_____)_| |_| \__)
#
# kitica Android Host Client
# Created by    : Joshua Kim Rivera
# Date          : February 7 2020 23:11 UTC-8
# Company       : Spiralworks Technologies Inc.
#
import time
from ppadb.client import Client
from KiticaClient.base import BaseClient


class AdbClient(BaseClient):
    """ Kitica Android Hosts Listener Client

        Kitica's Android ADB Listener.

        Listens to the ADB server for device changes.

        Methods
        ------

        initialize_connection
            Creates a connection between the listener client
            and the target adb server.
    """

    def __init__(self, kiticaUri, hostIP=None):
        """
        """
        super().__init__(kiticaUri, hostIP)

    def initialize_connection(self,
                              host='localhost',
                              port=5037
                              ):
        """Create a new ADB connection to the specified host.

        Connects to the host's port.

        Fetches all the device connected upon successful handshake.

        Parameters
        ------

        host: str
            The adb host to connect to. Defaults to localhost.
        port: int
            The adb port of the host. Defaults to 5037
        """
        self.host = host
        self.port = port
        session = Client(self.host, self.port)
        self.session = session
        self.devicesConnected = self._fetch_device()

    def _fetch_device(self):
        pool = []
        devices = self.session.devices()
        for device in devices:
            pool.append(device.serial)
        return pool
