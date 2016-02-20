from Tkinter import *
from ttk import Notebook, Style


class PyEdit:
    def __init__(self, root):
        # Window init
        self.root = root
        self.root.title('pyEdit')
        self.root.minsize(500, 430)
        self.root.option_add('*tearOff', FALSE)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Menu init
        self.menu_bar = self.menu_init()

        # Toolbar init
        self.frame_toolbar = self.toolbar_init()

        # Tabs init
        self.notebook = self.notebook_init()

        # Status bar init
        self.status_bar = self.status_bar_init()

        self.root.update()

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
        frame_toolbar = Frame(self.root)
        frame_toolbar.grid(column=0, row=0, sticky='nw')

        # Toolbar buttons
        self.img_new_file = PhotoImage(file='icons/24x24/document-new-8.png')
        button_new_file = Button(frame_toolbar, image=self.img_new_file, relief='flat', activebackground='LightBlue3')
        button_new_file.grid(column=0, row=0)

        self.img_open = PhotoImage(file='icons/24x24/document-open-7.png')
        button_open = Button(frame_toolbar, image=self.img_open, relief='flat', activebackground='LightBlue3')
        button_open.grid(column=1, row=0)

        self.img_save = PhotoImage(file='icons/24x24/document-save-2.png')
        button_save = Button(frame_toolbar, image=self.img_save, relief='flat', activebackground='LightBlue3')
        button_save.grid(column=2, row=0)

        self.img_search = PhotoImage(file='icons/24x24/edit-find-5.png')
        button_search = Button(frame_toolbar, image=self.img_search, relief='flat', activebackground='LightBlue3')
        button_search.grid(column=3, row=0)

        return frame_toolbar

    def notebook_init(self):
        self.tab_img_1 = PhotoImage('img_close', file='icons/CloseBtn_Normal.png')
        self.tab_img_2 = PhotoImage('img_close_pressed', file='icons/CloseBtn_Pressed.png')
        self.tab_img_3 = PhotoImage('img_close_mouse_over', file='icons/CloseBtn_MouseOver.png')

        style = Style()
        style.element_create('close', 'image', 'img_close',
                             ('active', 'pressed', '!disabled', 'img_close_pressed'),
                             ('active', '!disabled', 'img_close_mouse_over'), border=1, sticky='')

        style.layout('NotebookBtn', [('NotebookBtn.client', {'sticky': 'nsew'})])
        style.layout('NotebookBtn.Tab', [
            ('NotebookBtn.tab', {'sticky': 'nsew', 'children':
                [('NotebookBtn.padding', {'side': 'top', 'sticky': 'nsew', 'children':
                    [('NotebookBtn.focus', {'side': 'top', 'sticky': 'nsew', 'children':
                        [('NotebookBtn.label', {'side': 'left', 'sticky': ''}),
                         ('NotebookBtn.close', {'side': 'left', 'sticky': ''})]
                                            })]
                                          })]
                                 })
        ])

        self.root.bind_class('TNotebook', '<ButtonPress-1>', self.tab_btn_press, True)
        self.root.bind_class('TNotebook', '<ButtonRelease-1>', self.tab_btn_release)

        tabs = Notebook(self.root, style='NotebookBtn')
        tabs.grid(column=0, row=1, sticky='nsew')
        tabs.columnconfigure(0, weight=1)
        tabs.rowconfigure(0, weight=1)

        text1 = Text(tabs)

        tabs.add(text1, text='Document 1')

        return tabs

    def tab_btn_press(self, event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify(x, y)
        index = widget.index('@%d,%d' % (x, y))

        if 'close' in elem:
            widget.state(['pressed'])
            widget.pressed_index = index

    def tab_btn_release(self, event):
        x, y, widget = event.x, event.y, event.widget

        if not widget.instate(['pressed']):
            return

        elem = widget.identify(x, y)
        index = widget.index('@%d,%d' % (x, y))

        if 'close' in elem and widget.pressed_index == index:
            widget.forget(index)
            widget.event_generate('<<NotebookClosedTab>>')

        widget.state(['!pressed'])
        widget.pressed_index = None

    def status_bar_init(self):
        status_bar = Frame(self.root)
        status_bar.grid(column=0, row=2, sticky='nsew')
        status_bar.config(relief='sunken')

        label = Label(status_bar, text='Status bar!')
        label.grid(column=0, row=0)

        return status_bar


tk = Tk()
app = PyEdit(tk)
tk.mainloop()
