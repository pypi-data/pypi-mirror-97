# -*- coding: utf-8 -*-

# Copyright (C) 2021 Spiralworks Technologies Inc.

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
# Date          : January 19 2021 20:22 UTC-8
# Company       : Spiralworks Technologies Inc.
#


class Logger():
    """
    Logger Methods.
    """
    def log(self, message, cat='Kitica'):
        """Kitica Client Logger Wrapper.
        """
        print('\u001b[36m[{cat}]\u001b[0m {message}'.format(cat=cat,
              message=message)
              )

    def info(self, message):
        """Kitica Client Logger Wrapper.
        """
        self.log('\t ' + message, 'Info')

    def warn(self, message):
        """
        """
        self.info('\u001b[33m{message}\u001b[0m'.format(message=message))

    def _log_header(self, length=74, char='='):
        """Logs Header in the console.
        """
        for i in range(0, length):
            print(char, end='')
        print('\n')
