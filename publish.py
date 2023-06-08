import time
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

echoPin = 4
Buzz = 12
triggerPin = 14


Do = [261]
Le = [294]
Mi = [330]

GPIO.setmode(GPIO.BCM)

GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(Buzz, GPIO.OUT)

Buzz = GPIO.PWM(Buzz,440)



MQTT_HOST = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60

MQTT_PUB_TOPIC = "mobile/waname/automaton"

client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

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
            
        while GPIO.input(echoPin) == 0:
            start = time.time()
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

        sensing = {
            "distance": distance
        }
        value = json.dumps(sensing)
        client.publish(MQTT_PUB_TOPIC, value)
        print(value)


except KeyboardInterrupt :
    GPIO.cleanup()
except KeyboardInterrupt:
    print("I'm done!")
finally:
    client.disconnect()
