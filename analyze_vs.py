import sys
import numpy as np
import rosbag
import tf

experiment_name = sys.argv[1]
output_dir = "experiments/"

bag_file = experiment_name + ".bag"
bag = rosbag.Bag(bag_file, "r") # Read bag file

# /gazebo/model_states
topic_name = "/gazebo/model_states"
sufix = "_state_"
output_file = output_dir + experiment_name + sufix + ".txt"

with open(output_file, 'w+') as data_file:
    for topic, msg, t in bag.read_messages(topics=[topic_name]):
        mask = msg.name.index('quadrotor') 
        position = msg.pose[mask].position
        orientation = msg.pose[mask].orientation
        linear = msg.twist[mask].linear
        angular = msg.twist[mask].angular
        quaternion = (orientation.x, orientation.y, orientation.z, orientation.w) 
        euler = tf.transformations.euler_from_quaternion(quaternion)
        line = 12 * "{}," + "{}\n" # 13 columns
        data_file.write(line.format(t, position.x, position.y, position.z,
                                    euler[0], euler[1], euler[2],
                                    linear.x, linear.y, linear.z,
                                    angular.x, angular.y, angular.z))

# /cmd_vel
topic_name = "/cmd_vel"
sufix = "_vel_"
output_file = output_dir + experiment_name + sufix + ".txt"

with open(output_file, 'w+') as data_file:
    for topic, msg, t in bag.read_messages(topics=[topic_name]):
        linear = msg.linear
        angular = msg.angular
        line = "{},{},{},{},{},{},{}\n"
        data_file.write(line.format(t, linear.x, linear.y, linear.z,
                                    angular.x, angular.y, angular.z))

# /visual_features
topic_name = "/visual_features"
sufix = "_features_"
output_file = output_dir + experiment_name + sufix + ".txt"

with open(output_file, 'w+') as data_file:
    for topic, msg, t in bag.read_messages(topics=[topic_name]):
        bl = msg.target.points[0]
        br = msg.target.points[1]
        tr = msg.target.points[2]
        tl = msg.target.points[3]
        cog = msg.cog
        error = msg.error
        height = msg.img_height
        width = msg.img_width
        line = 16 * "{}," + "{}\n" # 17 columns
        data_file.write(line.format(t, bl.u, bl.v, br.u, br.v, tr.u, tr.v, tl.u, tl.v,
                                    cog.u, cog.v, error.x, error.y, error.z, error.ang,
                                    height, width))

