# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:00:27 2017

@author: clancien
"""
import time
import tqdm
import ConfigParser
import re 

config= ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))


Concatenation_Entrez=config.get('Convert','Concatenation_Entrez')
GI_transcript=config.get('Convert','GI_transcript')
GI_protein=config.get('Convert','GI_protein')


def getCompare():
    with open (Concatenation_Entrez, 'r') as infile,\
    open(GI_transcript,'r') as GIT:
        for line in tqdm.tqdm(GIT, "Time for loop"):
            toCompare= (re.sub("\n","",line)).split("\t")[2]
            for _line in infile:
                GeneID= _line.split("\t")[0]
                #print GeneID
                if(GeneID == toCompare):
                    print line
t0 = time.time()
getCompare()
print time.time() - t0, "seconds wall time"