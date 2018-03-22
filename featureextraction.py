from utils import pefeatures, interface
import hashlib

file_name = "/home/manuel/Downloads/FoxitReader90_enu_Setup_Prom.exe"

fe = pefeatures.PEFeatureExtractor()
file = interface.fetch_file_withsha256_chunked(file_name)
feats = fe.extract(file['data'])
feats_list = feats.tolist()

print("file name = {}, file sha256 = {}, features size: {}, feature_format: {}\n".format(file_name, file['sha256'], feats.size, type(feats[0])))

section_start = 0
section_end = 0
for feature in fe.raw_features + fe.parsed_features:
    section_end = section_end + feature.dim
    print("Name: {}, Size: {}, Section Start: {}, Section End: {}".format(feature.name, feature.dim, section_start, section_end))
    print("{}".format(feats_list[section_start:section_end]))
    section_start = section_end