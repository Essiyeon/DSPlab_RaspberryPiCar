##Motor controll + Pi cam + web2

from flask import Flask, request
from flask import render_template
from flask import Response
import RPi.GPIO as GPIO
import cv2
import time

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 모터 채널
CH1 = 0
CH2 = 1

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWORD = 2

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
#PWM PIN
ENA = 26  #37 pin
ENB = 0   #27 pin
#GPIO PIN
IN1 = 19  #37 pin
IN2 = 13  #35 pin
IN3 = 6   #31 pin
IN4 = 5   #29 pin

Trig = 23
Echo = 24

GPIO.setwarnings(False)

# GPIO 모드 설정 
GPIO.setmode(GPIO.BCM)

GPIO.setup(Trig, GPIO.OUT) #Trig
GPIO.setup(Echo, GPIO.IN) #Echo
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

pwmA=GPIO.PWM(ENA,100)
pwmA.start(0)
pwmB=GPIO.PWM(ENB,100)
pwmB.start(0)


 # 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor(ch, speed, stat):
    if ch == CH1:
        #모터 속도 제어 PWM
        pwmA.ChangeDutyCycle(speed)  
    
        if stat == FORWARD:
            GPIO.output(IN1, LOW)
            GPIO.output(IN2, HIGH)
        
        #뒤로
        elif stat == BACKWORD:
            GPIO.output(IN1, HIGH)
            GPIO.output(IN2, LOW)
        
        #정지
        elif stat == STOP:
            GPIO.output(IN1, LOW)
            GPIO.output(IN2, LOW)
    else:
        #모터 속도 제어 PWM
        pwmB.ChangeDutyCycle(speed)  
    
        if stat == FORWARD:
            GPIO.output(IN3, LOW)
            GPIO.output(IN4, HIGH)
        
        #뒤로
        elif stat == BACKWORD:
            GPIO.output(IN3, HIGH)
            GPIO.output(IN4, LOW)
        
        #정지
        elif stat == STOP:
            GPIO.output(IN3, LOW)
            GPIO.output(IN4, LOW)

        
camera=cv2.VideoCapture(0)

def gen_frames() :
    while True :
        success, frame = camera.read()
        if(not success):
            break
        else :
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route("/")
def home():
    return render_template("index5.html")

@app.route("/Go")
def Go():
    setMotor(CH1, 40, FORWARD)
    setMotor(CH2, 20, FORWARD)
    return "LED on"

@app.route("/Left")
def Left():
    setMotor(CH2, 20, FORWARD)
    return "LED on"

@app.route("/Right")
def Right():
    setMotor(CH1, 40, FORWARD)
    return "LED on"

@app.route("/Back")
def Back():
    setMotor(CH1, 40, BACKWORD)
    setMotor(CH2, 20, BACKWORD)
    return "LED on"

@app.route("/Stop")
def Stop():
    setMotor(CH1, 40, STOP)
    setMotor(CH2, 20, STOP)
    return "LED off"


@app.route("/automatic")
def automatic() :
    try:   
        while True :
            GPIO.output(Trig, False)
            time.sleep(0.1)

            GPIO.output(Trig, True)
            time.sleep(0.001)
            GPIO.output(Trig, False)

            # 18번이 OFF가 되는 시점을 시작시간으로 설정
            while GPIO.input(Echo) == 0:
                start = time.time()
            
            # 18번이 ON이 되는 시점을 반사파 수신시간으로 설정
            while GPIO.input(Echo) == 1:
                stop = time.time()
            
            # 초음파가 되돌아오는 시간차로 거리를 계산한다
            time_interval = stop - start
            distance = time_interval * 17000
            distance = round(distance, 2)
            ##distance = time_interval / 58

            print("Distance => ", distance, "cm")
            
            if distance <= 15 :
                setMotor(CH1, 35, STOP)
                setMotor(CH2, 20, STOP)
            else :
                setMotor(CH1, 35, FORWARD)
                setMotor(CH2, 20, FORWARD)
                time.sleep(0.001)
        return "auto"
    except :
        return "fail"
    
@app.route("/manual")
def manual() :
    try:
        setMotor(CH1, 100, STOP)
        setMotor(CH2, 100, STOP)
        print('manu')
        return "manu"
    except :
        return "fail"

@app.route('/video_feed')
def video_feed() :
    return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_Capture')
def video_Cap() :
    success, frame = camera.read()
    if success :
        cv2.imwrite('Cap.jpg', frame)
        return 'Cap.jpg'
    else :
        return 'self camera test'

if __name__ == "__main__":  
   app.run(host="192.168.0.8", port = "8080")