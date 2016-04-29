import UI.pageaccesscontrol as pac
import UI.actioncontrol as ac
import tkinter as tk

# TITLE_FONT = ("Helvetica", 34, "bold")


class Ui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # container for stacking frames
        container = tk.Frame(self)
        self.attributes("-fullscreen", True)
        container.config(cursor='none')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (pac.StartPage, pac.PageHelp, pac.PageHoliday, pac.PageGone, pac.PageService, pac.PageConfirm ):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name, **kwargs):
        # Show a frame for the given page name

        if kwargs:
            # print(kwargs)
            ac.ActionControl.actcontrol(self, **kwargs)

        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = Ui()
    app.mainloop()




