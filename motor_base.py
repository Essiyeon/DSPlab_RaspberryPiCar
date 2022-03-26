## Motor controll with PWM
## Ű����� �Է��� �޾� 1�̸� ����(manual mode����������)
## 2�̸� auto mode �� ���� �����İŸ����������� 15cm �̳��� ��ֹ��� �ִ� ��� ����

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ���� ä��
CH1 = 0
CH2 = 1

# ���� ����
STOP  = 0
FORWARD  = 1
BACKWORD = 2

# PIN ����� ����
OUTPUT = 1
INPUT = 0

# PIN ����
HIGH = 1
LOW = 0

# ���� �� ����
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

# GPIO ��� ���� 
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

 # ���� �����Լ� �����ϰ� ����ϱ� ���� �ѹ��� ����(����)
def setMotor(ch, speed, stat):
    if ch == CH1:
        #���� �ӵ� ���� PWM
        pwmA.ChangeDutyCycle(speed)  
    
        if stat == FORWARD:
            GPIO.output(IN1, LOW)
            GPIO.output(IN2, HIGH)
        
        #�ڷ�
        elif stat == BACKWORD:
            GPIO.output(IN1, HIGH)
            GPIO.output(IN2, LOW)
        
        #����
        elif stat == STOP:
            GPIO.output(IN1, LOW)
            GPIO.output(IN2, LOW)
    else:
        #���� �ӵ� ���� PWM
        pwmB.ChangeDutyCycle(speed)  
    
        if stat == FORWARD:
            GPIO.output(IN3, LOW)
            GPIO.output(IN4, HIGH)
        
        #�ڷ�
        elif stat == BACKWORD:
            GPIO.output(IN3, HIGH)
            GPIO.output(IN4, LOW)
        
        #����
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

            # 18���� OFF�� �Ǵ� ������ ���۽ð����� ����
            while GPIO.input(Echo) == 0:
                start = time.time()
                    
            # 18���� ON�� �Ǵ� ������ �ݻ��� ���Žð����� ����
            while GPIO.input(Echo) == 1:
                stop = time.time()
                    
            # �����İ� �ǵ��ƿ��� �ð����� �Ÿ��� ����Ѵ�
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