# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:41:30 2017

@author: clancien
"""

import time
import ConfigParser
import tqdm

config=ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))

uniprot_data=config.get('Download','UniProtKB_trembl')
trEmblID=config.get('Convert', 'trEmblID')

def converttrEMBL():
    i=0
    with open(uniprot_data, 'r') as info,\
    open(trEmblID,'w') as result:
        ID=""
        AC=[]
        for line in tqdm.tqdm(info, 'Time for loop of Convert trEMBL'):
            if("AC" in line[:2]):
                newLine=line[5:].split("; ")
                for ac in newLine:
                    AC.append(ac)
            if("GeneID" in line and "DR" in line):
                #print (line)
                newID=line[5:].split("; ")
                ID=newID[1]
            if("//" in line):
                if(ID != ""):
                    for ac in AC:
                        result.write(str(ID) + "\t" + str(ac.split(";")[0]) + "\n")
                        i=i+1
                ID=""
                AC=[]

    print("nbre : "+ str(i))
t0= time.time()
converttrEMBL()
print time.time() - t0, "seconds wall time"

