# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:12:10 2017

@author: clancien
"""

import ConfigParser
import time
import tqdm
import glob
 
config=ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))
GPL_path=config.get('Download','GPL')
GPLnumberToSpecies= config.get('Other', 'GPLnumberToSpecies')

def getSpeciesFromGPL():
    
    files = glob.glob( GPL_path + '*.annot' )
    with open(GPLnumberToSpecies, 'w' ) as output:
        number_file=0
        
        for file_ in tqdm.tqdm(files,"Time for loop of GPL files"):
            number_file=number_file + 1
            for line in open( file_, 'r' ):

                if("!Annotation_platform_organism" in line):
                    filename= file_.split(".")[4].split("/")[2]
                    organism = line.split("= ")
                    output.write(str(filename) + "," + organism[1].split("\n")[0] + "\n")
                    break

t0=time.time()
#getSpeciesFromGPL()
print time.time() - t0, "seconds wall time"
a="GST0,GST10"
print a.split(",")
def numberSpecies():
    species=[]
    with open(GPLnumberToSpecies, 'r' ) as infile:
        for line in infile:
            lineList=line.split(',')
            species.append(lineList[1])
    newList=[]
    for specy in species:
        if specy not in newList:
            newList.append(specy)
    print 'number of species : ', len(newList)
print numberSpecies()