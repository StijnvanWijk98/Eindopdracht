from Constants import *
from random import random, randint
from Sensors import I2CBusMock, GarminLidarLiteV3, SpeedSensor
import actuators
from time import time
from Controller import Controller

class Environment:
  def __init__(self, i2c_bus, lidar, speed_sensor, throttle, brakes):
    self.car_speed = startSpeed
    self.car_distance_ahead = startDistance
    self.car_wheel_circumference = round((car_diameter_wheel * PI / 100), 2)
    self.throttle = throttle
    self.brakes = brakes
    self.i2c_bus = i2c_bus
    self.lidar = lidar
    self.speed_sensor = speed_sensor
    self.last_time_speed = time()

  def updateI2CDistance(self):
    """
    Updates the I2C distance by writing the high and low bytes of the car distance ahead to the I2C bus.
    """
    distance_h = (self.car_distance_ahead >> 8) & 0xFF
    distance_l = self.car_distance_ahead & 0xFF
    self.i2c_bus.write(GARMIN_I2C_ADDRESS, DISTANCE_REGISTER_H, distance_h)
    self.i2c_bus.write(GARMIN_I2C_ADDRESS, DISTANCE_REGISTER_L, distance_l)

  def updateSpeedSensor(self):
    """
    Updates the speed sensor count based on the current car speed.

    This method calculates the new count for the speed sensor based on the current car speed and the time elapsed since the last update.
    It converts the car speed from kilometers per hour to meters per second, and then calculates the distance traveled by the car wheel in that time.
    The new count is then set on the speed sensor, and the last update time is updated.
    """
    current_time = time()
    delta_time = current_time - self.last_time_speed
    speed_m_s = self.car_speed / 3.6
    new_count = (speed_m_s / self.car_wheel_circumference) * delta_time
    self.speed_sensor.set_count(new_count)
    self.last_time_speed = current_time

  def updateDistance(self):
    """
    Updates the distance ahead of the car based on the current state of the brakes and car speed.

    If the brakes are active, the distance ahead increases by a fixed value (distAheadWhenBraking).
    How higher the car speed there is a higher chance for the distance ahead to change randomly within a range (distAheadChanceMin to distAheadChanceMax).
    """
    if self.brakes.get_state():
      self.car_distance_ahead += distAheadWhenBraking
    elif random() < (self.car_speed / distAheadChanging):
      self.car_distance_ahead += randint(distAheadChanceMin, distAheadChanceMax)
  
  def updateSpeed(self):
    """
    Updates the speed of the car based on the state of the brakes and throttle.

    If the brakes are engaged, the car speed is decreased based on the pressure applied.
    If the throttle is engaged, the car speed is increased based on the position of the throttle.
    The car speed is then reduced by the resistance caused by the car.
    The car speed is clamped to a minimum of 0 and rounded.
    """
    if self.brakes.get_state():
      print('Braking', self.brakes.get_pressure())
      self.car_speed -= maxBraking * (self.brakes.get_pressure() / 100)
    elif self.throttle.get_state():
      print('Accelerating', self.throttle.get_position())
      self.car_speed += maxAcceleration * (self.throttle.get_position() / 100)
    self.car_speed -= carResistance
    self.car_speed = round(max(0, self.car_speed), 2)

  def update(self):
    self.updateDistance()
    self.updateSpeed()
    self.updateI2CDistance()
    self.updateSpeedSensor()

class Simulator:
  def __init__(self):
    self.i2c_bus = I2CBusMock({GARMIN_I2C_ADDRESS: {DISTANCE_REGISTER_H: 0, DISTANCE_REGISTER_L: 0}})
    self.lidar = GarminLidarLiteV3(self.i2c_bus, GARMIN_I2C_ADDRESS)
    self.speed_sensor = SpeedSensor(car_diameter_wheel)
    self.throttle = actuators.ThrottleActuator()
    self.brakes = actuators.BrakeActuator()
    self.env = Environment(self.i2c_bus, self.lidar, self.speed_sensor, self.throttle, self.brakes)
    self.controller = Controller(self.lidar, self.speed_sensor, self.throttle, self.brakes)
    self.ticks = 0

  def run(self):
    while True:
      print("======= {} =======".format(self.ticks))
      self.env.update()
      self.controller.update()
      print(f"Distance ahead: {self.env.car_distance_ahead} cm")
      print(f"Speed: {self.env.car_speed} km/h")
      print("Controller | Throttle {}, brakes {}".format(self.controller.cur_throttle_position, self.controller.cur_brake_pressure))
      print("Actuators | Throttle {}, brakes {}".format(self.throttle.get_position(), self.brakes.get_pressure()))
      input("Press any key to continue")
      self.ticks += 1

if __name__ == "__main__":
  sim = Simulator()
  sim.run()