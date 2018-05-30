#!/bin/bash
#find . -maxdepth 1
function count_in_folder {
   echo -e "Counting $(find ${1} -type f | wc -l) \t files and $(find ${1} -type d | wc -l) \t folders with total size of $(du -Sch ${1} | grep total | awk '{print $1}') \t in folder ${1}"
}

#if no argument is given, count in current folder
if [ $# -eq 0 ]; then
   count_in_folder "."
else
   #if first argument and recursive switch is given, do a recursive scan
   if [ $1 = "-r" ]; then
      #if second arg is given, expect path
      if [ $# -eq 2 ]; then
         for FOLDER in $(find $2 -type d); do
           count_in_folder "${FOLDER}"
         done
      #otherwise count in current dir
      elif [ $# -eq 1 ]; then
         for FOLDER in $(find . -type d); do
           count_in_folder "${FOLDER}"
         done
      fi
   else
     #take first argument as folder path
     count_in_folder "${1}"
   fi
fi
