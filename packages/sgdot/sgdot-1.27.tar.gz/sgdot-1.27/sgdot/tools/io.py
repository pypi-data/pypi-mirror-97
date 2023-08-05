import os


def make_folder(folder):
    """
    If no folder of the given name already exists, create new one.

    Parameters
    ----------
    folder: str
        Name of the folder to be created.
    """

    if not os.path.exists(folder):
        parent_folders = folder.split('/')
        for i in range(1, len(parent_folders) + 1):
            path = ''
            for x in parent_folders[0:i]:
                path += x + '/'
            if not os.path.exists(path[0:-1]):
                os.mkdir(path[0:-1])
