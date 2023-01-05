import os
from fnmatch import fnmatch

root = os.getcwd()
pattern = "*.csv"

original_csv = []
for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            file_path = os.path.join(path, name)
            original_csv.append(file_path)
            # print(file_path)

dict_rename = {
    'Coppel Moda.csv':'_1_',
    'Coppel Seleccion.csv':'_2_',
    ''_3_'.csv':'_3_',
    'Wild & Fork 39s (1).csv':'_4_'
}

for name, newname in dict_rename.items():
    for filepath in original_csv:
        if name in filepath:
            # print(name, filepath,'\n')
            newpath = filepath.replace(name, newname)
            print(newpath)
            os.rename(filepath, newpath)
