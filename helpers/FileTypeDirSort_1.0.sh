#!/bin/bash
############################
## FileTypeDirSort v: 1.0
##
## sort files by type
## creates a directory for every file type in given folder and
## move corresponding file to
############################

if [ $# -eq 0 ]; then
    echo "$0 [path]"
    exit 0
fi

#for folder (not recursive)
#FOLDER_PATH="/"
FOLDER_PATH="$1"

[[ -d "$FOLDER_PATH" ]] || exit 1

#for every file in folder do
for filename in $FOLDER_PATH/*; do
   #clean file type and remove unwanted chars
   CLEAN_FILE_TYPE=$(/usr/bin/file -b "$filename" | sed -r 's/[/,.;:]+//g' | sed -r 's/[ ]+/_/g')
   #only if file is not a directory
   if [ "$CLEAN_FILE_TYPE" != "directory" ]; then
      #if folder does not exist, create one
      [[ -d "$FOLDER_PATH/$CLEAN_FILE_TYPE" ]] || mkdir "$FOLDER_PATH/$CLEAN_FILE_TYPE"
      #and move file to corresponding folder
      mv "$filename" "$FOLDER_PATH/$CLEAN_FILE_TYPE"
   fi
done
