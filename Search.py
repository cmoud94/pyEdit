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

import Utils


class Search:
    def __init__(self, parent, find_type):
        self.parent = parent

        self.var_exact = BooleanVar()
        self.var_nocase = BooleanVar()

        self.style = Style()
        self.style.theme_use('clam')

        self.root = Toplevel()
        self.root.title('pyEdit - Search' + (' and replace' if find_type == 'replace' else ''))
        self.root.resizable(False, False)
        self.root.minsize(400, 200)

        self.root.bind('<Expose>', lambda e: Utils.on_expose(self))
        self.root.wm_protocol('WM_DELETE_WINDOW', lambda: Utils.on_close(self))

        self.active_editor = self.parent.editors[self.parent.get_selected_tab_index()]

        self.gui = None

        self.root.columnconfigure(0, weight=1)

        self.frame_find = Frame(self.root)
        self.frame_find.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
        self.frame_find.columnconfigure(1, weight=1)

        self.label_find = Label(self.frame_find, text='Find: ', width=10, anchor='w')
        self.label_find.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)

        self.entry_find = Entry(self.frame_find)
        self.entry_find.grid(column=1, row=0, sticky='nsew', padx=5, pady=5, ipadx=2, ipady=2)

        if find_type == 'replace':
            self.frame_replace = Frame(self.root)
            self.frame_replace.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)
            self.frame_replace.columnconfigure(1, weight=1)

            self.label_replace = Label(self.frame_replace, text='Replace: ', width=10, anchor='w')
            self.label_replace.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)

            self.entry_replace = Entry(self.frame_replace)
            self.entry_replace.grid(column=1, row=0, sticky='nsew', padx=5, pady=5, ipadx=2, ipady=2)

        self.frame_chkbtns = Frame(self.root)
        self.frame_chkbtns.grid(column=0, row=2, sticky='nsew', padx=5, pady=5)

        self.chkbtn_exact = Checkbutton(self.frame_chkbtns, text='Exact', variable=self.var_exact)
        self.chkbtn_exact.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)

        self.chkbtn_nocase = Checkbutton(self.frame_chkbtns, text='Ignore case', variable=self.var_nocase)
        self.chkbtn_nocase.grid(column=0, row=1, sticky='nsw', padx=5, pady=5)
