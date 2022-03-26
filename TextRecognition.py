import RPi.GPIO as GPIO
import time

import cv2 
import pytesseract
from picamera.array import PiRGBArray
from picamera import PiCamera


GPIO.setwarnings(False)


GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(640, 480))

while True :
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

        if GPIO.input(27) == 1:
            text = pytesseract.image_to_string(image)
            print(text)
            
            if text.startswith('LEDon'):
                GPIO.output(26,True)
                time.sleep(1)
            elif text.startswith('LEDoff'):
                GPIO.output(26,False)
                time.sleep(1)
        
            cv2.imshow("Frame", image)
'''          
        if GPIO.input(17) == 1:
            cv2.waitKey(0)
            break
'''        
cv2.destroyAllWindows()