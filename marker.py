#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker

class MarkerPub():
    def __init__(self, frame):
        self.frame = frame
        marker_pub1 = rospy.Publisher('docker_marker1', Marker, queue_size = 1)
        marker_pub2 = rospy.Publisher('docker_marker2', Marker, queue_size = 1)

        point1 = [0.9,1.1,0.32]
        point2 = [1,0.498,0.107]
        rate = rospy.Rate(5)
        while not rospy.is_shutdown():
            marker_pub1.publish(self.setting_marker(point1))
            marker_pub2.publish(self.setting_marker(point2))
            rate.sleep()

    def setting_marker(self, docker_point):
        marker = Marker()
        marker.header.frame_id = self.frame
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.lifetime = rospy.Duration(1.0)
        marker.color.r = 1.0
        marker.color.g = 0
        marker.color.b = 0
        marker.color.a = 1.0
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05

        marker.pose.position.x = docker_point[0]
        marker.pose.position.y = docker_point[1]
        marker.pose.position.z = docker_point[2]

        return marker


if __name__ == '__main__':
    rospy.init_node('marker_pub')
    frame = rospy.get_param('~frame', 'base')
    MarkerPub(frame)
    rospy.spin()
