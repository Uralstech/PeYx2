from tkinter import *
from tkinter.font import Font
from tkinter.simpledialog import Dialog
from tkinter.colorchooser import askcolor
from os.path import abspath, dirname, join

class ListDialog(Dialog):
    __here = abspath(dirname(__file__))

    def __init__(self, master, title, data):
        self.data = data
        super().__init__(master, title)

    def body(self, master):
        master.pack(fill='both', expand=1)
        self.iconphoto(False, PhotoImage(file=abspath(join(ListDialog.__here, 'graphics/winicon.png'))))
        self.resizable(True, False)
        self.geometry('300x230')

        self.list_ = Listbox(master)
        for i, v in enumerate(self.data): self.list_.insert(i, v)
        self.list_.pack(fill='both', expand=1, padx=5, pady=1)

        return master
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="Close", width=10, command=self.ok, default=ACTIVE)
        w.pack(fill='x', expand=1, padx=5)
        self.bind("<Return>", lambda _:self.ok())
        box.pack(fill='both', expand=1)

class EditorSettingsDialog(Dialog):
    __fonts = ['Arial', 'Arial Black', 'Arial CE', 'Arial CYR', 'Arial TUR', 'Bahnschrift', 'Bodoni Bd BT', 'Calibri', 'Cambria', 'Candara', 'Cascadia Code', 'Cascadia Mono', 'CentSchbkCyrill BT', 'Century725 Cn BT', 'Comic Sans MS', 'Consolas', 'Constantia', 'Corbel', 'Courier', 'Courier New', 'DeVinne Txt BT', 'Ebrima', 'Embassy BT', 'EngraversGothic BT', 'Exotc350 Bd BT', 'Fixedsys', 'Franklin Gothic Medium', 'Freehand521 BT', 'Futura Bk BT', 'Gabriola', 'Gadugi', 'Geometr212 BkCn BT', 'Georgia', 'Humanst521 BT', 'Impact', 'Ink Free', 'Javanese Text', 'Kaufmann BT', 'Leelawadee UI', 'Lucida Console', 'Lucida Sans Unicode', 'MS Gothic', 'MS Sans Serif', 'MS Serif', 'MV Boli', 'Malgun Gothic', 'Marlett', 'Microsoft Himalaya', 'Microsoft JhengHei', 'Microsoft New Tai Lue', 'Microsoft PhagsPa', 'Microsoft Sans Serif', 'Microsoft Tai Le', 'Microsoft YaHei', 'Microsoft Yi Baiti', 'MingLiU-ExtB', 'Modern', 'Mongolian Baiti', 'Myanmar Text', 'News701 BT', 'NewsGoth BT', 'OCR-A BT', 'Palatino Linotype', 'Roman', 'Schadow BT', 'Script', 'Segoe Print', 'Segoe Script', 'Segoe UI', 'SimSun', 'Sitka Text', 'Small Fonts', 'Square721 BT', 'Swis721 Blk BT', 'Sylfaen', 'Symbol', 'System', 'Tahoma', 'Terminal', 'Times New Roman', 'Trebuchet MS', 'TypoUpright BT', 'Verdana', 'Webdings', 'Wingdings', 'Yu Gothic']
    __here = abspath(dirname(__file__))

    def __init__(self, master, title, font, size, fg, bg):
        self.font         = font
        self.size         = size
        self.fg           = fg
        self.bg           = bg
        self.isdefault    = False
        self.hasSubmitted = False

        super().__init__(master, title)
        
    def inverseColor(self, col):
        color = hex(16777215 - int(col[1:], 16))[2:]
        if len(color) < 6:
            for _ in range(6 - len(color)): color = f'0{color}'

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