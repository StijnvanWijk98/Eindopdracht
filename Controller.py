from Sensors import GarminLidarLiteV3, SpeedSensor
import actuators
from Constants import desiredDistance, desiredSpeed, \
                      brakeDistSensitive, brakeSpeedSensitive, \
                      throttleDistSensitive, throttleSpeedSensitive, \
                      throttleError, throttleErrorCorrection

class Controller:
  def __init__(self, dist_sensor: GarminLidarLiteV3, speed_sensor : SpeedSensor, throttle, brakes):
    self.dist_sensor = dist_sensor
    self.speed_sensor = speed_sensor
    self.throttle = throttle
    self.brakes = brakes
    self.desired_speed = desiredSpeed
    self.desired_distance = desiredDistance
    self.cur_throttle_position = 0
    self.cur_brake_pressure = 0
    self.set_throttle(0)
    self.set_brakes(0)
  
  def set_desired_speed(self, speed):
    self.desired_speed = speed

  def set_desired_distance(self, distance):
    self.desired_distance = distance

  def calculate_diff_dist(self, cur_dist):
    if cur_dist < 0:
      return -10
    return cur_dist - self.desired_distance
  
  def calculate_diff_speed(self, cur_speed):
    return cur_speed - self.desired_speed

  def set_throttle(self, throttle):
    self.throttle.set_position(throttle)
    self.cur_throttle_position = throttle

  def set_brakes(self, brakes):
    self.brakes.set_pressure(brakes)
    self.cur_brake_pressure = brakes

  def calculate_brake_pressure(self, cur_speed, diff_dist) -> int:
    # Diff dist is negative so *-1 to make it positive for the calculation
    cur_brake_pressure = self.brakes.get_pressure()
    n_brake_pressure = cur_brake_pressure + ((diff_dist * -1 * brakeDistSensitive) + cur_speed * brakeSpeedSensitive)
    return int(min(n_brake_pressure, 100))

  def calculate_throttle_position(self, diff_speed, cur_dist) -> int:
    # Diff speed is negative so *-1 to make it positive for the calculation
    cur_throttle_position = self.throttle.get_position()
    n_throttle_position = cur_throttle_position + ((diff_speed * -1 * throttleSpeedSensitive)  + cur_dist * throttleDistSensitive)
    return int(min(n_throttle_position, 100))

  def update(self):
    cur_dist = self.dist_sensor.get_distance_cm()
    diff_dist = self.calculate_diff_dist(cur_dist)
    cur_speed = self.speed_sensor.get_speed()
    diff_speed = self.calculate_diff_speed(cur_speed)
    print("diff_dist: ", diff_dist, "diff_speed: ", diff_speed)
    if(diff_dist < 0): # Car is to close to the car in front
      self.set_throttle(0)
      n_pres = self.calculate_brake_pressure(cur_speed, diff_dist)
      self.set_brakes(n_pres)
    elif(diff_speed < 0): # Car is going to slow and has enough distance
      self.set_brakes(0)
      n_pos = self.calculate_throttle_position(diff_speed, cur_dist)
      self.set_throttle(n_pos)
    elif(diff_speed > throttleError): # Car is going to fast so decrease throttle so it slows down
      self.cur_throttle_position -= throttleErrorCorrection
      self.cur_throttle_position = max(0, self.cur_throttle_position)
      self.throttle.set_position(self.cur_throttle_position)
    
    
