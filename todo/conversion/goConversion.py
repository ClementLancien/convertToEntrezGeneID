# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:07:43 2017

@author: clancien
"""

import time
import re
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('db_path_conf.ini'))

gene2go = config.get('Download','g)
def fileGO():
    """ tax_ID GeneID Status Symbol"""
    with open('gene2go/gene2go' , 'r') as infile:
        with open('gene2go/gene2go_convert', 'w') as newFile:
            for line in infile:
                lineList= line.split("\t")
                newStr = str(lineList[0]) + "\t" + str(lineList[1]) + "\t" + str(lineList[2]) + "\t" + str(lineList[5]) + "\t" + str(lineList[7])
                newFile.write(newStr)
t0 = time.time()
fileGO()
print time.time() - t0, "seconds wall time"