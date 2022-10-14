from tkinter import Toplevel
from classes import LangData
from dialogs import LangConfigDialog, ListDialog
from tkinter.messagebox import showerror, askyesno
from os.path import abspath, dirname, isfile, join, splitext
from os import scandir

class LangConfigHelper:
    __here = abspath(dirname(__file__))

    def GetLangConfig(self, filepath):
        lang_config = abspath(join(LangConfigHelper.__here, f'configs/{splitext(filepath)[1]}.langConfig'))
        if not isfile(lang_config): return None

        data = LangData([], [], [], '')

        try:
            with open(lang_config, 'r') as f:
                data.modules  = list(f.readline().rstrip('\n').split(','))
                data.keywords = list(f.readline().rstrip('\n').split(','))
                data.imports  = list(f.readline().rstrip('\n').split(','))
                data.command  = str(f.readline().rstrip('\n').replace('___FILE___', abspath(filepath)).replace('___FOLDER___', abspath(dirname(filepath))))
        except Exception as error:
            showerror('PeYx2 langConfig Retriever', f'An unexpected error occured!\n\n{str(error)}')
            return None

        return data

    def CreateLangConfig(self, master):
        root = Toplevel(master)
        root.withdraw()

        configInfo = LangConfigDialog(root, 'PeYx2 langConfig Creator')
        root.destroy()

        if not configInfo.hasSubmitted: return None

        extension = configInfo.extension
        modules = configInfo.modules
        keywords = configInfo.keywords
        imports = configInfo.imports
        command = configInfo.command

        filepath = abspath(join(LangConfigHelper.__here, f'configs/{extension}.langConfig'))

        try:
            if isfile(filepath):
                ans = askyesno('PeYx2 langConfig Creator', f'A langConfig file for \'{extension}\' files already exists.\nDo you want to overwrite the langConfig?')
                if ans == False: return

            with open(filepath, 'w') as f: f.write(',\n'.join((modules, keywords, imports, command)))
        except Exception as error:
            showerror('PeYx2 langConfig Creator', f'An unexpected error occured!\n\n{str(error)}')
            configInfo.destroy()

    def ShowLangConfigs(self, master):
        root = Toplevel(master)
        root.withdraw()

        filepath = abspath(join(LangConfigHelper.__here, f'configs'))
        files = []

        try:
            for file in scandir(filepath):
                if file.is_file() and splitext(file.name)[1] == '.langConfig': files.append(file.name)
        except Exception as error:
            showerror('PeYx2 langConfigs', f'An unexpected error occured!\n\n{str(error)}')
            return None

        ListDialog(root, 'PeYx2 langConfigs', files)