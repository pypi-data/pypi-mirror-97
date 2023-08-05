# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.consumer_control.ConsumerControl`
====================================================

* Author(s): Dan Halbert
"""

import sys

if sys.implementation.version[0] < 3:
    raise ImportError(
        "{0} is not supported in CircuitPython 2.x or lower".format(__name__)
    )

# pylint: disable=wrong-import-position
import struct
import time
from . import find_device


class ConsumerControl:
    """Send ConsumerControl code reports, used by multimedia keyboards, remote controls, etc."""

    def __init__(self, devices):
        """Create a ConsumerControl object that will send Consumer Control Device HID reports.

        Devices can be a list of devices that includes a Consumer Control device or a CC device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._consumer_device = find_device(devices, usage_page=0x0C, usage=0x01)

        # Reuse this bytearray to send consumer reports.
        self._report = bytearray(2)

        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.send(0x0)
        except OSError:
            time.sleep(1)
            self.send(0x0)

    def send(self, consumer_code):
        """Send a report to do the specified consumer control action,
        and then stop the action (so it will not repeat).

        :param consumer_code: a 16-bit consumer control code.

        Examples::

            from adafruit_hid.consumer_control_code import ConsumerControlCode

            # Raise volume.
            consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)

            # Advance to next track (song).
            consumer_control.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        """
        struct.pack_into("<H", self._report, 0, consumer_code)
        self._consumer_device.send_report(self._report)
        self._report[0] = self._report[1] = 0x0
        self._consumer_device.send_report(self._report)
