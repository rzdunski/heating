import RPi.GPIO as GPIO
import gettime
import relay
import time
import os
import gettemp

pins= [37, 38, 40] #pins used to control relays

heater1 = pins[0]
heater2 = pins[1]
pump = pins[2]
secure_sensor_id = '28-000006891ce7'
treshold_temp = 30

def sleep(sec):
    time.sleep(sec)

def init():
    for pin in pins:
	GPIO.setmode(GPIO.BOARD) #use PCB numberig
        GPIO.setwarnings(False) #turn of warnings about port usage
        GPIO.setup(pin, GPIO.OUT) #set pin on borad as output
        GPIO.output(pin, GPIO.HIGH) #set high state on each pin


def test():
    relay.relay_on(pump)
    sleep(4)
    relay.relay_on(heater1)
    sleep(4)    
    relay.relay_on(heater2)
    sleep(4)
    relay.relay_off(heater1)
    sleep(1)
    relay.relay_off(heater2)
    sleep(1)
    relay.relay_off(pump)
    init()

def temp_control():
    if round(float(gettemp.gettemp(secure_sensor_id)/1000),1) > (treshold_temp - 3):
        relay.relay_off(heater2)
        print 'Temp_control: Turn off H2, sleeping 60 sec...'
        sleep(60)

def main():
    init()
    #print round(float(gettemp.gettemp(secure_sensor_id)/1000),1) < treshold_temp
    while round(float(gettemp.gettemp(secure_sensor_id)/1000),1) < treshold_temp:
        relay.relay_on(pump)
        sleep(4)
        relay.relay_on(heater1)
        relay.relay_on(heater2)
        temp_control()
        print 'Temp secure:' , round(float(gettemp.gettemp(secure_sensor_id)/1000),1)
        print 'Main: Sleeping 60 sec ...'
        sleep(60)

while round(float(gettemp.gettemp(secure_sensor_id)/1000),1) < treshold_temp:
    main()
    
relay.relay_off(heater1)
sleep(1)
relay.relay_off(heater2)
print 'Turn H1 and H2 off'
print 'Waiting 120 sec and turn pump off'
sleep(120)
relay.relay_off(pump)
print 'Exit program'
sleep(2)
