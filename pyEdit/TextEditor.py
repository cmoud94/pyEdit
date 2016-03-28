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

from tkinter import font

from pyEdit.LineNumbers import *


class TextEditor:
    def __init__(self, parent, file_path='', content='', config=None):
        self.parent = parent
        self.file_path = file_path

        self.conf_text_wrap = True
        self.conf_text_wrap_mode = 'word'
        self.conf_show_line_numbers = False
        self.conf_highlight_current_line = False
        self.conf_font = None
        self.conf_tab_width = 4

        if self.file_path != '':
            index = file_path.rfind('/')
            self.file_name = self.file_path[index + 1:]
        else:
            self.file_name = 'Document'

        self.frame = Frame(self.parent.notebook)
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.text_widget = Text(self.frame,
                                relief='flat',
                                bd=0,
                                selectbackground='LightBlue3',
                                undo=True,
                                maxundo=-1,
                                autoseparator=True)
        self.text_widget.grid(column=1, row=0, sticky='nsew')
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('end', content)
        self.text_widget.mark_set('insert', '1.0')
        self.text_widget.see('1.0')
        self.text_widget.edit_modified(False)

        self.scroll_bar = Scrollbar(self.frame, bd=0, orient='vertical', command=self.scroll_update)
        self.scroll_bar.grid(column=2, row=0, sticky='ns')
        self.text_widget.config(yscrollcommand=self.scroll_bar.set)

        self.scroll_bar_horizontal = None

        self.line_number_widget = None

        self.parent.notebook.add(self.frame, text=self.file_name, compound='left')
        self.index = self.parent.notebook.index(self.parent.notebook.tabs()[-1])
        self.parent.notebook.select(self.index)

        # Banned keys for <KeyRelease> event
        self.banned_event_keys = ['Control_L', 'Control_R',
                                  'Shift_L', 'Shift_R',
                                  'Alt_L', 'Alt_R']

        # Unbinding
        self.text_widget.unbind_class('Text', '<Control-o>')
        self.text_widget.unbind_class('Text', '<Control-a>')
        self.text_widget.unbind_class('Text', '<Control-d>')
        # self.text_widget.unbind_class('Text', '<<Undo>>')
        # self.text_widget.unbind_class('Text', '<<Redo>>')
        # self.text_widget.unbind_class('Text', '<<Cut>>')
        # self.text_widget.unbind_class('Text', '<<Copy>>')
        # self.text_widget.unbind_class('Text', '<<Paste>>')

        # Shortcuts init
        self.text_widget.bind('<KeyRelease>', self.key)
        self.text_widget.bind('<ButtonRelease>', self.mouse)
        self.text_widget.bind('<B1-Motion>', self.mouse_motion)
        self.text_widget.bind('<Control-a>', self.select_all)

        self.config_update(config)

        self.text_widget.focus_set()

    def scroll_update(self, *event):
        if 'moveto' in event[0]:
            self.text_widget.yview_moveto(event[1])
            if self.conf_show_line_numbers:
                self.line_number_widget.line_widget.yview_moveto(event[1])
        elif 'scroll' in event[0]:
            self.text_widget.yview_scroll(event[1], event[2])
            if self.conf_show_line_numbers:
                self.line_number_widget.line_widget.yview_scroll(event[1], event[2])

    def key(self, event=None):
        if event.keysym in self.banned_event_keys:
            return

        if self.conf_show_line_numbers:
            self.line_number_widget.update()

        self.highlight_current_line()

        if self.text_widget.edit_modified():
            selected_tab = self.parent.notebook.index(self.parent.notebook.select())
            self.parent.notebook.tab(selected_tab, text='* ' + self.file_name)

        self.update_statusbar()
        self.parent.update_title()

    def mouse(self, event=None):
        left_btn = 1
        right_btn = 3
        scroll_up = 4
        scroll_down = 5

        if event.num == left_btn:
            self.highlight_current_line()
            self.update_statusbar()

        if event.num in (scroll_up, scroll_down):
            if self.conf_show_line_numbers:
                self.line_number_widget.line_widget.yview_moveto(self.text_widget.yview()[0])

    def mouse_motion(self, event=None):
        self.highlight_selected_text()

    def update_file_name(self, file_path):
        self.file_path = file_path
        index = file_path.rfind('/')
        self.file_name = file_path[index + 1:]
        print('File name updated to \'' + self.file_name + '\'')

    def update_statusbar(self, event=None):
        line_row_index = self.text_widget.index('insert').split('.')
        self.parent.statusbar_tab_width.set(self.parent.statusbar_text[0] + ': ' + str(self.parent.config[7]))
        self.parent.statusbar_current_line.set(self.parent.statusbar_text[1] + ': ' + str(line_row_index[0]))
        self.parent.statusbar_current_row.set(self.parent.statusbar_text[2] + ': ' + str(line_row_index[1]))

    def highlight_current_line(self):
        if self.conf_highlight_current_line:
            self.text_widget.tag_remove('current_line', '1.0', 'end')
            # Where is the insert cursor
            current_pos = self.text_widget.index('insert')
            current_line = current_pos[:current_pos.find('.')]
            start_index = str(current_line) + '.0'
            end_index = str(int(current_line) + 1) + '.0'
            # print(str(current_pos) + ' | ' + str(current_line) + ' | ' + str(start_index) + ' | ' + str(end_index))
            self.text_widget.tag_add('current_line', start_index, end_index)
            self.text_widget.tag_config('current_line', background='#e0e0e0')
        self.highlight_selected_text()

    def highlight_selected_text(self):
        self.text_widget.tag_remove('selected_text', '1.0', 'end')
        try:
            self.text_widget.tag_add('selected_text', 'sel.first', 'sel.last')
            self.text_widget.tag_config('selected_text', background='LightBlue3')
        except TclError:
            # print('highlight_selected_text error')
            return

    def unhighlight_current_line(self):
        self.text_widget.tag_remove('current_line', '1.0', 'end')

    def config_update(self, config):
        self.conf_text_wrap = True if config[0] == 1 else False
        if self.conf_text_wrap:
            self.conf_text_wrap_mode = 'word' if config[1] == 1 else 'char'
        else:
            self.conf_text_wrap_mode = 'none'
        self.conf_show_line_numbers = True if config[2] == 1 else False
        self.conf_highlight_current_line = True if config[3] == 1 else False
        self.conf_font = font.Font(family=config[4], size=config[5], weight=config[6])
        self.conf_tab_width = config[7]

        # Font metrics
        tab_width = self.conf_font.measure('a') * self.conf_tab_width

        self.text_widget.config(wrap=self.conf_text_wrap_mode,
                                font=self.conf_font,
                                tabs=tab_width,
                                tabstyle='wordprocessor')

        if not self.conf_text_wrap:
            if self.scroll_bar_horizontal is None:
                self.scroll_bar_horizontal = Scrollbar(self.frame, bd=0, orient='horizontal',
                                                       command=self.text_widget.xview)
                self.scroll_bar_horizontal.grid(column=1, row=1, sticky='ew')
                self.text_widget.config(xscrollcommand=self.scroll_bar_horizontal.set)
        else:
            if self.scroll_bar_horizontal is not None:
                self.scroll_bar_horizontal.grid_forget()
                self.scroll_bar_horizontal = None

        if self.conf_show_line_numbers:
            if self.line_number_widget is None:
                self.line_number_widget = LineNumbers(self.frame, self.text_widget)
                self.text_widget.bind('<Configure>', self.line_number_widget.update)
            self.line_number_widget.line_widget.config(font=self.conf_font)
            self.line_number_widget.update()
        else:
            if self.line_number_widget is not None:
                self.line_number_widget.delete()
            self.line_number_widget = None
            self.text_widget.unbind('<Configure>')

        if self.conf_highlight_current_line:
            self.highlight_current_line()
        else:
            self.unhighlight_current_line()

        self.update_statusbar()

        window_geometry = self.parent.root.geometry()
        self.parent.root.geometry(window_geometry)

    def select_all(self, event=None):
        self.text_widget.tag_add('sel', '1.0', 'end')
        self.text_widget.mark_set('insert', '1.0')
        self.text_widget.see('insert')
        return 'break'
