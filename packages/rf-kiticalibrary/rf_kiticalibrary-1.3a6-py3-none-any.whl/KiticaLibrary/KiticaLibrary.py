# -*- coding: utf-8 -*-

# Copyright (C) 2019 Spiralworks Technologies Inc.

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
#  _     _       _             _  _ _
# | |   (_)  _  (_)           | |(_) |
# | |  _ _ _| |_ _  ____ _____| | _| |__   ____ _____  ____ _   _
# | |_/ ) (_   _) |/ ___|____ | || |  _ \ / ___|____ |/ ___) | | |
# |  _ (| | | |_| ( (___/ ___ | || | |_) ) |   / ___ | |   | |_| |
# |_| \_)_|  \__)_|\____)_____|\_)_|____/|_|   \_____|_|    \__  |
#                                                          (____/
# kitica DevicePool API
# Created by    : Joshua Kim Rivera
# Date          : February 4 2020 14:55 UTC-8
# Company       : Spiralworks Technologies Inc.
#
import re
import requests
import logging
import json
import socket
from os import environ

from KiticaLibrary.version import VERSION
from KiticaLibrary.errors import DeviceBorrowError

from robotlibcore import (HybridCore,
                          keyword)

__version__ = VERSION

LOGGER = logging.getLogger(__name__)


class KiticaLibrary(HybridCore):
    """
    A test library providing device pool support for testing.

        ``KiticaLibrary`` is a Robot Framework third party library that \
        enables test to borrow available user from a device pool. These \
        allows test to run in CI server without device conflict and \
        lessen setup and maintenance on a project.

        - borrowing an available device from the devicepool and returning it.
        - retrieving a device from the devicepool by `deviceId`

        ``KiticaLibrary`` is part of the ``kitica`` project and is built to
        provide support devicepool setup for running tests in RobotFramework
        setup.

        ``kitica`` is a devicepool project written in Python that provides
        RESTful API service, Host Client Listener for both iOS and Android
        and aims to support local device farm setups.

        == Table of contents ==

        - `Usage`
        - `Borrowed Device Object Values`
        - `Author`
        - `Importing`
        - `Shortcuts`
        - `Keywords`

    = Usage =

    == Adding this Library to your Test Suite ==

    | =Settings= | =Value=         | =Parameter=                        |
    | Library    | KiticaLibrary   | base_url                           |

    You can import this library in your robot test suite by using the   \
        syntax below.
    For the parameters on import. Read `Importing`.

    *Example:*
    | =Settings= | =Value=         | =Parameter=                        |
    | Library    | UserpoolLibrary | http://kitica.dev                  |

    `Borrow Device`, `Borrow Android Device` and `Borrow iOS Device`    \
    returns a json object containing the following information:

    *JSON Representation:*
    | {
    |     "deviceId": 1,
    |     "deviceName": "Samsung Galaxy S20 Ultra",
    |     "platformName": "Android",
    |     "server": "192.168.xxx.xxx:4723/wd/hub",
    |     "systemPort": "4725/wd/hub",
    |     "udid": "xxxxxxx",
    |     "platformVersion": "10",
    |     "status": "FREE",
    |     "teamName": "CMS",
    |     "version": 1,
    |     "borrowerIp": "192.168.xxx.xxx",
    |     "borrowerHostname": "joshuarivera[User-Borrowed]",
    |     "lastBorrowed": "2020-02-04 18:33:31",
    |     "deviceType": "Real Device",
    |     "driverPath": "/path/to/webdriver"
    | }
    See `Borrowed Device Object Values` for the values decription.

    = Borrowed Device Object Values =

    == deviceId ==
    The unique integer value that is tagged to a specific device, could be used
    as parameter in `Borrow Device` Keyword to target a specific device.

    Could be used together with the `forced` argument to force the service to
    provide the device even when the device's ``status`` is ``ACTIVE``
    but not ``UNPLUGGED``.

    == deviceName ==
    The name of the device borrowed. When Running Appium XCUITEST in real iOS
    devices, this value is required.

    == platformName ==
    Denotes the platform of the device, should only be either ``Android``
    or ``iOS``.

    == server ==
    The device farm host the returned device is connected to.

    == systemPort ==
    systemPort used to connect to appium-uiautomator2-server or
    appium-espresso-driver. The default is 8200 in general and selects one
    port from 8200 to 8299 for appium-uiautomator2-server, it is 8300 from
    8300 to 8399 for appium-espresso-driver. When you run tests in parallel,
    you must adjust the port to avoid conflicts. Read Parallel Testing Setup
    Guide for more details.

    == mjpegServerPort ==
    Must be in range 1024..65535. 7810 by default

    == udid ==
    The device's unique Identification, at least for real devices, for AVD
    emulated devices uses the pattern ``emulator-xxxx`` as its `udid` value.

    == platformVersion ==
    The version of the platform of the borrowed device.

    == status ==
    Denotes the status of the device returned by the kitica API service.

    == teamName ==
    The team owner of the device, will be bypassed when `Borrow Device` is
    provided by ``forced==true`` and ``deviceId`` parameter.

    == version ==
    iterates whenever the device field is updated.

    == borrowerIp ==
    Stores the value of the latest borrower of the device.

    == borrowerHostname ==
    Stores the hostname of the latest borrower of the device.

    == lastBorrowed ==
    Logs the date and time the device was last borrowed.

    == deviceType ==
    Indicates whether the returned device is either a `Real Device` or an
    `Emulator`.

    == driverpath ==
    The resolvable PATH of the device host server the device is connected to.


    = Author =

    Created: February 4 2020 14:55 UTC-8

    Author: Joshua Kim Rivera | email:joshua.rivera@mnltechnology.com

    Company: Spiralworks Technologies Inc.

    = Contributor(s) =

    Shiela Buitizon | email: shiela.buitizon@mnltechnology.com

    Company: Spiralworks Technologies Inc.

    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, base_url=None):
        """
        Sets the kitica server to connect to.
        """
        libraries = []
        HybridCore.__init__(self, libraries)
        self.base_url = base_url
        if base_url is not None:
            self.device_url = base_url + '/devices'
            self.device_lending = base_url + '/device/lending'
            self.device_utils = base_url + '/device/utils'
        self.machineHostName = self._append_test_trigger_category()
        self.machineIp = self._get_machine_ip()

    @keyword
    def borrow_android_device(self,
                              platformVersion=None,
                              teamName='',
                              ):
        """ Borrows an Android Device with a status of ``FREE``.

        Accepts `platformVersion` as parameter.

        `Borrow Android Device` is just a wrapper keyword for
        `Borrow Device`, if more complicated approach to
        borrowing is needed, use `Borrow Device` instead.

        == Example ==
        | ${device} | `Borrow Android Device`   |                   |
        | ${device} | `Borrow Android Device`   | platformVersion=9 |
        """
        device = self.borrow_device('Android',
                                    platformVersion,
                                    teamName)
        return device

    @keyword
    def borrow_ios_device(self,
                          platformVersion=None,
                          teamName='',
                          ):
        """ Borrows an iOS Device with a status of ``FREE``.

        Accepts `platformVersion` as parameter.

        `Borrow iOS Device` is just a wrapper keyword for
        `Borrow Device`, if more complicated approach to
        borrowing is needed, use `Borrow Device` instead.

        == Example ==
        | ${device} | `Borrow iOS Device`   |                       |
        | ${device} | `Borrow iOS Device`   | platformVersion=13.3  |
        """
        device = self.borrow_device('iOS',
                                    platformVersion,
                                    teamName)
        return device

    @keyword
    def return_device(self, device):
        if device:
            return self._free_device(device['deviceId'])
        raise TypeError('Cannot Return Nonetype Device')

    @keyword
    def borrow_device(self,
                      platformName='Android',
                      teamName="",
                      forced=False,
                      platformVersion=None,
                      deviceId=None,
                      deviceType=None
                      ):
        """Borrows Device in the devicepool.

        Takes `platformName, `teamName, `forced, `platformVersion,
        ``deviceId``
        as parameters.
        | =param=           | =type=    | =description=                     |
        | `platformName`    | String    | Indicates what platform the       \
                                          deviceto be borrowed will be.     \
                                          Should be either ``Android`` or   \
                                          ``iOS``, case-sensitive. Defaults \
                                          to ``Android`` when no value is   \
                                          provided. Ignored when            \
                                          ``deviceId`` value is provided.   |
        | `teamName`        | String    | Indicates to which teamName       \
                                          will the devices should belong    \
                                          to. Ignored when ``deviceId``     \
                                          value is provided                 |
        | forced            | Boolean   | Sets the borrow mode. If set to   \
                                          True and ``deviceId`` is          \
                                          provided, ignores the status when \
                                          ACTIVE, but not UNPLUGGED. If     \
                                          ``deviceId`` is not provided,     \
                                          will pull any device from the     \
                                          device pool with status value of  \
                                          FREE or ACTIVE.                   |
        | `platformVersion` | String    | Indicates the platformVersion of  \
                                          the device to be borrowed.        |
        | `deviceId`        | Int       | Indicates the device to be        \
                                          borrowed by the ``deviceId``      \
                                          value. Will fail if forced is set \
                                          to False and target device has a  \
                                          status of ACTIVE. Ignores         \
                                          device's ACTIVE status if forced  \
                                          is set True but not UNPLUGGED.    \
                                          Borrow device will ignore all     \
                                          parameters except for forced      \
                                          when this is passed.              |

        == Example ==

        === Borrowing an Android Device ===
        | ${device}     | `Borrow Device`   |                               |
        | ${device}     | `Borrow Device`   | platformName=Android          |
        Both example will produce the same result since ``platformName``
        will default to ``Android`` when no value is provided.

        === Borrowing an iOS Device ===
        | ${device}     | `Borrow Device`   | platformName=iOS              |
        Note that ``iOS`` parameter is case sensitive.

        === Borrowing Device with specific platformVersion ===
        | ${device}     | `Borrow Device`   | platformName=Android  \
                                            | platformVersion=9     |
        | ${device}     | `Borrow Device`   | platformVersion=iOS   \
                                            | platformVersion=13.3  |
        When ``platformVersion`` is omitted as an argument, the service will
        try to search for the specific version, but, if no device with such
        version is found, kitica API will return None.

        === Borrowing a Device using deviceId ===
        | ${device}     | `Borrow Device`   | deviceId=1            |
        The service will return the specific device if and only if the
        specified device's status is ``FREE``. Will raise a
        ``DeviceBorrowError`` if the device specified is ``ACTIVE`` or
        ``UNPLUGGED``.

        === NOTE ===
         - When ``deviceId`` is provided all other arguments provided is\
         ignored except for ``forced``.

        === Borrowing a device using deviceID with forced set to True ===
        | ${device}     | `Borrow Device`   | deviceID=1            \
                                            | forced=True           |
        When borrowing a device with forced set to ``True``, the service will
        return the specified device even when it's current status is
        ``ACTIVE``, but not when it is ``UNPLUGGED``.

        ``forced`` is only implemented when ``deviceId`` is specified and will
        be ignored when ``deviceId`` is not provided.
        """
        params = {'platformName': platformName,
                  'borrowerIp': self.machineIp,
                  'borrowerHostname': self.machineHostName,
                  'teamName': teamName,
                  'forced': forced
                  }
        if deviceId is not None:
            params.update({'deviceId': deviceId})
        if deviceType is not None:
            params.update({'deviceType': deviceType})
        else:
            if platformVersion is not None:
                params.update({'platformVersion': platformVersion})
        response = self._get_request(self.device_lending, params)
        device = response.json()

        if bool(response):
            if deviceId is not None and forced \
                    and device == 'No device available.':
                raise DeviceBorrowError('Device is UNPLUGGED.')
            else:
                return device
        return None

    def _free_device(self, deviceId):
        try:
            response = self._post_request(self.device_lending,
                                          params={'deviceId': int(deviceId)}
                                          )
            return response
        except Exception as err:
            raise err

    def _get_request(self, url, params):
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response

    def _post_request(self, url, params):
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response

    def _get_machine_hostname(self):
        """Uses python 3 socket library to get the machine IP and hostname.
        """
        try:
            hostName = socket.gethostname()
            return hostName
        except Exception as err:
            raise err

    def _append_test_trigger_category(self):
        """Appends test trigger category to machine hostname.
        """
        if environ.get('CI_RUNNER_DESCRIPTION') is not None:
            hostName = environ.get('CI_RUNNER_DESCRIPTION')
        else:
            hostName = self._get_machine_hostname()
        return hostName[:50] if len(hostName) > 50 else hostName

    def _get_machine_ip(self, hostName=None):
        """Uses python 3 socket library to obtain machine IP Address.
        Takes machine hostName as parameter
        """
        try:
            hostIp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            hostIp.connect(("8.8.8.8", 80))
            return hostIp.getsockname()[0]
        except Exception as err:
            raise err
