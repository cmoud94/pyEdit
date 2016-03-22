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
from tkinter import font
from tkinter.ttk import Style


class Help:
    def __init__(self, parent):
        self.parent = parent

        self.style = Style()
        self.style.theme_use('clam')

        self.root = Toplevel()
        self.root.title('pyEdit - Help')
        self.root.resizable(False, False)
        self.root.minsize(200, 50)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.root.bind('<Expose>', self.on_expose)
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)

        self.text = self.get_content()

        self.font = font.Font(family='Monospace', size=10, weight='normal')

        self.text_widget = Text(self.root,
                                relief='flat',
                                bd=0,
                                spacing1=2,
                                spacing2=2,
                                spacing3=2,
                                font=self.font)
        self.text_widget.grid(column=0, row=0, sticky='nsew')
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', self.text)
        self.text_widget.config(state='disabled')

        self.scrollbar = Scrollbar(self.root, bd=0, orient='vertical', command=self.text_widget.yview)
        self.scrollbar.grid(column=1, row=0, sticky='nsew')
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

    def on_expose(self, event=None):
        if self.parent.os != 'Linux':
            return
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

    def get_content(self):
        text = ''
        try:
            file = open('help.txt', 'r')
            file.seek(0, 2)
            size = file.tell()
            file.seek(0, 0)
            text = file.read(size)
            file.close()
        except IOError:
            print('IOError while reading help text.')

        return text
