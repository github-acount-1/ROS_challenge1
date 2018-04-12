#!/usr/bin/env python
"""OpenCV feature detectors with ros CompressedImage Topics in python.

This example subscribes to a ros topic containing sensor_msgs 
CompressedImage. It converts the CompressedImage into a numpy.ndarray, 
then detects and marks features in that image. It finally displays 
and publishes the new image - again as CompressedImage topic.
"""
__author__ =  'Belayneh, at iCog labs ethiopia>'
__version__=  '0'
#__license__ = 'BMG'
# Python libs
import sys, time

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2
import cv2 as cv 

# Ros libraries
import roslib
roslib.load_manifest('image_transform1')
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

VERBOSE=False

class image_feature:

   def __init__(self):
       '''Initialize ros publisher, ros subscriber'''
       # topic where we publish
       self.image_pub = rospy.Publisher("/output/image_raw/compressed", CompressedImage, queue_size = 1)
       # self.bridge = CvBridge()

       # subscribed Topic
       self.subscriber = rospy.Subscriber("/camera/image/compressed",
           CompressedImage, self.callback,  queue_size = 1)
       if VERBOSE :
           print "subscribed to /camera/image/compressed"


       camera = cv2.VideoCapture(0)
        #camera =cvCaptureFromCAM(0)
       cv2.namedWindow("test")

       img_counter = 0
       i=0

       while True:
            ret, frame = camera.read()
            cv2.imshow("test", frame)
            k = cv2.waitKey(25)
            #return_value, image = camera.read()

            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif (k%256 == 32 or i == 100 or k == 's'):
            #for i in range(10):
              return_value, image = camera.read()
              cv2.imwrite('opencv'+str(i)+'.png', image)
              i+=1
              self.callback(image)
              break

            i+=1  
        #self.callback(image)
       del(camera)




   def callback(self, ros_data):
       '''Callback function of subscribed topic. 
       Here images get converted and features detected'''
       if VERBOSE :
           print 'received image of type: "%s"' % ros_data.format

       #### direct conversion to CV2 ####
       np_arr = np.fromstring(ros_data.data, np.uint8)
       image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
       #image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # OpenCV >= 3.0:
       
       #### Feature detectors using CV2 #### 
       # "","Grid","Pyramid" + 
       # "FAST","GFTT","HARRIS","MSER","ORB","SIFT","STAR","SURF"
       method = "GridFAST"
       feat_det = cv2.FeatureDetector_create(method)
       time1 = time.time()

       # convert np image to grayscale
       featPoints = feat_det.detect(
           cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY))
       time2 = time.time()
       if VERBOSE :
           print '%s detector found: %s points in: %s sec.'%(method,
               len(featPoints),time2-time1)

       for featpoint in featPoints:
           x,y = featpoint.pt
           cv2.circle(image_np,(int(x),int(y)), 3, (0,0,255), -1)
       
       cv2.imshow('cv_img', image_np)
       cv2.waitKey(2)

       #### Create CompressedIamge ####
       msg = CompressedImage()
       msg.header.stamp = rospy.Time.now()
       msg.format = "jpeg"
       msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
       # Publish new image
       self.image_pub.publish(msg)
       
       #self.subscriber.unregister()

def main(args):
   '''Initializes and cleanup ros node'''
   ic = image_feature()
   rospy.init_node('image_feature', anonymous=True)
   try:
       rospy.spin()
   except KeyboardInterrupt:
       print "Shutting down ROS Image feature detector module"
   cv2.destroyAllWindows()

if __name__ == '__main__':
  #print("sys.argv:", sys.argv)
  main(sys.argv)

