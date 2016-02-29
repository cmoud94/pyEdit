from tkinter import *


class Tooltip:
    def __init__(self, parent, text, timeout=500):
        self.parent = parent
        self.text = text
        self.timeout = timeout

        self.tipwindow = None
        self.id = None

        self.parent.bind('<Enter>', self.enter)
        self.parent.bind('<Leave>', self.leave)
        self.parent.bind('<ButtonPress>', self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.parent.after(self.timeout, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.parent.after_cancel(id)

    def showtip(self):
        if self.tipwindow:
            return

        x = self.parent.winfo_rootx() + (self.parent.winfo_width() / 2)
        y = self.parent.winfo_rooty() + self.parent.winfo_height() + 1
        self.tipwindow = tw = Toplevel(self.parent)
        tw.wm_overrideredirect(True)
        tw.wm_geometry('+%d+%d' % (x, y))
        self.showcontent()

    def showcontent(self):
        label = Label(self.tipwindow,
                      text=self.text,
                      justify='center',
                      background='#333333',
                      foreground='#eeeeee',
                      relief='solid',
                      padx=3,
                      pady=3)
        label.pack()

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
