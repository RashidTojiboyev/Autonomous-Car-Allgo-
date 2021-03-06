from  allgo_utils import PCA9685,ultrasonic,ir_sens
import wiringpi as wp
import time

DIR_DISTANCE_ALERT = 20
preMillis = 0

ULTRASONIC_TRIG	= 3 # TRIG port is to use as output signal
ULTRASONIC_ECHO = 23 # ECHO port is to use as input signal
OUT = {'front_left_led':5,
       'front_right_led':0,
       'rear_right_led':1,
       'rear_left_led':2,
       'ultra_trig':3} # 5:front_left_led, 0:front_right_led, 1:rear_right_led, 2:rear_left_led, 3:ultra_trig
IN = {'left_IR':21,
      'center_IR':22,
      'right_IR':26,
      'ultra_echo':23} # 21:left_IR, 22:center_IR, 26:right_IR, 23:ultra_echo


LOW = 0
HIGH = 1
OUTPUT = wp.OUTPUT
INPUT = wp.INPUT


pca = PCA9685()
ultra = ultrasonic(ULTRASONIC_TRIG,ULTRASONIC_ECHO)
def setup():
    wp.wiringPiSetup()  # Initialize wiringPi to load Raspbarry Pi PIN numbering scheme
    for key in OUT:
        wp.pinMode(OUT[key],OUTPUT)
        wp.digitalWrite(OUT[key], LOW)
    for key in IN:
        wp.pinMode(IN[key],INPUT)
def warn(times=3):
    for i in range(times):
        wp.digitalWrite(OUT['front_right_led'], HIGH)
        wp.digitalWrite(OUT['front_left_led'], HIGH)

        wp.digitalWrite(OUT['rear_right_led'], HIGH)
        wp.digitalWrite(OUT['rear_left_led'], HIGH)
        time.sleep(0.15)

        wp.digitalWrite(OUT['front_right_led'], LOW)
        wp.digitalWrite(OUT['front_left_led'], LOW)

        wp.digitalWrite(OUT['rear_right_led'], LOW)
        wp.digitalWrite(OUT['rear_left_led'], LOW)
        time.sleep(0.15)

def ex1():
    """1. DC Motor Application
        Create a program that:  - Turn smoothly"""
    while(True):
        pca.go_left(speed_cur=85,turning_rate=0.8)
        time.sleep(2)
        pca.stop()
        time.sleep(2)
        pca.go_right(speed_cur=85,turning_rate=0.8)
        time.sleep(2)
        pca.stop()
        #time.sleep(2)
        pass

    pass

def ex2():
    """2.Ultrasonic sensor application
         Create a program that
            1. Go forward
            2. Stop and flicker warning light when an Object is closer than 30cm"""


    pca.stop()
    pca.set_normal_speed(80)
    while True:

        dist = ultra.distance()

        print 'Distance(cm):%.2f'%dist
        if dist>50:
            pca.set_normal_speed(120)
            pca.go_forward()
        elif dist>40:
            pca.set_normal_speed(70)
            pca.go_forward()
        #elif dist>30:
        #    pca.set_normal_speed(60)
        #    pca.go_forward()
        elif dist<30:
            pca.stop()
            warn(1)
        #time.sleep(0.001)
    pass

def ex3():
    """3.Ultrasonic Sensor Application
         Create a program that Keep the 50cm distance with an object"""
    pca.stop()
    pca.set_normal_speed(85)
    while True:

        dist = ultra.distance()
        print 'Distance(cm):%.2f' % dist
        if dist > 52:
            pca.go_forward()
        elif dist<48:
            pca.go_back()
        else:
            pca.stop_extreme()
        #time.sleep(0.2)
    pass
def ex4():
    """4.IR sensor application
        Create a program with TCRT 5000 IR sensor
            1. Go straight until it detect the 2nd black belt
            2. Stop"""
    count=0
    state = False
    state_old=False
    while(count!=2):
        l_ir = wp.digitalRead(IN['left_IR'])
        c_ir = wp.digitalRead(IN['center_IR'])
        r_ir = wp.digitalRead(IN['right_IR'])

        pca.go_forward(speed_cur=70)
        print 'left:%d center:%d right:%d '%(l_ir,c_ir,r_ir)
        if bool(c_ir) is True:
            state = True
            if(state_old != state):
                count += 1
                if count == 2:
                    pca.stop()
                    break
                state = state_old
            time.sleep(0.2)
    pca.stop_extreme()
    pass
def ex4_demo():
    count = 0
    state = False
    while (True):
        l_ir = wp.digitalRead(IN['left_IR'])
        c_ir = wp.digitalRead(IN['center_IR'])
        r_ir = wp.digitalRead(IN['right_IR'])

        print 'left:%d center:%d right:%d ' % (l_ir, c_ir, r_ir)
        if bool(c_ir)==True:
            warn(1)
        time.sleep(0.2)
def ex5():
    """5.Multiple Sensor Application
         Create a program that
             Trace the line
             Stop, beep the buzzer and flicker warning light when obstacle is detected
             Wait until no object detected on the line.
             Stop on stop line"""

    pca.set_normal_speed(100)
    def detect(l_ir, c_ir, r_ir):

        if bool(l_ir) and (bool(r_ir) is False) is True:
            pca.go_left()
        elif bool(r_ir) and (bool(r_ir) is False) is True:
            pca.go_right()
        elif bool(c_ir) is True:
            pca.go_forward()
        else:
            pca.stop()
        print l_ir, c_ir, r_ir
        time.sleep(0.3)

    count = 0
    state = False
    state_old = False

    while True:
        l_ir = wp.digitalRead(IN['left_IR'])
        c_ir = wp.digitalRead(IN['center_IR'])
        r_ir = wp.digitalRead(IN['right_IR'])

        # detect if obstacle
        dist = ultra.distance()
        print 'Distance(cm):%.2f' % dist

        if dist < 30:
            pca.stop()
            warn()
            continue
        #detect and follow line
        detect(l_ir, c_ir, r_ir)
        print 'left:%d center:%d right:%d ' % (l_ir, c_ir, r_ir)
        """if bool(c_ir) is True:
            state = True
            if (state_old != state):
                count += 1
                if count == 4:
                    pca.stop()
                    break
                state = state_old"""
        print 'Current Speed: ', pca.nSpeed
    pass

def ex2_demo():
    """2.Ultrasonic sensor application
         Create a program that
            1. Go forward
            2. Stop and flicker warning light when an Object is closer than 30cm"""
    pca.stop()
    pca.go_forward(speed_cur=255)
    time.sleep(1)
    start_ = time.time()
    print 'stop started: ', start_

    dist=ultra.distance()
    print dist
    pca.stop()
    end_= time.time()

    print 'stop stopped', end_ , ultra.distance()


    pass
def test_forward(sp=45):
    pca.go_forward(delay=1.1,speed_cur=sp)
    time.sleep(0)
    pca.stop()
def test_right():
    
    #pca.go_forward(delay=0.02)
    for i in range(5):
        pca.go_right(speed_max=120,speed_norm=70,delay=0.05,motor_back=False)
        time.sleep(0.5)
    #pca.go_left(speed_max=120,speed_norm=70,delay=0.05,motor_back=False)
    #time.sleep(0.5)
    #pca.go_forward()
    #time.sleep(0.5)
    pca.stop()
    
def test_left():
    for i in range(20):
        pca.go_left(speed_max=100,speed_norm=70,delay=0.05,motor_back=False)
    pca.stop()
def test_begin():
    #pca.go_forward(delay=1.2)
    pca.go_right(delay=0.5, speed_max=100, speed_norm=70,motor_back=True)
    pca.stop()

            
    
def main():
    setup()
    while(True):
        print 'Welcome to the Home work assignment'
        print 'Please select exercise to run:\n' \
              '1 - DC Motor Application\n' \
              '2 - Ultrasonic sensor application\n' \
              '3 - Ultrasonic sensor application\n' \
              '4 - IR sensor application\n' \
              '5 - Multiple Sensor Application\n'\
              '6 - TEST RIGHT\n' \
              '7 - TEST Left\n'
            
        
        inp=[int(x) for x in raw_input().split()]
        menu=inp[0]
        if menu == 1:
            ex1()
        elif menu == 2:
            ex2()
        elif menu == 3:
            ex3()
        elif menu == 4:
            ex4()
        elif menu == 5:
            ex5()
        elif menu == 6:
            test_right()
        elif menu == 7:
            test_left()
        elif menu == 8:
            test_forward(sp=inp[1])
        elif menu == 9:
            test_begin()

    pass
#here

if __name__ == "__main__":
    main()