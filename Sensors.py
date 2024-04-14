from time import time, sleep
from Constants import LOG_LOCATION
from Decorator import log_func_execution_time
from Constants import (
    COMMAND_REGISTER,
    DISTANCE_REGISTER_H,
    DISTANCE_REGISTER_L,
    MEASURE,PI, LOG_LOCATION
)


class I2CBusMock:
    """
    Represents an I2C bus mock for communication with I2C devices.
    Attributes:
      data (dict): A dictionary representing the data stored in the I2C devices.

    Methods:
      write(address, register, value): Writes a value to the specified register of the device at the given address.
      read(address, register): Reads the value from the specified register of the device at the given address.
    """

    def __init__(self, data: dict = {}):
        self.data = data

    @log_func_execution_time(LOG_LOCATION)
    def write(self, address, register, value):
        self.data[address][register] = value

    @log_func_execution_time(LOG_LOCATION)
    def read(self, address, register):
        return self.data[address][register]


class GarminLidarLiteV3:
    """
    Represents the Garmin Lidar Lite V3 that communicates with an I2C bus.

    The sensor measures distance in centimeters. The sensor uses a different address for reading and writing data.
    The distance registers are updated by calling a measure command to the command register.

    Attributes:
      i2c_bus (I2CBus): An I2C bus object that the sensor is connected to.
      read_address (int): The I2C address used for reading data from the sensor.
      write_address (int): The I2C address used for writing data to the sensor.
    """
    def __init__(self, i2c_bus, i2c_address):
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address

    @log_func_execution_time(LOG_LOCATION)
    def get_distance_cm(self):
        self.i2c_bus.write(self.i2c_address, COMMAND_REGISTER, MEASURE)
        distance_h = self.i2c_bus.read(self.i2c_address, DISTANCE_REGISTER_H)
        distance_l = self.i2c_bus.read(self.i2c_address, DISTANCE_REGISTER_L)
        return (distance_h << 8) + distance_l


class SpeedSensor:
    def __init__(self, wheel_diameter_cm):
        self._count = 0
        self._last_time = time()
        self.set_wheel_circumference(wheel_diameter_cm)

    def set_wheel_circumference(self, wheel_diameter_cm):
        self._wheel_circumference_m = round((wheel_diameter_cm * PI / 100), 2)

    def set_count(self, count):
        self._count = count

    def interrupt(self):
        self._count += 1

    def get_speed(self):
        current_time = time()
        delta_time = max(current_time - self._last_time, 1)
        speed_m_s = self._wheel_circumference_m * (self._count / delta_time) 
        speed_formatted = speed_m_s * 3.6 # convert m/s to km/h
        self._count = 0
        self._last_time = current_time
        return speed_formatted