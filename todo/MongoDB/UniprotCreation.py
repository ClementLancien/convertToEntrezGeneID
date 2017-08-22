# -*- coding: utf-8 -*-
"""
Created on Tue May  9 08:34:54 2017

@author: clancien
"""

import time
import tqdm
from pymongo import MongoClient
import ConfigParser

config= ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))

UniProtKB_sprot=config.get('Convert','UniProtKB_sprot')

def pushSwissProt():
    client = MongoClient()
    db=client["GeneULike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(UniProtKB_sprot , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.SwissProt.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             "ID" : str(lineList[1]),
                             "Accession" : str(lineList[2])
                             })
            except:
                #print file_
                print "lastline is : ", line

def push():
    pushSwissProt()

t0 = time.time()
push()
print time.time() - t0, "seconds wall time"