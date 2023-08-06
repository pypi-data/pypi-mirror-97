# -*- coding: utf-8 -*-

# Copyright (C) 2020 Spiralworks Technologies Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#  _     _ _       _             _______ _  _
# (_)   | (_)  _  (_)           (_______) |(_)             _
#  _____| |_ _| |_ _  ____ _____ _      | | _ _____ ____ _| |_
# |  _   _) (_   _) |/ ___|____ | |     | || | ___ |  _ (_   _)
# | |  \ \| | | |_| ( (___/ ___ | |_____| || | ____| | | || |_
# |_|   \_)_|  \__)_|\____)_____|\______)\_)_|_____)_| |_| \__)
# kitica Client
# Created by    : Joshua Kim Rivera
# Date          : September 22 2020 19:52 UTC-8
# Company       : Spiralworks Technologies Inc.
#
from pathlib import Path
from os.path import join


class Constants():
    """
    Constant Variables.
    """
    ADB_START = 'Starting Android Host Client Listener Service'
    IOS_START = 'Starting iOS Host Client Listener Service'
    ADB_STOP = 'Stopping Android Host Client Listener Service'
    IOS_STOP = 'Stopping iOS Host Client Listener Service'
    NO_DEVICE = 'No Connected Device.'
    KITICA_SERVER = 'http://localhost:5000'
    KITICA_CLIENT_HOME = join(str(Path.home()), 'kitica', 'client')
    KITICA_CLIENT_WEBDRIVERS = join(KITICA_CLIENT_HOME, 'webdrivers')
    STATUS = {'FREE': '\u001b[32mFREE\u001b[0m',
              'UNPLUGGED': '\u001b[31mUNPLUGGED\u001b[0m'
              }
