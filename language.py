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

    def __CreateLangConfig(self, data):
        syntaxes = []
        tags = []

        for i in data:
            sub_syntaxes = None
            sub_tags = []

            tags.append(i['name'])
            if 'sub-syntaxes' in i.keys(): sub_syntaxes, sub_tags = self.__CreateLangConfig(i['sub-syntaxes'])

            syntaxes.append(LangSyntax(i['name'], compile(i['regex']), i['color'], sub_syntaxes))
            tags.extend(sub_tags)
        return syntaxes, tags

    def GetLangConfig(self, filepath):
        lang_config = abspath(join(LangConfigHelper.__here, f'configs/{splitext(filepath)[1]}.json'))
        if not isfile(lang_config): return None

        data = LangData([], [], '')

        try:
            with open(lang_config, 'r') as f:
                jsondata = load(f)

                data.command = jsondata['command'].replace('___FILE___', abspath(filepath)).replace('___FOLDER___', abspath(dirname(filepath)))
                data.syntaxes, data.syntax_tags = self.__CreateLangConfig(jsondata['syntaxes'])
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
                if file.is_file() and splitext(file.name)[1] == '.json': files.append(f'{file.name}{" "*(60-len(file.name))}{splitext(file.name)[0]} files')
        except Exception as error:
            showerror('PeYx2 langConfigs', f'An unexpected error occured!\n\n{str(error)}')
            return None

        ListDialog(root, 'PeYx2 langConfigs', files)