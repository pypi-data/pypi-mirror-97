# -*- coding: utf-8 -*-
#  _     _       _
# | |   (_)  _  (_)
# | |  _ _ _| |_ _  ____ _____
# | |_/ ) (_   _) |/ ___|____ |
# |  _ (| | | |_| ( (___/ ___ |
# |_| \_)_|  \__)_|\____)_____|
#
#  ______                   _______ _  _
# (____  \                 (_______) |(_)             _
#  ____)  )_____  ___ _____ _      | | _ _____ ____ _| |_
# |  __  ((____ |/___) ___ | |     | || | ___ |  _ (_   _)
# | |__)  ) ___ |___ | ____| |_____| || | ____| | | || |_
# |______/\_____(___/|_____)\______)\_)_|_____)_| |_| \__)
#
# kitica base Client
# Created by    : Joshua Kim Rivera
# Date          : February 10 2020 13:14 UTC-8
# Company       : Spiralworks Technologies Inc.
#
import requests
import socket
import sys
from KiticaClient.version import VERSION
from pathlib import Path
from os import environ
from KiticaClient.common import Constants, Logger


class BaseClient(Logger, Constants):
    """
    """
    def __init__(self, kiticaUri, hostIP=None):
        """Kitica Base Client Class.
        All Client Instance Should Inherit from this Class.
        """
        self.log('Kitica Client Instance v' + VERSION)
        self._create_kitica_home()
        self._create_webdriver_home()
        self.hostIP = hostIP if hostIP is not None else str(self._get_host_ip())
        self.devicesConnected = None
        self.devices = None
        self.kitica_url = str(kiticaUri + '/hosts/listener')
        self.kitica_hosts = str(kiticaUri + '/device/utils')
        self.driverPath = self.KITICA_CLIENT_WEBDRIVERS
        self.log('Host: \u001b[4m' + self.hostIP + '\u001b[0m')
        self.log('Server: \u001b[4m' + str(kiticaUri) + '\u001b[0m')
        self.log('Webdrivers: \u001b[4m' + str(self.driverPath) + '\u001b[0m')

    def _report(self, setData, status):
        params = {}
        devicesEnrolled = self._fetch_devices_enrolled()
        devicesEnrolled = [udid['udid'] for udid in devicesEnrolled]
        if devicesEnrolled == []:
            self.warn('No Devices Affiliated for Host-{ip}'.format(ip=self.hostIP))
        for device in setData:
            if device in devicesEnrolled:
                self.info('Found Affiliated Device ' + str(device)
                          + ' with status ' + Constants.STATUS[status])
                params = {'udid': device,
                          'status': status,
                          'server': self.hostIP
                          }
                self._send(params)
            else:
                self.info('Found Non-Affiliated Device ' + str(device)
                          + ' with status ' + str(status))
                self._grab_device(device,
                                  status
                                  )

    def _get_host_ip(self, hostName=None):
        """Uses python 3 socket library to obtain machine IP Address.
        Takes machine hostName as parameter
        """
        try:
            hostIp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            hostIp.connect(("8.8.8.8", 80))
            return hostIp.getsockname()[0]
        except Exception as err:
            raise err

    def _send(self, params):
        response = requests.post(self.kitica_url, json=params)
        response.raise_for_status()
        return response

    def _grab_device(self, udid, status):
        params = {'server': str(self.hostIP),
                  'udid': udid,
                  'status': status,
                  'driverPath': self.driverPath
                  }
        response = requests.patch(self.kitica_hosts, json=params)
        response.raise_for_status()
        return response

    def _fetch_devices_enrolled(self):
        params = {'server': str(self.hostIP)}
        response = requests.get(self.kitica_hosts, json=params)
        response.raise_for_status()
        return response.json()

    def update(self):
        """Updates all the device's status affiliated with the host.
        """
        devices = self._fetch_devices_enrolled()
        devicesConnected = self._fetch_device()
        if devices == []:
            self.warn('No Devices Affiliated for Host-{ip}'.format(ip=self.hostIP))
        else:
            self.info(str(devicesConnected))
        for device in devices:
            if device['udid'] in devicesConnected:
                if device['server'] == '':
                    self._grab_device((device['udid']).split(), 'FREE')
                else:
                    self._report((device['udid']).split(), 'FREE')
            else:
                if device['server'] == '':
                    self._grab_device((device['udid']).split(), 'UNPLUGGED')
                else:
                    self._report((device['udid']).split(), 'UNPLUGGED')
        if devicesConnected == []:
            self.warn('No Connected Devices')

    def listen(self):
        """Base Listener Service Method

        """
        self.devices = self._fetch_device()
        if self.devicesConnected is not None:
            if self.devices != self.devicesConnected:
                if len(self.devices) > len(self.devicesConnected):
                    self.info('Device Plugged')
                    diff = set(self.devices).difference(self.devicesConnected)
                    self._report(diff, 'FREE')
                else:
                    self.warn('A Device was Unplugged')
                    diff = set(self.devicesConnected).difference(self.devices)
                    self._report(diff, 'UNPLUGGED')
                self.devicesConnected = self.devices
        else:
            self.devicesConnected = self._fetch_device()

    def stop(self):
        """Stops Client Service
        """
        self.log('Stopping Client Service')

    def _create_webdriver_home(self):
        """
        As per python sys module.
        The following are the potential values for sys.platform.
        | System           | platform value  |
        |------------------|-----------------|
        | AIX              | 'aix'           |
        | Linux            | 'linux'         |
        | Windows          | 'win32'         |
        | Windows/Cygwin   | 'cygwin'        |
        | macOS            | 'darwin'        |

        :return platform String
        """
        Path(self.KITICA_CLIENT_WEBDRIVERS).mkdir(parents=True, exist_ok=True)

    def _create_kitica_home(self):
        Path(self.KITICA_CLIENT_HOME).mkdir(parents=True, exist_ok=True)
