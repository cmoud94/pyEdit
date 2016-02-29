from LineNumbers import *


class TextEditor:
    def __init__(self, parent, file_path='', content=''):
        self.parent = parent
        self.file_path = file_path

        if self.file_path != '':
            index = file_path.rfind('/')
            self.file_name = self.file_path[index + 1:]
        else:
            self.file_name = 'Document'

        self.frame = Frame(self.parent.notebook)
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.text_widget = Text(self.frame,
                                relief='flat',
                                bd=0,
                                selectbackground='LightBlue3',
                                undo=True,
                                maxundo=-1,
                                autoseparator=True)
        self.text_widget.grid(column=1, row=0, sticky='nsew')
        self.text_widget.insert('1.0', content)
        self.text_widget.edit_modified(False)

        self.scroll_bar = Scrollbar(self.frame, bd=0, orient='vertical', command=self.scroll_update)
        self.scroll_bar.grid(column=2, row=0, sticky='ns')
        self.text_widget.config(yscrollcommand=self.scroll_bar.set)

        self.line_number_widget = LineNumbers(self.frame, self.text_widget)
        self.line_number_widget.update()

        self.parent.notebook.add(self.frame, text=self.file_name, compound='left')
        self.index = self.parent.notebook.index(self.parent.notebook.tabs()[-1])
        self.parent.notebook.select(self.index)

        self.text_widget.focus_set()

        # Banned keys for <KeyRelease> event
        self.banned_event_keys = ['Control_L', 'Control_R',
                                  'Shift_L', 'Shift_R',
                                  'Alt_L', 'Alt_R']

        # Shortcuts init
        self.text_widget.bind('<KeyRelease>', self.key_release)
        self.text_widget.bind('<Configure>', self.line_number_widget.update)
        self.text_widget.bind('<ButtonRelease>', self.mouse)

        # Unbinding
        self.text_widget.unbind_class('Text', '<Control-o>')
        self.text_widget.unbind_class('Text', '<<Undo>>')
        self.text_widget.unbind_class('Text', '<<Redo>>')
        self.text_widget.unbind_class('Text', '<<Cut>>')
        self.text_widget.unbind_class('Text', '<<Copy>>')
        self.text_widget.unbind_class('Text', '<<Paste>>')

        # print(self.text_widget.bind_class('Text'))

    def scroll_update(self, *event):
        # self.line_number_widget.update()
        if 'moveto' in event[0]:
            self.text_widget.yview_moveto(event[1])
            self.line_number_widget.line_widget.yview_moveto(event[1])
        elif 'scroll' in event[0]:
            self.text_widget.yview_scroll(event[1], event[2])
            self.line_number_widget.line_widget.yview_scroll(event[1], event[2])

    def key_release(self, event=None):
        if event.keysym in self.banned_event_keys:
            return
        self.line_number_widget.update()
        self.highlight_current_line()
        if self.text_widget.edit_modified():
            selected_tab = self.parent.notebook.index(self.parent.notebook.select())
            self.parent.notebook.tab(selected_tab, text='* ' + self.file_name)

    def mouse(self, event=None):
        left_btn = 1
        right_btn = 3
        scroll_up = 4
        scroll_down = 5

        if event.num == left_btn:
            self.highlight_current_line()

        if event.num in (scroll_up, scroll_down):
            self.line_number_widget.line_widget.yview_moveto(self.text_widget.yview()[0])

    def update_file_name(self, file_path):
        self.file_path = file_path
        index = file_path.rfind('/')
        self.file_name = file_path[index + 1:]
        print('File name updated to \'' + self.file_name + '\'')

    def highlight_current_line(self):
        self.text_widget.tag_remove('current_line', '1.0', 'end')
        # Where is the insert cursor
        current_pos = self.text_widget.index('insert')
        current_line = current_pos[:current_pos.find('.')]
        start_index = str(current_line) + '.0'
        end_index = str(int(current_line) + 1) + '.0'
        # print(str(current_pos) + ' | ' + str(current_line) + ' | ' + str(start_index) + ' | ' + str(end_index))
        self.text_widget.tag_add('current_line', start_index, end_index)
        self.text_widget.tag_config('current_line', background='#e0e0e0')
        self.highlight_selected_text()

    def highlight_selected_text(self):
        self.text_widget.tag_remove('selected_text', '1.0', 'end')
        try:
            self.text_widget.tag_add('selected_text', 'sel.first', 'sel.last')
            self.text_widget.tag_config('selected_text', background='LightBlue3')
        except TclError:
            print('highlight_selected_text error')
            return
