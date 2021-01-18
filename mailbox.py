import time
import RPi.GPIO as GPIO
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.clock import Clock
GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 16
GPIO_ECHO = 12
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO_SERVOMOTOR = 5 # adapt to your wiring
fPWM = 50  # Hz (not higher with software )
a = 10
b = 2

GPIO.setup(GPIO_SERVOMOTOR, GPIO.OUT)
pwm = GPIO.PWM(GPIO_SERVOMOTOR, fPWM)
pwm.start(0)
upperBound = 12
lowerBound = 6.5
direction = 90
'''

    try:
        while True:
            GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, GPIO.LOW)
            while GPIO.input(GPIO_ECHO) == 0:
                startTime = time.time()
            while GPIO.input(GPIO_ECHO) == 1:
                endTime = time.time()
            timeSpan = endTime - startTime
            dist = 17150 * timeSpan
            if dist > upperBound:
                direction = 90
            elif dist < lowerBound and direction == 90:
                direction = 0
            setDirection(direction)
            time.sleep(1)
            print('distance {:.1f} cm'.format(dist))
    except KeyboardInterrupt:
        print("stop detect")
    finally:
        direction = 0    
        setDirection(0)    
        GPIO.cleanup() 

'''



class BoxLayoutApp(App):
    
    letters = NumericProperty(0)

    layout = BoxLayout(orientation = "horizontal")
    def build(self):
        #layout = BoxLayout(orientation = "horizontal")
        self.setDirection(direction)
        btn_open = Button(text = "Open The MailBox")
        btn_open.bind(on_press = self.open_lock) # bind function
        

        self.letter_num = Label(text = str(self.letters))
       
       
        self.layout.add_widget(btn_open)
        self.layout.add_widget(self.letter_num)
        Clock.schedule_interval(self.update, 0.1) 
        Clock.schedule_interval(self.sonic_detect, 0.07)
        return self.layout 
    def setDirection(self, _direction):

        duty = a / 180 * _direction + b
        pwm.ChangeDutyCycle(duty)
        print ("direction =", _direction, "-> duty =", duty)
        time.sleep(1) # allow to settle
    def open_lock(self,arg): 
        _direction = 0
        duty = a / 180 * _direction + b
        pwm.ChangeDutyCycle(duty)
        time.sleep(15)
        self.letters = 0
        _direction = 90
        duty = a / 180 * _direction + b
        pwm.ChangeDutyCycle(duty)
    def update(self, *args):
        self.letter_num.text = str(self.letters)   
    def sonic_detect(self, arg):
            
        try:
       
            GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, GPIO.LOW)
            while GPIO.input(GPIO_ECHO) == 0:
                startTime = time.time()
            while GPIO.input(GPIO_ECHO) == 1:
                endTime = time.time()
            timeSpan = endTime - startTime
            dist = 17150 * timeSpan
               
            if dist < lowerBound: # put in mail once a time
                self.letters += 1
            #setDirection(direction)
            
            time.sleep(0.05)
            print('distance {:.1f} cm'.format(dist))
        except KeyboardInterrupt:
            print("stop detect")
            direction = 90    
            setDirection(90)    
            GPIO.cleanup() 
BoxLayoutApp().run()


