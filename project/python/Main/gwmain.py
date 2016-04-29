import threading
import time
import tkinter as tk
import UI.userinterface as ui
import Sensors.accstartuptest as act
import Sensors.doorsensor as ds
import DBC.dbcreate as dbc
import Sensors.accthread as acct
import CTRL.tracker as track
import DBC.config as cf

# import UI.pageaccesscontrol


class GwMain(tk.Tk):
    def __init__(self, *args, **kwargs):
        # tk.Tk.__init__(self, *args, **kwargs)
        p = "testi"

if __name__ == "__main__":
    # accelemeter testing
    try:
        #accelometer
        acc = act.Accelometer()
        txtAcc = acc.testonline()
        print(txtAcc)

        # config
        cfc = cf.config()
        # cfc.createconfig()
        # cfc.readconfig()
        cfc.checkid()
        # door sensor
        door_sensor = ds.Doorsensor()
        dbc = dbc.DBClient()
        # database creation
        dbc.create()
        dbc.readconfclient()
        # bed sensor threading
        accthread = acct.accThread()
        accthread.daemon = True
        accthread.start()
        # tracker
        tracker = track.Tracker()
        tracker.daemon = True
        tracker.start()
        # UI
        app = ui.Ui()
        app.mainloop()
        # kill all after ui KILL
    except(KeyboardInterrupt, SystemExit):
        raise
    except:
        raise



