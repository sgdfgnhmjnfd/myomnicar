# MyOmniCar Project

## Mô tả
Dự án **MyOmniCar** là một hệ thống mô phỏng robot omni 4 bánh tích hợp tay máy (robot arm) được triển khai trên ROS và Gazebo. Robot có khả năng di chuyển linh hoạt, điều khiển tay máy, và sử dụng dữ liệu GPS để tính toán odometry.

## Các tính năng chính
- **Điều khiển robot omni 4 bánh**: Nhận lệnh vận tốc từ bàn phím hoặc joystick và chuyển đổi thành vận tốc bánh xe.
- **Điều khiển tay máy**: Điều khiển các khớp quay và tịnh tiến của tay máy.
- **Tích hợp GPS**: Chuyển đổi dữ liệu GPS thành odometry để định vị robot.
- **Mô phỏng trên Gazebo**: Hiển thị chuyển động của robot và tay máy trong môi trường ảo.
- **Hiển thị trên RViz**: Hiển thị trạng thái robot, tay máy, và dữ liệu odometry.

## HƯớng dẫn chạy dự án
**Step1:** git repo
git clone https://github.com/sgdfgnhmjnfd/myomnicar
cd myomnicar

**Step2:** Chạy mô phỏng
roslaunch myomnicar display.launch

**Step3:** Mở file config thủ công ( của em bị lỗi ko hiển thị file config từ trước )
**Vào RViz-> Open-> Myomnicar -> config -> config_sensors.rviz**

**Step4:** Khởi chạy node điều khiển
roscore
rosrun myomnicar omni_keyboard_control.py
rosrun teleop_twist_keyboard teleop_twist_keyboard.py 
rosrun myomnicar arm_controller.py

**Step5:** Điều khiển tại 2 node điều khiển xe và tay máy
