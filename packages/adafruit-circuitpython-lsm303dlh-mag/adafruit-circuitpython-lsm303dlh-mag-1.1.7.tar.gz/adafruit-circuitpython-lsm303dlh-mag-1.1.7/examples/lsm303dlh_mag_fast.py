# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Read data from the magnetometer and print it out, ASAP! """

import board
import busio
import adafruit_lsm303dlh_mag

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

while True:
    mag_x, mag_y, mag_z = sensor.magnetic
    print("{0:10.3f} {1:10.3f} {2:10.3f}".format(mag_x, mag_y, mag_z))
