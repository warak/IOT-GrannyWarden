import tkinter as tk

TITLE_FONT = ("Helvetica", 24, "bold")
SIZE = 24


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button1 = tk.Button(self, text="Lähden Lomalle", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageHoliday"))
        button3 = tk.Button(self, text="Apupyyntö", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageHelp"))
        button4 = tk.Button(self, text="Huolto", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageService"))
        button1.pack(side="left", fill="both", expand=1)
        button3.pack(side="left", fill="both", expand=1)
        button4.pack(side="left", fill="both", expand=1)


class PageHelp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button1 = tk.Button(self, text="112", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageConfirm", act="112"))
        button2 = tk.Button(self, text="Siivous", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageConfirm", act="cleaning"))
        button3 = tk.Button(self, text="Hoito", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageConfirm", act="care"))
        button4 = tk.Button(self, text="Takaisin", bd=SIZE, font=TITLE_FONT, bg="red", activebackground="red",
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack(side="left", fill="both", expand=1)
        button2.pack(side="left", fill="both", expand=1)
        button3.pack(side="left", fill="both", expand=1)
        button4.pack(side="left", fill="both", expand=1)


class PageService(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button1 = tk.Button(self, text="Siivottu", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageConfirm", react="cleaned"))
        button2 = tk.Button(self, text="Huollettu", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageConfirm", react="serviced"))
        button3 = tk.Button(self, text="Hoidettu", bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageConfirm", react="cared"))
        button4 = tk.Button(self, text="Takaisin", bd=SIZE, font=TITLE_FONT, bg="red", activebackground="red",
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack(side="left", fill="both", expand=1)
        button2.pack(side="left", fill="both", expand=1)
        button3.pack(side="left", fill="both", expand=1)
        button4.pack(side="left", fill="both", expand=1)


class PageHoliday(tk.Frame):
    global intVar
    intVar = 1

    def countn(self):
        global intVar
        if intVar != 1:
            intVar -= 1
            strCounter.set(str(intVar) + " päivää")

    def countp(self):
        global intVar
        intVar += 1
        strCounter.set(str(intVar) + " päivää")

    def __init__(self, parent, controller):
        global intVar
        global strCounter
        strCounter = tk.StringVar()
        strCounter.set(str(intVar) + " päivä")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button1 = tk.Button(self, text="<<<", bd=SIZE, font=TITLE_FONT,
                            command=lambda: self.countn())
        button2 = tk.Button(self, textvariable=strCounter, bd=SIZE, font=TITLE_FONT,
                            command=lambda: controller.show_frame("PageGone", hrs=intVar * 24))
        button3 = tk.Button(self, text=">>>", bd=SIZE, font=TITLE_FONT,
                            command=lambda: self.countp())
        button4 = tk.Button(self, text="Takaisin", bd=SIZE, font=TITLE_FONT, bg="red", activebackground="red",
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack(side="left", fill="both", expand=1)
        button2.pack(side="left", fill="both", expand=1)
        button3.pack(side="left", fill="both", expand=1)
        button4.pack(side="left", fill="both", expand=1)


class PageGone(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button1 = tk.Button(self, text="Tulin takaisin", bd=64, font=TITLE_FONT, bg="green", activebackground="green",
                            command=lambda: controller.show_frame("StartPage", back="back"))

        button1.pack(side="left", fill="both", expand=1)


class PageConfirm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        text = "OK"
        button1 = tk.Button(self, text=text, bd=64, font=TITLE_FONT, bg="green", activebackground="green",
                            command=lambda: controller.show_frame("StartPage"))

        button1.pack(side="left", fill="both", expand=1)
