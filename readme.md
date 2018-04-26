# setup
## install requirements
$ pip3 install -r requirements.txt

## run tool
$ cd /media/dataspacedisk  <br/>
$ python3 ./mymodellisknowntoo/featureextraction.py > malware_20180323.csv

# helpers
## count lines in csv (progress)
$ wc -l /media/dataspacedisk/malware_20180323.csv  <br/> 
434 malware_20180323.csv

## count files in folder
$ find /media/dataspacedisk/pe32files -type f | wc -l <br/>
7197

## count each folder and sort by number of items
for dir in clean/*; do echo -e filecount: $(find $dir -type f | wc -l)'\t' $dir; done | sort -k2 --numeric-sort -r <br/>
for dir in infected/*; do echo -e filecount: $(find $dir -type f | wc -l)'\t' $dir; done | sort -k2 --numeric-sort -r <br/>

## BENIGN count
grep -e "^[0-9a-f]\{32\};0;[.]*" XYZ_20180424.csv | wc -l

## MALWARE count
grep -e "^[0-9a-f]\{32\};1;[.]*" XYZ_20180424.csv | wc -l

## invalid entries
grep -v -e "[0-9a-f]\{32\};[.]*" XYZ_20180424.csv ##todo

## syntaxcheck - 2350 floats
grep -e "^[0-9a-f]\{32\};0;[0-9.;]*$" ikarus_20180424.csv | wc -l ##todo

# todo
- command line interface
  - preselection
  - folder
  - file
  - classification
  - debug#count files in dir

