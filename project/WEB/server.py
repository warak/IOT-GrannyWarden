import socketserver
import os
import threading
import time
import datetime
import sqlite3 as lite
import sys
import random
import string

HOST ='192.168.53.12'
PORT = 5050 

class MyTCPHandler(socketserver.StreamRequestHandler):


    #id = 0
    #def readline(self):
    #    server.request_line= self.rfile.readline().rstrip('\r\n')
    def handle(self):
        #clientsocket,addr = self.accept()
        #print("Got a connection from %s" % str(addr))
        while True:
            self.data = self.rfile.readline().decode('utf-8')
            if not self.data:
                print('DISCONNECTED')
                break
            data = str(self.data)
            print(len(data))
            if (len(data) == 16):
                usr = data[0:15]
                print ("got connection from id: %s"% usr)
                #out = data[0:15]
            elif(len(data)>4 and len(data)<16):
                usr= str(self.data)
                usr= usr[:-1]
                con=lite.connect('recdb/grannylist.db')
                cur=con.cursor()
                cur.execute("SELECT Uid FROM Grannys WHERE Username = '%s' OR Uid = '%s'"% (usr, usr))
                row = cur.fetchone()
                print(row)
                if row:
                    out=','.join(map(str, row))
                else:
                    print('got none type')
                    print(row)
                    break
            #out = '5L7VDF04SZ6MTQJ'
            #print(out)
                if out == 'None':
                    #self.id_generator()
                    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
                    cur.execute("UPDATE Grannys SET Uid = '%s' WHERE Username='%s'" % (id, usr))
                    con.commit()
                    connect = False
                    self.wfile.write(id.encode('ascii'))
                    os.makedirs('/var/www/html/recdb/%s'% id)
            elif (len(data) < 4):
                print ("latest action id is %s"% data)
                if (int(data[0:2]) == 12):
                    date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
                    f= open('recdb/%s/%s_%s_sleep.db'% (usr,usr,date),'wb')
                    #id= clientsocket.recv(1024).decode
                    l = self.rfile.read(1024)
                    while l:
                        print ("getting some data...")
                        f.write(l)
                        l = self.rfile.read(1024)
                    print("all done here!(sleep data)")
                    f.close()

                    db_a = lite.connect('recdb/%s/%s_sleep.db'% (usr,usr))
                    db_b = lite.connect('recdb/%s/%s_%s_sleep.db'% (usr,usr,date))
                    b_cursor = db_b.cursor()
                    b_cursor.execute('SELECT * FROM Sleep')
                    #output = b_cursor.fetchall()   # Returns the results as a list.
                    #b_cursor.close()
                    # Insert those contents into another table.
                    a_cursor = db_a.cursor()
                    a_cursor.execute('CREATE TABLE IF NOT EXISTS Sleep(Id INTEGER PRIMARY KEY, Time DATETIME, X NUMERIC, Y NUMERIC, Z NUMERIC)')
                    for row in b_cursor.fetchall():
                        #time=row["Time"]
                        #x =row["X"]
                        #y =row["Y"]
                        #z =row["Z"]
                        #print(row["Time"])
                        id, time, x, y, z = row
                        print("----------------------------------------------------------")
                        print("Time: %s, X:%s, Y:%s, Z:%s"% (time, x, y, z))
                        print("----------------------------------------------------------")
                        a_cursor.execute("INSERT INTO Sleep (Time, X, Y, Z) VALUES ('%s','%s','%s','%s')"% (time, x, y, z))
                    db_a.commit()
                    a_cursor.close()
                    b_cursor.close()
           
                elif (int(data[0:2]) == 3 or int(data[0:2]) == 4 or int(data[0:2]) == 5):
                    date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M')
                    f= open('recdb/%s/%s_%s_pic.png'% (usr,usr,date),'wb')
                    #id= clientsocket.recv(1024).decode
                    l = self.rfile.read(1024)
                    while l:
                        print ("getting some data...")
                        f.write(l)
                        l = self.rfile.read(1024)
                    print("all done here!(naked pictures)")
                    f.close()
                else:
                    f= open('recdb/%s/%s_Actions.db'% (usr,usr),'wb')
                    #id= clientsocket.recv(1024).decode
                    l = self.rfile.read(1024)
                    while l:
                        print ("getting some data...")
                        f.write(l)
                        l = self.rfile.read(1024)
                    f.close()
                    print ("all done here!(action data)")
                self.data = self.rfile.readline().decode('utf-8')
                msg = str(self.data)
                print(msg)

    def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
        self.id = ''.join(random.choice(chars) for _ in range(size))


server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
server.allow_reuse_address = True
server.serve_forever()
