import os



def find(path, itemType='a'):
    """
    Return folders and/or files in a given path.

    Arguments:
        path (str)

    Keyword Arguments:
        itemType (str)
            'd': dir
            'f': file
            'a': dir & file [default]

    Returns:
        list
    """
    result = []
    if itemType == 'a':
        for itemName in os.listdir(path):
            itemPath = path + '/' + itemName
            result.append(itemPath)
    elif itemType == 'd':
        for itemName in os.listdir(path):
            itemPath = path + '/' + itemName
            if os.path.isdir(itemPath):
                result.append(itemPath)
    elif itemType == 'f':
        for itemName in os.listdir(path):
            itemPath = path + '/' + itemName
            if os.path.isfile(itemPath):
                result.append(itemPath)
    return result


def findall(path, fileExts=[]):
    """
    Return all files in a given path recursively.

    Arguments:
        path (str)

    Keyword Arguments:
        fileExts (list)
            e.g.:
                ['exe', 'jpg']
                ['ini']
            []: matches all files [default]

    Returns:
        list
    """
    result = []
    if fileExts == []:
        for root, _, files in os.walk(path):
            for i in files:
                result.append(root.replace('\\','/') + '/' + i)
    else:
        for root, _, files in os.walk(path):
            for i in files:
                if os.path.splitext(i.lower())[-1][1:] in fileExts:
                    result.append(root.replace('\\','/') + '/' + i)
    return result
