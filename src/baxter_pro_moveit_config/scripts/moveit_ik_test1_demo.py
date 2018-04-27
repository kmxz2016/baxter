#!/usr/bin/env python

"""
    test
  
"""

import rospy, sys
import moveit_commander
from moveit_commander import MoveGroupCommander, PlanningSceneInterface
from moveit_msgs.msg import  PlanningScene, ObjectColor
from geometry_msgs.msg import PoseStamped, Pose
from moveit_msgs.msg import Grasp, GripperTranslation, MoveItErrorCodes

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from tf.transformations import quaternion_from_euler
from copy import deepcopy

GRIPPER_OPEN = [0.0,0.0]
GRIPPER_CLOSE = [-0.015,-0.015]

GRIPPER_EFFORT = [1.0]

class MoveItDemo:
    def __init__(self):
        # Initialize the move_group API
        moveit_commander.roscpp_initialize(sys.argv)
        
        #rospy.init_node('moveit_demo')
        
        # Initialize the ROS node
        rospy.init_node('moveit_demo', anonymous=True)
        cartesian = rospy.get_param('~cartesian', True)
        print "===== It is OK ===="
        rospy.sleep(3)
        
        # Construct the initial scene object
        scene = PlanningSceneInterface()
        
        # Create a scene publisher to push changes to the scene
        self.scene_pub = rospy.Publisher('planning_scene', PlanningScene, queue_size=1)
        
        # Create a dictionary to hold object colors
        self.colors = dict()
        
        # Pause for the scene to get ready
        rospy.sleep(1)
                        
        # Initialize the move group for the left arm
        left_arm = MoveGroupCommander('left_arm')
        left_gripper = MoveGroupCommander('left_gripper')
        # Get the name of the end-effector link
        left_eef = left_arm.get_end_effector_link()
        
        # Allow some leeway in position (meters) and orientation (radians)
        left_arm.set_goal_position_tolerance(0.01)
        left_arm.set_goal_orientation_tolerance(0.05)
       
        # Allow replanning to increase the odds of a solution
        left_arm.allow_replanning(True)
        
        left_reference_frame = left_arm.get_planning_frame()
        # Set the left arm reference frame
        left_arm.set_pose_reference_frame('base')
        # Allow 5 seconds per planning attempt
        left_arm.set_planning_time(10)
        
        # Set a limit on the number of pick attempts before bailing
        max_pick_attempts = 10
        
        # Set a limit on the number of place attempts
        max_place_attempts = 10
                
        # Give the scene a chance to catch up
        rospy.sleep(2)

        object1_id = 'object1'      
        table_id = 'table'
        target_id = 'target'
        tool_id = 'tool'
        #obstacle1_id = 'obstacle1'
        # Remove leftover objects from a previous run
        scene.remove_world_object(object1_id)
        scene.remove_world_object(table_id)
        scene.remove_world_object(target_id)
        scene.remove_world_object(tool_id)

        # Remove any attached objects from a previous session
        scene.remove_attached_object('base', target_id) 
               
        # Give the scene a chance to catch up
        rospy.sleep(1)
        
        # Start the arm in the "resting" pose stored in the SRDF file
        left_arm.set_named_target('left_arm_zero')
        left_arm.go()
        rospy.sleep(1)
        left_gripper.set_joint_value_target(GRIPPER_OPEN)
        left_gripper.go()
        rospy.sleep(1)

        # Set the height of the table off the ground
        table_ground = 0.0

        object1_size = [0.088, 0.04, 0.02]
        
        # Set the target size [l, w, h]
        target_size = [0.02, 0.01, 0.12]
        # Add a table top and two boxes to the scene
        #obstacle1_size = [0.3, 0.05, 0.45]
        
        # Add a table top and two boxes to the scene
        
        #obstacle1_pose = PoseStamped()
        #obstacle1_pose.header.frame_id = left_reference_frame
        #obstacle1_pose.pose.position.x = 0.96
        #obstacle1_pose.pose.position.y = 0.24
        #obstacle1_pose.pose.position.z = 0.04
        #obstacle1_pose.pose.orientation.w = 1.0   
        #scene.add_box(obstacle1_id, obstacle1_pose, obstacle1_size)
       
        #self.setColor(obstacle1_id, 0.8, 0.4, 0, 1.0)

        object1_pose = PoseStamped()
        object1_pose.header.frame_id = left_reference_frame
        object1_pose.pose.position.x = 0.80
        object1_pose.pose.position.y = 0.04
        object1_pose.pose.position.z = table_ground + table_size[2] + object1_size[2] / 2.0
        object1_pose.pose.orientation.w = 1.0   
        scene.add_box(object1_id, object1_pose, object1_size)

       # Add a table top and two boxes to the scene
        table_pose = PoseStamped()
        table_pose.header.frame_id = left_reference_frame
        table_pose.pose.position.x = 1
        table_pose.pose.position.y = 0.7
        table_pose.pose.position.z = table_ground + table_size[2] / 2.0
        table_pose.pose.orientation.w = 1.0
        scene.add_box(table_id, table_pose, table_size)    
        
        # Set the target pose in between the boxes and on the table
        target_pose = PoseStamped()
        target_pose.header.frame_id = left_reference_frame
        target_pose.pose.position.x = 0.58
        target_pose.pose.position.y = 0.1878
        target_pose.pose.position.z = .1116
        target_pose.pose.orientation.x = 0.1325
        target_pose.pose.orientation.y = 0.9908
        target_pose.pose.orientation.z = table_ground + table_size[2] + target_size[2] / 2.0
        target_pose.pose.orientation.w = 0.0254
        # Add the target object to the scene
        scene.add_box(target_id, target_pose, target_size)
        
        # Make the table red and the boxes orange
        self.setColor(object1_id, 0.8, 0, 0, 1.0)
        self.setColor(table_id, 0.8, 0, 0, 1.0)
        
        # Make the target yellow
        self.setColor(target_id, 0.9, 0.9, 0, 1.0)
        
        # Send the colors to the planning scene
        self.sendColors()
        
        # Set the support surface name to the table object
        left_arm.set_support_surface_name(table_id)
        
        # Specify a pose to place the target after being picked up
        place_pose = PoseStamped()
        place_pose.header.frame_id = left_reference_frame
        place_pose.pose.position.x = 0.18
        place_pose.pose.position.y = -0.18
        place_pose.pose.position.z = table_ground + table_size[2] + target_size[2] / 2.0
        place_pose.pose.orientation.w = 1.0
        0
        # Initialize the grasp pose to the target pose
        grasp_pose = target_pose
        
        # Shift the grasp pose by half the width of the target to center it
        #grasp_pose.pose.position.y -= target_size[1] / 2.0
                
        # Generate a list of grasps
        grasps = self.make_grasps(grasp_pose, [target_id])

        # Publish the grasp poses so they can be viewed in RViz
        for grasp in grasps:
            self.gripper_pose_pub.publish(grasp.grasp_pose)
            rospy.sleep(0.2)
    
        # Track success/failure and number of attempts for pick operation
        result = None
        n_attempts = 0
        
        # Repeat until we succeed or run out of attempts
        while result != MoveItErrorCodes.SUCCESS and n_attempts < max_pick_attempts:
            n_attempts += 1
            rospy.loginfo("Pick attempt: " +  str(n_attempts))
            result = left_arm.pick(target_id, grasps)
            rospy.sleep(0.2)
        
        # If the pick was successful, attempt the place operation   
        if result == MoveItErrorCodes.SUCCESS:
            result = None
            n_attempts = 0
            
            # Generate valid place poses
            places = self.make_places(place_pose)
            
            # Repeat until we succeed or run out of attempts
            while result != MoveItErrorCodes.SUCCESS and n_attempts < max_place_attempts:
                n_attempts += 1
                rospy.loginfo("Place attempt: " +  str(n_attempts))
                for place in places:
                    result = left_arm.place(target_id, place)
                    if result == MoveItErrorCodes.SUCCESS:
                        break
                rospy.sleep(0.2)
                
            if result != MoveItErrorCodes.SUCCESS:
                rospy.loginfo("Place operation failed after " + str(n_attempts) + " attempts.")
        else:
            rospy.loginfo("Pick operation failed after " + str(n_attempts) + " attempts.")
                
        # Return the arm to the "resting" pose stored in the SRDF file
        left_arm.set_named_target('left_arm_zero')
        left_arm.go()
        
        # Open the gripper to the neutral position
        left_gripper.set_joint_value_target(GRIPPER_OPEN)
        left_gripper.go()
       
        rospy.sleep(1)

        # Shut down MoveIt cleanly
        moveit_commander.roscpp_shutdown()
        
        # Exit the script
        moveit_commander.os._exit(0)
        
    # Get the gripper posture as a JointTrajectory
    def make_gripper_posture(self, joint_positions):
        # Initialize the joint trajectory for the gripper joints
        t = JointTrajectory()
        
        # Set the joint names to the gripper joint names
        t.joint_names = 'left_eef'
        
        # Initialize a joint trajectory point to represent the goal
        tp = JointTrajectoryPoint()
        
        # Assign the trajectory joint positions to the input positions
        tp.positions = joint_positions
        
        # Set the gripper effort
        tp.effort = GRIPPER_EFFORT
        
        tp.time_from_start = rospy.Duration(1.0)
        
        # Append the goal point to the trajectory points
        t.points.append(tp)
        
        # Return the joint trajectory
        return t
    
    # Generate a gripper translation in the direction given by vector
    def make_gripper_translation(self, min_dist, desired, vector):
        # Initialize the gripper translation object
        g = GripperTranslation()
        
        # Set the direction vector components to the input
        g.direction.vector.x = vector[0]
        g.direction.vector.y = vector[1]
        g.direction.vector.z = vector[2]
        
        # The vector is relative to the gripper frame
        g.direction.header.frame_id = 'left_gripper_base'
        
        # Assign the min and desired distances from the input
        g.min_distance = min_dist
        g.desired_distance = desired
        
        return g

    # Generate a list of possible grasps
    def make_grasps(self, initial_pose_stamped, allowed_touch_objects):
        # Initialize the grasp object
        g = Grasp()
        
        # Set the pre-grasp and grasp postures appropriately
        g.pre_grasp_posture = self.make_gripper_posture(GRIPPER_OPEN)
        g.grasp_posture = self.make_gripper_posture(GRIPPER_CLOSED)
                
        # Set the approach and retreat parameters as desired
        g.pre_grasp_approach = self.make_gripper_translation(0.01, 0.1, [1.0, 0.0, 0.0])
        g.post_grasp_retreat = self.make_gripper_translation(0.1, 0.15, [0.0, -1.0, 1.0])
        
        # Set the first grasp pose to the input pose
        g.grasp_pose = initial_pose_stamped
    
        # Pitch angles to try
        pitch_vals = [0, 0.1, -0.1, 0.2, -0.2, 0.3, -0.3]
        
        # Yaw angles to try
        yaw_vals = [0]

        # A list to hold the grasps
        grasps = []

        # Generate a grasp for each pitch and yaw angle
        for y in yaw_vals:
            for p in pitch_vals:
                # Create a quaternion from the Euler angles
                q = quaternion_from_euler(0, p, y)
                
                # Set the grasp pose orientation accordingly
                g.grasp_pose.pose.orientation.x = q[0]
                g.grasp_pose.pose.orientation.y = q[1]
                g.grasp_pose.pose.orientation.z = q[2]
                g.grasp_pose.pose.orientation.w = q[3]
                
                # Set and id for this grasp (simply needs to be unique)
                g.id = str(len(grasps))
                
                # Set the allowed touch objects to the input list
                g.allowed_touch_objects = allowed_touch_objects
                
                # Don't restrict contact force
                g.max_contact_force = 0
                
                # Degrade grasp quality for increasing pitch angles
                g.grasp_quality = 1.0 - abs(p)
                
                # Append the grasp to the list
                grasps.append(deepcopy(g))
                
        # Return the list
        return grasps
    
    # Generate a list of possible place poses
    def make_places(self, init_pose):
        # Initialize the place location as a PoseStamped message
        place = PoseStamped()
        
        # Start with the input place pose
        place = init_pose
        
        # A list of x shifts (meters) to try
        x_vals = [0, 0.005, 0.01, 0.015, -0.005, -0.01, -0.015]
        
        # A list of y shifts (meters) to try
        y_vals = [0, 0.005, 0.01, 0.015, -0.005, -0.01, -0.015]
        
        pitch_vals = [0]
        
        # A list of yaw angles to try
        yaw_vals = [0]

        # A list to hold the places
        places = []
        
        # Generate a place pose for each angle and translation
        for y in yaw_vals:
            for p in pitch_vals:
                for y in y_vals:
                    for x in x_vals:
                        place.pose.position.x = init_pose.pose.position.x + x
                        place.pose.position.y = init_pose.pose.position.y + y
                        
                        # Create a quaternion from the Euler angles
                        q = quaternion_from_euler(0, p, y)
                        
                        # Set the place pose orientation accordingly
                        place.pose.orientation.x = q[0]
                        place.pose.orientation.y = q[1]
                        place.pose.orientation.z = q[2]
                        place.pose.orientation.w = q[3]
                        
                        # Append this place pose to the list
                        places.append(deepcopy(place))
        
        # Return the list
        return places
    
        # Set the start state to the current state
        left_arm.set_start_state_to_current_state()
        # Set the target pose in between the boxes and above the table
        
        
        # Set the target pose for the arm
        left_arm.set_pose_target(target_pose, left_eef)
        
        # Move the arm to the target pose (if possible)
        left_arm.go()
        
        # Pause for a moment...
        rospy.sleep(2)
        left_gripper.set_joint_value_target(GRIPPER_CLOSE)
        left_gripper.go()
        rospy.sleep(1)
        scene.attach_box(left_eef, object1_id, object1_pose, object1_size)
        # Cartesian Paths
        waypoints1 = []
        start_pose = left_arm.get_current_pose(left_eef).pose
        wpose = deepcopy(start_pose)
        waypoints1.append(deepcopy(wpose))
       
        wpose.position.x -= 0.05
        wpose.position.y += 0.105
        wpose.position.z += 0.07
        waypoints1.append(deepcopy(wpose))
  
        wpose.position.x -= 0.05
        wpose.position.y += 0.105
        wpose.position.z -= 0.07
        waypoints1.append(deepcopy(wpose))

        (cartesian_plan, fraction) = left_arm.compute_cartesian_path (
                                        waypoints1,   # waypoint poses
                                        0.01,        # eef_step 1cm
                                        0.0,         # jump_threshold
                                        True)        # avoid_collisions

         

        left_arm.execute(cartesian_plan)
        rospy.sleep(2)
        left_gripper.set_joint_value_target(GRIPPER_OPEN)
        left_gripper.go()
        rospy.sleep(1)
        scene.remove_attached_object(left_eef, object1_id) 
        # Exit MoveIt cleanly
        waypoints2 = []
        start_pose = left_arm.get_current_pose(left_eef).pose
        wpose = deepcopy(start_pose)
        waypoints2.append(deepcopy(wpose))
        wpose.position.z += 0.07
        waypoints2.append(deepcopy(wpose))

        wpose.position.x += 0.1
        wpose.position.y -= 0.21
        waypoints2.append(deepcopy(wpose))

        wpose.position.z -= 0.07
        waypoints2.append(deepcopy(wpose))

        (cartesian_plan, fraction) = left_arm.compute_cartesian_path (
                                        waypoints2,   # waypoint poses
                                        0.01,        # eef_step 1cm
                                        0.0,         # jump_threshold
                                        True)        # avoid_collisions

         

        left_arm.execute(cartesian_plan)
        rospy.sleep(2)
        moveit_commander.roscpp_shutdown()
        
        # Exit the script        
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
    try:
        MoveItDemo()
    except KeyboardInterrupt:
        raise
    
    