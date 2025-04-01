#!/usr/bin/env python3
# filepath: /home/judyshin/catkin_ws/src/myomnicar/scripts/omni_keyboard_control.py

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

# Kích thước robot (cần điều chỉnh theo mô hình thực tế)
WHEEL_RADIUS = 0.06  # Điều chỉnh giá trị này theo URDF
ROBOT_RADIUS = 0.2   # Khoảng cách từ tâm robot đến bánh xe (m)

# Hàm chuyển đổi từ Twist (vận tốc tuyến tính và góc) sang vận tốc bánh xe
def twist_to_wheel_speeds(twist):
    vx = twist.linear.x  # Vận tốc tuyến tính theo trục x
    vy = twist.linear.y  # Vận tốc tuyến tính theo trục y
    wz = twist.angular.z  # Vận tốc góc quanh trục z

    # Công thức tính vận tốc bánh xe cho robot omni 4 bánh
    wheel_LeFro = (vx - vy - wz * ROBOT_RADIUS) / WHEEL_RADIUS  # Bánh trước trái
    wheel_LeBa = (vx + vy - wz * ROBOT_RADIUS) / WHEEL_RADIUS   # Bánh sau trái
    wheel_RiFro = (vx + vy + wz * ROBOT_RADIUS) / WHEEL_RADIUS  # Bánh trước phải
    wheel_RiBa = (vx - vy + wz * ROBOT_RADIUS) / WHEEL_RADIUS   # Bánh sau phải

    return wheel_LeFro, wheel_LeBa, wheel_RiFro, wheel_RiBa

# Callback nhận thông điệp Twist và xuất vận tốc bánh xe
def twist_callback(msg):
    # Chuyển đổi từ Twist sang vận tốc bánh xe
    wheel_LeFro_speed, wheel_LeBa_speed, wheel_RiFro_speed, wheel_RiBa_speed = twist_to_wheel_speeds(msg)

    # Xuất vận tốc bánh xe lên các topic ROS
    pub_LeFro.publish(wheel_LeFro_speed)
    pub_LeBa.publish(wheel_LeBa_speed)
    pub_RiFro.publish(wheel_RiFro_speed)
    pub_RiBa.publish(wheel_RiBa_speed)

    # Log thông tin vị trí và vận tốc
    rospy.loginfo(f"Received Twist: linear.x={msg.linear.x}, linear.y={msg.linear.y}, angular.z={msg.angular.z}")
    rospy.loginfo(f"Wheel Speeds: LeFro={wheel_LeFro_speed:.2f}, LeBa={wheel_LeBa_speed:.2f}, RiFro={wheel_RiFro_speed:.2f}, RiBa={wheel_RiBa_speed:.2f}")

# Node ROS chính
def omni_keyboard_control():
    global pub_LeFro, pub_LeBa, pub_RiFro, pub_RiBa

    rospy.init_node('omni_keyboard_control', anonymous=True)

    # Publisher cho vận tốc bánh xe
    pub_LeFro = rospy.Publisher('/LeFro_joint_velocity_controller/command', Float64, queue_size=10)
    pub_LeBa = rospy.Publisher('/LeBa_joint_velocity_controller/command', Float64, queue_size=10)
    pub_RiFro = rospy.Publisher('/RiFro_joint_velocity_controller/command', Float64, queue_size=10)
    pub_RiBa = rospy.Publisher('/RiBa_joint_velocity_controller/command', Float64, queue_size=10)

    # Subscriber nhận thông điệp Twist từ bàn phím
    rospy.Subscriber('/cmd_vel', Twist, twist_callback)

    rospy.loginfo("Omni keyboard control node started. Listening to /cmd_vel...")
    rospy.spin()

if __name__ == '__main__':
    try:
        omni_keyboard_control()
    except rospy.ROSInterruptException:
        pass