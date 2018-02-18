import glob
from subprocess import call
import os

uiFolder = 'ui'
rcFolder = 'res'
uiFilesExtension = 'ui'
rcFilesExtension = 'qrc'
generationResultFolder = uiFolder + '/autogen_ui'


def get_files_list(path, file_extension):
    for filename in glob.iglob(path + '.' + file_extension, recursive=True):
        yield filename


'''
# disabled:
def get_qt_ui_files_list():
    files_list = os.listdir(uiFolder)
    qt_ui_files = list(filter(lambda f: f.split('.')[-1] == uiFilesExtension, files_list))
    return qt_ui_files
'''

print('Building resources...')
for file in get_files_list(rcFolder + '*/*', rcFilesExtension):
    print(file)
    call(['pyrcc5', file, '-o', (file.split('\\')[-1].split('.')[0] + '_rc.py')])

print('Building GUI...')
for file in get_files_list(uiFolder + '/**/*', uiFilesExtension):
    print(file)
    call(['pyuic5', file, '-o', generationResultFolder + '/' + ('Ui_' + (file.split('\\')[-1].split('.')[0] + '.py'))])

# Start the application
import main