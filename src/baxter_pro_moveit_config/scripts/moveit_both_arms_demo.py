#!/usr/bin/env python

"""
    moveit_ik_demo.py - Version 0.1 2014-01-14
    
    Use inverse kinemtatics to move the end effector to a specified pose
    
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2014 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.5
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html
"""

import rospy, sys
import moveit_commander
from trajectory_msgs.msg import JointTrajectoryPoint

from geometry_msgs.msg import PoseStamped, Pose
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from copy import deepcopy

from moveit_commander import MoveGroupCommander, PlanningSceneInterface
from moveit_msgs.msg import CollisionObject, AttachedCollisionObject, PlanningScene,ObjectColor

GRIPPER_OPEN = [0.0,0.0]
GRIPPER_CLOSE = [-0.025,-0.025]
class MoveItDemo:
    def __init__(self):
        # Initialize the move_group API
        moveit_commander.roscpp_initialize(sys.argv)
        
        rospy.init_node('moveit_demo')
        # Construct the initial scene object
        scene = PlanningSceneInterface()
        self.scene_pub = rospy.Publisher('planning_scene', PlanningScene)
        
        # Create a dictionary to hold object colors
        self.colors = dict()
        # Pause for the scene to get ready
        rospy.sleep(1)
   
        # Initialize the move group 
        both_arms = moveit_commander.MoveGroupCommander('both_arms')
        right_arm = moveit_commander.MoveGroupCommander('right_arm')
        left_arm = moveit_commander.MoveGroupCommander('left_arm')
        left_gripper = MoveGroupCommander('left_gripper')
        # Get the name of the end-effector link
        right_eef = right_arm.get_end_effector_link()
        left_eef = left_arm.get_end_effector_link()
 
        print "============ Printing end-effector link"
        print right_eef         
        print left_eef 
        # Set the reference frame for pose targets
        right_reference_frame = right_arm.get_planning_frame()
        left_reference_frame = left_arm.get_planning_frame()
        # Set the right arm reference frame accordingly
        #right_arm.set_pose_reference_frame(reference_frame)
                
        # Allow replanning to increase the odds of a solution
        right_arm.allow_replanning(True)
        # Allow some leeway in position (meters) and orientation (radians)
        right_arm.set_goal_position_tolerance(0.01)
        right_arm.set_goal_orientation_tolerance(0.01)
        
        left_arm.allow_replanning(True)
        # Allow some leeway in position (meters) and orientation (radians)
        left_arm.set_goal_position_tolerance(0.01)
        left_arm.set_goal_orientation_tolerance(0.01)
        # Allow 5 seconds per planning attempt
        left_arm.set_planning_time(5)
        right_arm.set_planning_time(5)

        object1_id = 'object1'
        # Remove leftover objects from a previous run
        scene.remove_world_object(object1_id)
        rospy.sleep(2)

        right_arm.set_named_target('right_ready')
        right_arm.go()
        left_arm.set_named_target('left_ready')
        left_arm.go()
        left_gripper.set_joint_value_target(GRIPPER_OPEN)
        left_gripper.go()
        rospy.sleep(1)
        # attach_box
        # Set the length, width and height of the object to attach
        object1_size = [0.09,0.057, 0.001]
        
        # Create a pose for the tool relative to the end-effector
        object1_p = PoseStamped()
        object1_p.header.frame_id = right_reference_frame
        object1_p.pose.position.x = 0.77
        object1_p.pose.position.y = -0.27
        object1_p.pose.position.z = -0.21
        object1_p.pose.orientation.w = 1

        scene.add_box(object1_id, object1_p, object1_size)
        self.setColor(object1_id, 0.8, 0.4, 0, 1.0)
        self.sendColors() 

        right_arm.set_start_state_to_current_state()
        left_arm.set_start_state_to_current_state()
        # target pose
        target_pose1 = PoseStamped()
        target_pose1.header.frame_id = right_reference_frame
        target_pose1.header.stamp = rospy.Time.now()     
        target_pose1.pose.position.x =  0.77
        target_pose1.pose.position.y = -0.27
        target_pose1.pose.position.z = -0.14
        target_pose1.pose.orientation.x = 0.500166303975
        target_pose1.pose.orientation.y = 0.865326245156
        target_pose1.pose.orientation.z = -0.0155702691449
        target_pose1.pose.orientation.w =  0.0283147405248

        right_arm.set_pose_target(target_pose1, right_eef)
        right_arm.go()
        rospy.sleep(1)
        # Attach the tool to the end-effector
        scene.attach_box(right_eef, object1_id, object1_p, object1_size)

        target_pose2 = PoseStamped()
        target_pose2.header.frame_id = right_reference_frame
        target_pose2.header.stamp = rospy.Time.now()     
        target_pose2.pose.position.x =  0.632
        target_pose2.pose.position.y = -0.125
        target_pose2.pose.position.z = 0.08
        target_pose2.pose.orientation.x = 0.2392
        target_pose2.pose.orientation.y = -0.9708
        target_pose2.pose.orientation.z = -0.0137
        target_pose2.pose.orientation.w =  0.0103

        target_pose3 = PoseStamped()
        target_pose3.header.frame_id = left_reference_frame
        target_pose3.header.stamp = rospy.Time.now()     
        target_pose3.pose.position.x = 0.632
        target_pose3.pose.position.y = 0.026
        target_pose3.pose.position.z = 0.013
        target_pose3.pose.orientation.x = -0.021
        target_pose3.pose.orientation.y = 0.017
        target_pose3.pose.orientation.z = -0.999
        target_pose3.pose.orientation.w =  0.031

        both_arms.set_pose_target(target_pose2, right_eef)
        both_arms.set_pose_target(target_pose3, left_eef)
        both_arms.go()
        rospy.sleep(3)
        #scene.remove_attached_object(right_eef, 'tool') 
        
        object1_p = left_arm.get_current_pose(left_eef)
        object1_p.pose.position.y -= 0.12
        object1_p.pose.orientation.x = 0
        object1_p.pose.orientation.y = 0
        object1_p.pose.orientation.z = 0.707
        object1_p.pose.orientation.w = 0.707
        scene.remove_attached_object(right_eef, object1_id) 
        scene.attach_box(left_eef,object1_id,object1_p,object1_size)
        rospy.sleep(1)
        left_gripper.set_joint_value_target(GRIPPER_CLOSE)
        left_gripper.go()
      

        target_pose4 = PoseStamped()
        target_pose4.header.frame_id = right_reference_frame
        target_pose4.header.stamp = rospy.Time.now()     
        target_pose4.pose.position.x =  0.58241
        target_pose4.pose.position.y = -0.30286
        target_pose4.pose.position.z = 0.05471
        target_pose4.pose.orientation.x = 0.23931
        target_pose4.pose.orientation.y = -0.97080
        target_pose4.pose.orientation.z = -0.01346
        target_pose4.pose.orientation.w =  0.01003

        target_pose5 = PoseStamped()
        target_pose5.header.frame_id = left_reference_frame
        target_pose5.header.stamp = rospy.Time.now()     
        target_pose5.pose.position.x = 0.843
        target_pose5.pose.position.y = 0.438
        target_pose5.pose.position.z = 0.105
        target_pose5.pose.orientation.x = -0.01386
        target_pose5.pose.orientation.y = -0.02950
        target_pose5.pose.orientation.z = -0.70489
        target_pose5.pose.orientation.w =  0.70856
        #right_arm.set_pose_target(target_pose4, right_eef)
        both_arms.set_pose_target(target_pose4, right_eef)
        both_arms.set_pose_target(target_pose5, left_eef)
        both_arms.go()
        rospy.sleep(2)
        # Shut down MoveIt cleanly
        moveit_commander.roscpp_shutdown()
        
        # Exit MoveIt
        moveit_commander.os._exit(0)
    # Set the color of an object
    def setColor(self, name, r, g, b, a = 0.9):
        # Initialize a MoveIt color object
        color = ObjectColor()
        
        # Set the id to the name given as an argument
        color.id = name
        
        # Set the rgb and alpha values given as input
        color.color.r = r
        color.color.g = g
        color.color.b = b
        color.color.a = a
        
        # Update the global color dictionary
        self.colors[name] = color

    # Actually send the colors to MoveIt!
    def sendColors(self):
        # Initialize a planning scene object
        p = PlanningScene()

        # Need to publish a planning scene diff        
        p.is_diff = True
        
        # Append the colors from the global color dictionary 
        for color in self.colors.values():
            p.object_colors.append(color)
        
        # Publish the scene diff
        self.scene_pub.publish(p)

if __name__ == "__main__":
    MoveItDemo()

    
    
