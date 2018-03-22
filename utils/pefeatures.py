# -*- coding: utf-8 -*-
''' Extracts some basic features from PE files. Many of the features
implemented have been used in previously published works. For more information,
check out the following resources:
* Schultz, et al., 2001: http://128.59.14.66/sites/default/files/binaryeval-ieeesp01.pdf
* Kolter and Maloof, 2006: http://www.jmlr.org/papers/volume7/kolter06a/kolter06a.pdf
* Shafiq et al., 2009: https://www.researchgate.net/profile/Fauzan_Mirza/publication/242084613_A_Framework_for_Efficient_Mining_of_Structural_Information_to_Detect_Zero-Day_Malicious_Portable_Executables/links/0c96052e191668c3d5000000.pdf
* Raman, 2012: http://2012.infosecsouthwest.com/files/speaker_materials/ISSW2012_Selecting_Features_to_Classify_Malware.pdf
* Saxe and Berlin, 2015: https://arxiv.org/pdf/1508.03096.pdf

It may be useful to do feature selection to reduce this set of features to a meaningful set
for your modeling problem.
'''
import lief  # pip install https://github.com/lief-project/LIEF/releases/download/0.7.0/linux_lief-0.7.0_py3.6.tar.gz
# see https://github.com/lief-project/LIEF/releases

import numpy as np
# FeatureHasher(n_features=10).transform( [ {k:v}, {k:v}])
from sklearn.feature_extraction import FeatureHasher

import re


class FeatureType(object):
    '''Base class from which each feature type may inherit'''

    def __init__(self):
        super().__init__()
        self.dim = 0
        self.dtype = np.float32
        self.name = ''

    def __call__(self, arg):
        raise(NotImplemented)

    def empty(self):
        return np.zeros((self.dim,), dtype=self.dtype)

    def __repr__(self):
        return '{}({})'.format(self.name, self.dim)


class ByteHistogram(FeatureType):
    ''' Byte histogram (normalized to sum to unity) over the entire binary file.'''

    def __init__(self):
        super().__init__()
        self.dim = 1 + 256
        self.name = 'ByteHistogram'

    def __call__(self, bytez):
        h = np.bincount(np.frombuffer(bytez, dtype=np.uint8), minlength=256)
        return np.concatenate([
            [h.sum()],  # total size of the byte stream
            h.astype(self.dtype).flatten() / h.sum(),  # normalized the histogram
        ])


class ByteEntropyHistogram(FeatureType):
    ''' 2d byte/entropy histogram based roughly on (Saxe and Berlin, 2015).
    This roughly approximates the joint probability of byte value and local entropy.
    See Section 2.1.1 in https://arxiv.org/pdf/1508.03096.pdf for more info.
    '''

    def __init__(self, step=1024, window=2048):
        super().__init__()
        self.dim = 256
        self.name = 'ByteEntropyHistogram'
        self.window = window
        self.step = step

    def _entropy_bin_counts(self, block):
        # coarse histogram, 16 bytes per bin
        c = np.bincount(block >> 4, minlength=16) # 16-bin histogram
        p = c.astype(np.float32) / self.window
        wh = np.where(c)[0]
        H = np.sum(-p[wh] * np.log2(p[wh]))*2 # * x2 b.c. we reduced information by half: 256 bins (8 bits) to 16 bins (4 bits)

        Hbin = int(H * 2)  # up to 16 bins (max entropy is 8 bits)
        if Hbin == 16:  # handle entropy = 8.0 bits
            Hbin = 15

        return Hbin, c

    def __call__(self, bytez):
        output = np.zeros((16, 16), dtype=np.int)
        a = np.frombuffer(bytez, dtype=np.uint8)
        if a.shape[0] < self.window:
            Hbin, c = self._entropy_bin_counts(a)
            output[Hbin, :] += c
        else:
            # strided trick from here: http://www.rigtorp.se/2011/01/01/rolling-statistics-numpy.html
            shape = a.shape[:-1] + (a.shape[-1] - self.window + 1, self.window)
            strides = a.strides + (a.strides[-1],)
            blocks = np.lib.stride_tricks.as_strided(
                a, shape=shape, strides=strides)[::self.step, :]

            # from the blocks, compute histogram
            for block in blocks:
                Hbin, c = self._entropy_bin_counts(block)
                output[Hbin, :] += c

        return output.flatten().astype(self.dtype)


class SectionInfo(FeatureType):
    '''Information about section names, sizes and entropy.  Uses hashing trick
    to summarize all this section info into a feature vector.
    '''

    def __init__(self):
        super().__init__()
        # sum of the vector sizes comprising this feature
        self.dim = 5 + 50 + 50 + 50 + 50 + 50
        self.name = 'SectionInfo'

    def __call__(self, binary):
        # general statistics about sections
        general = [len(binary.sections),                         # total number of sections
                   # number of sections with nonzero size
                   sum(1 for s in binary.sections if s.size == 0),
                   # number of sections with an empty name
                   sum(1 for s in binary.sections if s.name == ""),
                   sum(1 for s in binary.sections if s.has_characteristic(lief.PE.SECTION_CHARACTERISTICS.MEM_READ)
                       and s.has_characteristic(lief.PE.SECTION_CHARACTERISTICS.MEM_EXECUTE)),  # number of RX
                   sum(1 for s in binary.sections if s.has_characteristic(
                       lief.PE.SECTION_CHARACTERISTICS.MEM_WRITE)),  # number of W
                   ]

        # gross characteristics of each section
        section_sizes = [(s.name, len(s.content)) for s in binary.sections]
        section_entropy = [(s.name, s.entropy) for s in binary.sections]
        section_vsize = [(s.name, s.virtual_size) for s in binary.sections]

        # properties of entry point, or if invalid, the first executable section
        try:
            entry = binary.section_from_offset(binary.entrypoint)
        except lief.not_found:
            # bad entry point, let's find the first executable section
            entry = None
            for s in binary.sections:
                if lief.PE.SECTION_CHARACTERISTICS.MEM_EXECUTE in s.characteristics_lists:
                    entry = s
                    break
        if entry is not None:
            entry_name = [entry.name]
            entry_characteristics = [str(c)
                                     for c in entry.characteristics_lists]
            # ['SECTION_CHARACTERISTICS.CNT_CODE', 'SECTION_CHARACTERISTICS.MEM_EXECUTE','SECTION_CHARACTERISTICS.MEM_READ']
        else:
            entry_name = []
            entry_characteristics = []

        # let's dump all this info into a single vector
        return np.concatenate([
            np.atleast_2d(np.asarray(general, dtype=self.dtype)),
            FeatureHasher(50, input_type="pair", dtype=self.dtype).transform(
                [section_sizes]).toarray(),
            FeatureHasher(50, input_type="pair", dtype=self.dtype).transform(
                [section_entropy]).toarray(),
            FeatureHasher(50, input_type="pair", dtype=self.dtype).transform(
                [section_vsize]).toarray(),
            FeatureHasher(50, input_type="string", dtype=self.dtype).transform(
                [entry_name]).toarray(),
            FeatureHasher(50, input_type="string", dtype=self.dtype).transform([entry_characteristics]).toarray()
            ], axis=-1).flatten().astype(self.dtype)


class ImportsInfo(FeatureType):
    '''Information about imported libraries and functions from the
    import address table.  Note that the total number of imported
    functions is contained in GeneralFileInfo.
    '''

    def __init__(self):
        super().__init__()
        self.dim = 256 + 1024
        self.name = 'ImportsInfo'

    def __call__(self, binary):
        libraries = [l.lower() for l in binary.libraries]
        # we'll create a string like "kernel32.dll:CreateFileMappingA" for each entry
        imports = [lib.name.lower() + ':' +
                   e.name for lib in binary.imports for e in lib.entries]

        # two separate elements: libraries (alone) and fully-qualified names of imported functions
        return np.concatenate([
            FeatureHasher(256, input_type="string", dtype=self.dtype).transform(
                [libraries]).toarray(),
            FeatureHasher(1024, input_type="string", dtype=self.dtype).transform(
                [imports]).toarray()
        ], axis=-1).flatten().astype(self.dtype)


class ExportsInfo(FeatureType):
    '''Information about exported functions. Note that the total number of exported
    functions is contained in GeneralFileInfo.
    '''

    def __init__(self):
        super().__init__()
        self.dim = 128
        self.name = 'ExportsInfo'

    def __call__(self, binary):
        return FeatureHasher(128, input_type="string", dtype=self.dtype).transform([binary.exported_functions]).toarray().flatten().astype(self.dtype)


class GeneralFileInfo(FeatureType):
    '''General information about the file.'''

    def __init__(self):
        super().__init__()
        self.dim = 9
        self.name = 'GeneralFileInfo'

    def __call__(self, binary):
        return np.asarray([
            binary.virtual_size,
            binary.has_debug,
            len(binary.exported_functions),
            len(binary.imported_functions),
            binary.has_relocations,
            binary.has_resources,
            binary.has_signature,
            binary.has_tls,
            len(binary.symbols),
        ]).flatten().astype(self.dtype)


class HeaderFileInfo(FeatureType):
    '''Machine, architecure, OS, linker and other information extracted from header.'''

    def __init__(self):
        super().__init__()
        self.dim = 62
        self.name = 'HeaderFileInfo'

    def __call__(self, binary):

        return np.concatenate([
            [[binary.header.time_date_stamps]],
            FeatureHasher(10, input_type="string", dtype=self.dtype).transform(
                [[str(binary.header.machine)]]).toarray(),
            FeatureHasher(10, input_type="string", dtype=self.dtype).transform(
                [[str(c) for c in binary.header.characteristics_list]]).toarray(),
            FeatureHasher(10, input_type="string", dtype=self.dtype).transform(
                [[str(binary.optional_header.subsystem)]]).toarray(),
            FeatureHasher(10, input_type="string", dtype=self.dtype).transform(
                [[str(c) for c in binary.optional_header.dll_characteristics_lists]]).toarray(),
            FeatureHasher(10, input_type="string", dtype=self.dtype).transform(
                [[str(binary.optional_header.magic)]]).toarray(),
            [[binary.optional_header.major_image_version]],
            [[binary.optional_header.minor_image_version]],
            [[binary.optional_header.major_linker_version]],
            [[binary.optional_header.minor_linker_version]],
            [[binary.optional_header.major_operating_system_version]],
            [[binary.optional_header.minor_operating_system_version]],
            [[binary.optional_header.major_subsystem_version]],
            [[binary.optional_header.minor_subsystem_version]],
            [[binary.optional_header.sizeof_code]],
            [[binary.optional_header.sizeof_headers]],
            [[binary.optional_header.sizeof_heap_commit]],
        ], axis=-1).flatten().astype(self.dtype)


class StringExtractor(FeatureType):
    ''' Extracts strings from raw byte stream '''

    def __init__(self):
        super().__init__()
        self.dim = 1 + 1 + 1 + 96 + 1 + 1 + 1 + 1
        self.name = 'StringExtractor'
        # all consecutive runs of 0x20 - 0x7f that are 5+ characters
        self._allstrings = re.compile(b'[\x20-\x7f]{5,}')
        # occurances of the string 'C:\'.  Not actually extracting the path
        self._paths = re.compile(b'c:\\\\', re.IGNORECASE)
        # occurances of http:// or https://.  Not actually extracting the URLs
        self._urls = re.compile(b'https?://', re.IGNORECASE)
        # occurances of the string prefix HKEY_.  No actually extracting registry names
        self._registry = re.compile(b'HKEY_')
        # crude evidence of an MZ header (dropper?) somewhere in the byte stream
        self._mz = re.compile(b'MZ')

    def __call__(self, bytez):
        allstrings = self._allstrings.findall(bytez)
        if allstrings:
            # statistics about strings:
            string_lengths = [len(s) for s in allstrings]
            avlength = sum(string_lengths) / len(string_lengths)
            # map printable characters 0x20 - 0x7f to an int array consisting of 0-95, inclusive
            as_shifted_string = [b - ord(b'\x20')
                                 for b in b''.join(allstrings)]
            c = np.bincount(as_shifted_string, minlength=96)  # histogram count
            # distribution of characters in printable strings
            p = c.astype(np.float32) / c.sum()
            wh = np.where(c)[0]
            H = np.sum(-p[wh] * np.log2(p[wh]))  # entropy
        else:
            avlength = 0
            p = np.zeros((96,), dtype=np.float32)
            H = 0

        return np.concatenate([
            [[len(allstrings)]],
            [[avlength]],
            [p.tolist()],
            [[H]],
            [[len(self._paths.findall(bytez))]],
            [[len(self._urls.findall(bytez))]],
            [[len(self._registry.findall(bytez))]],
            [[len(self._mz.findall(bytez))]]
        ], axis=-1).flatten().astype(self.dtype)


class PEFeatureExtractor(object):
    ''' Extract useful features from a PE file, and return as a vector
        of fixed size.
    '''

    def __init__(self):
        # features come in 2 types: those that are extracted from the raw byte stream, and those that require parsing of the PE file
        self.raw_features = [
            ByteHistogram(),
            ByteEntropyHistogram(),
            StringExtractor()
        ]

        self.parsed_features = [
            GeneralFileInfo(),
            HeaderFileInfo(),
            SectionInfo(),
            ImportsInfo(),
            ExportsInfo()
        ]
        self.dim = sum(o.dim for o in self.raw_features) + \
            sum(o.dim for o in self.parsed_features)

    def extract(self, bytez):
        # feature vectors that require only raw bytez
        featurevectors = [fe(bytez) for fe in self.raw_features]

        # feature vectors that require a parsed file
        try:
            binary = lief.parse(list(bytez))
        except (lief.bad_format, lief.bad_file, lief.pe_error, lief.parser_error,RuntimeError):
            # some kind of parsing problem, none of these feature extractors will work
            print("error while parsing with lief")
            binary = None
            featurevectors.extend([fe.empty() for fe in self.parsed_features])
        # except: # everything else (KeyboardInterrupt, SystemExit, ValueError):
        #     raise

        if binary is not None:
            for fe in self.parsed_features:
                try:
                    featurevectors.append(fe(binary))
                except(KeyboardInterrupt, SystemExit):
                    raise
                except:
                    # some property was invalid or missing
                    featurevectors.append(fe.empty())

        return np.concatenate(featurevectors)

    def test(self, bytez):
        for fe in self.raw_features:
            print(fe.name)
            v = fe(bytez)
            assert len(v) == fe.dim, 'length of {} different than expecting!'

        binary = lief.PE.parse(list(bytez))
        for fe in self.parsed_features:
            print(fe.name)
            v = fe(binary)
            assert len(v) == fe.dim, 'length of {} different than expecting!'
