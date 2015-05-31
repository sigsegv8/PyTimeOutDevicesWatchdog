"""Module to describe remote computer watchdog device
"""

import os
import serial

class TimeoutDevice2400:
    """Class to describe the watchdog TimeOut(c) device"""
    def __send_and_ignore(self, char):
        self.sp.write("%s\r" % char)
        self.sp.read(3)  # The switch always respond with 2 char and \r

    def __init__(self, serialPort):
        self.sp = serial.Serial(serialPort, baudrate=2400, bytesize=8, parity=serial.PARITY_NONE, stopbits=1)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.sp.close()

    def off(self):
        """Tell watchdog to turn off host device

        Args:
          nothing
        Returns:
          nothing
        Raises:
          nothing
        """
        # calibration
        self.__send_and_ignore('c')

        # disable off cycle (switch will stay off until it's told otherwise)
        self.__send_and_ignore('f01')

        # kick off off cycle (infinite)
        self.__send_and_ignore('w')

    def on(self):
        """Tell watchdog to turn on host device

        Args:
          nothing
        Returns:
          nothing
        Raises:
          nothing
        """
        # calibration
        self.__send_and_ignore('c')

        # disable on cycle (switch will stay on until it's told otherwise)
        self.__send_and_ignore('e01')

        # kick off off cycle (infinite)
        self.__send_and_ignore('y')

    def reset(self):
        """Tell watchdog to power cycle host device

        Args:
          nothing
        Returns:
          nothing
        Raises:
          nothing
          nothing
        """
        # calibration
        self.__send_and_ignore('c')

        # set off cycle hours
        self.__send_and_ignore('j00')

        # set off cycle minutes
        self.__send_and_ignore('o00')

        # set off cycle seconds
        self.__send_and_ignore('u10')

        # disable on cycle (switch will stay on until it's told otherwise)
        self.__send_and_ignore('e01')

        # enable off cycle
        self.__send_and_ignore('f00')

        # kick off reset
        self.__send_and_ignore('w')
