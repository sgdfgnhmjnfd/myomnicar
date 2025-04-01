#!/usr/bin/env python3
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import sys
import tty
import termios

class ArmController:
    def __init__(self):
        # Lấy thông tin từ parameter server
        self.joint1_name = rospy.get_param('~joint1_name', 'link1_rot')
        self.joint2_name = rospy.get_param('~joint2_name', 'link2_pris')
        self.joint1_limit = rospy.get_param('~joint1_limit', [-1.57, 1.57])  # Giới hạn joint quay
        self.joint2_limit = rospy.get_param('~joint2_limit', [-0.5, 0.5])   # Giới hạn mới: -0.5m đến 0.5m

        # Khởi tạo client cho controller
        self.client = actionlib.SimpleActionClient(
            '/arm_controller/follow_joint_trajectory', 
            FollowJointTrajectoryAction
        )
        
        rospy.loginfo("Waiting for arm controller server...")
        self.client.wait_for_server()
        rospy.loginfo("Connected to arm controller server")

    def move_arm(self, joint1_pos, joint2_pos, duration=2.0):
        """ Di chuyển tay máy đến vị trí mong muốn
        
        Args:
            joint1_pos (float): Vị trí khớp quay joint1 (radian)
            joint2_pos (float): Vị trí khớp tịnh tiến joint2 (mét)
            duration (float): Thời gian thực hiện chuyển động (giây)
        """
        # Giới hạn giá trị các khớp
        joint1_pos = max(self.joint1_limit[0], min(self.joint1_limit[1], joint1_pos))
        rospy.loginfo(f"Requested joint2_pos: {joint2_pos}")
        joint2_pos = max(self.joint2_limit[0], min(self.joint2_limit[1], joint2_pos))
        rospy.loginfo(f"Clamped joint2_pos: {joint2_pos}")

        # Tạo goal message
        goal = FollowJointTrajectoryGoal()
        trajectory = JointTrajectory()
        
        # Đặt tên các khớp (phải khớp với tên trong URDF)
        trajectory.joint_names = [self.joint1_name, self.joint2_name]
        
        # Tạo điểm đích
        point = JointTrajectoryPoint()
        point.positions = [joint1_pos, joint2_pos]
        point.time_from_start = rospy.Duration(duration)
        
        trajectory.points.append(point)
        goal.trajectory = trajectory
        
        # Gửi goal và chờ kết quả
        self.client.send_goal(goal)
        rospy.loginfo(f"Moving arm to position: {joint1_pos} rad, {joint2_pos} m in {duration} sec")
        
        if self.client.wait_for_result():
            rospy.loginfo("Arm movement completed")
        else:
            rospy.logwarn("Arm movement did not complete before the timeout")

def arm_controller():
    """Hàm chính để điều khiển tay máy."""
    rospy.init_node('arm_teleop_keyboard', anonymous=True)

    # Khởi tạo ArmController
    arm = ArmController()

    # Hướng dẫn sử dụng
    print("Điều khiển tay máy:")
    print("w: Tăng vị trí joint1 (khớp quay)")
    print("s: Giảm vị trí joint1 (khớp quay)")
    print("a: Tăng vị trí joint2 (khớp tịnh tiến)")
    print("d: Giảm vị trí joint2 (khớp tịnh tiến)")
    print("q: Thoát")

    joint1_pos = 0.0
    joint2_pos = 0.0

    rate = rospy.Rate(50)  # Tần số vòng lặp
    while not rospy.is_shutdown():
        key = get_key()
        if key == 'w':
            joint1_pos += 0.1
        elif key == 's':
            joint1_pos -= 0.1
        elif key == 'a':
            joint2_pos += 0.01
            rospy.loginfo(f"Joint2 position increased to: {joint2_pos}")
        elif key == 'd':
            joint2_pos -= 0.01
            rospy.loginfo(f"Joint2 position decreased to: {joint2_pos}")
        elif key == 'q':
            print("Thoát chương trình.")
            break

        # Di chuyển tay máy
        arm.move_arm(joint1_pos, joint2_pos)
        rate.sleep()

def get_key():
    """Hàm đọc phím từ bàn phím."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

if __name__ == '__main__':
    try:
        arm_controller()
    except rospy.ROSInterruptException:
        pass