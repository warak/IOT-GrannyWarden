import socket
import DBC.dbcreate as dbc
from threading import Thread
import threading

import time
import datetime
from microstacknode.hardware.accelerometer.mma8452q import MMA8452Q
import sqlite3 as lite
import sys


try:
    from Queue import Queue, Empty
except:
    from queue import Queue, Empty

THRESSHOLD = 100


class accThread(Thread):

    qx = Queue()
    qy = Queue()
    qz = Queue()
    con = None
    sleepingflag = False
    dbcl = dbc.DBClient

    G_RANGE = 2
    INTERVAL = 1  # seconds

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = '192.168.45.158'
    # HOST = '192.168.0.6'
    PORT = 12397
    BUFF = 1024000

    date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')


    #Routine that processes whatever you want as background
    def Accelerometer(self):

        with MMA8452Q() as accelerometer:
            date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
            print(date)
            con = lite.connect('/home/pi/project/Database/sleep.db', check_same_thread=False)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Sleep(Id INTEGER PRIMARY KEY, Time DATETIME, X NUMERIC, Y NUMERIC, Z NUMERIC)")
            # Configure (This is completely optional -- shown here as an example)
            accelerometer.standby()
            accelerometer.set_g_range(self.G_RANGE)
            accelerometer.activate()
            #print("g = {}".format(G_RANGE))
            time.sleep(self.INTERVAL)  # settle
            # print data
            oldraw = accelerometer.get_xyz(raw=True)
            x=0
            y=0
            z=0
            while True:

                for i in range(30):
                    raw = accelerometer.get_xyz(raw=True)
                    raw['x'] =abs(oldraw['x']-raw['x'])
                    raw['y'] =abs(oldraw['y']-raw['y'])
                    raw['z'] =abs(oldraw['z']-raw['z'])
                    self.qx.put(raw['x'])
                    self.qy.put(raw['y'])
                    self.qz.put(raw['z'])
                    oldraw = accelerometer.get_xyz(raw=True)
                    time.sleep(self.INTERVAL)
                    raw['x']=0
                    raw['y']=0
                    raw['z']=0
                    i = 0
                while not self.qx.empty():
                    if i>0:
                        raw['x']+=self.qx.get()
                        raw['y']+=self.qy.get()
                        raw['z']+=self.qz.get()
                    i = i+1
    #                q.task_done()
                if raw['x'] > THRESSHOLD:
                    if not self.sleepingflag:
                        self.sleepingflag = True
                        print("sleeping")
                        # con = lite.connect('/home/pi/project/Database/sleep.db', check_same_thread=False)
                        self.dbcl.createaction(self, 11, 0)
                    try:
                        con = lite.connect('/home/pi/project/Database/sleep.db', check_same_thread=False)
                        cur = con.cursor()
                        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M')
                        cur.execute("INSERT INTO Sleep(Time, X, Y, Z) VALUES('{}','{:.4f}','{:.4f}','{:.4f}')".format(date,raw['x'],raw['y'],raw['z']))
                        # cur.execute("SELECT * FROM Sleep")
                        con.commit()
                        con.close()
                    except Exception as e:
                        print("accthread:"+str(e))

                elif self.sleepingflag:
                    print("woke up")
                    self.sleepingflag = False
                    self.dbcl.createaction(self, 12, 0)

    def run(self):
        self.Accelerometer()

    def issleeping(self):
        return self.sleepingflag



'''lag
if __name__ == "__main__":
   while True:

        print("pääohjelma käynnissä")
        time.sleep(5000)

'''