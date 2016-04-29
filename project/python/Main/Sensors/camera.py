import picamera
import time


class Camera:

    def takepicture(who):

        try:
            camera = picamera.PiCamera()
            camera.rotation = 180
            # camera.start_preview()
            # time.sleep(2)
            print(camera.recording)
            # if camera.recording == 0:
            camera.capture('/home/pi/project/Database/PICS/%s.png' % who)
            camera.close()
        except:
            print("fail")

