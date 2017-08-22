# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:58:13 2017

@author: clancien
"""
import elasticsearch
import time
import tqdm
from pymongo import MongoClient
import ConfigParser

config= ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))


GPL_all=config.get('Convert','GPL_all')


        
def getEntrezCollection():
    client = MongoClient()
    db=client["GeneULike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(GPL_all,'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.GPL.insert(
                         {
                          "GeneID" : str(lineList[0]),
                          "GPLname" : str(lineList[1]),
                          "ProbeID" : str(lineList[2].split("\n")[0])
                          })
            except all:
                #print file_
                print "lastline is : ", line
                

t0 = time.time()
getEntrezCollection()
print time.time() - t0, "seconds wall time"