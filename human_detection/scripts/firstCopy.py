import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

ub_cas = cv2.CascadeClassifier('haarcascade_upperbody.xml')
ff_cas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cas = cv2.CascadeClassifier('haarcascade_eye.xml')
image_sub = None
detection_pub = None
bridge = CvBridge()
def image_callback(message):
    #result_image = bridge.imgmsg_to_cv2(message)
    cv_image = bridge.imgmsg_to_cv2(message, desired_encoding="mono8")
    #cv_image = bridge.cv2_to_imgmsg(message, encoding="passthrough")

    ff = ff_cas.detectMultiScale(cv_image)
    #ff = ff_cas.detectMultiScale(gsFeed, 1.3, 5)
    ffU = ub_cas.detectMultiScale(cv_image)
    # ff = ff_cas.detectMultiScale(gsFeed, 1.01, 5)
    ffE = eye_cas.detectMultiScale(cv_image)

    for (x, y, width, length) in ffU:
        cv2.rectangle(cv_image, (x, y), (x + width, y + length), (0, 191, 255), 2)

    for (x, y, width, length) in ff:
        cv2.rectangle(cv_image, (x, y), (x + width, y + length), (100, 50, 200), 2)
        cv2.circle(cv_image, (x+(w/2), y+(h/2)), 5, 255,-1)
    #cv2.imshow('Detection Window', feed)

    for (x, y, width, length) in ffE:
        cv2.rectangle(cv_image, (x, y), (x + width, y + length), (0, 128, 0), 2)
    #cv2.imshow('Detection Window', feed)

    

    result_message = bridge.cv2_to_imgmsg(cv_image)
    detection_pub.publish(result_message)
    #cv2.imshow('Detection Window', feed)

# Release capture when closing application

if __name__ == '__main__':
    rospy.init_node("upperbodyDetectionWithoutCV")
    image_sub = rospy.Subscriber("/multisense_sl/camera/left/image_raw", Image, image_callback)
    detection_pub = rospy.Publisher("/upperbodyDetection/result", Image)
    rospy.spin()
