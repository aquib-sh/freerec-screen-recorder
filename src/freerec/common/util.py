import os

def mod_fname(basename, fformat):
    """ If a file exists with same name then add 'n' 
        to the end of new file. """
    if (basename + fformat) in os.listdir():
        basename += "n"
        return mod_fname(basename, fformat)
    return basename + fformat 


