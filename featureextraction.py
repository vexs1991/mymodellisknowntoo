from utils.interface import file_extraction, binary, file_handler, file_action

fe = file_extraction()
fe = file_extraction(folder_engine=file_handler.get_exe_files_in_folder)
fa = file_action(file_classification=binary.type.MALWARE)
fe.extract_folder_threaded("/home/manuel/Downloads", fa.print_csv, 6)
#fe.extract_folder("/home/manuel/Downloads", fa.print_csv)