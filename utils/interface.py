import os
import hashlib

class FileRetrievalFailure(Exception):
    pass

def fetch_file_withsha256(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as infile:
            data = infile.read()
            sha256.update(data)
    except IOError:
        print(IOError.strerror)
        raise FileRetrievalFailure(
            "Unable to read file from {}".format(file_path))
    return {'data':data, 'sha256':sha256.hexdigest()}