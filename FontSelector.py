from collections import OrderedDict
from tkinter import *
from tkinter import font


class FontSelector:
    def __init__(self, parent):
        self.parent = parent
        self.selected_family = parent.config[4]
        self.selected_size = parent.config[5]
        self.selected_weight = parent.config[6]

        families = list(OrderedDict.fromkeys(font.families()))
        families.sort()

        sizes_low = [x for x in range(7, 19)]
        sizes_high = [x for x in range(20, 74, 2)]
        sizes = sizes_low + sizes_high

        weights = ('normal', 'bold')

        self.families = StringVar()
        self.sizes = StringVar()
        self.weight = StringVar()

        self.families.set(tuple(families))
        self.sizes.set(tuple(sizes))
        self.weight.set(weights)

        self.font = font.Font(size=9, weight='bold')

        self.root = Toplevel()
        self.root.title('pyEdit Font Selector')
        self.root.resizable(False, False)

        # Family
        self.lf_family = LabelFrame(self.root, text='Family:', font=self.font, relief='flat')
        self.lf_family.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        self.frame_family = Frame(self.lf_family)
        self.frame_family.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        self.listbox_family = Listbox(self.frame_family, listvariable=self.families)
        self.listbox_family.grid(column=0, row=0, sticky='nsew')

        self.scrollbar_family = Scrollbar(self.frame_family, orient='vertical', command=self.listbox_family.yview)
        self.scrollbar_family.grid(column=1, row=0, sticky='ns')
        self.listbox_family.config(yscrollcommand=self.scrollbar_family.set)

        # Size
        self.lf_size = LabelFrame(self.root, text='Size:', font=self.font, relief='flat')
        self.lf_size.grid(column=1, row=0, sticky='nsew', padx=5, pady=5)

        self.frame_size = Frame(self.lf_size)
        self.frame_size.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        self.listbox_size = Listbox(self.frame_size, listvariable=self.sizes, width=3)
        self.listbox_size.grid(column=0, row=0, sticky='nsew')

        self.scrollbar_size = Scrollbar(self.frame_size, orient='vertical', command=self.listbox_size.yview)
        self.scrollbar_size.grid(column=1, row=0, sticky='ns')
        self.listbox_size.config(yscrollcommand=self.scrollbar_size.set)

        # Weight
        self.lf_weight = LabelFrame(self.root, text='Weight:', font=self.font, relief='flat')
        self.lf_weight.grid(column=0, row=1, sticky='nsew', padx=5, pady=5, columnspan=2)
        self.lf_weight.columnconfigure(0, weight=1)

        self.frame_weight = Frame(self.lf_weight)
        self.frame_weight.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
        self.frame_weight.columnconfigure(0, weight=1)

        self.listbox_weight = Listbox(self.frame_weight, listvariable=self.weight, height=2)
        self.listbox_weight.grid(column=0, row=0, sticky='nsew')

        # Slant
        # self.lf_slant = LabelFrame(self.root, text='Slant:', font=self.font, relief='flat')
        # self.lf_slant.grid(column=0, row=2, sticky='nsew', padx=5, pady=5, columnspan=2)
        # self.lf_slant.columnconfigure(0, weight=1)
        #
        # self.frame_slant = Frame(self.lf_slant)
        # self.frame_slant.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
        # self.frame_slant.columnconfigure(0, weight=1)
        #
        # self.listbox_slant = Listbox(self.frame_slant, listvariable=self.weight, height=2)
        # self.listbox_slant.grid(column=0, row=0, sticky='nsew')

        self.frame_btn = Frame(self.root)
        self.frame_btn.grid(column=0, row=2, sticky='nsew', padx=5, pady=5, columnspan=2)
        self.frame_btn.columnconfigure(0, weight=1)

        self.btn_close = Button(self.frame_btn, text='Close', command=self.btn_click)
        self.btn_close.grid(column=0, row=0, sticky='nse', padx=5, pady=5)

    def btn_click(self):
        family = StringVar()
        size = IntVar()
        weight = StringVar()

        if len(self.listbox_family.curselection()) == 1:
            family.set(self.listbox_family.get(self.listbox_family.curselection()[0]))
            self.parent.config[4] = family

        if len(self.listbox_size.curselection()) == 1:
            size.set(self.listbox_size.get(self.listbox_size.curselection()[0]))
            self.parent.config[5] = size

        if len(self.listbox_weight.curselection()) == 1:
            weight.set(self.listbox_weight.get(self.listbox_weight.curselection()[0]))
            self.parent.config[6] = weight

        self.root.destroy()
