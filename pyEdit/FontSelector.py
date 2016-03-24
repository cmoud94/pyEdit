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

from collections import OrderedDict
from tkinter import *
from tkinter import font
from tkinter.ttk import Style

from pyEdit import Utils


class FontSelector:
    def __init__(self, parent):
        self.parent = parent
        self.selected_family = parent.config[4]
        self.selected_size = parent.config[5]
        self.selected_weight = parent.config[6]

        families = list(OrderedDict.fromkeys(font.families()))
        families.sort()

        sizes_low = [x for x in range(7, 19)]
        sizes_high = [x for x in range(20, 74, 2)]
        sizes = sizes_low + sizes_high

        weights = ('normal', 'bold')

        self.style = Style()
        self.style.theme_use('clam')

        self.families = StringVar()
        self.sizes = StringVar()
        self.weight = StringVar()

        self.families.set(tuple(families))
        self.sizes.set(tuple(sizes))
        self.weight.set(weights)

        self.font = font.Font(size=9, weight='bold')

        self.root = Toplevel()
        self.root.title('pyEdit - Font Selector')
        self.root.resizable(False, False)

        self.root.bind('<Expose>', lambda e: Utils.on_expose(self))
        self.root.wm_protocol('WM_DELETE_WINDOW', lambda: Utils.on_close(self))

        # Family
        self.lf_family = LabelFrame(self.root, text='Family:', font=self.font, relief='flat')
        self.lf_family.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        self.frame_family = Frame(self.lf_family)
        self.frame_family.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        self.listbox_family = Listbox(self.frame_family, bd=0, listvariable=self.families)
        self.listbox_family.grid(column=0, row=0, sticky='nsew')
        self.listbox_family.bind('<ButtonRelease-1>', lambda e: self.listbox_event_handler(event=e, listbox='family'))

        self.scrollbar_family = Scrollbar(self.frame_family, orient='vertical', bd=0, command=self.listbox_family.yview)
        self.scrollbar_family.grid(column=1, row=0, sticky='ns')
        self.listbox_family.config(yscrollcommand=self.scrollbar_family.set)

        # Size
        self.lf_size = LabelFrame(self.root, text='Size:', font=self.font, relief='flat')
        self.lf_size.grid(column=1, row=0, sticky='nsew', padx=5, pady=5)

        self.frame_size = Frame(self.lf_size)
        self.frame_size.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        self.listbox_size = Listbox(self.frame_size, bd=0, listvariable=self.sizes, width=3)
        self.listbox_size.grid(column=0, row=0, sticky='nsew')
        self.listbox_size.bind('<ButtonRelease-1>', lambda e: self.listbox_event_handler(event=e, listbox='size'))

        self.scrollbar_size = Scrollbar(self.frame_size, orient='vertical', bd=0, command=self.listbox_size.yview)
        self.scrollbar_size.grid(column=1, row=0, sticky='ns')
        self.listbox_size.config(yscrollcommand=self.scrollbar_size.set)

        # Weight
        self.lf_weight = LabelFrame(self.root, text='Weight:', font=self.font, relief='flat')
        self.lf_weight.grid(column=0, row=1, sticky='nsew', padx=5, pady=5, columnspan=2)
        self.lf_weight.columnconfigure(0, weight=1)

        self.frame_weight = Frame(self.lf_weight)
        self.frame_weight.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
        self.frame_weight.columnconfigure(0, weight=1)

        self.listbox_weight = Listbox(self.frame_weight, bd=0, listvariable=self.weight, height=2)
        self.listbox_weight.grid(column=0, row=0, sticky='nsew')
        self.listbox_weight.bind('<ButtonRelease-1>', lambda e: self.listbox_event_handler(event=e, listbox='weight'))

        # Slant
        # self.lf_slant = LabelFrame(self.root, text='Slant:', font=self.font, relief='flat')
        # self.lf_slant.grid(column=0, row=2, sticky='nsew', padx=5, pady=5, columnspan=2)
        # self.lf_slant.columnconfigure(0, weight=1)
        #
        # self.frame_slant = Frame(self.lf_slant)
        # self.frame_slant.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
        # self.frame_slant.columnconfigure(0, weight=1)
        #
        # self.listbox_slant = Listbox(self.frame_slant, listvariable=self.weight, height=2)
        # self.listbox_slant.grid(column=0, row=0, sticky='nsew')

        self.frame_btn = Frame(self.root)
        self.frame_btn.grid(column=0, row=2, sticky='nsew', padx=5, pady=5, columnspan=2)
        self.frame_btn.columnconfigure(0, weight=1)

        self.btn_close = Button(self.frame_btn, text='Close', command=lambda: Utils.on_close(self))
        self.btn_close.grid(column=0, row=0, sticky='nse', padx=5, pady=5)

    def listbox_event_handler(self, event=None, listbox=''):
        if listbox == 'family':
            family = StringVar()
            family.set(self.listbox_family.get(self.listbox_family.curselection()[0]))
            self.parent.config[4] = family

        if listbox == 'size':
            size = IntVar()
            size.set(self.listbox_size.get(self.listbox_size.curselection()[0]))
            self.parent.config[5] = size

        if listbox == 'weight':
            weight = StringVar()
            weight.set(self.listbox_weight.get(self.listbox_weight.curselection()[0]))
            self.parent.config[6] = weight

        self.parent.config_write(close=False)
