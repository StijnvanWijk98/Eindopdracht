LOG_LOCATION = "log.txt"


# Garmin Lidar Lite v3
# https://static.garmin.com/pumac/LIDAR_Lite_v3_Operation_Manual_and_Technical_Specifications.pdf
# I2C ADDRESSES
# The I2C address of the device is 0x62. The read address is 0xC4 and the write address is 0xC5.
GARMIN_I2C_ADDRESS = 0x62

# REGISTERS
COMMAND_REGISTER = 0x00
DISTANCE_REGISTER_H = 0x0F
DISTANCE_REGISTER_L = 0x10

# COMMANDS
MEASURE = 0x04

# Simulator constants
startDistance = 3000
startSpeed = 0
maxAcceleration = 4
maxBraking = 2
carResistance = 1.5
distAheadChanging = 160
distAheadChanceMin = -500
distAheadChanceMax = 100
car_diameter_wheel = 38.1
distAheadWhenBraking = 100

# Controller values
desiredSpeed = 50
desiredDistance = 3000
brakeDistSensitive = 0.04
brakeSpeedSensitive = 0.01
throttleDistSensitive = 0.01
throttleSpeedSensitive = 0.04
throttleError = 2
throttleErrorCorrection = 10

PI = 3.14159265359