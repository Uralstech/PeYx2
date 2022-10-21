from tkinter import Toplevel
from dialogs import ListDialog
from tkinter.messagebox import showerror
from classes import LangData, LangMetaData, LangSyntax
from os.path import abspath, dirname, isfile, join, splitext, basename
from re import compile
from os import scandir
from json import load

class LangConfigHelper:
    __here = abspath(dirname(__file__))

    def GetLangSyntaxes(self, data):
        syntaxes = []
        tags = []

        for i in data:
            sub_syntaxes = None
            sub_tags = []

            tags.append(i['name'])
            if 'sub-syntaxes' in i.keys(): sub_syntaxes, sub_tags = self.GetLangSyntaxes(i['sub-syntaxes'])

            syntaxes.append(LangSyntax(i['name'], compile(i['regex']), i['color'], sub_syntaxes))
            tags.extend(sub_tags)
        return syntaxes, tags

    def GetLangConfig(self, filepath):
        lang_config = abspath(join(LangConfigHelper.__here, f'configs/{splitext(filepath)[1]}.json'))
        if not isfile(lang_config): return None

        data = LangData('', [], [], '', None)

        try:
            with open(lang_config, 'r') as f:
                jsondata = load(f)

                data.filename = f'{splitext(filepath)[1]}.json'
                data.command = jsondata['command'].replace('___FILE___', abspath(filepath)).replace('___FOLDER___', abspath(dirname(filepath)))
                data.syntaxes, data.syntax_tags = self.GetLangSyntaxes(jsondata['syntaxes'])

                if 'metadata' in  jsondata.keys(): data.metadata = LangMetaData(jsondata['metadata']['version'], jsondata['metadata']['web-version'], jsondata['metadata']['download'], jsondata['metadata']['author'], jsondata['metadata']['language'])
        except Exception as error:
            showerror('PeYx2 langConfig Retriever', f'An unexpected error occured!\n\n{str(error)}')
            return None
            
        return data

    def GetAllLangConfigs(self):
        filepath = abspath(join(LangConfigHelper.__here, f'configs'))
        configs = []

        try:
            for file in scandir(filepath):
                if file.is_file() and splitext(file.name)[1] == '.json': configs.append(self.GetLangConfig(f'_{splitext(basename(file.name))[0]}'))
        except Exception as error:
            showerror('PeYx2 langConfig Retriever', f'An unexpected error occured!\n\n{str(error)}')
            return None
        return configs

    def ShowLangConfigs(self, master, langConfigs):
        root = Toplevel(master)
        root.withdraw()
        data = [f'FILE{" "*15}LANGUAGE{" "*10}AUTHOR{" "*30}VERSION']

        try:
            for langData_ in langConfigs:
                filename = langData_.filename
                language = langData_.metadata.language if langData_.metadata else "???"
                author   = langData_.metadata.author   if langData_.metadata else "???"
                version  = langData_.metadata.version  if langData_.metadata else "???"
                data.append(f'{filename}{" "*(19-len(filename))}{language}{" "*(18-len(language))}{author}{" "*(36-len(author))}{version}')
        except Exception as error:
            showerror('PeYx2 langConfigs', f'An unexpected error occured!\n\n{str(error)}')
            return None

        ListDialog(root, 'PeYx2 langConfigs', data)