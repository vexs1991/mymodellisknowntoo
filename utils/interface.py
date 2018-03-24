import os
import sys
import hashlib
import magic
from numpy import ndarray
from utils.pefeatures import PEFeatureExtractor, NoPEFileException
from queue import Queue
from threading import Thread

class file_handler():
    class FileRetrievalFailure(Exception):
        pass

    @staticmethod
    def load_file(file_path):
        try:
            with open(file_path, 'rb') as infile:
                data = infile.read()
        except IOError:
            raise file_handler.FileRetrievalFailure(
                "Unable to read file from {}".format(file_path))
        return data

    @staticmethod
    def get_files_in_folder(folder_path):
        files = []
        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path):
                files.append(full_path)

        return files

    @staticmethod
    def get_exe_files_in_folder(folder_path):
        return [f for f in file_handler.get_files_in_folder(folder_path) if file_handler.file_is_exe(f)]

    @staticmethod
    def file_is_exe(file_path):
        if(magic.from_file(file_path, mime=True) == "application/x-dosexec"):
            return True
        return False

'''binary object'''
class binary():
    class type(enumerate):
        BENIGN = 0
        MALWARE = 1
        UKNOWN = 2

    def __init__(self, classificiation=type.UKNOWN):
        self.features = ndarray
        self.md5sum = ''
        self.file_path = ''
        self.data = bytes
        self.classification = classificiation

    def process(self, file_path):
        try:
            self.file_path = file_path
            self.data = file_handler.load_file(self.file_path)
            self.get_md5()
            self.do_static_analysis()
        except(Exception):
            raise
        return self

    def get_md5(self):
        md5 = hashlib.md5()
        md5.update(self.data)
        self.md5sum = md5.hexdigest()

    def do_static_analysis(self):
        try:
            fe = PEFeatureExtractor()
            self.features = fe.extract(self.data)
        except (Exception):
            raise

'''file_extraction works with binary objects'''
class file_extraction():
    def __init__(self, folder_engine=file_handler.get_files_in_folder, file_handle_error=sys.stderr):
        '''folder_engine
        get_exe_files_in_folder* preselects windows executables by guessing the file type (performance hit)
        get_files_in_folder* selects every file in this folder for further processing, eventually pefeature will handle errors
        '''
        self.folder_engine = folder_engine
        self.file_handle_error = file_handle_error

    '''use for single file extraction, takes output_action as argument'''
    def extract_single_file(self, file_path, out):
        try:
            processed_binary = binary()
            out(processed_binary.process(file_path))
        except (NoPEFileException, file_handler.FileRetrievalFailure):
            print('Error while processing file: {}; {}'.format(file_path, str(Exception)), file=self.file_handle_error)

    '''worker thread for file extraction'''
    def extract_single_file_worker(self, file_queue, out):
        while not file_queue.empty():
            element = file_queue.get()
            self.extract_single_file(element, out)
            file_queue.task_done()
        exit(0)

    '''use for folder file extraction, takes output_action as argument'''
    def extract_folder(self, folder_path, out):
        'use get_files_in_folder if your pe-files files are sorted already'
        for file_path in self.folder_engine(folder_path):
            self.extract_single_file(file_path, out)

    '''use for threaded folder file extraction, takes output_action, and thread count as argument'''
    def extract_folder_threaded(self, folder_path, out, threads):
        q = Queue(maxsize = 0)

        for file_path in self.folder_engine(folder_path):
            q.put(file_path)

        for i in range(threads):
            worker = Thread(target=self.extract_single_file_worker, args=(q, out,))
            worker.setDaemon(True)
            worker.start()

        q.join()

'''Various action functions that take a binary object as parameter'''
class file_action():
    def __init__(self, file_classification=binary.type.UKNOWN, file_handle_info=sys.stdout, file_handle_error=sys.stdout):
        self.file_classificiation = file_classification
        self.file_handle_info = file_handle_info
        self.file_handle_error = file_handle_error

    '''Outputs debug binary information to file_handle_info (default: stdout)'''
    def print_debug(self, processed_binary):
        print("file name = {}, file md5 = {}, features size: {}, feature_format: {}\n".format(processed_binary.file_path, processed_binary.md5sum, processed_binary.features.size, type(processed_binary.features[0])), file=self.file_handle_info)

        fe = PEFeatureExtractor()

        section_start = 0
        section_end = 0
        for feature in fe.raw_features + fe.parsed_features:
            section_end = section_end + feature.dim
            print("{}: Section Start: {}, Section End: {}".format(feature.__repr__(), section_start, section_end), file=self.file_handle_info)
            print("{}".format(processed_binary.features.tolist()[section_start:section_end]), file=self.file_handle_info)
            section_start = section_end

    '''Outputs binary information in format specified by project group to file_handle_info (default: stdout)'''
    def print_csv(self, processed_binary):
        print("{};{};{}".format(processed_binary.md5sum, self.file_classificiation,
                                ';'.join(str(x) for x in processed_binary.features)), file=self.file_handle_info)

