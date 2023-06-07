import RPi.GPIO as GPIO
import time

Buzz = 12
triggerPin = 14
echoPin = 4

Do = [261]
Le = [294]
Mi = [330]

GPIO.setmode(GPIO.BCM)

GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(Buzz, GPIO.OUT)

Buzz = GPIO.PWM(Buzz,440)

try:
    while True:
        GPIO.output(triggerPin, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(triggerPin, GPIO.HIGH)
            
        start = time.time()
        stop = time.time()
            
    #에코핀이 on 되는 시점을 시작 시간으로 잡는다
        while GPIO.input(echoPin) == 0:
            start = time.time()
    #에코핀이 다시 off 되는 시점을 반사판 수신 시간으로 잡는다
        while GPIO.input(echoPin) == 1:
            stop = time.time()

    #Calculate Pulse length
        rtTotime = stop - start
        distance = rtTotime * 34000/2
        print("distance : %.2fcm" % distance)
    
        if 1 < distance < 5 :
            Buzz.start(50)
            for i in range(0,len(Do)):
                Buzz.ChangeFrequency(Do[i])
            time.sleep(1)

        elif 6 < distance < 10:
            Buzz.start(50)
            for i in range(0,len(Le)):
                Buzz.ChangeFrequency(Le[i])
            time.sleep(0.1)

        elif distance >11:
            Buzz.start(50)
            for i in range(0,len(Mi)):
                Buzz.ChangeFrequency(Mi[i])
            time.sleep(0.1)
        else: 
            Buzz.stop()
            time.sleep(0.3)

except KeyboardInterrupt :
    GPIO.cleanup()