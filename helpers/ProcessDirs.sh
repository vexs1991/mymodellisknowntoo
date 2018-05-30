#!/bin/bash
#set -x

FOLDER_PATH="/media/dataspacedisk/ikarus"
LOG_FOLDER_PATH="/media/dataspacedisk/statcsv"
LOG_FILE=$LOG_FOLDER_PATH/stat_extr_$(date +%Y%m%d-%H%M%S).log

mkdir -p $LOG_FOLDER_PATH
echo "[$(date +%Y%m%d-%H%M%S)] Start analysing $FOLDER_PATH, outputting infos to $LOG_FOLDER_PATH" >> $LOG_FILE 2>&1
for folder in $FOLDER_PATH/inf/*; do
   type="${folder##*/}"
   logfile_path="$LOG_FOLDER_PATH/inf/${type}.csv"
   err_logfile_path="$LOG_FOLDER_PATH/inf/${type}.err"
   mkdir -p $LOG_FOLDER_PATH/inf
   echo "[$(date +%Y%m%d-%H%M%S)] starting INFECTED ${folder##*/}; CSV: ${logfile_path}; Error-Log: ${err_logfile_path}" >> $LOG_FILE 2>&1
   python3 ../mymodellisknowtoo_cmd.py -c -o "$logfile_path" MALWARE "$folder" >> $LOG_FILE 2> ${err_logfile_path}
   echo "[$(date +%Y%m%d-%H%M%S)] finishing INFECTED ${folder##*/}" >> $LOG_FILE 2>&1
done

for folder in $FOLDER_PATH/cln/*; do
   type="${folder##*/}"
   logfile_path="$LOG_FOLDER_PATH/cln/${type}.csv"
   err_logfile_path="$LOG_FOLDER_PATH/cln/${type}.err"
   mkdir -p $LOG_FOLDER_PATH/cln
   echo "[$(date +%Y%m%d-%H%M%S)] starting CLEAN ${folder##*/}; CSV: ${logfile_path}; Error-Log: ${err_logfile_path}" >> $LOG_FILE 2>&1
   python3 ../mymodellisknowtoo_cmd.py -c -o "$logfile_path" BENIGN "$folder" >> $LOG_FILE 2> ${err_logfile_path}
   echo "[$(date +%Y%m%d-%H%M%S)] finishing CLEAN ${folder##*/}" >> $LOG_FILE 2>&1
done
echo "[$(date +%Y%m%d-%H%M%S)] Done analysing $FOLDER_PATH, outputting infos to $LOG_FOLDER_PATH" >> $LOG_FILE 2>&1
