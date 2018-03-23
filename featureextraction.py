import sys
from utils.interface import file_classificiation, get_exe_files_in_folder, fetch_file_with_hash, FileRetrievalFailure
from utils.pefeatures import PEFeatureExtractor, NoPEFileException

for file_path in get_exe_files_in_folder("/home/manuel/Downloads"):
    try:
        'read file, generate hash'
        file = fetch_file_with_hash(file_path)

        'start analysing'
        fe = PEFeatureExtractor()
        feats = fe.extract(file['data'])
    except (NoPEFileException, FileRetrievalFailure):
        print('Error while processing file: {}; {}'.format(file_path, str(Exception)), file=sys.stderr)
        continue

    print("{};{};{}".format(file['md5'], file_classificiation.MALWARE, ';'.join(str(x) for x in feats)))
'''
    'dirty debug stuff'
    print("file name = {}, file md5 = {}, features size: {}, feature_format: {}\n".format(file_path, file['md5'], feats.size, type(feats[0])))

    section_start = 0
    section_end = 0
    for feature in fe.raw_features + fe.parsed_features:
        section_end = section_end + feature.dim
        print("{}: Section Start: {}, Section End: {}".format(feature.__repr__(), section_start, section_end))
        print("{}".format(feats.tolist()[section_start:section_end]))
        section_start = section_end
'''

