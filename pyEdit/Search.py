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
from tkinter import messagebox
from tkinter.ttk import Style

from pyEdit import Utils


class Search:
    def __init__(self, parent, find_type):
        self.parent = parent

        self.var_match_entire_word = BooleanVar()
        self.var_ignore_case = IntVar()
        self.var_regexp = BooleanVar()
        self.var_search_backwards = BooleanVar()
        self.var_found_length = IntVar()
        self.var_last_found_index = StringVar()

        self.var_last_found_index.set('1.0')

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

        self.chkbtn_exact = Checkbutton(self.frame_chkbtns, text='Match entire word',
                                        variable=self.var_match_entire_word)
        self.chkbtn_exact.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)

        self.chkbtn_nocase = Checkbutton(self.frame_chkbtns, text='Ignore case', variable=self.var_ignore_case)
        self.chkbtn_nocase.grid(column=0, row=1, sticky='nsw', padx=5, pady=5)

        self.chkbtn_regexp = Checkbutton(self.frame_chkbtns, text='Regexp', variable=self.var_regexp)
        self.chkbtn_regexp.grid(column=0, row=2, sticky='nsw', padx=5, pady=5)

        self.chkbtn_search_backwards = Checkbutton(self.frame_chkbtns, text='Search backwards',
                                                   variable=self.var_search_backwards)
        self.chkbtn_search_backwards.grid(column=0, row=3, sticky='nsw', padx=5, pady=5)

        self.frame_buttons = Frame(self.root)
        self.frame_buttons.grid(column=0, row=3, sticky='nse', padx=5, pady=5)

        self.btn_close = Button(self.frame_buttons, text='Close', command=lambda: Utils.on_close(self))
        self.btn_close.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        if find_type == 'replace':
            self.btn_replace = Button(self.frame_buttons, text='Replace', command=self.replace)
            self.btn_replace.grid(column=1, row=0, sticky='nsew', padx=5, pady=5)

            self.btn_replace_all = Button(self.frame_buttons, text='Replace all',
                                          command=lambda: self.replace(replace_all=True))
            self.btn_replace_all.grid(column=2, row=0, sticky='nsew', padx=5, pady=5)

        self.btn_find = Button(self.frame_buttons, text='Find', command=self.find)
        self.btn_find.grid(column=3, row=0, sticky='nsew', padx=5, pady=5)

        self.entry_find.focus_set()

    def find(self, event=None, replace_all=False):
        pattern = self.entry_find.get()
        last_found_index = self.var_last_found_index.get()
        exact = self.var_match_entire_word.get()
        nocase = self.var_ignore_case.get()
        regexp = self.var_regexp.get()
        backwards = self.var_search_backwards.get()

        index = self.active_editor.text_widget.search(pattern=pattern,
                                                      index=last_found_index,
                                                      exact=exact,
                                                      nocase=nocase,
                                                      regexp=regexp,
                                                      backwards=backwards,
                                                      count=self.var_found_length)

        if index != '':
            ln_col = str(index).split('.')
            index2 = str(ln_col[0]) + '.' + str(int(ln_col[1]) + self.var_found_length.get())

            self.var_last_found_index.set(index2)

            self.active_editor.text_widget.tag_remove('sel', '1.0', 'end')
            self.active_editor.text_widget.tag_add('sel', index, index2)
            self.active_editor.text_widget.mark_set('insert', index2)
            self.active_editor.text_widget.see('insert')
            self.active_editor.highlight_selected_text()

            return True
        else:
            if not replace_all:
                messagebox.showerror('Search/Replace', 'Nothing found for \'' + pattern + '\'.')
            return False

    def replace(self, event=None, replace_all=False):
        replace_with = self.entry_replace.get()
        if not replace_all:
            self.find()
            self.active_editor.text_widget.delete('sel.first', 'sel.last')
            self.active_editor.text_widget.insert('insert', replace_with)
        else:
            while self.find(replace_all=True):
                self.active_editor.text_widget.delete('sel.first', 'sel.last')
                self.active_editor.text_widget.insert('insert', replace_with)
        self.active_editor.highlight_current_line()
