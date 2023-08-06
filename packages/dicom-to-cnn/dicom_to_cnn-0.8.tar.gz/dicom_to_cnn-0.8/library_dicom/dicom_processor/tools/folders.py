import os
import json

def get_series_path(path):
    """Go through all the folder to find every series path

    Arguments:
        path {[string]} -- [Absolute path where the repertory is located]

    Returns:
        [list] -- [Path's list of every series]
    """

    seriesPath = []
    for (path, dirs, files) in os.walk(path): 
        if not (dirs) :
            seriesPath.append(path)
    return seriesPath

"""
ATTENTION A TOUT EFFACE
def remove_empty_folders(path):

    empty_folder = []
    for (path, dirs, files) in os.walk(path): 
        if (len(files) ==0) :
            empty_folder.append(path)
    return empty_folder
"""

def write_json_file(path, file_name, content, extension = 'json'):
    wrinting_file = open(os.path.join(path, file_name+'.'+extension), 'w')
    wrinting_file.write(json.dumps(content))
    wrinting_file.close()

def remove_bi_file(path):
    file_names = os.listdir(path)
    if('graphic.brownFat.gr2' in file_names):
        os.remove( os.path.join(path,"graphic.brownFat.gr2") )

def remove_index_ini(path):
    file_names = os.listdir(path)
    if ('index.ini' in file_names):
        os.remove(os.path.join(path, 'index.ini'))
