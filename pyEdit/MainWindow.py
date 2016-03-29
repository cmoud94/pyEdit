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

import os
import platform
from os.path import expanduser
from tkinter import filedialog
from tkinter.ttk import Separator, Notebook

from pyEdit.About import *
from pyEdit.Help import *
from pyEdit.Preferences import *
from pyEdit.Search import *
from pyEdit.TextEditor import *
from pyEdit.Tooltip import *


class PyEdit:
    def __init__(self, root):
        self.editors = []
        self.config = []

        self.os = platform.system()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.supported_file_extensions = self.get_supported_file_extensions()

        # Style init
        self.style = Style()
        self.style.theme_use('clam')

        # Window init
        self.root = root
        self.root.title('pyEdit')
        self.root.minsize(400, 250)
        self.root.option_add('*tearOff', FALSE)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Read config
        self.config = Preferences(self).config_read_startup()

        # Menu init
        self.menu_bar = self.menu_init()

        # Toolbar init
        self.img_new_file = PhotoImage(file='icons/24x24/document-new-8.png')
        self.img_open = PhotoImage(file='icons/24x24/document-open-7.png')
        self.img_save = PhotoImage(file='icons/24x24/document-save-2.png')
        self.img_undo = PhotoImage(file='icons/24x24/edit-undo-5.png')
        self.img_redo = PhotoImage(file='icons/24x24/edit-redo-5.png')
        self.img_cut = PhotoImage(file='icons/24x24/edit-cut.png')
        self.img_copy = PhotoImage(file='icons/24x24/edit-copy.png')
        self.img_paste = PhotoImage(file='icons/24x24/edit-paste-2.png')
        self.img_search = PhotoImage(file='icons/24x24/edit-find-5.png')
        self.img_replace = PhotoImage(file='icons/24x24/edit-find-and-replace-2.png')

        self.frame_toolbar = self.toolbar_init()

        # Tabs init
        self.tab_doc_img = PhotoImage('tab_doc', file='icons/document-new-7.png')
        self.tab_img_1 = PhotoImage('img_close', file='icons/close.png')
        self.tab_img_2 = PhotoImage('img_close_pressed', file='icons/close-pressed.png')
        self.tab_img_3 = PhotoImage('img_close_mouse_over', file='icons/close-focus.png')

        self.notebook = self.notebook_init()

        # Status bar init
        self.statusbar_tab_width = StringVar()
        self.statusbar_current_line = StringVar()
        self.statusbar_current_row = StringVar()
        self.statusbar_text = ['tab width', 'ln', 'col']
        self.statusbar = self.statusbar_init()

        # Shortcuts init
        self.shortcuts_init()

        # Set geometry from last time
        self.root.geometry(self.config[8])

    def menu_init(self):
        # Main menu_bar
        menu_bar = Menu(self.root)
        menu_bar.config(relief='flat')

        self.root.configure(menu=menu_bar)

        # File menu
        menu_file = Menu(menu_bar)

        menu_file.add_command(label='New File', accelerator='Ctrl+N', command=self.new_tab)
        menu_file.add_command(label='Open', accelerator='Ctrl+O', command=self.open_file)
        menu_file.add_separator()
        menu_file.add_command(label='Save', accelerator='Ctrl+S', command=self.save_file)
        menu_file.add_command(label='Save as...', accelerator='Ctrl+Shift+S',
                              command=lambda: self.save_file(save_as=True))
        menu_file.add_separator()
        menu_file.add_command(label='Exit', accelerator='Ctrl+Q', command=self.window_close)

        menu_bar.add_cascade(menu=menu_file, label='File')

        # Edit menu
        menu_edit = Menu(menu_bar)

        menu_edit.add_command(label='Undo', accelerator='Ctrl+Z', command=self.undo)
        menu_edit.add_command(label='Redo', accelerator='Ctrl+Shift+Z', command=self.redo)
        menu_edit.add_separator()
        menu_edit.add_command(label='Cut', accelerator='Ctrl+X', command=self.cut)
        menu_edit.add_command(label='Copy', accelerator='Ctrl+C', command=self.copy)
        menu_edit.add_command(label='Paste', accelerator='Ctrl+V', command=self.paste)
        menu_edit.add_separator()
        menu_edit.add_command(label='Preferences', accelerator='Ctrl+.', command=self.preferences)

        menu_bar.add_cascade(menu=menu_edit, label='Edit')

        # Search/Replace menu
        menu_search = Menu(menu_bar)

        menu_search.add_command(label='Find', accelerator='Ctrl+F', command=self.find)
        menu_search.add_command(label='Replace', accelerator='Ctrl+R', command=self.find_and_replace)

        menu_bar.add_cascade(menu=menu_search, label='Search')

        # Help menu
        menu_help = Menu(menu_bar)

        menu_help.add_command(label='Help', accelerator='F1', command=self.help)
        menu_help.add_command(label='About', command=self.about)

        menu_bar.add_cascade(menu=menu_help, label='Help')

        return menu_bar

    def toolbar_init(self):
        frame_toolbar = Frame(self.root)
        frame_toolbar.grid(column=0, row=0, sticky='nsew')

        # New file button
        button_new_file = Button(frame_toolbar,
                                 image=self.img_new_file,
                                 relief='flat',
                                 command=self.new_tab)
        button_new_file.grid(column=0, row=0, sticky='nsew')

        tooltip_new_file = Tooltip(button_new_file, 'Create new file')

        # Open file button
        button_open = Button(frame_toolbar,
                             image=self.img_open,
                             relief='flat',
                             command=self.open_file)
        button_open.grid(column=1, row=0, sticky='nsew')

        tooltip_open = Tooltip(button_open, 'Open file')

        # Save file button
        button_save = Button(frame_toolbar,
                             image=self.img_save,
                             relief='flat',
                             command=self.save_file)
        button_save.grid(column=2, row=0, sticky='nsew')

        tooltip_save = Tooltip(button_save, 'Save file')

        # Separator
        separator_1 = Separator(frame_toolbar, orient='vertical')
        separator_1.grid(column=3, row=0, sticky='nsew')

        # Undo button
        button_undo = Button(frame_toolbar,
                             image=self.img_undo,
                             relief='flat',
                             command=self.undo)
        button_undo.grid(column=4, row=0, sticky='nsew')

        tooltip_undo = Tooltip(button_undo, 'Undo')

        # Redo button
        button_redo = Button(frame_toolbar,
                             image=self.img_redo,
                             relief='flat',
                             command=self.redo)
        button_redo.grid(column=5, row=0, sticky='nsew')

        tooltip_redo = Tooltip(button_redo, 'Redo')

        # Separator
        separator_2 = Separator(frame_toolbar, orient='vertical')
        separator_2.grid(column=6, row=0, sticky='nsew')

        # Cut button
        button_cut = Button(frame_toolbar,
                            image=self.img_cut,
                            relief='flat',
                            command=self.cut)
        button_cut.grid(column=7, row=0, sticky='nsew')

        tooltip_cut = Tooltip(button_cut, 'Cut')

        # Copy button
        button_copy = Button(frame_toolbar,
                             image=self.img_copy,
                             relief='flat',
                             command=self.copy)
        button_copy.grid(column=8, row=0, sticky='nsew')

        tooltip_copy = Tooltip(button_copy, 'Copy')

        # Paste button
        button_paste = Button(frame_toolbar,
                              image=self.img_paste,
                              relief='flat',
                              command=self.paste)
        button_paste.grid(column=9, row=0, sticky='nsew')

        tooltip_paste = Tooltip(button_paste, 'Paste')

        # Separator
        separator_3 = Separator(frame_toolbar, orient='vertical')
        separator_3.grid(column=10, row=0, sticky='nsew')

        # Search button
        button_search = Button(frame_toolbar,
                               image=self.img_search,
                               relief='flat',
                               command=self.find)
        button_search.grid(column=11, row=0, sticky='nsew')

        tooltip_search = Tooltip(button_search, 'Search')

        # Replace button
        button_replace = Button(frame_toolbar,
                                image=self.img_replace,
                                relief='flat',
                                command=self.find_and_replace)
        button_replace.grid(column=12, row=0, sticky='nsew')

        tooltip_replace = Tooltip(button_replace, 'Replace')

        return frame_toolbar

    def notebook_init(self):
        self.style.element_create('close', 'image', 'img_close',
                                  ('active', 'pressed', '!disabled', 'img_close_pressed'),
                                  ('active', '!disabled', 'img_close_mouse_over'))

        self.style.layout('NotebookBtn', [('Notebook.client', {'sticky': 'nsew'})])

        self.style.layout('NotebookBtn.Tab', [
            ('Notebook.tab', {'sticky': 'nsew', 'children': [
                ('Notebook.padding', {'side': 'top', 'sticky': 'nsew', 'children': [
                    ('Notebook.focus', {'side': 'top', 'sticky': 'nsew', 'children': [
                        ('Notebook.label', {'side': 'left', 'sticky': 'nsew'}),
                        ('Notebook.close', {'side': 'right', 'sticky': 'nsew'})
                    ]})
                ]})
            ]})
        ])

        self.style.configure('NotebookBtn.Tab', padding=2, image='tab_doc')
        self.style.map('NotebookBtn.Tab', background=[('selected', '#f0f0f0')])

        self.root.bind_class('TNotebook', '<ButtonPress-1>', self.tab_btn_press, True)
        self.root.bind_class('TNotebook', '<ButtonRelease-1>', self.tab_btn_release)

        tabs = Notebook(self.root, style='NotebookBtn')
        tabs.grid(column=0, row=1, sticky='nsew')
        tabs.columnconfigure(0, weight=1)
        tabs.rowconfigure(0, weight=1)

        return tabs

    def tab_btn_press(self, event=None):
        if self.notebook_no_tabs():
            return

        if event is not None:
            x, y, widget = event.x, event.y, event.widget
            elem = widget.identify(x, y)
            index = widget.index('@%d,%d' % (x, y))

            if 'close' in elem:
                widget.state(['pressed'])
                widget.pressed_index = index

            self.editors[self.get_selected_tab_index()].update_statusbar()

    def tab_btn_release(self, event=None):
        if self.notebook_no_tabs():
            return

        x, y, widget = event.x, event.y, event.widget

        if not widget.instate(['pressed']):
            return

        elem = widget.identify(x, y)
        index = widget.index('@%d,%d' % (x, y))

        if 'close' in elem and widget.pressed_index == index:
            # widget.forget(index)
            widget.event_generate('<<NotebookClosedTab>>')
            self.close_tab()

        widget.state(['!pressed'])
        widget.pressed_index = None

    def statusbar_init(self):
        frame = Frame(self.root)
        frame.grid(column=0, row=2, sticky='nsew')

        lbl_tab_width = Label(frame, textvariable=self.statusbar_tab_width, relief='sunken')
        lbl_tab_width.grid(column=0, row=0, sticky='nsew', ipadx=2, ipady=2)

        lbl_current_line = Label(frame, textvariable=self.statusbar_current_line, relief='sunken')
        lbl_current_line.grid(column=1, row=0, sticky='nse', ipadx=2, ipady=2)

        lbl_current_row = Label(frame, textvariable=self.statusbar_current_row, relief='sunken')
        lbl_current_row.grid(column=2, row=0, sticky='nse', ipadx=2, ipady=2)

        self.statusbar_tab_width.set(self.statusbar_text[0] + ': ' + str(self.config[7]))
        self.statusbar_current_line.set(self.statusbar_text[1] + ': None')
        self.statusbar_current_row.set(self.statusbar_text[2] + ': None')

        return frame

    def shortcuts_init(self):
        # File shortcuts
        self.root.bind_all('<Control-n>', self.new_tab)
        self.root.bind_all('<Control-o>', self.open_file)
        self.root.bind_all('<Control-s>', self.save_file)
        self.root.bind_all('<Control-S>', lambda e: self.save_file(e, save_as=True))
        self.root.bind_all('<Control-w>', self.close_tab)

        # Edit shortcuts
        self.root.bind_all('<Control-z>', self.undo)
        self.root.bind_all('<Control-Z>', self.redo)
        self.root.bind_all('<Control-x>', self.cut)
        self.root.bind_all('<Control-c>', self.copy)
        self.root.bind_all('<Control-v>', self.paste)
        self.root.bind_all('<Control-period>', self.preferences)

        # Search shortcuts
        self.root.bind_all('<Control-f>', self.find)
        self.root.bind_all('<Control-r>', self.find_and_replace)

        # Help options
        self.root.bind_all('<F1>', self.help)

        # Window shortcuts
        self.root.bind_all('<Control-q>', self.window_close)
        self.root.wm_protocol('WM_DELETE_WINDOW', self.window_close)

        # Debug shortcuts
        self.root.bind_all('<Control-d>', self.debug_file)

    def new_tab(self, event=None, file_path='', content=''):
        self.editors.append(TextEditor(self, file_path, content, self.config))
        # self.clipboards.append('')
        self.update_title()

    def close_tab(self, event=None, app_exit=False):
        if self.notebook_no_tabs('close'):
            return

        selected_tab = self.get_selected_tab_index()
        if self.editors[selected_tab].text_widget.edit_modified():
            if not app_exit:
                response = messagebox.askquestion('File edited',
                                                  'Save file before closing?',
                                                  icon='question',
                                                  type='yesnocancel',
                                                  default='cancel',
                                                  parent=self.root)
                if response == 'yes':
                    self.save_file()
                elif response == 'cancel':
                    return
            else:
                response = messagebox.askquestion('File edited',
                                                  'Save file before closing?',
                                                  icon='question',
                                                  type='yesno',
                                                  default='yes',
                                                  parent=self.root)
                if response == 'yes':
                    self.save_file()

        print('Closing tab \'' + str(self.editors[selected_tab].file_name) + '\'')

        for bind in self.editors[selected_tab].text_widget.bind():
            self.editors[selected_tab].text_widget.unbind(bind)

        self.editors.remove(self.editors[selected_tab])
        # self.clipboards.remove(self.clipboards[selected_tab])
        self.notebook.forget(selected_tab)

        if self.notebook_no_tabs('', message_type='none'):
            self.statusbar_tab_width.set(self.statusbar_text[0] + ': ' + str(self.config[7]))
            self.statusbar_current_line.set(self.statusbar_text[1] + ': None')
            self.statusbar_current_row.set(self.statusbar_text[2] + ': None')

        self.update_title()

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(title='Open file...',
                                               defaultextension=self.supported_file_extensions[0],
                                               filetypes=self.supported_file_extensions,
                                               initialdir=expanduser('~/Desktop'))

        try:
            file = open(file_path, 'r')
            file.seek(0, 2)
            size = file.tell()
            file.seek(0, 0)
            content = file.read(size - 1)
            file.close()
            self.new_tab(file_path=file_path, content=content)
        except IOError:
            print('File not found or \'Cancel\' pressed.')

    def save_file(self, event=None, save_as=False):
        if self.notebook_no_tabs('save'):
            return

        selected_tab = self.get_selected_tab_index()
        if not save_as:
            if not self.editors[selected_tab].text_widget.edit_modified():
                print('File already saved...')
                return

        if save_as and self.editors[selected_tab].file_name == 'Document':
            print('Document not edited yet.')
            return

        file_path = self.editors[selected_tab].file_path
        if file_path == '' or save_as:
            title = 'Save file...' if not save_as else 'Save file as...'
            file_path = filedialog.asksaveasfilename(title=title,
                                                     defaultextension=self.supported_file_extensions[0],
                                                     filetypes=self.supported_file_extensions,
                                                     initialdir=expanduser('~/Desktop'))
            if file_path != '':
                self.editors[selected_tab].update_file_name(file_path)

        try:
            save_file = open(file_path, 'w')
            save_file.write(self.editors[selected_tab].text_widget.get('1.0', 'end'))
            save_file.close()
            print('File saved successfully!')
            self.editors[selected_tab].text_widget.edit_modified(False)
        except IOError:
            print('IO error while saving or \'Cancel\' pressed.')

        if not self.editors[selected_tab].text_widget.edit_modified():
            self.notebook.tab(selected_tab, text=self.editors[selected_tab].file_name)

        self.update_title()

    def undo(self, event=None):
        if self.notebook_no_tabs('No tabs, no undo...', 'message'):
            return

        selected_tab = self.get_selected_tab_index()
        try:
            self.editors[selected_tab].text_widget.edit_undo()
            if not self.editors[selected_tab].text_widget.edit_modified():
                self.notebook.tab(selected_tab, text=self.editors[selected_tab].file_name)
            else:
                self.notebook.tab(selected_tab, text='*' + self.editors[selected_tab].file_name)
        except TclError:
            print('undo error')
            return

        self.editors[selected_tab].highlight_current_line()
        self.update_title()

    def redo(self, event=None):
        if self.notebook_no_tabs('No tabs, no redo...', 'message'):
            return

        selected_tab = self.get_selected_tab_index()
        try:
            self.editors[selected_tab].text_widget.edit_redo()
            if not self.editors[selected_tab].text_widget.edit_modified():
                self.notebook.tab(selected_tab, text=self.editors[selected_tab].file_name)
            else:
                self.notebook.tab(selected_tab, text='*' + self.editors[selected_tab].file_name)
        except TclError:
            print('redo error')
            return

        self.editors[selected_tab].highlight_current_line()
        self.update_title()

    # TODO: Fix me!
    def cut(self, event=None):
        if self.notebook_no_tabs('No tabs, nothing to cut...', 'message'):
            return

        selected_tab = self.get_selected_tab_index()
        try:
            # self.editors[selected_tab].text_widget.event_generate('<<Cut>>')
            text = self.editors[selected_tab].text_widget.get('sel.first', 'sel.last')
            self.editors[selected_tab].text_widget.delete('sel.first', 'sel.last')
            self.editors[selected_tab].text_widget.clipboard_clear()
            self.editors[selected_tab].text_widget.clipboard_append(text)
        except TclError:
            print('cut error')
            return

        self.editors[selected_tab].highlight_current_line()
        self.update_title()

    # TODO: Fix me!
    def copy(self, event=None):
        if self.notebook_no_tabs('No tabs, nothing to copy...', 'message'):
            return

        selected_tab = self.get_selected_tab_index()
        try:
            # self.editors[selected_tab].text_widget.event_generate('<<Copy>>')
            text = self.editors[selected_tab].text_widget.get('sel.first', 'sel.last')
            self.editors[selected_tab].text_widget.clipboard_clear()
            self.editors[selected_tab].text_widget.clipboard_append(text)
        except TclError:
            print('copy error')
            return

        self.editors[selected_tab].highlight_current_line()
        self.update_title()

    def paste(self, event=None):
        if self.notebook_no_tabs('No tabs, nothing to paste...', 'message'):
            return

        selected_tab = self.get_selected_tab_index()
        try:
            self.editors[selected_tab].text_widget.event_generate('<<Paste>>')
        except TclError:
            print('paste error')

        self.editors[selected_tab].highlight_current_line()
        self.update_title()

    def preferences(self, event=None):
        Preferences(self)

    def config_update(self, default_geometry=False):
        if default_geometry:
            self.root.geometry(self.config[8])

        if self.notebook_no_tabs('', 'none'):
            return

        # print('config_update: ' + str(self.config))

        for i in range(len(self.editors)):
            self.editors[i].config_update(self.config)

        selected_tab = self.get_selected_tab_index()
        if selected_tab is not None:
            self.editors[selected_tab].text_widget.focus_force()

    def update_title(self, event=None):
        if self.notebook_no_tabs('', 'none'):
            self.root.title('pyEdit')
            return
        selected_tab = self.get_selected_tab_index()
        text = self.notebook.tab(selected_tab).get('text')
        self.root.title('pyEdit - ' + text)

    def find(self, event=None):
        if self.notebook_no_tabs('find'):
            return
        Search(self, 'find')

    def find_and_replace(self, event=None):
        if self.notebook_no_tabs('replace'):
            return
        Search(self, 'replace')

    def help(self, event=None):
        Help(self)

    def about(self, event=None):
        About(self)

    def window_close(self, event=None):
        if not self.notebook_no_tabs('Nothing to close, destroying immediately!', 'message'):
            for index in range(len(self.editors) - 1, -1, -1):
                self.notebook.select(index)
                self.close_tab(app_exit=True)
        conf = Preferences(self).config_read()
        conf[8] = self.root.geometry()
        Preferences(self).config_write(config=conf)
        self.root.destroy()

    def notebook_no_tabs(self, message='', message_type='word'):
        try:
            if self.notebook.tabs() == ():
                if message_type == 'word':
                    if message == '':
                        return True
                    print('There\'s nothing to ' + message + ', open some file first!')
                elif message_type == 'message':
                    print(message)
                elif message_type == 'none':
                    pass
                return True
            return False
        except AttributeError:
            return

    def get_selected_tab_index(self, event=None):
        if self.notebook_no_tabs('work with'):
            return None
        try:
            index = self.notebook.index(self.notebook.select())
        except AttributeError:
            index = None
        return index

    def debug_file(self, event=None):
        if self.notebook_no_tabs('debug'):
            return

        selected_tab = self.get_selected_tab_index()
        print('File name: ' + self.editors[selected_tab].file_name)
        print('File path: ' + self.editors[selected_tab].file_path)
        print('File modified (from last save): ' + str(bool(self.editors[selected_tab].text_widget.edit_modified())))
        print('Lines: ' + str(self.editors[selected_tab].text_widget.get('1.0', 'end').count('\n')))

    def get_supported_file_extensions(self):
        sfe = []
        try:
            file = open(self.current_dir + '/supported_file_extensions.txt', 'r')
            file.seek(0, 2)
            size = file.tell()
            file.seek(0, 0)
            content = file.read(size).splitlines()
            for i in range(len(content)):
                f_type = []
                f_type.append(content[i].split('=')[0])
                f_type.append('*.' + content[i].split('=')[1])
                sfe.append(tuple(f_type))
            file.close()
        except IOError:
            print('IOError')

        return sfe


def main():
    tk = Tk()
    app = PyEdit(tk)
    tk.mainloop()


if __name__ == '__main__':
    main()
