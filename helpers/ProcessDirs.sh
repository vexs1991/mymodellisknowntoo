#!/bin/bash
#set -x

FOLDER_PATH="/media/dataspacedisk/ikarus"
LOG_FOLDER_PATH="/media/dataspacedisk/statcsv"
#FOLDER_PATH="/media/dataspacedisk/ikarus"
#LOG_FOLDER_PATH="/media/dataspacedisk/statcsv"
LOG_FILE=$LOG_FOLDER_PATH/stat_extr_$(date +%Y%m%d-%H%M%S).log

mkdir -p $LOG_FOLDER_PATH
echo "[$(date +%Y%m%d-%H%M%S)] Start analysing $FOLDER_PATH, outputting infos to $LOG_FOLDER_PATH" >> $LOG_FILE 2>&1

run_stan() {
  DIRNAME=$1
  DIRTYPE=$2
  COMPL_FOLDER_PATH=$LOG_FOLDER_PATH/$DIRNAME
  for folder in $FOLDER_PATH/$DIRNAME/*; do
     type="${folder##*/}"
     logfile_path="$COMPL_FOLDER_PATH/${type}.csv"
     err_logfile_path="$COMPL_FOLDER_PATH/${type}.err"
     mkdir -p $COMPL_FOLDER_PATH
     echo "[$(date +%Y%m%d-%H%M%S)] starting CLEAN ${type}; CSV: ${logfile_path}; Error-Log: ${err_logfile_path}" >> $LOG_FILE 2>&1
     python3 ../mymodellisknowtoo_cmd.py -c -o "$logfile_path" $DIRTYPE "$folder" >> $LOG_FILE 2> ${err_logfile_path}
     echo "[$(date +%Y%m%d-%H%M%S)] finishing CLEAN ${type}" >> $LOG_FILE 2>&1
  done
}

#run_stan cln BENIGN
echo "[$(date +%Y%m%d-%H%M%S)] Done analysing $FOLDER_PATH, outputting infos to $LOG_FOLDER_PATH" >> $LOG_FILE 2>&1
