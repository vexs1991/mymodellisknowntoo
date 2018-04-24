from utils.interface import file_extraction, binary, file_handler, file_action

fe = file_extraction(folder_engine=file_handler.get_exe_files_in_folder)
fam = file_action(file_classification=binary.type.MALWARE)
fab = file_action(file_classification=binary.type.BENIGN)
fe.extract_folder_threaded("/media/dataspacedisk/ikarus_upload/clean", fab.print_csv, 6)
fe.extract_folder_threaded("/media/dataspacedisk/ikarus_upload/infected", fam.print_csv, 6)
#fe.extract_folder_threaded("/mnt/ikarus/clean", fab.print_csv, 12)
#fe.extract_folder_threaded("/mnt/ikarus/infected", fam.print_csv, 12)
#fe.extract_folder("/home/manuel/Downloads", fa.print_csv)
