import sqlite3 as lite
import datetime
import DBC.pushdb as dbc
import os.path


class DBClient:
    global con
    global cur
    global dbpush

    dbpush = dbc.pushdb()

    con = lite.connect('/home/pi/project/Database/ActionData.db', check_same_thread=False)
    cur = con.cursor()

    def create(self):
        cur.execute("CREATE TABLE IF NOT EXISTS TTime"
                    "(Id INTEGER PRIMARY KEY, Time DATETIME, UNIQUE(Time))")
                    # "(Id INTEGER AUTO_INCREMENT PRIMARY KEY, Time DATETIME, UNIQUE(Time))")
        con.commit()
        cur.execute("CREATE TABLE IF NOT EXISTS TReason(Id INTEGER PRIMARY KEY, Reason TEXT)")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(1, 'Holiday')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(2, 'Back')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(3, 'Cleaned')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(4, 'Serviced')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(5, 'Cared')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(6, 'Called 112')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(7, 'Called Service')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(8, 'Called Care')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(9, 'User left')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(10, 'User home')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(11, 'User went to bed')")
        cur.execute("INSERT OR REPLACE INTO TReason(Id, Reason) VALUES(12, 'User woke up')")
        con.commit()

        cur.execute("CREATE TABLE IF NOT EXISTS TActions"
                    "(Id INTEGER PRIMARY KEY, TimeId INTEGER, Action INTEGER, Away NUMERIC, "
                    # "(Id INTEGER AUTO_INCREMENT PRIMARY KEY, TimeId INTEGER, Action INTEGER, Away NUMERIC, "
                    "FOREIGN KEY(TimeId) REFERENCES TTime(Id), "
                    "FOREIGN KEY(Action) REFERENCES TReason(Id))")
        con.commit()

    def createaction(self, action, time):
        cur.execute("SELECT Time From TTime ORDER BY Id DESC LIMIT 1")
        data = cur.fetchone()
        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M')
        if data != date:
            cur.execute("INSERT OR IGNORE INTO TTime(Time) VALUES('{}')".format(date))
        cur.execute("SELECT Id From TTime ORDER BY Id DESC LIMIT 1")
        rowid = cur.fetchone()
        rowid = ",".join(map(str, rowid))
        cur.execute("INSERT INTO TActions(TimeId, Action, Away) VALUES('{}','{}','{}')".format(rowid, action, time))
        con.commit()
        dbpush.send_action_data(action)
        if action == 3 or action == 4 or action == 5 or action == 12:
            dbpush.send_action_data(19)

    def getlasttime(self):
        try:
            cur.execute("SELECT Time From TTime ORDER BY Id DESC LIMIT 1")
            data = cur.fetchone()
            data = ",".join(map(str, data))
        except TypeError:
            data = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M')
        return data

    def getlastaction(self):
        cur.execute("SELECT Id From TActions ORDER BY Id DESC LIMIT 1")
        data = cur.fetchone()
        data = ",".join(map(str, data))
        return data

    def getlastaway(self):
        try:
            cur.execute("SELECT away From TActions ORDER BY Id DESC LIMIT 1")
            data = cur.fetchone()
            data = ",".join(map(str, data))
        except TypeError:
            data = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M')
        return data

    def readconfclient(self):
        dbpush.readconfclient()