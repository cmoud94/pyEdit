from Tkinter import *
from ttk import Notebook, Style

root = Tk()

style = Style()

i1 = PhotoImage('img_close', file='CloseBtn_Normal.png')
i2 = PhotoImage('img_close_mouse_over', file='CloseBtn_MouseOver.png')
i3 = PhotoImage('img_close_pressed', file='CloseBtn_Pressed.png')

style.element_create('close', 'image', 'img_close',
                     ('active', 'pressed', '!disabled', 'img_close_pressed'),
                     ('active', '!disabled', 'img_close_mouse_over'), border=1, sticky='')

style.layout('ButtonNotebook', [('ButtonNotebook.client', {'sticky': 'nsew'})])
style.layout('ButtonNotebook.Tab', [
    ('ButtonNotebook.tab', {'sticky': 'nsew', 'children':
        [('ButtonNotebook.padding', {'side': 'top', 'sticky': 'nsew', 'children':
            [('ButtonNotebook.focus', {'side': 'top', 'sticky': 'nsew', 'children':
                [('ButtonNotebook.label', {'side': 'left', 'sticky': ''}),
                 ('ButtonNoteboook.close', {'side': 'right', 'sticky': ''})]
                                       })]
                                     })]
                            })
])


def btn_press(event):
    x, y, widget = event.x, event.y, event.widget
    elem = widget.identify(x, y)
    index = widget.index('@%d,%d' % (x, y))

    if 'close' in elem:
        widget.state(['pressed'])
        widget.pressed_index = index


def btn_release(event):
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


root.bind_class('TNotebook', '<ButtonPress-1>', btn_press, True)
root.bind_class('TNotebook', '<ButtonRelease-1>', btn_release)

nb = Notebook(width=200, height=200, style='ButtonNotebook')
nb.pressed_index = None

f1 = Frame(nb, bg='red')
f2 = Frame(nb, bg='green')
f3 = Frame(nb, bg='blue')

nb.add(f1, text='Red', padding=3)
nb.add(f2, text='Green', padding=3)
nb.add(f3, text='Blue', padding=3)

nb.pack(expand=True, fill='both')

root.mainloop()
