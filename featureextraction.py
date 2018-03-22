from utils import pefeatures, interface

file_name = "/bin/bash"

fe = pefeatures.PEFeatureExtractor()
feats = fe.extract(interface.fetch_file(file_name))
feats_list = feats.tolist()

print("file name = {}, features size: {}, feature_format: {}\n".format(file_name, feats.size, type(feats[0])))
#print(type(fe.raw_features))

section_start = 0
section_end = 0
for feature in fe.raw_features + fe.parsed_features:
    section_size = feature.dim
    section_name = feature.name
    section_end = section_end + section_size

    print("Name: {}, Size: {}, Section Start: {}, Section End: {}".format(section_name, section_size, section_start, section_end))
    print("{}".format(feats_list[section_start:section_end]))
    section_start = section_end


#print("Section 1.: raw_features ByteHistogram()\n{}".format(feats_list[0:section_size]))
#print("Section 2.: raw_features ByteEntropyHistogram()\n{}".format(feats_list[section_size:(section_size = section_size + 256)]))
