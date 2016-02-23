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

        self.scroll_bar = Scrollbar(self.frame, bd=0, orient='vertical', command=self.scroll_update)
        self.scroll_bar.grid(column=2, row=0, sticky='ns')
        self.text_widget.config(yscrollcommand=self.scroll_bar.set)

        # self.line_number_widget = LineNumbers(self.frame, self.text_widget)
        # self.line_number_widget.daemon = True
        # self.line_number_widget.start()

        self.notebook.add(self.frame, text=self.file_name, compound='left')
        self.index = self.notebook.index(self.notebook.tabs()[-1])
        self.notebook.select(self.index)

    def scroll_update(self, *args):
        print(args)
        # self.text_widget.update_idletasks()
        # self.line_number_widget.line_widget.update_idletasks()
        if 'moveto' in args[0]:
            print('\t' + args[1])
            self.text_widget.yview(*args)
            # self.line_number_widget.line_widget.yview(*args)
        elif 'scroll' in args[0]:
            print('\t' + args[1] + '\t' + args[2])
            self.text_widget.yview_scroll(args[1], args[2])
            # self.line_number_widget.line_widget.yview_scroll(args[1], args[2])
