## Motor controll with PWM
## 키보드로 입력을 받아 1이면 정지(manual mode구현을위한)
## 2이면 auto mode 로 동작 초음파거리측정센서로 15cm 이내에 장애물이 있는 경우 멈춤
## 키보드 인터럽트 이후에 다시 입력값을 받음

import RPi.GPIO as GPIO
import time

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
            
while True:
    try:
        data = int(input())
        
        if data == 1:
            setMotor(CH1, 35, STOP)
            setMotor(CH2, 20, STOP)
            print('here')
        
        while data == 2:
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

            print("Distance => ", distance, "cm")
            if distance <= 15 :
                setMotor(CH1, 35, STOP)
                setMotor(CH2, 20, STOP)
            elif distance > 16 :
                setMotor(CH1, 35, FORWARD)
                setMotor(CH2, 20, FORWARD)
                time.sleep(0.01)
    
    except KeyboardInterrupt :
        setMotor(CH1, 35, STOP)
        setMotor(CH2, 20, STOP)
        print('re')
