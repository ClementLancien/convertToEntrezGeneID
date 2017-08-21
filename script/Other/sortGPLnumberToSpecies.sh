#!/bin/bash

stuff="../../GPL/GPLnumberToSpecies"
cat ${stuff} | \
while read num
do
	awk '{printf $NF;$NF = " "; printf " "$0"\n" }' | sort -nr | \
	awk '{printf $NF;$NF = " "; printf " "$0"\n" }' | \
	awk '{printf $NF;$NF = " "; printf " "$0"\n" }' > file1.txt
done
