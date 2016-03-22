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
from tkinter.ttk import Style


class About:
    def __init__(self, parent):
        self.parent = parent

        self.style = Style()
        self.style.theme_use('clam')

        self.root = Toplevel()
        self.root.title('pyEdit - About')
        self.root.resizable(False, False)
        self.root.minsize(200, 50)
        self.root.columnconfigure(0, weight=1)

        self.root.bind('<Expose>', self.on_expose)
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)

        self.label_app_name = Label(self.root, text='pyEdit (Lightweight IDE)')
        self.label_app_name.grid(column=0, row=0, sticky='nsew', ipadx=5, ipady=5)

        self.label_author = Label(self.root, text='by KOU0120')
        self.label_author.grid(column=0, row=1, sticky='nsew', ipadx=5, ipady=5)

        self.label_year = Label(self.root, text='in 2k16')
        self.label_year.grid(column=0, row=2, sticky='nsew', ipadx=5, ipady=5)

        self.label_course = Label(self.root, text='for \'URO\' course')
        self.label_course.grid(column=0, row=3, sticky='nsew', ipadx=5, ipady=5)

    def on_expose(self, event=None):
        # Center widget on top of parent window
        parent_x = self.parent.root.winfo_x()
        parent_y = self.parent.root.winfo_y()
        parent_w = self.parent.root.winfo_width()
        parent_x_mid = parent_x + (parent_w / 2)
        root_x = parent_x_mid - (self.root.winfo_width() / 2)
        root_y = parent_y
        self.root.geometry(
            str(self.root.winfo_width()) + 'x' + str(self.root.winfo_height()) + '+' + str(int(root_x)) + '+' + str(
                int(root_y)))

        self.root.grab_set()
        self.root.transient(self.parent.root)

    def on_close(self, event=None):
        self.root.grab_release()
        self.root.destroy()
