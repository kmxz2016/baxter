#!/usr/bin/env python

"""
    moveit_attached_object_demo.py - Version 0.1 2014-01-14
    
    Attach an object to the end-effector and then move the arm to test collision avoidance.
    
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyleft (c) 2014 Patrick Goebel.  All lefts reserved.

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
import thread, copy
import moveit_commander
from moveit_commander import RobotCommander, MoveGroupCommander, PlanningSceneInterface
from geometry_msgs.msg import PoseStamped, Pose
from moveit_msgs.msg import CollisionObject, AttachedCollisionObject, PlanningScene
from math import radians
from copy import deepcopy

class MoveItDemo:
    def __init__(self):
        # Initialize the move_group API
        moveit_commander.roscpp_initialize(sys.argv)
        
        rospy.init_node('moveit_demo')
        
        # Construct the initial scene object
        scene = PlanningSceneInterface()
        
        # Pause for the scene to get ready
        rospy.sleep(1)
                                
        # Initialize the MoveIt! commander for the left arm
        left_arm = MoveGroupCommander('left_arm')
                
        # Initialize the MoveIt! commander for the gripper
        left_gripper = MoveGroupCommander('left_gripper')
        
        # Get the name of the end-effector link
        end_eef = left_arm.get_end_effector_link()
        
        # Allow some leeway in position (meters) and orientation (radians)
        left_arm.set_goal_position_tolerance(0.01)
        left_arm.set_goal_orientation_tolerance(0.05)
       
        # Allow replanning to increase the odds of a solution
        left_arm.allow_replanning(True)
        
        # Allow 5 seconds per planning attempt
        left_arm.set_planning_time(5)
        
        # Remove leftover objects from a previous run
        scene.remove_attached_object(end_eef, 'tool')
        scene.remove_world_object('table') 
        scene.remove_world_object('box1')    
        scene.remove_world_object('box2')
        scene.remove_world_object('target')

        # Set the height of the table off the ground
        table_ground = 0.3
        
        # Set the length, width and height of the table
        table_size = [0.2, 0.7, 0.01]
        
        # Set the length, width and height of the object to attach
        tool_size = [0.3, 0.02, 0.02]
        
        # Create a pose for the tool relative to the end-effector
        p = PoseStamped()
        p.header.frame_id = end_eef
        
        scene.attach_mesh
        
        # Place the end of the object within the grasp of the gripper
        p.pose.position.x = tool_size[0] / 2.0 - 0.025
        p.pose.position.y = 0.0
        p.pose.position.z = 0.0
        
        # Align the object with the gripper (straight out)
        p.pose.orientation.x = 0
        p.pose.orientation.y = 0
        p.pose.orientation.z = 0
        p.pose.orientation.w = 1
        
        # Attach the tool to the end-effector
        scene.attach_box(end_eef, 'tool', p, tool_size)

        # Add a floating table top
        table_pose = PoseStamped()
        table_pose.header.frame_id = 'base'
        table_pose.pose.position.x = 0.35
        table_pose.pose.position.y = 0.0
        table_pose.pose.position.z = table_ground + table_size[2] / 2.0
        table_pose.pose.orientation.w = 1.0
        scene.add_box('table', table_pose, table_size)
        
        # Update the current state
        left_arm.set_start_state_to_current_state()

        # Move the arm with the attached object to the 'straight_forward' position
        left_arm.set_named_target('left_ready')
        left_arm.go()
        rospy.sleep(2)  
        
        # Return the arm in the "left_ready" pose stored in the SRDF file
        left_arm.set_named_target('left_arm_zero')
        left_arm.go()
        rospy.sleep(2)
         
        scene.remove_attached_object(end_eef, 'tool')   
        
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)


if __name__ == "__main__":
    MoveItDemo()

    