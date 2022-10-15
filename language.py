from tkinter import Toplevel
from dialogs import ListDialog
from tkinter.messagebox import showerror
from classes import LangData, LangSyntax
from os.path import abspath, dirname, isfile, join, splitext
from re import compile
from os import scandir
from json import load

class LangConfigHelper:
    __here = abspath(dirname(__file__))

    def GetLangConfig(self, filepath):
        lang_config = abspath(join(LangConfigHelper.__here, f'configs/{splitext(filepath)[1]}.json'))
        if not isfile(lang_config): return None

        data = LangData([], '')

        try:
            with open(lang_config, 'r') as f:
                jsondata = load(f)

                data.command = jsondata['command'].replace('___FILE___', abspath(filepath)).replace('___FOLDER___', abspath(dirname(filepath)))
                for i in jsondata['syntaxes']: data.syntaxes.append(LangSyntax(i['name'], compile(i['regex']), i['color']))
        except Exception as error:
            showerror('PeYx2 langConfig Retriever', f'An unexpected error occured!\n\n{str(error)}')
            return None
            
        return data

    def ShowLangConfigs(self, master):
        root = Toplevel(master)
        root.withdraw()

        filepath = abspath(join(LangConfigHelper.__here, f'configs'))
        files = []

        try:
            for file in scandir(filepath):
                if file.is_file() and splitext(file.name)[1] == '.json': files.append(file.name)
        except Exception as error:
            showerror('PeYx2 langConfigs', f'An unexpected error occured!\n\n{str(error)}')
            return None

        ListDialog(root, 'PeYx2 langConfigs', files)