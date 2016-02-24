from LineNumbers import *


class TextEditor:
    def __init__(self, notebook, file_path='', file_name='Document', content=''):
        self.notebook = notebook
        self.file_path = file_path
        self.file_name = file_name

        self.frame = Frame(self.notebook)
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.text_widget = Text(self.frame, relief='flat', bd=0)
        self.text_widget.grid(column=1, row=0, sticky='nsew')
        self.text_widget.insert('1.0', content)
        self.text_widget.edit_modified(False)

        self.scroll_bar = Scrollbar(self.frame, bd=0, orient='vertical', command=self.scroll_update)
        self.scroll_bar.grid(column=2, row=0, sticky='ns')
        self.text_widget.config(yscrollcommand=self.scroll_bar.set)

        self.line_number_widget = LineNumbers(self.frame, self.text_widget)
        self.line_number_widget.update()

        self.notebook.add(self.frame, text=self.file_name, compound='left')
        self.index = self.notebook.index(self.notebook.tabs()[-1])
        self.notebook.select(self.index)

        # Shortcuts init
        self.text_widget.bind('<Key>', self.key_press)
        self.text_widget.bind('<Configure>', self.window_resize)
        self.text_widget.bind('<Button>', self.mouse_wheel)

    def scroll_update(self, *event):
        # self.line_number_widget.update()
        if 'moveto' in event[0]:
            self.text_widget.yview_moveto(event[1])
            self.line_number_widget.line_widget.yview_moveto(event[1])
        elif 'scroll' in event[0]:
            self.text_widget.yview_scroll(event[1], event[2])
            self.line_number_widget.line_widget.yview_scroll(event[1], event[2])

    def key_press(self, event=None):
        self.line_number_widget.update()
        if self.text_widget.edit_modified():
            selected_tab = self.notebook.index(self.notebook.select())
            self.notebook.tab(selected_tab, text='* ' + self.file_name)

    def window_resize(self, event=None):
        self.line_number_widget.update()

    # FIXME: Don't work!
    def mouse_wheel(self, event=None):
        scroll_up = 4
        scroll_down = 5
        if event.num in (scroll_up, scroll_down):
            self.line_number_widget.line_widget.yview_moveto(self.text_widget.yview()[0])
            print('txt: ' + str(self.text_widget.yview()))
            print('ln:  ' + str(self.line_number_widget.line_widget.yview()))
