#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import NavSatFix, LaserScan, Image
from std_srvs.srv import Trigger, TriggerResponse

# Global variables
gps_data = lidar_data = camera_data = None

# Callbacks
def gps_callback(msg):
    global gps_data
    gps_data = msg

def lidar_callback(msg):
    global lidar_data
    lidar_data = msg

def camera_callback(msg):
    global camera_data
    camera_data = msg

# Generic service handler
def sensor_service(data, name):
    return TriggerResponse(success=bool(data), message=f"{name} data available" if data else f"No {name} data")

def main():
    rospy.init_node('sensor_services')
    
    rospy.Subscriber('/gps/fix', NavSatFix, gps_callback)
    rospy.Subscriber('/scan', LaserScan, lidar_callback)
    rospy.Subscriber('/camera/image_raw', Image, camera_callback)
    
    rospy.Service('/get_gps_data', Trigger, lambda req: sensor_service(gps_data, "GPS"))
    rospy.Service('/get_lidar_data', Trigger, lambda req: sensor_service(lidar_data, "LiDAR"))
    rospy.Service('/get_camera_data', Trigger, lambda req: sensor_service(camera_data, "Camera"))
    
    rospy.loginfo("Sensor services are ready.")
    rospy.spin()

if __name__ == '__main__':
    main()
