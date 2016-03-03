from tkinter import *
from tkinter import font
from tkinter.ttk import Notebook, Style


class Preferences:
    def __init__(self, root):
        # Variables
        self.text_wrap_enable = BooleanVar()
        self.text_wrap_mode = StringVar()
        self.show_line_numbers = BooleanVar()

        self.font = font.Font(size=9, weight='bold')

        self.style = Style()
        self.style.theme_use('clam')

        self.root = Toplevel(root)
        self.root.title('Preferences')
        self.root.minsize(300, 400)
        self.root.resizable(False, False)
        self.root.option_add('*tearOff', FALSE)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.notebook = Notebook(self.root)
        self.notebook.grid(column=0, row=0, sticky='nsew')

        self.tab_view = self.init_tab_view()
        self.notebook.add(self.tab_view, text='View')

        # self.tab_editor = self.init_tab_editor()

    def init_tab_view(self):
        frame = Frame(self.notebook)
        frame.columnconfigure(0, weight=1)

        lf_text_wrapping = LabelFrame(frame, text='Text wrapping', font=self.font)
        lf_text_wrapping.grid(column=0, row=0, stick='nsew', padx=5, pady=5)

        chkbtn_text_wrap_enable = Checkbutton(lf_text_wrapping,
                                              text='Enable text wrapping',
                                              variable=self.text_wrap_enable)
        chkbtn_text_wrap_enable.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)

        chkbtn_text_wrap_mode = Checkbutton(lf_text_wrapping,
                                            text='Wrap whole words',
                                            variable=self.text_wrap_mode)
        chkbtn_text_wrap_mode.grid(column=0, row=1, sticky='nsw', padx=5, pady=5)

        lf_line_numbers = LabelFrame(frame, text='Line numbers', font=self.font)
        lf_line_numbers.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)

        chkbtn_line_numbers = Checkbutton(lf_line_numbers,
                                          text='Show line numbers',
                                          variable=self.show_line_numbers)
        chkbtn_line_numbers.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)

        return frame

    def init_tab_editor(self):
        pass
