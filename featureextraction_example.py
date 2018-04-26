from utils.interface import file_extraction, binary, file_handler, file_action

fe = file_extraction(folder_engine=file_handler.get_exe_files_in_folder)
fam = file_action(file_classification=binary.type.MALWARE)
fab = file_action(file_classification=binary.type.BENIGN)
fe.extract_folder_threaded("/media/dataspacedisk/XX/clean", fab.print_csv, 6)
fe.extract_folder_threaded("/media/dataspacedisk/XX/infected", fam.print_csv, 6)
