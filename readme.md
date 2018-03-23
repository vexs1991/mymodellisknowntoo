
#install requirements
$ pip3 install -r requirements.txt

#run tool
$ cd /media/dataspacedisk  <br/>
$ python3 ./mymodellisknowntoo/featureextraction.py > malware_20180323.csv

#count lines in csv
$ wc -l /media/dataspacedisk/malware_20180323.csv  <br/> 
434 malware_20180323.csv

#count files in folder
$ find /media/dataspacedisk/pe32files -type f | wc -l <br/>
7197

#todo
- multithreading
- command line interface
  - preselection
  - folder
  - file
  - classification
  - debug