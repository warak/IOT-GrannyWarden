# client.py
import socket 
import time
import os
import configparser
import DBC.config as cf
import sqlite3 as lite


class pushdb():

    confclient = cf.config()
    # confclient.readconfig()
    print(confclient.gethost())
    print(confclient.getuser())
    host = confclient.gethost()
    user = confclient.getuser()
    user += "\n"
    port = confclient.getport()
    # print(user)

    def __init__(self, s=None):

        if s is None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.s = s

    def connect(self):
        # self.__init__()
        self.s.connect((self.host, self.port))

    def readconfclient(self):
        self.confclient.readconfig()
        self.host = self.confclient.gethost()
        self.user = self.confclient.getuser()
        self.user += "\n"
        self.port = self.confclient.getport()


    def send_action_data(self, action):
        # self.user = self.confclient.getuser()
        '''
        (3, 'Cleaned')")
        (4, 'Serviced')")
        (5, 'Cared')")
        '''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.send(self.user.encode('utf-8'))
        except ConnectionRefusedError:
            print("Server is down")
        except ConnectionError:
            print("connection error")
        except BrokenPipeError:
            print("No connection")
        except Exception as e:
            print(str(e))

        # self.connect()

        # user = config['GW']['userid']
        # print(self.user)


        connected = True
        while connected:
            try:
                print(action)
                backtion = str(action)+"\n"
                s.send(backtion.encode('utf-8'))

                if action == 3:
                    # send cleaned picture
                    f = open('/home/pi/project/Database/PICS/cleaned.png', 'rb')
                    print('sending cleaned picture')
                    l = f.read(1024)
                    while l:
                        s.send(l)
                        l = f.read(1024)
                    f.close()
                    print('Cleaned picture send')
                elif action == 4:
                    # send serviced picture
                    f = open('/home/pi/project/Database/PICS/serviced.png', 'rb')
                    print('sending serviced picture')
                    l = f.read(1024)
                    while l:
                        s.send(l)
                        l = f.read(1024)
                    f.close()
                    print('Serviced picture send')
                elif action == 5:
                    # send cared picture
                    f = open('/home/pi/project/Database/PICS/cared.png', 'rb')
                    print('sending cared picture')
                    l = f.read(1024)
                    while l:
                        s.send(l)
                        l = f.read(1024)
                    f.close()
                    print('Cared picture send')
                elif action == 12:
                    # send sleep database
                    try:
                        f = open('/home/pi/project/Database/sleep.db', 'rb')
                        print('sending sleep db')
                        l = f.read(1024)
                        while l:
                            s.send(l)
                            l = f.read(1024)
                    finally:
                        f.close()
                        os.remove('/home/pi/project/Database/sleep.db')
                        con = lite.connect('/home/pi/project/Database/sleep.db', check_same_thread=False)
                        cur = con.cursor()
                        cur.execute("CREATE TABLE IF NOT EXISTS Sleep(Id INTEGER PRIMARY KEY, Time DATETIME, X NUMERIC, Y NUMERIC, Z NUMERIC)")
                        con.commit
                        con.close()
                    # data = s.recv(1024).decode()
                    # print(data)

                    print('Sleep db send')
                else:
                    f = open('/home/pi/project/Database/ActionData.db', 'rb')
                    print('sending action data')
                    l = f.read(1024)
                    while l:
                        s.send(l)
                        l = f.read(1024)
                    f.close()
                    print('Action data sent')
                connected = False
            except BrokenPipeError:
                print("No connection")
                connected = False
            except Exception as e:
                print(str(e))
                connected = False
            finally:
                print("closing pushdb")
                s.close()
