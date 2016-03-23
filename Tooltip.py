"""
pyEdit - Lightweight IDE
Copyright (C) 2016 Marek Kouřil <cmoud94@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
        iD = self.id
        self.id = None
        if iD:
            self.parent.after_cancel(iD)

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
