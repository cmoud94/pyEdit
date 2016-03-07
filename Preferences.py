from tkinter.ttk import Style

from FontSelector import *


class Preferences:
    def __init__(self, parent):
        self.parent = parent
        self.config = []
        self.config_keys = ['text_wrap', 'text_wrap_whole_words', 'show_line_numbers', 'highlight_current_line',
                            'font_family', 'font_size', 'font_weight']
        self.config_default_values = [1, 1, 1, 1, 'Monospace', 10, 'normal']

        # text_wrap
        self.config.append(IntVar())

        # text_wrap_mode
        self.config.append(IntVar())

        # show_line_numbers
        self.config.append(IntVar())

        # highlight_current_line
        self.config.append(IntVar())

        # font_family
        self.config.append(StringVar())

        # font_size
        self.config.append(IntVar())

        # font_weight
        self.config.append(StringVar())

        self.font_btn_text = StringVar()

        self.font = font.Font(size=9, weight='bold')

        self.style = Style()
        self.style.theme_use('clam')

        self.root = Toplevel()
        self.root.title('pyEdit Preferences')
        self.root.minsize(300, 0)
        self.root.resizable(False, False)
        self.root.option_add('*tearOff', FALSE)
        self.root.columnconfigure(0, weight=1)

        self.root.bind('<Expose>', self.on_expose)
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)

        # Text wrapping
        self.lf_text_wrapping = LabelFrame(self.root, text='Text wrapping', font=self.font, relief='flat')
        self.lf_text_wrapping.grid(column=0, row=0, stick='nsew', padx=5, pady=5)

        self.chkbtn_text_wrap_enable = Checkbutton(self.lf_text_wrapping,
                                                   text='Enable text wrapping',
                                                   variable=self.config[0],
                                                   command=self.update_wrap_chkbtns)
        self.chkbtn_text_wrap_enable.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)
        self.chkbtn_text_wrap_enable.var = self.config[0]

        self.chkbtn_text_wrap_mode = Checkbutton(self.lf_text_wrapping,
                                                 text='Wrap whole words',
                                                 variable=self.config[1])
        self.chkbtn_text_wrap_mode.grid(column=0, row=1, sticky='nsw', padx=5, pady=5)
        self.chkbtn_text_wrap_mode.var = self.config[1]

        # Line numbers
        self.lf_line_numbers = LabelFrame(self.root, text='Line numbers', font=self.font, relief='flat')
        self.lf_line_numbers.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)

        self.chkbtn_line_numbers = Checkbutton(self.lf_line_numbers,
                                               text='Show line numbers',
                                               variable=self.config[2])

        self.chkbtn_line_numbers.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)
        self.chkbtn_line_numbers.var = self.config[2]

        # Current line
        self.lf_highlight_current_line = LabelFrame(self.root, text='Current line', font=self.font, relief='flat')
        self.lf_highlight_current_line.grid(column=0, row=2, sticky='nsew', padx=5, pady=5)

        self.chkbtn_highlight_current_line = Checkbutton(self.lf_highlight_current_line,
                                                         text='Highlight current line',
                                                         variable=self.config[3])
        self.chkbtn_highlight_current_line.grid(column=0, row=0, sticky='nsw', padx=5, pady=5)
        self.chkbtn_highlight_current_line.var = self.config[3]

        # Font
        self.lf_font = LabelFrame(self.root, text='Font settings', font=self.font, relief='flat')
        self.lf_font.grid(column=0, row=3, sticky='nsew', padx=5, pady=5)
        self.lf_font.columnconfigure(0, weight=1)

        self.btn_font = Button(self.lf_font,
                               textvariable=self.font_btn_text,
                               command=self.font_config)
        self.btn_font.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        # Buttons
        self.frame_buttons = Frame(self.root)
        self.frame_buttons.grid(column=0, row=4, sticky='se', padx=5, pady=5)

        self.btn_close = Button(self.frame_buttons,
                                text='Close',
                                command=self.config_write)
        self.btn_close.grid(column=0, row=0, sticky='se', padx=5, pady=5)

        # Read config
        if self.config_read() is None:
            self.config_write(create_new=True)
        self.config_read()

    def config_read(self):
        config_file = None
        try:
            config_file = open('config.conf', 'r')

            config_file.seek(0, 2)
            size = config_file.tell()
            config_file.seek(0, 0)
            config = config_file.read(size)

            config_file.close()

            if size == 0:
                return None
        except IOError:
            print('Error while reading config file!')
            return

        config_list = config.splitlines()
        config_list.remove(config_list[-1])
        ret = []

        for i in range(len(config_list)):
            kv = config_list[i].split('=')
            if kv[0] == 'text_wrap':
                self.config[0].set(int(kv[1]))
                ret.append(int(kv[1]))
            if kv[0] == 'text_wrap_whole_words':
                self.config[1].set(int(kv[1]))
                ret.append(int(kv[1]))
            if kv[0] == 'show_line_numbers':
                self.config[2].set(int(kv[1]))
                ret.append(int(kv[1]))
            if kv[0] == 'highlight_current_line':
                self.config[3].set(int(kv[1]))
                ret.append(int(kv[1]))
            if kv[0] == 'font_family':
                self.config[4].set(kv[1])
                ret.append(kv[1])
            if kv[0] == 'font_size':
                self.config[5].set(int(kv[1]))
                ret.append(int(kv[1]))
            if kv[0] == 'font_weight':
                self.config[6].set(kv[1])
                ret.append(kv[1])

        self.font_btn_text.set(self.config[4].get() + ' | ' + str(self.config[5].get()))

        self.update_wrap_chkbtns()

        return ret

    def config_read_startup(self):
        config = self.config_read()
        self.root.destroy()
        return config

    def config_write(self, event=None, create_new=False):
        try:
            conf_file = open('config.conf', 'w')
        except IOError:
            print('Error while opening config file for write!')
            return

        if not create_new:
            conf = [self.config[i].get() for i in range(len(self.config))]
        else:
            conf = [self.config_default_values[i] for i in range(len(self.config_default_values))]

        for i in range(len(conf)):
            conf_file.write(self.config_keys[i] + '=' + str(conf[i]) + '\n')

        conf_file.write('\n')
        conf_file.close()

        self.parent.config = conf
        self.root.grab_release()
        self.on_close()
        self.parent.config_update()

    def font_config(self, event=None):
        FontSelector(self)

    def update_wrap_chkbtns(self, event=None):
        if self.chkbtn_text_wrap_enable.var.get() == 0:
            self.chkbtn_text_wrap_mode.config(state='disable')
        else:
            self.chkbtn_text_wrap_mode.config(state='normal')

    def on_expose(self, event=None):
        # Center widget on top of parent window
        parent_x = self.parent.root.winfo_x()
        parent_y = self.parent.root.winfo_y()
        parent_w = self.parent.root.winfo_width()
        parent_x_mid = parent_x + (parent_w / 2)
        root_x = parent_x_mid - (self.root.winfo_width() / 2)
        root_y = parent_y
        self.root.geometry(
            str(self.root.winfo_width()) + 'x' + str(self.root.winfo_height()) + '+' + str(int(root_x)) + '+' + str(
                int(root_y)))

        self.root.grab_set()
        self.root.transient(self.parent.root)

    def on_close(self, event=None):
        self.root.grab_release()
        self.root.destroy()
