#!/usr/bin/env python

"""

Script to return Baxter's arms to a "home" position

"""

#rospy - ROS Python API 
import rospy

#baxter_interface - Baxter Python API 
import baxter_interface
#initialize our ROS node, registering it with the Master 
rospy.init_node('Home_Arms')

#create instances of baxter_interface's Limb class

limb_right = baxter_interface.Limb('right') 
limb_left = baxter_interface.Limb('left')

# store the home position of the arms

home_right = {'right_s0': 0.5353, 'right_s1': -0.5508, 'right_w0': 

0.00, 'right_w1': 0.8588, 'right_w2': 0.00, 'right_e0': 0.00,

'right_e1': 0.7554}

home_left = {'left_s0': -0.5353, 'left_s1': -0.5508, 'left_w0': 0.00,

'left_w1': 0.8588, 'left_w2': 0.00, 'left_e0': 0.00, 'left_e1': 0.7554}

# move both arms to home position 
limb_right.move_to_joint_positions(home_right) 
limb_left.move_to_joint_positions(home_left)

quit()