#!/usr/bin/env python
#################################################################################
# Copyright 2019 LE MINH TAN TAI LAB BO1_FENG CHIA UNIVERSITY, TAICHUNG, TAIWAN #
#################################################################################
import rospy
from std_msgs.msg import String
import cv2
import numpy as np

from geometry_msgs.msg import Twist

def DetectFace() :
        #pub = rospy.Publisher('video', String, queue_size=10)
        #rospy.init_node('GetImage',anonymous=True)
        video = cv2.VideoCapture(0)
        face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        while not rospy.is_shutdown():
                ret,image = video.read()
                image = FindFace(image,face_cascade)
                cv2.imshow('VideoCamera',image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                #rate.sleep()
def FindFace(photo,cascade):
        gray = cv2.cvtColor(photo,cv2.COLOR_BGR2GRAY) # create gray color
        image =cascade.detectMultiScale(gray,1.3,5) # to upload cascade to check Face
        checkFace = 0
        #rospy.loginfo("Waiting Object")
        for (x,y,w,h) in image: # create Rectangle to detect face
                checkFace = 1 # Create have Face
                #rospy.loginfo("Have Object")
                cv2.rectangle(photo, (x,y),(x+w,y+h),(255,0,0),2)     
                distanceFromCenter = ((2*x+w)/2)-320 # Fomular get value Center
                distancePerDegree = 4
                xPosition = distanceFromCenter/distancePerDegree
                disObject = h
                #rospy.loginfo(disObject) # Print value x
                twist = Twist() # Get function cmd TWIST
                #Define angle parameters
                angleTooRight = 0.3
                angleNormalRight = 0.2
                angleCenter = 0.0
                angleNormalLeft = -0.2
                angleTooLeft = -0.3
                #Define speed parameters
                speedZero = 0.0
                speedSlow = 0.1
                speedNormal = 0.2
                speedQuick = 0.3
                #TooLeft --------------------------------------------#
                if(((xPosition>-60)and(xPosition<=-40))and((disObject>=160)and(disObject<240))): # Too_left - closely
                    twist.linear.x = speedSlow; twist.angular.z= angleTooRight;
                elif(((xPosition>-60)and(xPosition<=-40))and((disObject>=100)and(disObject<160))): # Too_left - Normal
                    twist.linear.x = speedNormal; twist.angular.z= angleTooRight;
                elif(((xPosition>-60)and(xPosition<=-40))and((disObject>=0)and(disObject<100))): # Too_left - Far
                    twist.linear.x = speedQuick; twist.angular.z= angleTooRight;
                #NormalLeft --------------------------------------------#
                elif(((xPosition>-40)and(xPosition<=-20))and((disObject>=160)and(disObject<240))): # Normal_Left - closely
                    twist.linear.x = speedSlow; twist.angular.z= angleNormalRight;
                elif(((xPosition>-40)and(xPosition<=-20))and((disObject>=100)and(disObject<160))): # Normal_Left - Normal
                    twist.linear.x = speedNormal; twist.angular.z= angleNormalRight;
                elif(((xPosition>-40)and(xPosition<=-20))and((disObject>=0)and(disObject<100))): # Normal_Left - Far
                    twist.linear.x = speedQuick; twist.angular.z= angleNormalRight;
                #Center --------------------------------------------#
                elif(((xPosition>-20)and(xPosition<=20))and((disObject>=160)and(disObject<240))): # Center - closely
                    twist.linear.x = speedSlow; twist.angular.z= angleCenter;
                elif(((xPosition>-20)and(xPosition<=20))and((disObject>=100)and(disObject<160))): # Center - Normal
                    twist.linear.x = speedNormal; twist.angular.z= angleCenter;
                elif(((xPosition>-20)and(xPosition<=20))and((disObject>=0)and(disObject<100))): # Center - Far
                    twist.linear.x = speedQuick; twist.angular.z= angleCenter;
                #NormalRight --------------------------------------------#
                elif(((xPosition>20)and(xPosition<=40))and((disObject>=160)and(disObject<240))): # NormalRight - closely
                    twist.linear.x = speedSlow; twist.angular.z= angleNormalLeft;
                elif(((xPosition>20)and(xPosition<=40))and((disObject>=100)and(disObject<160))): # NormalRight - Normal
                    twist.linear.x = speedNormal; twist.angular.z= angleNormalLeft;
                elif(((xPosition>20)and(xPosition<=40))and((disObject>=0)and(disObject<100))): # NormalRight - Far
                    twist.linear.x = speedQuick; twist.angular.z= angleNormalLeft;
                #TooRight --------------------------------------------#
                elif(((xPosition>40)and(xPosition<=60))and((disObject>=160)and(disObject<240))): # TooRight - closely
                    twist.linear.x = speedSlow; twist.angular.z= angleTooLeft;
                elif(((xPosition>40)and(xPosition<=60))and((disObject>=100)and(disObject<160))): # TooRight - Normal
                    twist.linear.x = speedNormal; twist.angular.z= angleTooLeft;
                elif(((xPosition>40)and(xPosition<=60))and((disObject>=0)and(disObject<100))): # TooRight - Far
                    twist.linear.x = speedQuick; twist.angular.z= angleTooLeft;
                else:
                    twist.linear.x = speedZero; twist.angular.z= speedZero;
                pub.publish(twist)
		#rospy.loginfo(twist)
        return photo
if __name__ == '__main__':
    try:
        pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        #pub = rospy.Publisher('rotate_robot', String, queue_size=10) # Create Pub
        rospy.init_node('GetImage',anonymous=True) # Init Node Get Image
        pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        DetectFace()

    except rospy.ROSInterruptException: pass
