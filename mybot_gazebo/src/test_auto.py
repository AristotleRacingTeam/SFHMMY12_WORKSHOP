#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan



def data_provider():

	rospy.init_node('motion_planner',anonymous=True)
	rospy.Subscriber("/robot/laser_scan",LaserScan,callback)
	rospy.spin()

def callback(SensorData):

	motion_activator=rospy.Publisher('/robot/cmd_vel',Twist,queue_size=100)
	motion_activator_object=Twist()
	rate=rospy.Rate(100)

	flag= False
	counter=0
	counter1=0
	counter2=0


	for i in range (260,460):
		if(SensorData.ranges[i]<0.4):
			flag=True
			break


	if(flag==True):
		for j in range (0,300): #look right
			if(SensorData.ranges[j]<0.4):
				counter1=counter1+SensorData.ranges[j]

		for k in range (420,720): #look left
			if(SensorData.ranges[k]<0.4):
				counter2=counter2+SensorData.ranges[k]
		if (counter1<counter2):  # more rays bumped into obstacles right so turn left
			motion_activator_object.linear.x= 0
			motion_activator_object.angular.z= 2.5
		elif (counter1>counter2):	# more rays bumped into obstacles right so turn left
			motion_activator_object.linear.x=0
			motion_activator_object.angular.z= -2.5


	else:
		motion_activator_object.linear.x=1.5
		motion_activator_object.angular.z=0




	motion_activator.publish(motion_activator_object)
	rate.sleep()

if __name__ == '__main__':
	try:data_provider()
	except rospy.ROSInterruptException: pass
