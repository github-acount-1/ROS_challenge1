#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
# import the library
import threading, time
from appJar import gui


class turtlesim_gui():
  #PI = 0 #3.1415926535897

  def __init__(self):
       #Creating our node,publisher and subscriber
       rospy.init_node('gui_turtlesim_control', anonymous=True)
       self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
       self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
       self.pose = Pose()
       self.rate = rospy.Rate(10)
       self.PI = 3.1415926535897

       self.app = gui("Turtles_move_GUI", "400x600")
       self.app.setBg("orange")
       self.app.setFont(18)

  # add & configure widgets - widgets get a name, to help referencing them later
       self.app.addLabel("title", "Command Your Robot")
       self.app.setLabelBg("title", "blue")
       self.app.setLabelFg("title", "orange")

	# link the buttons to the function called press
       self.app.addButtons(["Forward", "Backward"], self.press)
       self.app.addButtons(["Right", "Left"], self.press)
       self.app.addButtons(["Circular", "Stop"], self.press)
       
	# start the GUI
       self.app.go()
       #app.stop()'''


   #Callback function implementing the pose value received
  def callback(self, data):
       self.pose = data
       self.pose.x = round(self.pose.x, 4)
       self.pose.y = round(self.pose.y, 4)

  def get_distance(self, goal_x, goal_y):
       distance = sqrt(pow((goal_x - self.pose.x), 2) + pow((goal_y - self.pose.y), 2))
       return distance

  
  def move(self, isForward):
        # Starts a new node
        #rospy.init_node('robot_cleaner', anonymous=True)
        #velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
       vel_msg = Twist()
       
       #Receiveing the user's input
       print("Let's move your robot")
       speed = 3 #1 #input("Input your speed:")
       distance = 3 #input("Type your distance:")
       #isForward = 1 #input("Foward?: ")#True or False
       
       #Checking if the movement is forward or backwards
       if(isForward == 1):
           vel_msg.linear.x = abs(speed)
       else:
           vel_msg.linear.x = -abs(speed)
       #Since we are moving just in x-axis
       vel_msg.linear.y = 0
       vel_msg.linear.z = 0
       vel_msg.angular.x = 0
       vel_msg.angular.y = 0
       vel_msg.angular.z = 0
       
           #Setting the current time for distance calculus
       t0 = rospy.Time.now().to_sec()
       current_distance = 0

       #Loop to move the turtle in an specified distance
       while(current_distance < distance):
           #Publish the velocity
           self.velocity_publisher.publish(vel_msg)
           #Takes actual time to velocity calculus
           t1=rospy.Time.now().to_sec()
           #Calculates distancePoseStamped
           current_distance= speed*(t1-t0)
       #After the loop, stops the robot
       vel_msg.linear.x = 0
       #Force the robot to stop
       self.velocity_publisher.publish(vel_msg)

  def rotate(self, isClockwise):
        #Starts a new node
        #rospy.init_node('robot_cleaner', anonymous=True)
        #velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
       vel_msg = Twist()
   
       # Receiveing the user's input
       print("Let's rotate your robot")
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
       if isClockwise == 1:
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

  def move_circle(self):

    # Create a publisher which can "talk" to Turtlesim and tell it to move
    pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
     
    # Create a Twist message and add linear x and angular z values
    move_cmd = Twist()
    move_cmd.linear.x = 1.0
    move_cmd.angular.z = 1.0

    # Save current time and set publish rate at 10 Hz
    now = rospy.Time.now()
    rate = rospy.Rate(20)

    # For the next 6 seconds publish cmd_vel move commands to Turtlesim
    while rospy.Time.now() < now + rospy.Duration.from_sec(6):
        pub.publish(move_cmd)
        #rate.sleep()
     
	   # handle button events
  def press(self, button):
	    #x1 = turtlebot()
	    #try:
		    if button == "Stop":
		        self.app.stop()
		    elif button == "Forward":
		    	#x1 = turtlebot()
		        self.move(1)
		    elif button == "Backward":
		        #pass
		        self.move(0)

		    elif button == "Right":
		        #pass
		        self.rotate(1)
		        self.move(1)

		    elif button == "Left":
		        #pass
		        self.rotate(0)
		        self.move(1)

		    
		    elif button == "Circular":
		         #move2goal()
		         self.move_circle()
		#except Exception as e:
         #   write_to_page( "<p>Error: %s</p>" % str(e) )
    


if __name__ == '__main__':
   try:
       obj = turtlesim_gui()
       
       #try: x = turtlebot()
    	#x.move2goal()
    	#gui_run()

    	
   except rospy.ROSInterruptException: pass

