import cv2
import numpy as np
import time
import alsaaudio
from adafruit_servokit import ServoKit
 
m = alsaaudio.Mixer('PCM')
 
kit = ServoKit(channels = 8)
 
# SET MINIMUM AND MAXIMUM POSITION OF SERVO
 
# kit.servo[0].set_pulse_width_range(300, 2610)
# kit.servo[1].set_pulse_width_range(1000, 2670)
 
x_position = 90
y_position = 90
 
cap = cv2.VideoCapture(0)
Ht = 480
Wd = 720
cap.set(3, Wd)
cap.set(4, Ht)
_, frame = cap.read()
rows, cols, ch = frame.shape
 
x_medium = int(cols/2)
y_medium = int(rows/2)
 
x_center = 360
y_center = 240
 
x_position = 90
y_position = 90
 
x_band = 70
y_band = 70
 
def nothing(x):
    print(x)
 
cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 151, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 70, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 8, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)
 
def translate(sensor_val, in_from, in_to, out_from, out_to):
    out_range = out_to - out_from
    in_range = in_to - in_from
    in_val = sensor_val - in_from
    val=(int(in_val)/in_range)*out_range
    out_val = out_from+val
    return out_val
 
while True:
    # exact color definition
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")
 
    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")
 
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
 
    # saving image in frame and HSV conversion
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
 
    #red color
    # low_red = np.array([0, 121, 70])
    # high_red = np.array([10, 255, 255])
    red_mask = cv2.inRange(hsv_frame, l_b, u_b)
    contours, hierarchy = cv2.findContours (red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contrours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
 
    #drawing and following object function
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        break
   
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        x_medium = int((x + x + w) /2)
        y_medium = int((y + y + h) /2)
       
 
    # drawing lines
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0,255,0), 2)
    cv2.line(frame, (0, y_medium), (720, y_medium), (0,255,0), 2)
#    
#     cv2.line(frame, (x_center, 0), (x_center, 480), (0,0,255), 2)
#     cv2.line(frame, (0, y_center), (720, y_center), (0,0,255), 2)
 
    # displaying windows
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", red_mask)
 
    # exit here
    key = cv2.waitKey(1)
    if key == 27:
        break
 
    # Move SERVO motor IFs
    if x_medium < x_center - x_band :
        x_position += 3
    elif x_medium > x_center + x_band :
        x_position -= 3
       
    if y_medium < y_center - y_band:
        y_position -= 3
    elif y_medium > y_center + y_band:
        y_position += 3
       
    if x_position >= 130:
        x_position = 130
    elif x_position <= 50:
        x_position = 50
    else:
        x_position = x_position
       
    if y_position >= 150:
        y_position = 150
    elif y_position <= 50:
        y_position = 50
    else:
        y_position = y_position
       
    volume = int(translate(y_position, 50, 150, 100, 60))
   
 
 
    print("x_position: " , x_position, "y_position: " , y_position, volume)
 
 
# MOVE!!!
 
    kit.servo[0].angle = (x_position)
   
    kit.servo[1].angle = (y_position)
   
#AUDIO SET
 
    current_volume = m.getvolume()
    print (current_volume)
    m.setvolume(volume)
 
cap.release()
cv2.destroyAllWindows()
print ("Goodbye")
 
 
