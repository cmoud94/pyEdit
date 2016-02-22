from tkinter import filedialog
from tkinter.ttk import Notebook, Style

from TextEditor import *


class PyEdit:
    def __init__(self, root):
        # Style init
        self.style = Style()
        # self.style.theme_use('clam')

        # Window init
        self.root = root
        self.root.title('pyEdit')
        self.root.minsize(400, 300)
        self.root.option_add('*tearOff', FALSE)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Menu init
        self.menu_bar = self.menu_init()

        # Toolbar init
        self.img_new_file = PhotoImage(file='icons/24x24/document-new-8.png')
        self.img_open = PhotoImage(file='icons/24x24/document-open-7.png')
        self.img_save = PhotoImage(file='icons/24x24/document-save-2.png')
        self.img_search = PhotoImage(file='icons/24x24/edit-find-5.png')

        self.frame_toolbar = self.toolbar_init()

        # Tabs init
        self.tab_doc_img = PhotoImage('tab_doc', file='icons/document-new-7.png')
        self.tab_img_1 = PhotoImage('img_close', file='icons/close.png')
        self.tab_img_2 = PhotoImage('img_close_pressed', file='icons/close-pressed.png')
        self.tab_img_3 = PhotoImage('img_close_mouse_over', file='icons/close-focus.png')

        self.notebook = self.notebook_init()

        # Status bar init
        self.status_bar = self.status_bar_init()

        self.root.update()

        # Obsahuje instance tridy Editor, ktera obsahuje cestu k souboru, samotny nazev souboru, obsah souboru
        self.editors = []

    def menu_init(self):
        # Main menu_bar
        menu_bar = Menu(self.root)
        menu_bar.config(activebackground='LightBlue3', relief='flat')

        self.root.configure(menu=menu_bar)

        # File menu
        menu_file = Menu(menu_bar)
        menu_file.config(activebackground='LightBlue3')

        menu_file.add_command(label='New File', accelerator='Ctrl+N', command=self.new_tab)
        menu_file.add_command(label='Open', accelerator='Ctrl+O')
        menu_file.add_command(label='Save', accelerator='Ctrl+S')
        menu_file.add_command(label='Save as...', accelerator='Ctrl+Shift+S')
        menu_file.add_separator()
        menu_file.add_command(label='Exit', accelerator='Ctrl+Q')

        menu_bar.add_cascade(menu=menu_file, label='File')

        # Edit menu
        # menu_edit = Menu(menu_bar)

        return menu_bar

    def toolbar_init(self):
        frame_toolbar = Frame(self.root)
        frame_toolbar.grid(column=0, row=0, sticky='nw')

        # Toolbar buttons
        button_new_file = Button(frame_toolbar, image=self.img_new_file, relief='flat', activebackground='LightBlue3',
                                 command=self.new_tab)
        button_new_file.grid(column=0, row=0)

        button_open = Button(frame_toolbar, image=self.img_open, relief='flat', activebackground='LightBlue3',
                             command=self.open_file)
        button_open.grid(column=1, row=0)

        button_save = Button(frame_toolbar, image=self.img_save, relief='flat', activebackground='LightBlue3')
        button_save.grid(column=2, row=0)

        button_search = Button(frame_toolbar, image=self.img_search, relief='flat', activebackground='LightBlue3')
        button_search.grid(column=3, row=0)

        return frame_toolbar

    def notebook_init(self):
        self.style.element_create('close', 'image', 'img_close',
                                  ('active', 'pressed', '!disabled', 'img_close_pressed'),
                                  ('active', '!disabled', 'img_close_mouse_over'), sticky='nsew')

        self.style.layout('NotebookBtn', [('NotebookBtn.client', {'sticky': 'nsew'})])
        self.style.layout('NotebookBtn.Tab', [
            ('NotebookBtn.tab', {'sticky': 'nsew', 'children':
                [('NotebookBtn.padding', {'side': 'top', 'sticky': 'nsew', 'children':
                    [('NotebookBtn.focus', {'side': 'top', 'sticky': 'nsew', 'children':
                        [('NotebookBtn.label', {'side': 'left', 'sticky': 'nsew'}),
                         ('NotebookBtn.close', {'side': 'right', 'sticky': 'nsew'})]
                                            })]
                                          })]
                                 })
        ])

        self.style.configure('NotebookBtn.Tab', padding=3, image='tab_doc')
        self.style.map('NotebookBtn.Tab', background=[('selected', 'white')])

        self.root.bind_class('TNotebook', '<ButtonPress-1>', self.tab_btn_press, True)
        self.root.bind_class('TNotebook', '<ButtonRelease-1>', self.tab_btn_release)

        tabs = Notebook(self.root, style='NotebookBtn')
        tabs.grid(column=0, row=1, sticky='nsew')
        tabs.columnconfigure(0, weight=1)
        tabs.rowconfigure(0, weight=1)

        return tabs

    @staticmethod
    def tab_btn_press(event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify(x, y)
        index = widget.index('@%d,%d' % (x, y))

        if 'close' in elem:
            widget.state(['pressed'])
            widget.pressed_index = index

    @staticmethod
    def tab_btn_release(event):
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

        label = Label(status_bar, text='Status bar!', relief='sunken', bg='LightBlue3')
        label.grid(column=0, row=0)

        return status_bar

    def new_tab(self, file_path='', file_name='Document', content=''):
        self.editors.append(TextEditor(self.notebook, file_path, file_name, content))

    def open_file(self):
        file_path = filedialog.askopenfilename()
        index = file_path.rfind('/')
        file_name = file_path[index + 1:]

        file = open(file_path, 'r')
        file.seek(0, 2)
        size = file.tell()
        file.seek(0, 0)

        content = file.read(size)

        self.new_tab(file_path, file_name, content)

        file.close()


tk = Tk()
app = PyEdit(tk)
tk.mainloop()
