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

# todo
- multithreading
- command line interface
  - preselection
  - folder
  - file
  - classification
  - debug#count files in dir
find ./infected/ ./clean/ -type f | wc -l

# BENIGN count
grep -e "^[0-9a-f]\{32\};0;[.]*" ikarus_20180424.csv | wc -l
# MALWARE count
grep -e "^[0-9a-f]\{32\};1;[.]*" ikarus_20180424.csv | wc -l

# invalid entries
grep -v -e "[0-9a-f]\{32\};[.]*" ikarus_20180424.csv

# syntaxcheck
grep -e "^[0-9a-f]\{32\};0;[0-9.;]*$" ikarus_20180424.csv | wc -l
2350 float werte
