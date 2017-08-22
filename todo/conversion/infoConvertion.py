# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:13:19 2017

@author: clancien
"""

import time

def fileInfo():
    """ tax_ID GeneID Status Symbol"""
    with open('gene_info/gene_info' , 'r') as infile:
        with open('gene_info/gene_info_convert', 'w') as newFile:
            for line in infile:
                lineList= line.split("\t")
                newStr = str(lineList[0]) + "\t" + str(lineList[1]) + "\t" + str(lineList[2]) + "\t" + str(lineList[4]) + "\t" + str(lineList[8])
                newFile.write(newStr)
t0 = time.time()
fileInfo()
print time.time() - t0, "seconds wall time"