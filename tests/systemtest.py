import unittest
from sys import path
from time import time

path.append("C:\\Users\StijnvanWijk\Documents\Projects\Python\ATP\Eindopdracht")

from time import sleep
from Sensors import GarminLidarLiteV3, I2CBusMock, SpeedSensor
import actuators
from Controller import Controller
from Constants import DISTANCE_REGISTER_H, DISTANCE_REGISTER_L, GARMIN_I2C_ADDRESS, car_diameter_wheel

class ControllerTest(unittest.TestCase):
  def setUp(self):
    self.i2c_bus = I2CBusMock({GARMIN_I2C_ADDRESS: {DISTANCE_REGISTER_H: 100, DISTANCE_REGISTER_L: 255}})
    self.lidar = GarminLidarLiteV3(self.i2c_bus, GARMIN_I2C_ADDRESS)
    self.speed_sensor = SpeedSensor(car_diameter_wheel)
    self.throttle = actuators.ThrottleActuator()
    self.brakes = actuators.BrakeActuator()
    self.controller = Controller(self.lidar, self.speed_sensor, self.throttle, self.brakes)
  
  def testSystem(self):
    self.controller.update()
    self.assertEqual(self.controller.cur_brake_pressure, 0)
    self.assertGreater(self.controller.cur_throttle_position, 0)

if __name__ == "__main__":
  unittest.main()