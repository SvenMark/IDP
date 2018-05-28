'''
Based on Jesse Merritt's script:
https://github.com/jes1510/python_dynamixels

and Josue Alejandro Savage's Arduino library:
http://savageelectronics.blogspot.it/2011/01/arduino-y-dynamixel-ax-12.html
'''

from time import sleep
import RPi.GPIO as GPIO
from serial import Serial


class Ax12:
    # important AX-12 constants
    # /////////////////////////////////////////////////////////// EEPROM AREA
    AX_MODEL_NUMBER_L = 0
    AX_MODEL_NUMBER_H = 1
    AX_VERSION = 2
    AX_ID = 13
    AX_BAUD_RATE = 4
    AX_RETURN_DELAY_TIME = 5
    AX_CW_ANGLE_LIMIT_L = 6
    AX_CW_ANGLE_LIMIT_H = 7
    AX_CCW_ANGLE_LIMIT_L = 8
    AX_CCW_ANGLE_LIMIT_H = 9
    AX_SYSTEM_DATA2 = 10
    AX_LIMIT_TEMPERATURE = 11
    AX_DOWN_LIMIT_VOLTAGE = 12
    AX_UP_LIMIT_VOLTAGE = 13
    AX_MAX_TORQUE_L = 14
    AX_MAX_TORQUE_H = 15
    AX_RETURN_LEVEL = 16
    AX_ALARM_LED = 17
    AX_ALARM_SHUTDOWN = 18
    AX_OPERATING_MODE = 19
    AX_DOWN_CALIBRATION_L = 20
    AX_DOWN_CALIBRATION_H = 21
    AX_UP_CALIBRATION_L = 22
    AX_UP_CALIBRATION_H = 23

    # ////////////////////////////////////////////////////////////// RAM AREA
    AX_TORQUE_STATUS = 24
    AX_LED_STATUS = 25
    AX_CW_COMPLIANCE_MARGIN = 1
    AX_CCW_COMPLIANCE_MARGIN = 1
    AX_CW_COMPLIANCE_SLOPE = 78
    AX_CCW_COMPLIANCE_SLOPE = 79
    AX_GOAL_POSITION_L = 30
    AX_GOAL_POSITION_H = 31
    AX_GOAL_SPEED_L = 32
    AX_GOAL_SPEED_H = 33
    AX_TORQUE_LIMIT_L = 34
    AX_TORQUE_LIMIT_H = 35
    AX_PRESENT_POSITION_L = 36
    AX_PRESENT_POSITION_H = 37
    AX_PRESENT_SPEED_L = 38
    AX_PRESENT_SPEED_H = 39
    AX_PRESENT_LOAD_L = 40
    AX_PRESENT_LOAD_H = 41
    AX_PRESENT_VOLTAGE = 42
    AX_PRESENT_TEMPERATURE = 43
    AX_REGISTERED_INSTRUCTION = 44
    AX_PAUSE_TIME = 45
    AX_MOVING = 46
    AX_LOCK = 47
    AX_PUNCH_L = 0
    AX_PUNCH_H = 0

    # /////////////////////////////////////////////////////////////// Status Return Levels
    AX_RETURN_NONE = 0
    AX_RETURN_READ = 1
    AX_RETURN_ALL = 2

    # /////////////////////////////////////////////////////////////// Instruction Set
    AX_PING = 1
    AX_READ_DATA = 2
    AX_WRITE_DATA = 3
    AX_REG_WRITE = 4
    AX_ACTION = 5
    AX_RESET = 6
    AX_SYNC_WRITE = 131

    # /////////////////////////////////////////////////////////////// Lengths
    AX_RESET_LENGTH = 2
    AX_ACTION_LENGTH = 2
    AX_ID_LENGTH = 4
    AX_LR_LENGTH = 4
    AX_SRL_LENGTH = 4
    AX_RDT_LENGTH = 4
    AX_LEDALARM_LENGTH = 4
    AX_SHUTDOWNALARM_LENGTH = 4
    AX_TL_LENGTH = 4
    AX_VL_LENGTH = 6
    AX_AL_LENGTH = 7
    AX_CM_LENGTH = 6
    AX_CS_LENGTH = 5
    AX_COMPLIANCE_LENGTH = 1
    AX_CCW_CW_LENGTH = 1
    AX_BD_LENGTH = 4
    AX_TEM_LENGTH = 4
    AX_MOVING_LENGTH = 4
    AX_RWS_LENGTH = 4
    AX_VOLT_LENGTH = 4
    AX_LOAD_LENGTH = 4
    AX_LED_LENGTH = 4
    AX_TORQUE_LENGTH = 4
    AX_POS_LENGTH = 4
    AX_GOAL_LENGTH = 5
    AX_MT_LENGTH = 5
    AX_PUNCH_LENGTH = 0
    AX_SPEED_LENGTH = 5
    AX_GOAL_SP_LENGTH = 7

    # /////////////////////////////////////////////////////////////// Specials
    AX_BYTE_READ = 1
    AX_INT_READ = 2
    AX_ACTION_CHECKSUM = 250
    AX_BROADCAST_ID = 254
    AX_START = 255
    AX_CCW_AL_L = 255
    AX_CCW_AL_H = 3
    AX_LOCK_VALUE = 1
    LEFT = 0
    RIGTH = 1
    RX_TIME_OUT = 10
    TX_DELAY_TIME = 0.00002

    # RPi constants
    RPI_DIRECTION_PIN = 23
    RPI_DIRECTION_TX = GPIO.HIGH
    RPI_DIRECTION_RX = GPIO.LOW
    RPI_DIRECTION_SWITCH_DELAY = 0.0001

    # static variables
    port = None
    gpioSet = False

    def __init__(self):
        if (Ax12.port == None):
            Ax12.port = Serial("/dev/serial0", baudrate=1000000, timeout=0.001)
        if (not Ax12.gpioSet):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Ax12.RPI_DIRECTION_PIN, GPIO.OUT)
            Ax12.gpioSet = True
        self.direction(Ax12.RPI_DIRECTION_RX)

    connected_servos = []

    # Error lookup dictionary for bit masking
    dict_errors = {1: "Input Voltage",
                  2: "Angle Limit",
                  4: "Overheating",
                  8: "Range",
                  16: "Checksum",
                  32: "Overload",
                  64: "Instruction"
                  }

    # Custom error class to report AX servo errors
    class ax_error(Exception):
        pass

    # Servo timeout
    class timeout_error(Exception):
        pass

    def direction(self, d):
        GPIO.output(Ax12.RPI_DIRECTION_PIN, d)
        sleep(Ax12.RPI_DIRECTION_SWITCH_DELAY)

    def read_data(self, id):
        self.direction(Ax12.RPI_DIRECTION_RX)
        reply = Ax12.port.read(5)  # [0xff, 0xff, origin, length, error]
        try:
            # assert ord(reply[0]) == 0xFF
            assert reply[0] == 0xFF
        except:
            e = "Timeout on servo " + str(id)





            # raise Ax12.timeout_error(e)








        try:
            # length = ord(reply[3]) - 2
            # error = ord(reply[4])
            length = reply[3] - 2
            error = reply[4]

            if (error != 0):
                print("Error from servo: " + Ax12.dict_errors[error] + ' (code  ' + hex(error) + ')')
                return -error
            # just reading error bit
            elif (length == 0):
                return error
            else:
                if (length > 1):
                    reply = Ax12.port.read(2)
                    # return_value = (ord(reply[1])<<8) + (ord(reply[0])<<0)
                    return_value = (reply[1] << 8) + (reply[0] << 0)
                else:
                    reply = Ax12.port.read(1)
                    return_value = reply[0]
                return return_value
        except:
            pass
        # except Exception, detail:
        #     raise Ax12.ax_error(detail)

    def ping(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_READ_DATA + Ax12.AX_PING)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_READ_DATA])
        out_data += bytes([Ax12.AX_PING])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def factory_reset(self, id, confirm=False):
        if (confirm):
            self.direction(Ax12.RPI_DIRECTION_TX)
            Ax12.port.flushInput()
            checksum = (~(id + Ax12.AX_RESET_LENGTH + Ax12.AX_RESET)) & 0xff
            out_data = bytes([Ax12.AX_START])
            out_data += bytes([Ax12.AX_START])
            out_data += bytes([id])
            out_data += bytes([Ax12.AX_RESET_LENGTH])
            out_data += bytes([Ax12.AX_RESET])
            out_data += bytes([checksum])
            Ax12.port.write(out_data)
            sleep(Ax12.TX_DELAY_TIME)
            return self.read_data(id)
        else:
            print(
                "nothing done, please send confirm = True as this fuction reset to the factory default value, i.e reset the motor ID")
            return

    def set_id(self, id, new_id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_ID_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_ID + new_id)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_ID_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_ID])
        out_data += bytes([new_id])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_baudrate(self, id, baudrate):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        br = ((2000000 / long(baudrate)) - 1)
        checksum = (~(id + Ax12.AX_BD_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_BAUD_RATE + br)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_BD_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_BAUD_RATE])
        out_data += bytes([br])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_status_return_level(self, id, level):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_SRL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_RETURN_LEVEL + level)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_SRL_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_RETURN_LEVEL])
        out_data += bytes([level])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_return_delay_time(self, id, delay):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_RDT_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_RETURN_DELAY_TIME + (
                    int(delay) / 2) & 0xff)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_RDT_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_RETURN_DELAY_TIME])
        out_data += bytes([(int(delay) / 2) & 0xff])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def lock_register(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_LR_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_LOCK + Ax12.AX_LOCK_VALUE)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_LR_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_LOCK])
        out_data += bytes([Ax12.AX_LOCK_VALUE])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def move(self, id, position):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [position & 0xff, position >> 8]
        checksum = (~(id + Ax12.AX_GOAL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_GOAL_POSITION_L + p[0] + p[1])) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_GOAL_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_GOAL_POSITION_L])
        out_data += bytes([p[0]])
        out_data += bytes([p[1]])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def move_speed(self, id, position, speed):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [position & 0xff, position >> 8]
        s = [speed & 0xff, speed >> 8]
        checksum = (~(
                    id + Ax12.AX_GOAL_SP_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_GOAL_POSITION_L + p[0] + p[1] + s[0] + s[
                1])) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_GOAL_SP_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_GOAL_POSITION_L])
        out_data += bytes([p[0]])
        out_data += bytes([p[1]])
        out_data += bytes([s[0]])
        out_data += bytes([s[1]])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def move_rw(self, id, position):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [position & 0xff, position >> 8]
        checksum = (~(id + Ax12.AX_GOAL_LENGTH + Ax12.AX_REG_WRITE + Ax12.AX_GOAL_POSITION_L + p[0] + p[1])) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_GOAL_LENGTH])
        out_data += bytes([Ax12.AX_REG_WRITE])
        out_data += bytes([Ax12.AX_GOAL_POSITION_L])
        out_data += bytes([p[0]])
        out_data += bytes([p[1]])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def move_speed_rw(self, id, position, speed):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [position & 0xff, position >> 8]
        s = [speed & 0xff, speed >> 8]
        checksum = (~(
                    id + Ax12.AX_GOAL_SP_LENGTH + Ax12.AX_REG_WRITE + Ax12.AX_GOAL_POSITION_L + p[0] + p[1] + s[0] + s[
                1])) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_GOAL_SP_LENGTH])
        out_data += bytes([Ax12.AX_REG_WRITE])
        out_data += bytes([Ax12.AX_GOAL_POSITION_L])
        out_data += bytes([p[0]])
        out_data += bytes([p[1]])
        out_data += bytes([s[0]])
        out_data += bytes([s[1]])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def action(self):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_BROADCAST_ID])
        out_data += bytes([Ax12.AX_ACTION_LENGTH])
        out_data += bytes([Ax12.AX_ACTION])
        out_data += bytes([Ax12.AX_ACTION_CHECKSUM])
        Ax12.port.write(out_data)
        # sleep(Ax12.TX_DELAY_TIME)

    def set_torque_status(self, id, status):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        ts = 1 if ((status == True) or (status == 1)) else 0
        checksum = (~(id + Ax12.AX_TORQUE_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_TORQUE_STATUS + ts)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_TORQUE_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_TORQUE_STATUS])
        out_data += bytes([ts])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_led_status(self, id, status):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        ls = 1 if ((status == True) or (status == 1)) else 0
        checksum = (~(id + Ax12.AX_LED_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_LED_STATUS + ls)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_LED_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_LED_STATUS])
        out_data += bytes([ls])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_temperature_limit(self, id, temp):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_TL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_LIMIT_TEMPERATURE + temp)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_TL_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_LIMIT_TEMPERATURE])
        out_data += bytes([temp])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_voltage_limit(self, id, low_volt, high_volt):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(
                    id + Ax12.AX_VL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_DOWN_LIMIT_VOLTAGE + low_volt + high_volt)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_VL_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_DOWN_LIMIT_VOLTAGE])
        out_data += bytes([low_volt])
        out_data += bytes([high_volt])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_angle_limit(self, id, cw_limit, ccw_limit):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        cw = [cw_limit & 0xff, cw_limit >> 8]
        ccw = [ccw_limit & 0xff, ccw_limit >> 8]
        checksum = (~(id + Ax12.AX_AL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_CW_ANGLE_LIMIT_L + cw[0] + cw[1] + ccw[0] +
                      ccw[1])) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_AL_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_CW_ANGLE_LIMIT_L])
        out_data += bytes([cw[0]])
        out_data += bytes([cw[1]])
        out_data += bytes([ccw[0]])
        out_data += bytes([ccw[1]])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_torque_limit(self, id, torque):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        mt = [torque & 0xff, torque >> 8]
        checksum = (~(id + Ax12.AX_MT_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_MAX_TORQUE_L + mt[0] + mt[1])) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_MT_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_MAX_TORQUE_L])
        out_data += bytes([mt[0]])
        out_data += bytes([mt[1]])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_punch_limit(self, id, punch):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [punch & 0xff, punch >> 8]
        checksum = (~(id + Ax12.AX_PUNCH_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_PUNCH_L + p[0] + p[1])) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_PUNCH_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_PUNCH_L])
        out_data += bytes([p[0]])
        out_data += bytes([p[1]])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_compliance(self, id, cw_margin, ccw_margin, cw_slope, ccw_slope):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(
                    id + Ax12.AX_COMPLIANCE_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_CW_COMPLIANCE_MARGIN + cw_margin + ccw_margin + cw_slope + ccw_slope)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_COMPLIANCE_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_CW_COMPLIANCE_MARGIN])
        out_data += bytes([cw_margin])
        out_data += bytes([ccw_margin])
        out_data += bytes([cw_slope])
        out_data += bytes([ccw_slope])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_led_alarm(self, id, alarm):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_LEDALARM_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_ALARM_LED + alarm)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_LEDALARM_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_ALARM_LED])
        out_data += bytes([alarm])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def set_shutdown_alarm(self, id, alarm):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_SHUTDOWNALARM_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_ALARM_SHUTDOWN + alarm)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_SHUTDOWNALARM_LENGTH])
        out_data += bytes([Ax12.AX_WRITE_DATA])
        out_data += bytes([Ax12.AX_ALARM_SHUTDOWN])
        out_data += bytes([alarm])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def read_temperature(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(
                    id + Ax12.AX_TEM_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_TEMPERATURE + Ax12.AX_BYTE_READ)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_TEM_LENGTH])
        out_data += bytes([Ax12.AX_READ_DATA])
        out_data += bytes([Ax12.AX_PRESENT_TEMPERATURE])
        out_data += bytes([Ax12.AX_BYTE_READ])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def read_position(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(
                    id + Ax12.AX_POS_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_POSITION_L + Ax12.AX_INT_READ)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_POS_LENGTH])
        out_data += bytes([Ax12.AX_READ_DATA])
        out_data += bytes([Ax12.AX_PRESENT_POSITION_L])
        out_data += bytes([Ax12.AX_INT_READ])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def read_voltage(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(
                    id + Ax12.AX_VOLT_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_VOLTAGE + Ax12.AX_BYTE_READ)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_VOLT_LENGTH])
        out_data += bytes([Ax12.AX_READ_DATA])
        out_data += bytes([Ax12.AX_PRESENT_VOLTAGE])
        out_data += bytes([Ax12.AX_BYTE_READ])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def read_speed(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(
                    id + Ax12.AX_SPEED_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_SPEED_L + Ax12.AX_INT_READ)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_SPEED_LENGTH])
        out_data += bytes([Ax12.AX_READ_DATA])
        out_data += bytes([Ax12.AX_PRESENT_SPEED_L])
        out_data += bytes([Ax12.AX_INT_READ])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def read_load(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_LOAD_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_LOAD_L + Ax12.AX_INT_READ)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_LOAD_LENGTH])
        out_data += bytes([Ax12.AX_READ_DATA])
        out_data += bytes([Ax12.AX_PRESENT_LOAD_L])
        out_data += bytes([Ax12.AX_INT_READ])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def read_moving_status(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_MOVING_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_MOVING + Ax12.AX_BYTE_READ)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_MOVING_LENGTH])
        out_data += bytes([Ax12.AX_READ_DATA])
        out_data += bytes([Ax12.AX_MOVING])
        out_data += bytes([Ax12.AX_BYTE_READ])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def read_rw_status(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(
                    id + Ax12.AX_RWS_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_REGISTERED_INSTRUCTION + Ax12.AX_BYTE_READ)) & 0xff
        out_data = bytes([Ax12.AX_START])
        out_data += bytes([Ax12.AX_START])
        out_data += bytes([id])
        out_data += bytes([Ax12.AX_RWS_LENGTH])
        out_data += bytes([Ax12.AX_READ_DATA])
        out_data += bytes([Ax12.AX_REGISTERED_INSTRUCTION])
        out_data += bytes([Ax12.AX_BYTE_READ])
        out_data += bytes([checksum])
        Ax12.port.write(out_data)
        sleep(Ax12.TX_DELAY_TIME)
        return self.read_data(id)

    def learn_servos(self, min_value=1, max_value=6, verbose=False):
        servo_list = []
        for i in range(min_value, max_value + 1):
            try:
                temp = self.ping(i)
                servo_list.append(i)
                if verbose: print("Found servo #" + str(i))
                time.sleep(0.1)

            # except Exception, detail:
            except:
                # if verbose : print("Error pinging servo #" + str(i) + ': ' + str(detail))
                pass
        return servo_list

#
# def playPose() :
#    '''
#    Open a file and move the servos to specified positions in a group move
#    '''
#    infile=open(Arguments.playpose, 'r')    # Open the file
#    poseDict = {}                           # Dictionary to hold poses and positions
#    if Arguments.verbose : print "Reading pose from", Arguments.playpose
#    for line in infile.readlines() :        # Read the file and step through it
#        servo = int(line.split(':')[0])     # Servo is first
#        position = int(line.split(':')[1])  # Position is second
#        poseDict[servo]=position            # add the servo to the Dictionary
#
#    groupMove2(poseDict)
#
#
#
# def writePose() :
#    '''
#    Read the servos and save the positions to a file
#    '''
#    of = open(Arguments.savepose, 'w')      # open the output file
#    pose = getPose2(connected_servos)        # get the positions
#    if Arguments.verbose :
#        print "Servo Positions"
#        print "---------------"
#
#    for key in  pose.keys():                # step through the keys, writing to the file
#        if Arguments.verbose : print "Servo " + str(key), pose[key]
#        of.write(str(key) + ':' + str(pose[key]) + '\n')    # Write to the file
#
#    if Arguments.verbose :
#        print "Wrote pose to " + Arguments.savepose
#        print
#
#    of.close()      # close the file
#
