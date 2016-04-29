import datetime
from threading import Thread
from time import sleep

import DBC.dbcreate as dbc


class Tracker(Thread):

    max_idle_time = 720 # minutes
    default_sleep = 3600 # secs

    def track(self):
        dbcl = dbc.DBClient()
        # print(dbcl.getlasttime())
        print("Tracker activated")

        while True:
            date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M')
            string = date.rsplit("-", 1)

            yearmonthday = (string[0].rsplit("-", 3))
            hoursminutes = (string[1].rsplit(":", 2))
            # print(yearmonthday)
            # print(hoursminutes)

            year = int(yearmonthday[0])
            month = int(yearmonthday[1])
            day = int(yearmonthday[2])
            hour = int(hoursminutes[0])
            minute = int(hoursminutes[1])

            date = dbcl.getlasttime()
            string = date.rsplit("-", 1)

            yearmonthday = (string[0].rsplit("-", 3))
            hoursminutes = (string[1].rsplit(":", 2))
            #print(yearmonthday)
            #print(hoursminutes)

            yeard = int(yearmonthday[0])
            monthd = int(yearmonthday[1])
            dayd = int(yearmonthday[2])
            hourd = int(hoursminutes[0])
            minuted = int(hoursminutes[1])


            # tämä loopitus tyhmää, voisi käyttää valmista kirjastoa
            if year == yeard:
                if month == monthd:
                    if day == dayd:
                        if hour == hourd:
                            away = minute - minuted
                        else:
                            away = ((hour*60) + minute) - ((hourd*60) + minuted)
                    else:
                        if hour == hourd:
                            away = ((hourd + (day-dayd)*24 - hour) * 60) + minute - minuted
                        else:
                            away = ((day*hour*60) + minute) - ((dayd*hourd*60) + minuted)
                else:
                    # puutteellinen
                    away = 3

            #print(away)
            self.actions(away, dbcl.getlastaway())

            sleep(self.default_sleep)

    def run(self):
        self.track()

    def actions(self, time, away):
        if time < self.max_idle_time:
            print("Everything ok")
        else:
            away = (int(away) * 60)
            if time > away:
                print("Contacting users")
            else:
                print("Holiday mode")