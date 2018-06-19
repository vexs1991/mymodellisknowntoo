#!/bin/bash
LOG_FOLDER_PATH="/media/dataspacedisk/statcsv"

INFLOG=${LOG_FOLDER_PATH}/inf
CLNLOG=${LOG_FOLDER_PATH}/cln
OUTLOG=${LOG_FOLDER_PATH}/combined

OUT_COMPL_cln=${OUTLOG}/COMPL_cln.csv
OUT_COMPL_inf=${OUTLOG}/COMPL_inf.csv
OUT_COMPLSHUF_inf=${OUTLOG}/COMPLSHUF_inf.csv
OUT_COMPLSHUF_cln=${OUTLOG}/COMPLSHUF_cln.csv

OUT_5050_1=${OUTLOG}/TC_50-50_1.csv
OUT_5050_2=${OUTLOG}/TC_50-50_2.csv
OUT_5050_3=${OUTLOG}/TC_50-50_3.csv
OUT_5050_4=${OUTLOG}/TC_50-50_4.csv
OUT_5050_5=${OUTLOG}/TC_50-50_5.csv
OUT_5050_6=${OUTLOG}/TC_50-50_6.csv
OUT_5050_7=${OUTLOG}/TC_50-50_7.csv
OUT_5050_8=${OUTLOG}/TC_50-50_8.csv
OUT_5050_9=${OUTLOG}/TC_50-50_9.csv
OUT_5050_10=${OUTLOG}/TC_50-50_10.csv

OUT_TOP10=${OUTLOG}/TC_TOP10.csv
OUT_TOP15=${OUTLOG}/TC_TOP15.csv
OUT_ALLTOGETHER=${OUTLOG}/TC_ALLTOGETHER.csv

OUT_5050_1_shuf=${OUTLOG}/TC_50-50_1_shuf.csv
OUT_5050_2_shuf=${OUTLOG}/TC_50-50_2_shuf.csv
OUT_5050_3_shuf=${OUTLOG}/TC_50-50_3_shuf.csv
OUT_5050_4_shuf=${OUTLOG}/TC_50-50_4_shuf.csv
OUT_5050_5_shuf=${OUTLOG}/TC_50-50_5_shuf.csv
OUT_5050_6_shuf=${OUTLOG}/TC_50-50_6_shuf.csv
OUT_5050_7_shuf=${OUTLOG}/TC_50-50_7_shuf.csv
OUT_5050_8_shuf=${OUTLOG}/TC_50-50_8_shuf.csv
OUT_5050_9_shuf=${OUTLOG}/TC_50-50_9_shuf.csv
OUT_5050_10_shuf=${OUTLOG}/TC_50-50_10_shuf.csv

OUT_TOP10_shuf=${OUTLOG}/TC_TOP10_shuf.csv
OUT_TOP15_shuf=${OUTLOG}/TC_TOP15_shuf.csv
OUT_ALLTOGETHER_shuf=${OUTLOG}/TC_ALLTOGETHER_shuf.csv

print_no_infcln() {
  echo #### Counting number of entries in $1
  echo -e "$(egrep -e "[0-9a-f]{32};0;[.]*" $1 | wc -l) \t CLEAN \t FILES IN $1"
  echo -e "$(egrep -e "[0-9a-f]{32};1;[.]*" $1 | wc -l) \t BENIGN FILES IN $1"
}

#first combine all data available, clean empty lines
#sort requires a lot of tmp space, therefore we redirect /tmp to /mnt
[ -f ${OUT_COMPL_cln} ] || cat ${CLNLOG}/*.csv | grep -v '^$' | sort -T /mnt -u > ${OUT_COMPL_cln}
[ -f ${OUT_COMPL_inf} ] || cat ${INFLOG}/*.csv | grep -v '^$' | sort -T /mnt -u > ${OUT_COMPL_inf}

#count number of entries
NO_COMPL_cln=$(wc -l ${OUT_COMPL_cln} | awk '{print $1}')
NO_COMPL_inf=$(wc -l ${OUT_COMPL_inf} | awk '{print $1}')
echo ${NO_COMPL_cln} written to ${OUT_COMPL_cln}
echo ${NO_COMPL_inf} written to ${OUT_COMPL_inf}

#shuffle
[ -f ${OUT_COMPLSHUF_cln} ] || shuf ${OUT_COMPL_cln} > ${OUT_COMPLSHUF_cln}
[ -f ${OUT_COMPLSHUF_inf} ] || shuf ${OUT_COMPL_inf} > ${OUT_COMPLSHUF_inf}

#test for completness
NO_COMPLSHUF_cln=$(wc -l ${OUT_COMPLSHUF_cln} | awk '{print $1}')
NO_COMPLSHUF_inf=$(wc -l ${OUT_COMPLSHUF_inf} | awk '{print $1}')
echo ###########################################################
echo ${NO_COMPLSHUF_cln} written to ${OUT_COMPLSHUF_cln}
echo ${NO_COMPLSHUF_inf} written to ${OUT_COMPLSHUF_inf}

#50/50 fairly shuffled
head -n ${NO_COMPLSHUF_cln} ${OUT_COMPLSHUF_inf} > ${OUT_5050_1}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_1}
print_no_infcln ${OUT_5050_1}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +${NO_COMPLSHUF_cln} ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_2}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_2}
print_no_infcln ${OUT_5050_2}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +$(( ${NO_COMPLSHUF_cln}*2 )) ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_3}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_3}
print_no_infcln ${OUT_5050_3}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +$(( ${NO_COMPLSHUF_cln}*3 )) ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_4}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_4}
print_no_infcln ${OUT_5050_4}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +$(( ${NO_COMPLSHUF_cln}*4 )) ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_5}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_5}
print_no_infcln ${OUT_5050_5}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +$(( ${NO_COMPLSHUF_cln}*5 )) ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_6}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_6}
print_no_infcln ${OUT_5050_6}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +$(( ${NO_COMPLSHUF_cln}*6 )) ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_7}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_7}
print_no_infcln ${OUT_5050_7}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +$(( ${NO_COMPLSHUF_cln}*7 )) ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_8}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_8}
print_no_infcln ${OUT_5050_8}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +$(( ${NO_COMPLSHUF_cln}*8 )) ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_9}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_9}
print_no_infcln ${OUT_5050_9}

#50/50 fairly shuffled (get next batch, skip first NO_COMPLSHUF_cln lines
tail -n +$(( ${NO_COMPLSHUF_cln}*9 )) ${OUT_COMPLSHUF_inf} | head -n ${NO_COMPLSHUF_cln} > ${OUT_5050_10}
cat ${OUT_COMPLSHUF_cln} >> ${OUT_5050_10}
print_no_infcln ${OUT_5050_10}

#top 10
for top10 in $(ls -S ${INFLOG} | egrep '*.csv' | head -10); do cat ${INFLOG}/$top10 | grep -v '^$' | sort -T /mnt -u >> ${OUT_TOP10}; done
for top10 in $(ls -S ${CLNLOG} | egrep '*.csv' | head -10); do cat ${CLNLOG}/$top10 | grep -v '^$' | sort -T /mnt -u >> ${OUT_TOP10}; done
print_no_infcln ${OUT_TOP10}

#top 15
for top15 in $(ls -S ${INFLOG} | egrep '*.csv' | head -15); do cat ${INFLOG}/$top15 | grep -v '^$' | sort -T /mnt -u >> ${OUT_TOP15}; done
for top15 in $(ls -S ${CLNLOG} | egrep '*.csv' | head -15); do cat ${CLNLOG}/$top15 | grep -v '^$' | sort -T /mnt -u >> ${OUT_TOP15}; done
print_no_infcln ${OUT_TOP15}

#alltogether
cat ${OUT_COMPLSHUF_inf} ${OUT_COMPLSHUF_cln} > ${OUT_ALLTOGETHER}
print_no_infcln ${OUT_ALLTOGETHER}

echo "creating shuffled versions of results"
shuf ${OUT_5050_1} > ${OUT_5050_1_shuf}
shuf ${OUT_5050_2} > ${OUT_5050_2_shuf}
shuf ${OUT_5050_3} > ${OUT_5050_3_shuf}
shuf ${OUT_5050_4} > ${OUT_5050_4_shuf}
shuf ${OUT_5050_5} > ${OUT_5050_5_shuf}
shuf ${OUT_5050_6} > ${OUT_5050_6_shuf}
shuf ${OUT_5050_7} > ${OUT_5050_7_shuf}
shuf ${OUT_5050_8} > ${OUT_5050_8_shuf}
shuf ${OUT_5050_9} > ${OUT_5050_9_shuf}
shuf ${OUT_5050_10} > ${OUT_5050_10_shuf}
shuf ${OUT_TOP10} > ${OUT_TOP10_shuf}
shuf ${OUT_TOP15} > ${OUT_TOP15_shuf}
shuf ${OUT_ALLTOGETHER} > ${OUT_ALLTOGETHER_shuf}

#sh ./DoAnalysis.sh
