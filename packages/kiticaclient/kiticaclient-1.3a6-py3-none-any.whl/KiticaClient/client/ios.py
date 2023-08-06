# -*- coding: utf-8 -*-
#  _     _       _
# | |   (_)  _  (_)
# | |  _ _ _| |_ _  ____ _____
# | |_/ ) (_   _) |/ ___|____ |
# |  _ (| | | |_| ( (___/ ___ |
# |_| \_)_|  \__)_|\____)_____|
#  _ _______ ______ _______ _  _
# (_|_______) _____|_______) |(_)             _
#  _ _     ( (____  _      | | _ _____ ____ _| |_
# | | |   | \____ \| |     | || | ___ |  _ (_   _)
# | | |___| |____) ) |_____| || | ____| | | || |_
# |_|\_____(______/ \______)\_)_|_____)_| |_| \__)
#
# kitica Apple iOS Host Client
# Created by    : Joshua Kim Rivera
# Date          : February 10 2020 10:04 UTC-8
# Company       : Spiralworks Technologies Inc.
#
import time
import subprocess
from KiticaClient.base import BaseClient


class iOSClient(BaseClient):
    """Kitica iOS Listener Client Class

    Uses ios-deploy to fetch the list of connected devices.

    Methods
    ------

    initialize_devices
        Fetches all the current connected devices and stores it in the
        devicesConnected variable of the class.
    """
    def __init__(self, kiticaUri, hostIP=None):
        """
        """
        super().__init__(kiticaUri, hostIP)

    def initialize_devices(self):
        """Create a new ADB connection to the specified host.

        Connects to the host's port.

        Fetches all the device connected upon successful handshake.
        """
        self.devicesConnected = self._fetch_device()

    def _decode(self, devices):
        """Devices Parser

        Accepts the raw type byte devices as output from the
        ios-deploy command, uses the next line escape character
        as delimiter to split the string into a python list, then
        removes the '' character from the list.

        Parameters
        ------

        devices: byte
            The output obtained from the ios-deploy subprocess command.
        """
        pool = []
        decoded_str = devices.decode('UTF-8')
        pool = decoded_str.split('\n')
        pool.remove('')
        pool.sort()
        return pool

    def _fetch_device(self):
        devices = subprocess.check_output("ios-deploy -c | grep -oE "
                                          "'Found ([0-9A-Za-z\\-]+)' "
                                          "| sed 's/Found //g'",
                                          shell=True
                                          )
        try:
            simulators = subprocess.check_output("xcrun simctl list "
                                                 "| grep 'Booted' "
                                                 "| grep -oE '([0-9A-Za-z\\-]+)' "
                                                 "| grep -x '.\\{20,50\\}' ",
                                                 shell=True)
        except Exception:
            simulators = b''
        devices = self._decode(devices)
        simulators = self._decode(simulators)
        devices += simulators
        return devices
