from utils import pefeatures, interface

file_name = "/home/manuel/Downloads/FoxitReader90_enu_Setup_Prom.exe"

fe = pefeatures.PEFeatureExtractor()
feats = fe.extract(interface.fetch_file(file_name))
feats_list = feats.tolist()

print("file name = {}, features size: {}, feature_format: {}\n".format(file_name, feats.size, type(feats[0])))

section_start = 0
section_end = 0
for feature in fe.raw_features + fe.parsed_features:
    section_end = section_end + feature.dim
    print("Name: {}, Size: {}, Section Start: {}, Section End: {}".format(feature.name, feature.dim, section_start, section_end))
    print("{}".format(feats_list[section_start:section_end]))
    section_start = section_end