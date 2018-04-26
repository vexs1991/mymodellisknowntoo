from utils.interface import file_extraction, binary, file_handler, file_action
import os
import sys
import argparse

# get list of implemented binary types
types = [item.name for item in binary.type]

parser = argparse.ArgumentParser()
parser.add_argument("type", help="type of binary to be found in folder {}".format(types))
parser.add_argument("folder", help="folder or file to scan")
parser.add_argument("-t", "--threats", type=int, help="number of threads to use")
parser.add_argument("-c", "--csv", action="store_true", help="outputs in csv format")
parser.add_argument("-o", "--output", help="csv output, if not defined we print to stdout")
args = parser.parse_args()

def exit_with_error(error):
   print("Error: {}".format(error))
   sys.exit(1)

# test if correct type was given
if not args.type in types:
   print("Incorrect type! {}".format(types))

fe = file_extraction(folder_engine=file_handler.get_files_in_folder)
fa = file_action(file_classification=binary.type[args.type])

if args.threats is None:
   threats = 4

if args.output is not None:
   # open and print to output log
   output_log = open(args.output, "w")
   fa.file_handle_info = output_log

print("Starting to analyze {}, classified as {}".format(args.folder, args.type))

# test if file or folder
if os.path.isdir(args.folder):
   # print as csv
   if args.csv:
      fe.extract_folder_threaded(args.folder, fa.print_csv, threats)
   # or some nice debug information
   else:
      fe.extract_folder_threaded(args.folder, fa.print_debug, threats)
   # print stats
   print("Files in folder: {}, Files processed: {}, Errors: {}".format(fe.file_count, fa.print_count, fe.file_count - fa.print_count))
elif os.path.isfile(args.folder):
   if args.csv:
      fe.extract_single_file(args.folder, fa.print_csv)
   else:
      fe.extract_single_file(args.folder, fa.print_debug)
else:
   exit_with_error("target is no file or folder")
