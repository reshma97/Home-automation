import RPi.GPIO as GPIO
import time,sys,re,os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIN_LIVING = 4
PIN_LAMP = 17
PIN_FAN = 27

GPIO.setup(PIN_LIVING,GPIO.OUT)
GPIO.setup(PIN_LAMP,GPIO.OUT)
GPIO.setup(PIN_FAN,GPIO.OUT)

FREQ = 1000 # frequency in Hz
FAN_FREQ = 30 #  flickering effect
   
# Duty Cycle (0 <= dc <=100)

living = GPIO.PWM(PIN_LIVING, FREQ)
living.start(0)
porch = GPIO.PWM(PIN_LAMP, FREQ)
porch.start(0)


#fire = GPIO.PWM(PIN_FAN, FAN_FREQ)
#fire.start(0)
GPIO.setup(PIN_FAN, GPIO.OUT)
def update(m):
    if m['item'] == 'lightpin':
        dc = int(m['value']) * 10
        living.ChangeDutyCycle(dc)

    elif m['item'] == 'lamppin':
        dc = int(m['value']) * 10
        porch.ChangeDutyCycle(dc)

    elif m['item'] == 'fan':
        if m['value'] == 'on' :
            GPIO.output(PIN_FAN, 1)
        else :
            GPIO.output(PIN_FAN, 0)
try:
    while 1:
        try :
            fcon = open('/tmp/control.txt', 'r')
        except :
            fcon = open('/tmp/control.txt', 'w')
            fcon.write('lightpin=0\nlamppin=0\nfan=\'on\'\n')
            fcon.close()
            print('change permissions')
            os.chmod('/tmp/control.txt',0777)
            fcon = open('/tmp/control.txt', 'r')
        control_data_list = fcon.readlines()
        control_data = {}
        for i in control_data_list:
            m = {}
            m['item'] = i.split('=')[0]
            m['value'] = i.split('=')[1]
            update(m)
        fcon.close()
        time.sleep(0.5)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)
	
	
	
	
	
