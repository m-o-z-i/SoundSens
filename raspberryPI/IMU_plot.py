#!/usr/bin/python
 
import smbus
import math
import time
 

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

gyro_scale = 131.0
accel_scale = 16384.0

# complementary filter
now = time.time()
K = 0.98
K1 = 1 - K
time_diff = 0.013
last_x = 0.0
last_y = 0.0
last_z = 0.0
gyro_offset_x = 0.0
gyro_offset_y = 0.0
gyro_offset_z = 0.0
gyro_total_x = 0.0
gyro_total_y = 0.0
gyro_total_z = 0.0

# gyro calibration
X_CALIB = -0.0245931693944 
Y_CALIB = -0.235268050528
Z_CALIB = -0.00280006555746

def read_all():
    raw_gyro_data = bus.read_i2c_block_data(address, 0x43, 6)
    raw_accel_data = bus.read_i2c_block_data(address, 0x3b, 6)

    gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / gyro_scale
    gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / gyro_scale
    gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / gyro_scale

    accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / accel_scale
    accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / accel_scale
    accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / accel_scale

    return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z)
 
def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

#roll
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

#pitch
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

#not same as yaw... is not possible to compute from accelerometer
def get_z_rotation(x,y,z):
    radians = math.atan2(dist(x,y), z)
    return math.degrees(radians)

def initComplementaryFilter():
    print "init complementary filter.." 
    global last_x, last_y, last_z, gyro_offset_x, gyro_offset_y, gyro_offset_z, gyro_total_x, gyro_total_y, gyro_total_z
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()
    last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    gyro_offset_x = gyro_scaled_x 
    gyro_offset_y = gyro_scaled_y
    gyro_offset_z = gyro_scaled_z
    gyro_total_x = last_x
    gyro_total_y = last_y
    gyro_total_z = last_z


def run():
        global id, now
	#deltaTime = time.time() - now
        #print "DELTAAA TIME", deltaTime
        #now = time.time()
	#time_diff = deltaTime

        
        global gyro_total_x, gyro_total_y, gyro_total_z, last_x, last_y, last_z

        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

        #gyro_scaled_x += X_CALIB
        #gyro_scaled_y += Y_CALIB
        #gyro_scaled_z += Z_CALIB    
        #gyro_scaled_x -= gyro_offset_x
        #gyro_scaled_y -= gyro_offset_y
        #gyro_scaled_z -= gyro_offset_z

        # accumulate gyro data
        gyro_delta_x = (gyro_scaled_x * time_diff)
        gyro_delta_y = (gyro_scaled_y * time_diff)
        gyro_delta_z = (gyro_scaled_z * time_diff)

        # get total gyro angle
        gyro_total_x += gyro_delta_x
        gyro_total_y += gyro_delta_y
        gyro_total_z += gyro_delta_z

        # get accelometer rotation
        rotation_accel_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
        rotation_accel_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

        # complementary filter
        last_x = K * (last_x + gyro_delta_x) + (K1 * rotation_accel_x)
        last_y = K * (last_y + gyro_delta_y) + (K1 * rotation_accel_y)

        print "{0:.4f} {1:.2f} {2:.2f} {3:.2f} {4:.2f} {5:.2f} {6:.2f}".format( time.time() - now, (rotation_accel_x), (gyro_total_x), (last_x), (rotation_accel_y), (gyro_total_y), (last_y)) 


if __name__ == "__main__":
    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)
    
    initComplementaryFilter()
    while True:
        time.sleep(0.01)
        run()