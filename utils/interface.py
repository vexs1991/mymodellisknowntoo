import os

class FileRetrievalFailure(Exception):
    pass

def fetch_file(file_path):
    try:
        with open(file_path, 'rb') as infile:
            bytez = infile.read()
    except IOError:
        raise FileRetrievalFailure(
            "Unable to read file from {}".format(file_path))
    return bytez