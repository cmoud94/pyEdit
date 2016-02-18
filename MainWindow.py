from tkinter import *


class PyEdit:
    def __init__(self, root):
        # Window init
        self.root = root
        self.root.title('pyEdit')
        self.root.geometry('500x400')
        self.root.option_add('*tearOff', FALSE)

        # Main frame init
        self.frame_main = Frame(root)
        self.frame_main.grid(column=0, row=0)

        # Menu init
        self.menu_bar = self.menu_init()

        # Toolbar init
        self.frame_toolbar = self.toolbar_init()

    def menu_init(self):
        # Main menu_bar
        menu_bar = Menu(self.root)
        menu_bar.config(activebackground='LightBlue3', relief='flat')

        self.root.configure(menu=menu_bar)

        # File menu
        menu_file = Menu(menu_bar)
        menu_file.config(activebackground='LightBlue3')

        menu_file.add_command(label='New File', accelerator='Ctrl+N')
        menu_file.add_command(label='Open', accelerator='Ctrl+O')
        menu_file.add_command(label='Save', accelerator='Ctrl+S')
        menu_file.add_command(label='Save as...', accelerator='Ctrl+Shift+S')
        menu_file.add_separator()
        menu_file.add_command(label='Exit', accelerator='Ctrl+Q')

        menu_bar.add_cascade(menu=menu_file, label='File')

        return menu_bar

    def toolbar_init(self):
        frame_toolbar = Frame(self.frame_main)
        frame_toolbar.grid(column=0, row=0)

        # Toolbar buttons
        button_new_file = Button(frame_toolbar, text='New File')
        button_new_file.grid(column=0, row=0)
        button_open = Button(frame_toolbar, text='Open')
        button_open.grid(column=1, row=0)
        button_save = Button(frame_toolbar, text='Save')
        button_save.grid(column=2, row=0)

        return frame_toolbar


tk = Tk()
app = PyEdit(tk)
tk.mainloop()
