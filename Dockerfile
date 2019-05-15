FROM ros:melodic

LABEL authors = "Yu Okamoto <yuokamoto1988@gmail.com>"

ENV ROS_HOME=/catkin_ws

# install base software
RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    ros-melodic-rospy \
    ros-melodic-roslaunch \
    build-essential \
    python-pip \
    python-wheel \
    python-snappy

RUN pip install -U catkin_tools bluepy

# create workspace and clone source
RUN mkdir -p /catkin_ws/src && cd /catkin_ws/src  && \ 
	git clone https://github.com/yuokamoto/sphero_mini_ros.git

# submodule update
RUN cd /catkin_ws/src/sphero_mini_ros && \
	git submodule init && git submodule update

# rosdep install
RUN cd /catkin_ws && \
	rosdep update && \ 
	rosdep install -y --from-paths src --ignore-src --rosdistro melodic


# build package
RUN	/bin/bash -c ". /opt/ros/melodic/setup.bash && \ 
	cd /catkin_ws && catkin init && catkin build -j4 "

# execute roslaunch
CMD ["roslaunch sphero_mini_ros sphero_mini.launch"]

# add entrypoint
RUN cp /catkin_ws/src/sphero_mini_ros/ros_entrypoint.sh .
ENTRYPOINT ["/ros_entrypoint.sh"]