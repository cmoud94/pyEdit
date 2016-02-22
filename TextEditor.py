from tkinter import *


class TextEditor:
    def __init__(self, notebook, file_path='', file_name='Document', content=''):
        self.notebook = notebook
        self.file_path = file_path
        self.file_name = file_name

        self.frame = Frame(self.notebook)
        self.frame.grid(column=0, row=0, sticky='nsew')

        self.text_widget = Text(self.frame, relief='flat')
        self.text_widget.grid(column=0, row=0, sticky='nsew')
        self.text_widget.insert('1.0', content)

        self.scroll_bar = Scrollbar(self.frame, orient='vertical', command=self.text_widget.yview)
        self.scroll_bar.grid(column=1, row=0, sticky='ns')
        self.text_widget.config(yscrollcommand=self.scroll_bar.set)

        self.notebook.add(self.frame, text=self.file_name, compound='left')
        self.index = self.notebook.index(self.notebook.tabs()[-1])
        self.notebook.select(self.index)
