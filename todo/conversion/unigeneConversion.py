# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:20:41 2017

@author: clancien
"""

import time
import re
import ConfigParser
import tqdm

config = ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini', 'r'))

gene2unigene = config.get('Download', 'gene2unigene')
UniGene = config.get('Convert', 'UniGene')

def fileUnigene():
    """Create one file named gene2gene from gene2unigene
    3 columns : GeneID gene2gene Gene2geneID    
    """
    
    with open(gene2unigene, 'r') as unigene,\
    open(UniGene, 'w') as gene:
        
        header_line = next(unigene)
        header_line= header_line.split("\t")
        
        
###################################################################################
#                                                                                 #
#                                                                                 #
#                       Index Value of columns we need                            #  
#                                                                                 # 
#                                                                                 #
################################################################################### 
        GeneID_index = header_line.index('#GeneID')
        Unigene_index = header_line.index('UniGene_cluster\n')
        
        for line in tqdm.tqdm(unigene, 'Time for loop of unigeneConversion'):
            lineList= line.split("\t")
            if (re.match(r"^[a-zA-Z]{2,3}[.]([0-9]*)$", lineList[1])):
                gene.write(lineList[GeneID_index] + "\tUniGene\t" + str(lineList[Unigene_index]))

t0 = time.time()
fileUnigene()
print time.time() - t0, "seconds wall time"
