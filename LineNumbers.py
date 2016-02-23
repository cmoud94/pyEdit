import time
from threading import Thread
from tkinter import *


class LineNumbers(Thread):
    def __init__(self, frame, text_widget):
        Thread.__init__(self)
        self.frame = frame
        self.text_widget = text_widget
        self.line_widget = Text(self.frame,
                                takefocus=0,
                                state='disabled',
                                font=self.text_widget.config().get('font')[-1],
                                width=4,
                                relief='flat',
                                bd=0,
                                bg='light gray')
        self.line_widget.grid(column=0, row=0, sticky='ns')

        self.update_interval = 100  # ms
        self.line_num = ''

    def run(self):
        while True:
            self.line_num = ''
            num_lines = self.text_widget.get('1.0', 'end').count('\n')
            # first_visible_line = self.text_widget.index('@0,0')
            # int(first_visible_line[:first_visible_line.find('.')])
            for i in range(1, num_lines + 1):
                self.line_num += str(i) + '\n'
                first_char_bbox = self.text_widget.bbox(self.text_widget.index('%i.0' % i))
                last_char_bbox = self.text_widget.bbox(self.text_widget.index('%i.end' % i))
                if first_char_bbox is not None and last_char_bbox is not None:
                    first_char_bbox = list(first_char_bbox)
                    last_char_bbox = list(last_char_bbox)
                    while first_char_bbox[1] != last_char_bbox[1]:
                        first_char_bbox[1] += first_char_bbox[3]
                        self.line_num += '\n'
            self.line_widget.config(state='normal')
            self.line_widget.delete('1.0', 'end')
            self.line_widget.insert('1.0', self.line_num)
            self.line_widget.config(state='disabled')
            time.sleep(self.update_interval / 1000.0)
