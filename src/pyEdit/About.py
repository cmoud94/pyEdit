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

from src.pyEdit import Utils


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

        self.root.bind('<Expose>', lambda e: Utils.on_expose(self))
        self.root.wm_protocol('WM_DELETE_WINDOW', lambda: Utils.on_close(self))

        self.label_app_name = Label(self.root, text='pyEdit (Lightweight IDE)')
        self.label_app_name.grid(column=0, row=0, sticky='nsew', ipadx=5, ipady=5)

        self.label_author = Label(self.root, text='Author: Marek Kouřil')
        self.label_author.grid(column=0, row=1, sticky='nsew', ipadx=5, ipady=5)

        self.label_year = Label(self.root, text='2016')
        self.label_year.grid(column=0, row=2, sticky='nsew', ipadx=5, ipady=5)

        self.label_course = Label(self.root, text='\'URO\' course')
        self.label_course.grid(column=0, row=3, sticky='nsew', ipadx=5, ipady=5)
