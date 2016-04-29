import DBC.dbcreate as dbc
import Sensors.camera as cam
import time


class ActionControl:
    def actcontrol(self, **kwargs):
        # con = lite.connect('/home/pi/project/Database/ActionData.db')
        # cur = con.cursor()
        dbcl = dbc.DBClient
        cmra = cam.Camera
        for name, value in kwargs.items():
            if name == "hrs":
                dbcl.createaction(self, 1, value)

            if name == "back":
                dbcl.createaction(self, 2, 0)

            if name == "act":
                if value == "112":
                    print("calling 112")
                    dbcl.createaction(self, 6, 0)
                if value == "cleaning":
                    print("calling cleaning")
                    dbcl.createaction(self, 7, 0)
                if value == "care":
                    print("calling caretaker ")
                    dbcl.createaction(self, 8, 0)

            if name == "react":
                if value == "cleaned":
                    print("saving to db cleaned")
                    cmra.takepicture(value)
                    time.sleep(1)
                    dbcl.createaction(self, 3, 0)

                if value == "serviced":
                    print("saving to db serviced")
                    cmra.takepicture(value)
                    time.sleep(1)
                    dbcl.createaction(self, 4, 0)
                if value == "cared":
                    print("saving to db cared")
                    cmra.takepicture(value)
                    time.sleep(1)
                    dbcl.createaction(self, 5, 0)