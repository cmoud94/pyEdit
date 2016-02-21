from tkinter import Text


class TextEditor:
    def __init__(self, notebook, file_path='', file_name='Document', content=''):
        self.notebook = notebook
        self.file_path = file_path
        self.file_name = file_name

        self.text_widget = Text(self.notebook)
        self.text_widget.insert('1.0', content)

        self.notebook.add(self.text_widget, text=self.file_name, compound='left')
        self.index = self.notebook.index(self.notebook.tabs()[-1])
        self.notebook.select(self.index)
