from tkinter import *
from tkinter.font import Font
from tkinter.simpledialog import Dialog
from tkinter.colorchooser import askcolor
from os.path import abspath, dirname, join

class LangConfigDialog(Dialog):
    __here = abspath(dirname(__file__))

    def __init__(self, master, title):
        self.extension    = None
        self.modules      = None
        self.keywords     = None
        self.imports      = None
        self.command      = None
        self.hasSubmitted = False
        self.e1FirstFocus = False
        self.e2FirstFocus = False
        self.e3FirstFocus = False
        self.e4FirstFocus = False
        self.e5FirstFocus = False

        super().__init__(master, title)

    def focus_e1(self):
        if not self.e1FirstFocus:
            self.e1.delete(0, END)
            self.e1.config(fg='black', font=Font(slant='roman'))
            self.e1FirstFocus = True

    def focus_e2(self):
        if not self.e2FirstFocus:
            self.e2.delete(0, END)
            self.e2.config(fg='black', font=Font(slant='roman'))
            self.e2FirstFocus = True

    def focus_e3(self):
        if not self.e3FirstFocus:
            self.e3.delete(0, END)
            self.e3.config(fg='black', font=Font(slant='roman'))
            self.e3FirstFocus = True

    def focus_e4(self):
        if not self.e4FirstFocus:
            self.e4.delete(0, END)
            self.e4.config(fg='black', font=Font(slant='roman'))
            self.e4FirstFocus = True

    def focus_e5(self):
        if not self.e5FirstFocus:
            self.e5.delete(0, END)
            self.e5.config(fg='black', font=Font(slant='roman'))
            self.e5FirstFocus = True

    def body(self, master):
        master.pack(fill='both', expand=1)
        self.iconphoto(False, PhotoImage(file=abspath(join(LangConfigDialog.__here, 'graphics/winicon.png'))))
        self.resizable(True, False)

        self.tx = Label(master, text='USE COMMA SEPERATED VALUES') 
        self.e1 = Entry(master, fg='grey', font=Font(slant='italic'))
        self.e2 = Entry(master, fg='grey', font=Font(slant='italic'))
        self.e3 = Entry(master, fg='grey', font=Font(slant='italic'))
        self.e4 = Entry(master, fg='grey', font=Font(slant='italic'))
        self.e5 = Entry(master, fg='grey', font=Font(slant='italic'))

        self.e1.insert(0, 'extension (.py, .cpp, .c, .cs, .java, .ezr, ...)')
        self.e2.insert(0, 'modules (tkinter, time, os, sys, ShrtCde, ...)')
        self.e3.insert(0, 'keywords (True, and, if, try, def, class, ...)')
        self.e4.insert(0, 'imports (import ___MODULE___, from ___MODULE___, ...)')
        self.e5.insert(0, 'command (python ___FILE___, ezrShell ___FILE___, ...)')

        self.tx.pack(fill='x', expand=1, padx=5, pady=5)
        self.e1.pack(fill='x', expand=1, padx=5)
        self.e2.pack(fill='x', expand=1, padx=5, pady=5)
        self.e3.pack(fill='x', expand=1, padx=5)
        self.e4.pack(fill='x', expand=1, padx=5, pady=5)
        self.e5.pack(fill='x', expand=1, padx=5)

        self.e1.bind('<FocusIn>', lambda _: self.focus_e1())
        self.e2.bind('<FocusIn>', lambda _: self.focus_e2())
        self.e3.bind('<FocusIn>', lambda _: self.focus_e3())
        self.e4.bind('<FocusIn>', lambda _: self.focus_e4())
        self.e5.bind('<FocusIn>', lambda _: self.focus_e5())

        return master
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="Create", width=10, command=self.ok, default=ACTIVE)
        w.pack(fill='x', expand=1, padx=5, pady=5)
        self.bind("<Return>", lambda x:self.ok())
        box.pack(fill='both', expand=1)

    def ok(self):
        self.hasSubmitted = True
        self.extension    = self.e1.get()
        self.modules      = self.e2.get()
        self.keywords     = self.e3.get()
        self.imports      = self.e4.get()
        self.command      = self.e5.get()

        self.destroy()

class ListDialog(Dialog):
    __here = abspath(dirname(__file__))

    def __init__(self, master, title, files):
        self.files = files
        super().__init__(master, title)

    def body(self, master):
        master.pack(fill='both', expand=1)
        self.iconphoto(False, PhotoImage(file=abspath(join(ListDialog.__here, 'graphics/winicon.png'))))
        self.resizable(True, False)

        self.list_ = Listbox(master)
        for i, v in enumerate(self.files): self.list_.insert(i, v)
        self.list_.pack(fill='both', expand=1, padx=5, pady=5)

        return master
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="Close", width=10, command=self.ok, default=ACTIVE)
        w.pack(fill='x', expand=1, padx=5, pady=5)
        self.bind("<Return>", lambda x:self.ok())
        box.pack(fill='both', expand=1)

class EditorSettingsDialog(Dialog):
    __fonts = ['Arial', 'Arial Black', 'Arial CE', 'Arial CYR', 'Arial TUR', 'Bahnschrift', 'Bodoni Bd BT', 'Calibri', 'Cambria', 'Candara', 'Cascadia Code', 'Cascadia Mono', 'CentSchbkCyrill BT', 'Century725 Cn BT', 'Comic Sans MS', 'Consolas', 'Constantia', 'Corbel', 'Courier', 'Courier New', 'DeVinne Txt BT', 'Ebrima', 'Embassy BT', 'EngraversGothic BT', 'Exotc350 Bd BT', 'Fixedsys', 'Franklin Gothic Medium', 'Freehand521 BT', 'Futura Bk BT', 'Gabriola', 'Gadugi', 'Geometr212 BkCn BT', 'Georgia', 'Humanst521 BT', 'Impact', 'Ink Free', 'Javanese Text', 'Kaufmann BT', 'Leelawadee UI', 'Lucida Console', 'Lucida Sans Unicode', 'MS Gothic', 'MS Sans Serif', 'MS Serif', 'MV Boli', 'Malgun Gothic', 'Marlett', 'Microsoft Himalaya', 'Microsoft JhengHei', 'Microsoft New Tai Lue', 'Microsoft PhagsPa', 'Microsoft Sans Serif', 'Microsoft Tai Le', 'Microsoft YaHei', 'Microsoft Yi Baiti', 'MingLiU-ExtB', 'Modern', 'Mongolian Baiti', 'Myanmar Text', 'News701 BT', 'NewsGoth BT', 'OCR-A BT', 'Palatino Linotype', 'Roman', 'Schadow BT', 'Script', 'Segoe Print', 'Segoe Script', 'Segoe UI', 'SimSun', 'Sitka Text', 'Small Fonts', 'Square721 BT', 'Swis721 Blk BT', 'Sylfaen', 'Symbol', 'System', 'Tahoma', 'Terminal', 'Times New Roman', 'Trebuchet MS', 'TypoUpright BT', 'Verdana', 'Webdings', 'Wingdings', 'Yu Gothic']
    __here = abspath(dirname(__file__))

    def __init__(self, master, title, font, size, fg, bg, h1, h2):
        self.font         = font
        self.size         = size
        self.fg           = fg
        self.bg           = bg
        self.h1           = h1
        self.h2           = h2
        self.isdefault    = False
        self.hasSubmitted = False

        super().__init__(master, title)
        
    def inverseColor(self, col):
        color = hex(16777215 - int(col[1:], 16))[2:]
        if len(color) < 6:
            for i in range(6 - len(color)): color = f'0{color}'

        return f'#{color}'
        
    def setbg(self):
        color = askcolor(title='Background Color')
        if color != (None, None):
            self.bg = color[1]
            self.bb.config(bg=self.bg, fg=self.inverseColor(self.bg))
        
    def setfg(self):
        color = askcolor(title='Foreground Color')
        if color != (None, None):
            self.fg = color[1]
            self.fb.config(bg=self.fg, fg=self.inverseColor(self.fg))
        
    def seth1(self):
        color = askcolor(title='Highlight (1) Color')
        if color != (None, None):
            self.h1 = color[1]
            self.h1b.config(bg=self.h1, fg=self.inverseColor(self.h1))
        
    def seth2(self):
        color = askcolor(title='Highlight (2) Color')
        if color != (None, None):
            self.h2 = color[1]
            self.h2b.config(bg=self.h2, fg=self.inverseColor(self.h2))

    def updateMenu(self):
        self.ft.config(font=Font(family=self.ftVar.get()))

    def body(self, master):
        master.pack(fill='both', expand=1)
        self.iconphoto(False, PhotoImage(file=abspath(join(EditorSettingsDialog.__here, 'graphics/winicon.png'))))
        self.resizable(False, False)

        self.ftVar = StringVar(master, self.font)
        self.ft = OptionMenu(master, self.ftVar, *EditorSettingsDialog.__fonts, command=lambda _:self.updateMenu())
        
        self.ft.config(font=Font(family=self.font))
        for i in range(self.ft['menu'].index(END)): self.ft['menu'].entryconfig(i, font=Font(family=EditorSettingsDialog.__fonts[i]))

        self.ft.pack(fill='x', expand=1, padx=5, pady=5)

        self.szVar = StringVar(master, self.size)
        self.sz = Spinbox(master, from_=5, to=50, textvariable=self.szVar, width=5)
        self.sz.pack(fill='x', expand=1, padx=5)

        self.bb = Button(master, text='Background', bg=self.bg, fg=self.inverseColor(self.bg), command=self.setbg)
        self.bb.pack(fill='x', expand=1, padx=5, pady=5)

        self.fb = Button(master, text='Foreground', bg=self.fg, fg=self.inverseColor(self.fg), command=self.setfg)
        self.fb.pack(fill='x', expand=1, padx=5)

        self.h1b = Button(master, text='Highlight (1)', bg=self.h1, fg=self.inverseColor(self.h1), command=self.seth1)
        self.h1b.pack(fill='x', expand=1, padx=5, pady=5)

        self.h2b = Button(master, text='Highlight (2)', bg=self.h2, fg=self.inverseColor(self.h2), command=self.seth2)
        self.h2b.pack(fill='x', expand=1, padx=5)

        return master
    
    def buttonbox(self):
        box = Frame(self)
        
        w = Button(box, text="Save", width=15, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, anchor=W, padx=5, pady=5)

        w = Button(box, text="Default", width=15, command=self.default)
        w.pack(side=RIGHT, anchor=E, padx=5, pady=5)

        self.bind("<Return>", lambda x:self.ok())
        box.pack(fill='both', expand=1)

    def default(self):
        self.hasSubmitted = True
        self.isdefault = True
        self.destroy()

    def ok(self):
        self.hasSubmitted = True
        self.font = self.ftVar.get()
        self.size = int(self.szVar.get())

        self.destroy()