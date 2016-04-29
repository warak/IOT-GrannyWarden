import configparser
import socket
import time
from tkinter import *


class config:

    config = configparser.ConfigParser()
    host = "192.168.53.16"
    port = 5050
    user = ""

    def createconfig(self):
        self.config['GW'] = {'ServerHost': self.host,
                        'ServerPort': self.port,
                        'userid': ''}

        with open('/home/pi/project/Database/config.ini', 'w') as configfile:
            self.config.write(configfile)

    def checkid(self):
        self.readconfig()
        if self.user == '':
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host, self.port))
                # s.connect(('192.168.53.31', 5050))
                connected = True
                # Receive no more than 1024 bytes
                # userid = self.askname()
                userid = input("insert username here")

                userid += "\n"
                print(userid)
                s.send(userid.encode('ascii'))
                while connected:
                    data = s.recv(1024).decode()
                    print(data)
                    #connected = False
                    if len(data) == 15:
                        # file = open('/home/pi/project/Database/%s.txt'%data, 'w+')
                        # file.write(data)
                        self.config['GW'] = {'ServerHost': self.host,
                                            'ServerPort': self.port,
                                            'userid': data}

                        with open('/home/pi/project/Database/config.ini', 'w') as configfile:
                            self.config.write(configfile)

                        self.readconfig()
                        connected = False
                    else:
                        print('Connection failed')
                        connected = False
                        #print('waiting for servers answer')
                    # time.sleep(5)
                s.close()
            except Exception as e:
                print(str(e))

    def readconfig(self):
        # self.config = configparser.ConfigParser()
        # config.sections()
        try:
            self.config.read('/home/pi/project/Database/config.ini')
            # config.sections()
            self.host = self.config['GW']['serverhost']
            self.port = int(self.config['GW']['serverport'])
            self.user = self.config['GW']['userid']
        except FileNotFoundError:
            self.createconfig()
            self.readconfig()
        except Exception:
            self.createconfig()
            self.readconfig()

    def gethost(self):
        return self.host

    def getport(self):
        return self.port

    def getuser(self):
        return self.user






