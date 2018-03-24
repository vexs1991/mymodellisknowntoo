import sys
from utils.interface import file_classificiation, get_exe_files_in_folder, fetch_file_with_hash, FileRetrievalFailure
from utils.pefeatures import PEFeatureExtractor, NoPEFileException
from queue import Queue
from threading import Thread

file_handle_error = sys.stderr

def extract(file_path):
    try:
        'read file, generate hash'
        file = fetch_file_with_hash(file_path)

        'start analysing'
        fe = PEFeatureExtractor()
        feats = fe.extract(file['data'])
    except (Exception):
        raise

    return {'features':feats, 'md5sum':file['md5'], 'file_path':file_path}

def extract_single_file_worker(file_queue, out):
    while not file_queue.empty():
        element = file_queue.get()
        try:
            out(extract(element))
        except (NoPEFileException, FileRetrievalFailure):
            print('Error while processing file: {}; {}'.format(element, str(Exception)), file=file_handle_error)
        file_queue.task_done()
    exit(0)

def extract_single_file(file_path, out):
    out(extract(file_path))

def extract_folder(folder_path, out):
    'use get_files_in_folder if your pe-files files are sorted already'
    for file_path in get_exe_files_in_folder(folder_path):
        try:
            out(extract(file_path))
        except (NoPEFileException, FileRetrievalFailure):
            print('Error while processing file: {}; {}'.format(file_path, str(Exception)), file=file_handle_error)
            continue

def extract_folder_threaded(folder_path, out, threads):
    q = Queue(maxsize = 0)

    for file_path in get_exe_files_in_folder(folder_path):
        q.put(file_path)

    for i in range(threads):
        worker = Thread(target=extract_single_file_worker, args=(q, out,))
        worker.setDaemon(True)
        worker.start()

    q.join()

def print_debug(file_info):
    'dirty debug stuff'
    print("file name = {}, file md5 = {}, features size: {}, feature_format: {}\n".format(file_info['file_path'], file_info['md5sum'], file_info['features'].size, type(file_info['features'][0])))

    fe = PEFeatureExtractor()

    section_start = 0
    section_end = 0
    for feature in fe.raw_features + fe.parsed_features:
        section_end = section_end + feature.dim
        print("{}: Section Start: {}, Section End: {}".format(feature.__repr__(), section_start, section_end))
        print("{}".format(file_info['features'].tolist()[section_start:section_end]))
        section_start = section_end

def print_csv(file_info):
    print("{};{};{}".format(file_info['md5sum'], file_classificiation.MALWARE,
                            ';'.join(str(x) for x in file_info['features'])))

#extract_folder("/home/manuel/Downloads", print_debug)
extract_folder_threaded("/home/manuel/Downloads", print_debug, 6)