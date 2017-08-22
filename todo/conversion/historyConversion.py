# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:01:55 2017

@author: clancien
"""

import re
import time
import ConfigParser
import tqdm

config= ConfigParser.ConfigParser()
config.readfp(open("../../../conf.ini", 'r'))

gene2history = config.get('Download', 'gene2history')
gene2gene = config.get('Convert', 'gene2gene')

def fileHistory():
    """Create one file named gene2gene 
    3 columns : GeneID gene2gene gene2geneID"""
    with open(gene2history, 'r') as history,\
    open(gene2gene , 'w') as gene:
        
        header_line = next(history)
        header_line= header_line.split("\t")
        
        
###################################################################################
#                                                                                 #
#                                                                                 #
#                       Index Value of columns we need                            #  
#                                                                                 # 
#                                                                                 #
###################################################################################        
        
        
        
        
        GeneID_index = header_line.index('GeneID')
        AncientGeneID_index = header_line.index('Discontinued_GeneID')
        
        for line in tqdm.tqdm(history, 'Time for loop of historyConversion'):
            lineList= line.split("\t")
            if(re.match(r"^([0-9]*)$", lineList[1]) and re.match(r"^([0-9]*)$", lineList[AncientGeneID_index])):
                gene.write(str(lineList[GeneID_index]) + "\tgene2gene\t" + str(lineList[AncientGeneID_index]) + "\n")
t0 = time.time()
fileHistory()
print time.time() - t0, "seconds wall time"