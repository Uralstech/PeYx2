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
                self.oldText = self.textbox.get('0.0', END)[:-1] + 'Ö¬╚{§'
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
        if self.oldText != self.textbox.get('0.0', END)[:-1] and self.langData != None:
            text = self.textbox.get('0.0', END)
            for i, v in enumerate(text.split('\n'), 0):
                wordSplit = v.split(' ')
                start = 0
                for v2 in wordSplit:
                    splitWord = ''
                    if ':' in v2 or '(' in v2 or '.' in v2:
                        keys = '.():'
                        for key in keys:
                            if key in v2:
                                if isinstance(splitWord, list):
                                    for i2 in range(len(splitWord)):
                                        if key in splitWord[i2]:
                                            word = splitWord[i2].split(key)

                                            index = 0
                                            for _ in range(len(word)-1):
                                                word.insert(index+1, key)
                                                index += 2
                                            
                                            index = i2
                                            del splitWord[i2]
                                            for v3 in word:
                                                splitWord.insert(index, v3)
                                                index += 1
                                else:
                                    splitWord = v2.split(key)

                                    index = 0
                                    for i2 in range(len(splitWord)-1):
                                        splitWord.insert(index+1, key)
                                        index += 2

                        for i2, v3 in enumerate(splitWord):
                            classCheck = False
                            for v4 in self.langData.imports:
                                if v4.replace('___MODULE___', v3) in text:
                                    classCheck = True
                                    break

                            if v3 in self.langData.keywords: splitWord[i2] += '#T0'
                            elif v3 in self.langData.modules and classCheck: splitWord[i2] += '#T1'
                    
                    if splitWord == '':
                        classCheck = False
                        for v3 in self.langData.imports:
                            if v3.replace('___MODULE___', v2) in text:
                                classCheck = True

                        if v2 in self.langData.keywords: self.textbox.replace(f'{i+1}.{start}', f'{i+1}.{start+len(v2)}', v2, 'highlight')
                        elif v2 in self.langData.modules and classCheck: self.textbox.replace(f'{i+1}.{start}', f'{i+1}.{start+len(v2)}', v2, 'highlight2')
                        else: self.textbox.replace(f'{i+1}.{start}', f'{i+1}.{start+len(v2)}', v2)
                    else:
                        length = 0
                        for i2, v3 in enumerate(splitWord):
                            if v3.endswith('#T0'): self.textbox.replace(f'{i+1}.{start+length}', f'{i+1}.{start+length+len(v3)-3}', v3[:-3], 'highlight'); length += len(v3) - 3
                            elif v3.endswith('#T1'): self.textbox.replace(f'{i+1}.{start+length}', f'{i+1}.{start+length+len(v3)-3}', v3[:-3], 'highlight2'); length += len(v3) - 3
                            else: self.textbox.replace(f'{i+1}.{start+length}', f'{i+1}.{start+length+len(v3)}', v3); length += len(v3)
                    
                    start += len(v2) + 1
            
            self.oldText = self.textbox.get('0.0', END)
        self.root.after(1000, self.updateText)

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

    def changeLangConfigs(self):
        self.langHelper.CreateLangConfig(self.root)
        self.langData = self.langHelper.GetLangConfig(self.filepath)
        self.textbox.get

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

        self.textbox = Text(self.root, width=10000, height=10000, bg=self.editorData.bg, fg=self.editorData.fg, insertbackground=self.editorData.fg, font=Font(family=self.editorData.font, size=self.editorData.size), xscrollcommand=hScroll.set, yscrollcommand=vScroll.set, wrap='none', undo=True)
        self.textbox.insert(END, self.tempText)
        self.textbox.tag_configure('highlight', foreground=self.editorData.h1)
        self.textbox.tag_configure('highlight2', foreground=self.editorData.h2)
        self.textbox.pack(fill='both', expand=1)

        hScroll.config(command=self.textbox.xview)
        vScroll.config(command=self.textbox.yview)

        menu = Menu(self.root)

        file = Menu(menu, tearoff=0)
        file.add_command(label='New', accelerator='Ctrl+N', command=self.newFile)
        file.add_command(label='Open', accelerator='Ctrl+O', command=lambda:self.openFile(filepath=self.filepath))
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
        ide.add_command(label='Create langConfig', command=self.changeLangConfigs)
        ide.add_command(label='List all langConfigs', command=lambda:self.langHelper.ShowLangConfigs(self.root))

        menu.add_cascade(label='IDE', menu=ide)

        peyx2 = Menu(menu, tearoff=0)
        peyx2.add_cascade(label='PeYx2 wiki', command=lambda:openweb('https://github.com/uralstech/peyx2/wiki', new=2))
        peyx2.add_cascade(label='PeYx2 code', command=lambda:openweb('https://github.com/uralstech/peyx2', new=2))

        menu.add_cascade(label='Help', menu=peyx2)

        self.root.config(menu=menu)

        self.root.bind('<Control-n>', lambda _:self.newFile())
        self.root.bind('<Control-o>', lambda _:self.openFile(filepath=self.filepath))
        self.root.bind('<Control-s>', lambda _:self.saveFile())
        self.root.bind('<Control-a>s', lambda _:self.saveFile(saveas=True))

        self.root.bind('<Control-z>', lambda _:self.textbox.edit_undo())
        self.root.bind('<Control-y>', lambda _:self.textbox.edit_redo())

        self.root.bind('<F5>', lambda _:self.runFile())
        self.root.bind('<F1>', lambda _:openweb('https://github.com/uralstech/peyx2/wiki', new=2))

        self.updateText()

def main():
    filepath = ''
    if len(argv) > 1: filepath = argv[1]
    
    PeYx2(filepath)

if __name__ == '__main__':
    main()