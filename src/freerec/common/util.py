import os

def mod_fname(basename, fformat):
    if (basename + fformat) in os.listdir():
        basename += "n"
        return mod_fname(basename, fformat)
    return basename + fformat 


