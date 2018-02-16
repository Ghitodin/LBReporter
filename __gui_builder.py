from subprocess import call
import os

uiFolder = 'ui'
uiFilesExtension = 'ui'
generationResultFolder = uiFolder + '/autogen_ui'


def get_qt_ui_files_list():
    files_list = os.listdir(uiFolder)
    qt_ui_files = list(filter(lambda f: f.split('.')[-1] == uiFilesExtension, files_list))
    return qt_ui_files


for file in get_qt_ui_files_list():
    call(["pyuic5", uiFolder + '/' + file, '-o', generationResultFolder + '/' + (file.split('.')[0] + '.py')])


import main