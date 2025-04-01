cmake_minimum_required(VERSION 2.8.3)

project(myomnicar)

find_package(catkin REQUIRED)

catkin_package()

find_package(roslaunch)

foreach(dir config launch meshes urdf)
    install(DIRECTORY ${dir}/
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

# Thêm đoạn mã yêu cầu
install(DIRECTORY launch config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(PROGRAMS scripts/arm_controller.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
install(FILES docs/docs/BÁO CÁO GIỮA KÌ.pdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/docs
)
catkin_install_python(PROGRAMS scripts/sensor_srv.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

