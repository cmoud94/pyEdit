from tkinter import *


class LineNumbers:
    def __init__(self, frame, text_widget):
        self.frame = frame
        self.text_widget = text_widget
        self.line_widget = Text(self.frame,
                                takefocus=0,
                                state='disabled',
                                font=self.text_widget.config().get('font')[-1],
                                width=1,
                                relief='flat',
                                bd=0,
                                bg='#e0e0e0',
                                fg='#000',
                                spacing1=2,
                                spacing2=2,
                                spacing3=2)
        self.line_widget.grid(column=0, row=0, sticky='ns')
        self.line_num = ''

    def update(self, event=None):
        self.line_num = ''
        num_lines = self.text_widget.get('1.0', 'end').count('\n')

        for i in range(1, num_lines + 1):
            try:
                if len(str(i)) > self.line_widget['width']:
                    self.line_widget.config(width=len(str(i)))

                if i == num_lines:
                    self.line_num += str(i)
                else:
                    self.line_num += str(i) + '\n'

                fci = self.text_widget.index('%i.0' % i)
                lci = self.text_widget.index('%i.end' % i)
                self.text_widget.see(lci)
                first_char_bbox = self.text_widget.bbox(fci)
                last_char_bbox = self.text_widget.bbox(lci)

                if first_char_bbox is not None and last_char_bbox is not None:
                    first_char_bbox = list(first_char_bbox)
                    last_char_bbox = list(last_char_bbox)
                    while first_char_bbox[1] != last_char_bbox[1]:
                        first_char_bbox[1] += first_char_bbox[3]
                        self.line_num += '\n'
            except Exception:
                return

        self.line_widget.config(state='normal')
        self.line_widget.delete('1.0', 'end')
        self.line_widget.insert('1.0', self.line_num)
        self.line_widget.config(state='disabled')
        self.text_widget.see('1.0')

    def delete(self):
        self.line_widget.grid_forget()
        self.line_widget.destroy()
