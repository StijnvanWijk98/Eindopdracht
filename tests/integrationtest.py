import unittest
from sys import path
from time import time

path.append("C:\\Users\StijnvanWijk\Documents\Projects\Python\ATP\Eindopdracht")

from time import sleep
from Sensors import GarminLidarLiteV3, I2CBusMock
import actuators
from Constants import DISTANCE_REGISTER_H, DISTANCE_REGISTER_L, GARMIN_I2C_ADDRESS


def is_between(value, lower_bound, upper_bound):
    return lower_bound <= value <= upper_bound


class testDistanceIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.i2c_bus = I2CBusMock(
            {GARMIN_I2C_ADDRESS: {DISTANCE_REGISTER_H: 0, DISTANCE_REGISTER_L: 0}}
        )
        self.lidar = GarminLidarLiteV3(self.i2c_bus, GARMIN_I2C_ADDRESS)
        self.brakes = actuators.BrakeActuator()

    def test_distance_integration(self):
        self.i2c_bus.write(GARMIN_I2C_ADDRESS, DISTANCE_REGISTER_H, 0x00)
        self.i2c_bus.write(GARMIN_I2C_ADDRESS, DISTANCE_REGISTER_L, 0xFF)
        distance = self.lidar.get_distance_cm()

        if distance > 200:
            self.brakes.off()
            self.assertEqual(self.brakes.get_state(), False)
        else:
            self.brakes.on()
            self.assertEqual(self.brakes.get_state(), True)


if __name__ == "__main__":
    unittest.main()
