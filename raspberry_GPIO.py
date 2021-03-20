import RPi.GPIO as GPIO
import time

def Set_Pin():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    # seven segment
    segment_pin = [[37,35,33,31],[32,36,38,40],[29,15,13,11]]
    for i in range(4):
        GPIO.setup(segment_pin[0][i],GPIO.OUT)
        GPIO.setup(segment_pin[1][i],GPIO.OUT)
        GPIO.setup(segment_pin[2][i],GPIO.OUT)

    for i in range(3):
        GPIO.output(segment_pin[i][0],GPIO.LOW)
        GPIO.output(segment_pin[i][1],GPIO.LOW)
        GPIO.output(segment_pin[i][2],GPIO.LOW)
        GPIO.output(segment_pin[i][3],GPIO.LOW)

    # motion sensor
    GPIO.setup(12,GPIO.IN)

    # range sensor
    GPIO.setup(18,GPIO.IN)


def sevenSegment(number):
    segment3 = int(( number % 100 ) % 10)
    segment2 = int((( number % 100 ) - segment3) / 10)
    segment1 = int((( number - (segment2 * 10) ) - segment3) / 100)

    segment_pin = [[37,35,33,31],[32,36,38,40],[29,15,13,11]]

    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setwarnings(False)

    # set GPIO pin for show output
    # for i in range(4):
    #     GPIO.setup(segment_pin[0][i],GPIO.OUT)
    #     GPIO.setup(segment_pin[1][i],GPIO.OUT)
    #     GPIO.setup(segment_pin[2][i],GPIO.OUT)

    senment_binary = ["{0:b}".format(segment1),"{0:b}".format(segment2),"{0:b}".format(segment3)]

    segment_state = [[ GPIO.LOW , GPIO.LOW , GPIO.LOW , GPIO.LOW ] , [ GPIO.LOW , GPIO.LOW , GPIO.LOW , GPIO.LOW ] , [ GPIO.LOW , GPIO.LOW , GPIO.LOW , GPIO.LOW ]]

    for j in range(3):
        for i in range( len(senment_binary[j]) ):
            if len(segment_state[j]) - 1 - i < 0 :
                break ;
            else :
                if senment_binary[j][ len(senment_binary[j]) - 1 - i ] == '1':
                    segment_state[j][ 3 - i ] = GPIO.HIGH
                else :
                    segment_state[j][ 3 - i ] = GPIO.LOW

    # for k in range(3):
    #     for i in range(3):
    #         GPIO.output(segment_pin[i][0],GPIO.HIGH)
    #         GPIO.output(segment_pin[i][1],GPIO.HIGH)
    #         GPIO.output(segment_pin[i][2],GPIO.HIGH)
    #         GPIO.output(segment_pin[i][3],GPIO.HIGH)
    #     time.sleep(0.1)

    #     for i in range(3):
    #         GPIO.output(segment_pin[i][0],segment_state[i][0])
    #         GPIO.output(segment_pin[i][1],segment_state[i][1])
    #         GPIO.output(segment_pin[i][2],segment_state[i][2])
    #         GPIO.output(segment_pin[i][3],segment_state[i][3])
    #     time.sleep(0.5)
    
    for i in range(3):
        GPIO.output(segment_pin[i][0],segment_state[i][0])
        GPIO.output(segment_pin[i][1],segment_state[i][1])
        GPIO.output(segment_pin[i][2],segment_state[i][2])
        GPIO.output(segment_pin[i][3],segment_state[i][3])


def Motion_sensor():
    
    inPut = GPIO.input(12)
    return inPut

def range_sensor():
    inPut = GPIO.input(18)
    return inPut