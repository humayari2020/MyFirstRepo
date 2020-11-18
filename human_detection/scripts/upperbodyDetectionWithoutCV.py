#!/usr/bin/python
import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

ub_cas = cv2.CascadeClassifier('/home/hyari/doggy/src/human_detection/scripts/haarcascade_upperbody.xml')
ff_cas = cv2.CascadeClassifier('/home/hyari/doggy/src/human_detection/scripts/haarcascade_frontalface_default.xml')
eye_cas = cv2.CascadeClassifier('/home/hyari/doggy/src/human_detection/scripts/haarcascade_eye.xml')
image_sub = None
detection_pub = None
bridge = CvBridge()
def image_callback(message):
    #result_image = bridge.imgmsg_to_cv2(message)
    cv_image = bridge.imgmsg_to_cv2(message, desired_encoding="mono8")
    #cv_image = bridge.cv2_to_imgmsg(message, desired_encoding="mono8")

    ff = ff_cas.detectMultiScale(cv_image)
   
    ffU = ub_cas.detectMultiScale(cv_image)
    
    ffE = eye_cas.detectMultiScale(cv_image)

    for (x, y, width, length) in ffU:
        cv2.rectangle(cv_image, (x, y), (x + width, y + length), (0, 191, 255), 2)

    for (x, y, width, length) in ff:
        cv2.rectangle(cv_image, (x, y), (x + width, y + length), (100, 50, 200), 2)
   
    
    for (x, y, width, length) in ffE:
        cv2.rectangle(cv_image, (x, y), (x + width, y + length), (0, 128, 0), 2)
    

    

    result_message = bridge.cv2_to_imgmsg(cv_image)
    detection_pub.publish(result_message)
    

# Release capture when closing application

if __name__ == '__main__':
    rospy.init_node("upperbodyDetectionWithoutCV")
    image_sub = rospy.Subscriber("/multisense_sl/camera/left/image_raw", Image, image_callback)
    detection_pub = rospy.Publisher("/upperbodyDetection/result", Image)
    rospy.spin()
