#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt

class turtlesim_fractals():
  #PI = 0 #3.1415926535897

  def __init__(self):
       #Creating our node,publisher and subscriber
       rospy.init_node('turtlesim_fractals_final', anonymous=True)
       self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
       self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
       self.pose = Pose()
       self.rate = rospy.Rate(10)
       self.PI = 3.1415926535897

   #Callback function implementing the pose value received
  def callback(self, data):
       self.pose = data
       self.pose.x = round(self.pose.x, 4)
       self.pose.y = round(self.pose.y, 4)

  def rotate(self):
        #Starts a new node
        #rospy.init_node('robot_cleaner', anonymous=True)
        #velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
       vel_msg = Twist()
   
       speed = 100 #30 #input("Input your speed (degrees/sec):")
       angle = 75 #input("Type your distance (degrees):")
       clockwise = 0 #input("Clockwise?: ") #True or false
   
       #Converting from angles to radians
       angular_speed = speed*2*self.PI/360
       relative_angle = angle*2*self.PI/360
   
       #We wont use linear components
       vel_msg.linear.x=0
       vel_msg.linear.y=0
       vel_msg.linear.z=0
       vel_msg.angular.x = 0
       vel_msg.angular.y = 0
   
       # Checking if our movement is CW or CCW
       if clockwise:
           vel_msg.angular.z = -abs(angular_speed)
       else:
           vel_msg.angular.z = abs(angular_speed)
       # Setting the current time for distance calculus
       t0 = rospy.Time.now().to_sec()
       current_angle = 0
   
       while(current_angle < relative_angle):
           self.velocity_publisher.publish(vel_msg)
           t1 = rospy.Time.now().to_sec()
           current_angle = angular_speed*(t1-t0)
   
   
       #Forcing our robot to stop
       vel_msg.angular.z = 0
       self.velocity_publisher.publish(vel_msg)
       #rospy.spin()

  def move_circle(self, x1, z1):

    # Create a publisher which can "talk" to Turtlesim and tell it to move
    pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
     
    # Create a Twist message and add linear x and angular z values
    move_cmd = Twist()
    move_cmd.linear.x = x1 #1.0
    move_cmd.angular.z = z1 #1.0

    # Save current time and set publish rate at 10 Hz
    now = rospy.Time.now()
    rate = rospy.Rate(20)

    # For the next 6 seconds publish cmd_vel move commands to Turtlesim
    while rospy.Time.now() < now + rospy.Duration.from_sec(6):
        pub.publish(move_cmd)
        #rate.sleep()
     


if __name__ == '__main__':
   try:
       #Testing our function
       f = turtlesim_fractals()
       #f.rotate()
       #f.move_circle(2, 2)
       f.rotate()
       f.move_circle(2, 2)
       f.rotate()
       f.move_circle(2, 2)
       f.rotate()
       f.move_circle(2, 2)
       f.rotate()
       f.move_circle(2, 2)
       f.rotate()
       f.move_circle(2, 2)
       f.rotate()
       f.move_circle(2, 2)
       f.rotate()
       f.move_circle(2, 2)
       f.rotate()
       f.move_circle(2, 2)
       
   except rospy.ROSInterruptException: pass
