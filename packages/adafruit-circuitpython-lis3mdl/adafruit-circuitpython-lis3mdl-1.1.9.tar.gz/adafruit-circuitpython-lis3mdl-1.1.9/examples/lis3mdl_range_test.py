# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Test Each range """
# pylint: disable=no-member
import time
import board
import busio
from adafruit_lis3mdl import LIS3MDL, Range

i2c = busio.I2C(board.SCL, board.SDA)
sensor = LIS3MDL(i2c)

while True:

    for mag_range in [
        Range.RANGE_4_GAUSS,
        Range.RANGE_8_GAUSS,
        Range.RANGE_12_GAUSS,
        Range.RANGE_16_GAUSS,
    ]:
        sensor.range = mag_range
        print("Range: %d Gauss" % Range.string[sensor.range])
        mag_x, mag_y, mag_z = sensor.magnetic

        print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))
        print("")
        time.sleep(0.3)
