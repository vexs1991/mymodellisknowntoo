import os
import hashlib
import magic

class file_classificiation(enumerate):
    BENIGN = 0
    MALWARE = 1
    UKNOWN = 2

class FileRetrievalFailure(Exception):
    pass

def fetch_file_with_hash(file_path):
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as infile:
            data = infile.read()
            sha256.update(data)
            md5.update(data)
    except IOError:
        raise FileRetrievalFailure(
            "Unable to read file from {}".format(file_path))
    return {'data':data, 'sha256':sha256.hexdigest(), 'md5':md5.hexdigest()}

def get_files_in_folder(folder_path):
    files = []
    for f in os.listdir(folder_path):
        full_path = os.path.join(folder_path, f)
        if os.path.isfile(full_path):
            files.append(full_path)

    return files

def get_exe_files_in_folder(folder_path):
    return [f for f in get_files_in_folder(folder_path) if file_is_exe(f)]

def file_is_exe(file_path):
    if(magic.from_file(file_path, mime=True) == "application/x-dosexec"):
        return True
    return False