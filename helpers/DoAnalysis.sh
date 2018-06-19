#!/bin/bash
#set -x

#KNN_SCRIPT=/home/localuser/Documents/manuel/kurt_old/project_ki/ann/prj_NN.py
#KNN_SCRIPT=/home/localuser/Documents/manuel/kurt/project_ki/ann/prj_NN.py
KNN_SCRIPT=/media/dataspacedisk/cengelma/project_ki/ann/prj_NN.py

FOLDER_PATH="/media/dataspacedisk/statcsv"
DATASETS=$FOLDER_PATH/combined
LOG_FOLDER_PATH=$DATASETS/results
LOG_FILE=$LOG_FOLDER_PATH/analysis_$(date +%Y%m%d-%H%M%S).log

mkdir -p $LOG_FOLDER_PATH
echo "[$(date +%Y%m%d-%H%M%S)] Start analysing $DATASETS, results will be available here $LOG_FOLDER_PATH" >> $LOG_FILE 2>&1

do_analysis() {
  for dataset in $(find $DATASETS -iname "TC_*.csv"); do
     type="${dataset##*/}"
     logfile_path="$LOG_FOLDER_PATH/${type}.txt"
     err_logfile_path="$LOG_FOLDER_PATH/${type}.err"
     echo "[$(date +%Y%m%d-%H%M%S)] starting ${type}; Resultsfile: ${logfile_path}; Error-Log: ${err_logfile_path}" >> $LOG_FILE 2>&1
     echo "### RUN $(date +%Y%m%d-%H%M%S)" >> $logfile_path 2> $err_logfile_path
     python3 $KNN_SCRIPT $dataset >> $logfile_path 2> $err_logfile_path
     echo "[$(date +%Y%m%d-%H%M%S)] finished ${type}" >> $LOG_FILE 2>&1
  done
}
do_analysis
do_analysis
do_analysis

echo "[$(date +%Y%m%d-%H%M%S)] Done analysing $FOLDER_PATH, results will be available here $LOG_FOLDER_PATH" >> $LOG_FILE 2>&1
