from tkinter import Toplevel
from classes import EditorData
from dialogs import EditorSettingsDialog
from tkinter.messagebox import showerror
from os.path import abspath, dirname, isfile, join
from os import remove

class EditorSettingsHelper:
    __here = abspath(dirname(__file__))

    def GetEditorSettings(self):
        data = EditorData('Consolas', 20, '#8aebff', '#1b1b1b', '#a80adc', '#00c161')

        filepath = abspath(join(EditorSettingsHelper.__here, 'PeYx2.PeYx2Config'))
        try:
            if isfile(filepath):
                with open(filepath, 'r') as f:
                    data.font = f.readline().rstrip('\n')
                    data.size = int(f.readline().rstrip('\n'))
                    data.fg = f.readline().rstrip('\n')
                    data.bg = f.readline().rstrip('\n')
                    data.h1 = f.readline().rstrip('\n')
                    data.h2 = f.readline().rstrip('\n')
        except Exception as error:
            showerror('PeYx2 Settings Retriever', f'An unexpected error occured!\n\n{str(error)}')
            return EditorData('Consolas', 20, '#8aebff', '#1b1b1b', '#a80adc', '#00c161')
        
        return data

    def CreateEditorSettings(self, master):
        root = Toplevel(master)
        root.withdraw()

        current = self.GetEditorSettings()
        settingsInfo = EditorSettingsDialog(root, 'PeYx2 Settings Editor', current.font, str(current.size), current.fg, current.bg, current.h1, current.h2)
        root.destroy()

        if not settingsInfo.hasSubmitted: return None
        filepath = abspath(join(EditorSettingsHelper.__here, 'PeYx2.PeYx2Config'))

        if settingsInfo.isdefault:
            try:
                if isfile(filepath): remove(filepath)
            except Exception as error:
                showerror('PeYx2 Settings Editor', f'An unexpected error occured!\n\n{str(error)}')

            return None

        try:
            with open(filepath, 'w') as f:
                f.write('\n'.join((settingsInfo.font, str(settingsInfo.size), settingsInfo.fg, settingsInfo.bg, settingsInfo.h1, settingsInfo.h2)))
        except Exception as error:
            showerror('PeYx2 Settings Editor', f'An unexpected error occured!\n\n{str(error)}')
            settingsInfo.destroy()