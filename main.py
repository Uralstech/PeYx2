from tkinter import *
from copy import copy
from tkinter.font import Font
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.dialog import Dialog
from os.path import abspath, dirname, isfile, join, splitext
from tkinter.messagebox import showerror
from language import LangConfigHelper
from settings import EditorSettingsHelper
from webbrowser import open as openweb
from os import getcwd, chdir, system
from sys import argv

class PeYx2:
    __here = abspath(dirname(__file__))

    def __init__(self, filepath):
        self.filepath = filepath
        self.startOpen = isfile(filepath)

        self.langHelper = LangConfigHelper()
        self.langData = self.langHelper.GetLangConfig(filepath)

        self.editorHelper = EditorSettingsHelper()
        self.editorData = self.editorHelper.GetEditorSettings()

        self.tempText = ''
        self.oldText = ''
        self.initializeWindow()

    def initializeWindow(self):
        self.root = Tk()
        self.root.title(f'PeYx2 - {self.filepath if isfile(self.filepath) else "Untitled"}')
        self.root.iconphoto(False, PhotoImage(file=abspath(join(PeYx2.__here, 'graphics/winicon.png'))))
        self.root.geometry('500x500')
        self.root.minsize(500, 500)

        self.initializeGraphics()
        if self.startOpen:
            self.openFile(filepath=self.filepath, override=True)
            self.startOpen = False

        self.root.protocol('WM_DELETE_WINDOW', self.checkAndQuit)
        self.root.mainloop()

    def checkAndQuit(self):
        num = self.checkSaveDialog('PeYx2: Quit?', f'Quitting will discard all changes.')
        if num != -1 and num != 3:
            self.root.destroy()

    def refreshWindow(self):
        self.root.destroy()
        del self.root

        self.initializeWindow()

    def openFile(self, filepath=None, override=False):
        if not override:
            num = self.checkSaveDialog('PeYx2: Open another file?', f'Opening another file will discard all changes.')
            if num == -1 or num == 3: return None

        if filepath == None or not isfile(filepath): filepath = askopenfilename(title="PeYx2: Open File", defaultextension='.txt', initialdir=getcwd(), filetypes=(("All Files", '*.*'), ("Text File (.txt)", '.txt'), ("Python Source File (.py)", '.py'), ("ezr Source File (.ezr)", '.ezr'), ("C Source File (.c)", '.c'), ("C++ Source File (.cpp)", '.cpp'), ("C/C++ Header File (.h)", '.h'), ("Java Source File (.java)", '.java')))
        if isfile(filepath):
            self.filepath = filepath

            chdir(abspath(dirname(self.filepath)))
            self.root.title(f'PeYx2 - {self.filepath}')

            try:
                with open(self.filepath, 'r') as f:
                    self.textbox.delete('0.0', END)
                    self.textbox.insert('0.0', f.read())
                self.langData = self.langHelper.GetLangConfig(self.filepath)
                self.oldText = ''
            except Exception as error:
                showerror('PeYx2 File Opener', f'An unexpected error occured!\n\n{str(error)}')

    def newFile(self):
        num = self.checkSaveDialog('PeYx2: Create new file?', 'Creating a new file will discard all changes.')
        if num == -1 or num == 3: return None

        self.filepath = ''
        self.oldText = ''
        self.textbox.delete('0.0', END)
    
    def saveFile(self, saveas=False):
        if not isfile(self.filepath) or saveas:
            filepath = asksaveasfilename(title="PeYx2: Save File", defaultextension='.txt', initialdir=getcwd(), filetypes=(("All Files", '*.*'), ("Text File (.txt)", '.txt'), ("Python Source File (.py)", '.py'), ("ezr Source File (.ezr)", '.ezr'), ("C Source File (.c)", '.c'), ("C++ Source File (.cpp)", '.cpp'), ("C/C++ Header File (.h)", '.h'), ("Java Source File (.java)", '.java')))
            if filepath != '': self.filepath = filepath
            else: return -1

        chdir(abspath(dirname(self.filepath)))
        self.root.title(f'PeYx2 - {self.filepath}')

        try:
            with open(self.filepath, 'w') as f:
                f.write(self.textbox.get('0.0',END)[:-1])
            self.openFile(filepath=self.filepath)
            self.langData = self.langHelper.GetLangConfig(self.filepath)
        except Exception as error:
            showerror('PeYx2 File Writer', f'An unexpected error occured!\n\n{str(error)}')
            return -1
        return 0

    def runFile(self):
        check = self.checkSave()
        if check == -1: return None

        if check:
            dialog = Dialog(None, {'title': 'PeYx2: File not saved',
                            'text': f'File \'{self.filepath if self.filepath != "" else "Untitled"}\' has been modified.\nIt must be saved before execution.',
                            'bitmap': 'error',
                            'default': 0,
                            'strings': ('Save File',
                                        'Cancel')})
            if dialog.num == 0:
                if self.saveFile() == -1: return None
            elif dialog.num == 1:
                return None
        
        if self.langData == None:
            showerror('PeYx2 File Executioner', f'No .langConfig has been set up for file type \'{splitext(self.filepath)[1]}\'')
            return None

        system(self.langData.command)

    def updateText(self):
        if self.oldText != self.textbox.get('0.0', END) and self.langData != None:
            oldText = self.oldText.split('\n')
            self.oldText = self.textbox.get('0.0', END)
            diff = [[i, v] for i, v in enumerate(self.textbox.get('0.0', END).split('\n')) if i >= len(oldText) or oldText[i] != v]

            for i in diff:
                for i2 in self.langData.syntaxes:
                    self.textbox.tag_remove(i2.name, f'{i[0]+1}.0', f'{i[0]+1}.{len(i[1])}')
                    if i2.sub_syntaxes != None:
                        for i3 in i2.sub_syntaxes: self.textbox.tag_remove(i3.name, f'{i[0]+1}.0', f'{i[0]+1}.{len(i[1])}')

                for i2 in self.langData.syntaxes:
                    matches = i2.regex.finditer(i[1])
                    for i3 in matches:
                        self.textbox.tag_configure(i2.name, foreground=i2.color)
                        self.textbox.tag_add(i2.name, f'{i[0]+1}.{i3.start()}', f'{i[0]+1}.{i3.end()}')
                        
                        if i2.sub_syntaxes != None:
                            for i4 in i2.sub_syntaxes:
                                sub_matches = i4.regex.finditer(i3.string)
                                for i5 in sub_matches:
                                    self.textbox.tag_configure(i4.name, foreground=i4.color)
                                    self.textbox.tag_add(i4.name, f'{i[0]+1}.{i5.start()}', f'{i[0]+1}.{i5.end()}')
        self.root.after(10, self.updateText)

    def fullUpdate(self):
        self.oldText = ''
        self.root.after(5000, self.fullUpdate)

    def checkSave(self):
        data = None
        if isfile(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    data = f.read()
            except Exception as error:
                showerror('PeYx2 File Save Checker', f'An unexpected error occured!\n\n{str(error)}')
                return -1

        notSaved = not isfile(self.filepath) and self.textbox.get('0.0', END)[:-1] != ''
        saved = data != None and data != self.textbox.get('0.0', END)[:-1]

        return saved or notSaved

    def checkSaveDialog(self, title, message):
        check = self.checkSave()
        if check == -1: return -1

        if check:
            dialog = Dialog(None, {'title': title,
                            'text': '\n'.join((f'File \'{self.filepath if self.filepath != "" else "Untitled"}\' has been modified.', message)),
                            'bitmap': 'warning',
                            'default': 0,
                            'strings': ('Save File',
                                        'Discard Changes',
                                        'Cancel')})

            if dialog.num == 0:
                if self.saveFile() == 0: return 1
                return -1
            elif dialog.num == 1:
                return 2
            elif dialog.num == 2:
                return 3
        return 0

    def changeTheme(self):
        self.editorHelper.CreateEditorSettings(self.root)
        oldEditorData = copy(self.editorData)

        self.editorData = self.editorHelper.GetEditorSettings()

        if oldEditorData != self.editorData:
            self.tempText = self.textbox.get('0.0', END)[:-1]
            self.refreshWindow()

    def copyText(self):
        self.textbox.clipboard_clear()
        if self.textbox.tag_ranges(SEL): self.textbox.clipboard_append(self.textbox.get(SEL_FIRST, SEL_LAST))

    def cutText(self):
        self.textbox.clipboard_clear()
        if self.textbox.tag_ranges(SEL):
            self.textbox.clipboard_append(self.textbox.get(SEL_FIRST, SEL_LAST))
            self.textbox.delete(SEL_FIRST, SEL_LAST)
    
    def pasteText(self):
        try: text = self.textbox.clipboard_get()
        except Exception: text = ''

        if self.textbox.tag_ranges(SEL):
            self.textbox.replace(SEL_FIRST, SEL_LAST, text)
        else:
            self.textbox.insert(self.textbox.index(INSERT), text)

    def initializeGraphics(self):
        vScroll = Scrollbar(self.root, orient=VERTICAL)
        vScroll.pack(side=RIGHT, fill='y', expand=1)
        hScroll = Scrollbar(self.root, orient=HORIZONTAL)
        hScroll.pack(side=BOTTOM, fill='x', expand=1)

        font = Font(family=self.editorData.font, size=self.editorData.size)
        self.textbox = Text(self.root, width=10000, height=10000, bg=self.editorData.bg, fg=self.editorData.fg, insertbackground=self.editorData.fg, font=font, xscrollcommand=hScroll.set, yscrollcommand=vScroll.set, tabs=font.measure('    '), wrap='none', undo=True)
        self.textbox.insert(END, self.tempText)
        self.textbox.pack(fill='both', expand=1)

        hScroll.config(command=self.textbox.xview)
        vScroll.config(command=self.textbox.yview)

        menu = Menu(self.root)

        file = Menu(menu, tearoff=0)
        file.add_command(label='New', accelerator='Ctrl+N', command=self.newFile)
        file.add_command(label='Open', accelerator='Ctrl+O', command=lambda:self.openFile())
        file.add_command(label='Save', accelerator='Ctrl+S', command=lambda:self.saveFile())
        file.add_command(label='Save as...', accelerator='Ctrl+A+S', command=lambda:self.saveFile(saveas=True))
        file.add_separator()
        file.add_command(label='Quit', accelerator='Alt+F4', command=self.checkAndQuit)

        menu.add_cascade(label='File', menu=file)

        edit = Menu(menu, tearoff=0)
        edit.add_command(label='Cut', accelerator='Ctrl+X', command=self.cutText)
        edit.add_command(label='Copy', accelerator='Ctrl+C', command=self.copyText)
        edit.add_command(label='Paste', accelerator='Ctrl+V', command=self.pasteText)
        edit.add_separator()
        edit.add_command(label='Undo', accelerator='Ctrl+Z', command=self.textbox.edit_undo)
        edit.add_command(label='Redo', accelerator='Ctrl+Y', command=self.textbox.edit_redo)

        menu.add_cascade(label='Edit', menu=edit)

        theme = Menu(menu, tearoff=0)
        theme.add_command(label='Change theme', command=self.changeTheme)

        menu.add_cascade(label='Theme', menu=theme)

        ide = Menu(menu, tearoff=0)
        ide.add_command(label='Run file', accelerator='F5', command=self.runFile)
        ide.add_separator()
        ide.add_command(label='List all langConfigs', command=lambda:self.langHelper.ShowLangConfigs(self.root))

        menu.add_cascade(label='IDE', menu=ide)

        peyx2 = Menu(menu, tearoff=0)
        peyx2.add_cascade(label='PeYx2 wiki', command=lambda:openweb('https://github.com/uralstech/peyx2/wiki', new=2))
        peyx2.add_cascade(label='PeYx2 code', command=lambda:openweb('https://github.com/uralstech/peyx2', new=2))
        peyx2.add_cascade(label='PeYx2 ReadMe', command=lambda:self.openFile(abspath(join(PeYx2.__here, 'README.md'))))
        peyx2.add_cascade(label='PeYx2 License', command=lambda:self.openFile(abspath(join(PeYx2.__here, 'LICENSE'))))

        menu.add_cascade(label='Help', menu=peyx2)

        self.root.config(menu=menu)

        self.root.bind('<Control-n>', lambda _:self.newFile())
        self.root.bind('<Control-o>', lambda _:self.openFile())
        self.root.bind('<Control-s>', lambda _:self.saveFile())
        self.root.bind('<Control-a>s', lambda _:self.saveFile(saveas=True))

        self.root.bind('<Control-z>', lambda _:self.textbox.edit_undo())
        self.root.bind('<Control-y>', lambda _:self.textbox.edit_redo())

        self.root.bind('<F5>', lambda _:self.runFile())
        self.root.bind('<F1>', lambda _:openweb('https://github.com/uralstech/peyx2/wiki', new=2))

        self.updateText()
        self.fullUpdate()

def main():
    filepath = ''
    if len(argv) > 1: filepath = argv[1]
    
    PeYx2(filepath)

if __name__ == '__main__':
    main()