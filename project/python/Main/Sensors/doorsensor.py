import RPi.GPIO as GPIO
import time
import DBC.dbcreate as dbc
import numpy as np
import picamera
import picamera.array


class Doorsensor():
    channel = 12

    # def __init__(self):
        # tes="tes"

    # not in use
    def dooropen(self):
        print("Door open")
        dbcl = dbc.DBClient
        dbcl.createaction(self, 9, 0)
        time.sleep(300)

    def doorclosed(self):
        print("Door closed")
        dbcl = dbc.DBClient



        with picamera.PiCamera() as camera:
            with DetectMotion(camera) as output:
                camera.resolution = (640, 480)
                camera.start_recording(
                    '/dev/null', format='h264', motion_output=output)
                camera.wait_recording(30)
                camera.stop_recording()
                # time.sleep(30)
                flag = output.getflag()
                if flag == 0:
                    print("saving to db left home")
                    dbcl.createaction(self, 9, 0)
                else:
                    print("Saving to db came home")
                    dbcl.createaction(self, 10, 0)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(channel, GPIO.RISING, callback=doorclosed, bouncetime=300)


class DetectMotion(picamera.array.PiMotionAnalysis):
    movement = 0
    flag = 0

    def analyse(self, a):
        self.movement += 1
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        #time.sleep(3)
        if (a > 60).sum() > 10 & self.movement > 4:
            print('Motion detected!')
            self.flag = 1
            print(self.movement)

    def getflag(self):
        return self.flag



