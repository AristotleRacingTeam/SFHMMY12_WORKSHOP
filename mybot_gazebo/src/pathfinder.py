#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def data_provider():
	#initialize our subscriber
	rospy.init_node('motion_planner',anonymous=True)
	rospy.Subscriber('/workbot/laser_scan',LaserScan,callback)
	rospy.spin()


def callback(SensorData):
	#creating our publisher 
	motion_activator=rospy.Publisher('workbot/cmd_vel',Twist,queue_size=100)
	motion_activator_object=Twist()
	rate=rospy.Rate(100)

	flag= False

	right_counter=0
	left_counter=0


	for i in range (260,460):
		if(SensorData.ranges[i]<0.6):
			flag=True
			break


	if(flag==True):
		for j in range (0,260): #look right
			right_counter=right_counter+SensorData.ranges[j]

		for k in range (460,720): #look left
			left_counter=left_counter+SensorData.ranges[k]

		if (right_counter<left_counter):  # more empty space left so turn left
			motion_activator_object.linear.x= 0
			motion_activator_object.angular.z= 2.5
		elif (right_counter>left_counter):	# more empty space right so turn right
			motion_activator_object.linear.x=0
			motion_activator_object.angular.z= -2.5
		else:
			motion_activator_object.linear.x=0.1
			motion_activator_object.angular.z=0

	else:
		motion_activator_object.linear.x=0.8
		motion_activator_object.angular.z=0




	motion_activator.publish(motion_activator_object)
	rate.sleep()

if _name_ == '_main_':
	try: data_provider()
	except rospy.ROSInterruptException: pass
