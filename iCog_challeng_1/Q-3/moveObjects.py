#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

#from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt, radians
#from math import radians

class MoveObjects():
    def __init__(self):
        # initiliaze
        rospy.init_node('moveObjects', anonymous=True)

        #Creating our node,publisher and subscriber
       #rospy.init_node('turtlesim_fractals_final', anonymous=True)
        self.vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_sub = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
        self.pose = Pose()
        self.rate = rospy.Rate(10)
        self.PI = 3.1415926535897

        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)

    	# Create a publisher which can "talk" to TurtleBot and tell it to move
            # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
         
    	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);

    #def go_in_specWay(self):
        # create two different Twist() variables.  One for moving forward.  One for turning 45 degrees.

        # let's go forward at 0.2 m/s
        move_cmd = Twist()
        move_cmd.linear.x = 2
        # by default angular.z is 0 so setting this isn't required

            #let's turn at 45 deg/s
        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = radians(45); #45 deg/s in radians/s

        #two keep drawing squares.  Go forward for 2 seconds (10 x 5 HZ) then turn for 2 second
        count = 0
        while not rospy.is_shutdown():
            # go forward 0.4 m (2 seconds * 0.2 m / seconds)
            rospy.loginfo("Going Straight")
            for x in range(0,15):
                    self.cmd_vel.publish(move_cmd)
                    self.vel_pub.publish(move_cmd)
                    r.sleep()
            # turn 90 degrees
            rospy.loginfo("Turning")
            for x in range(0,15):
                    self.cmd_vel.publish(turn_cmd)
                    self.vel_pub.publish(turn_cmd)
                    r.sleep()            
            count = count + 1
            #if(count == 4): 
             #   count = 0
            #if(count == 0): 
                   #rospy.loginfo("TurtleBot should be close to the original starting position (but it's probably way off)")
                                
     #Callback function implementing the pose value received
    def callback(self, data):
       self.pose = data
       self.pose.x = round(self.pose.x, 4)
       self.pose.y = round(self.pose.y, 4)

    def shutdown(self):
        # stop objects
        rospy.loginfo("Stop objects")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop Turtle/object
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        MoveObjects()
        #obj.move()
        #obj.go_in_specWay()
        #GoForward()
    except:
        rospy.loginfo("Object moving node terminated.")


