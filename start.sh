roscore &
sleep 3
rm /usr/bin/python && ln -s /usr/bin/python3.6 /usr/bin/python
source /catkin_ws/devel/setup.bash 
rosrun sphero_mini_ros sphero_mini.py _mac:=C5:AB:0E:0F:74:D9
