# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:13:27 2017

@author: clancien
"""

import re
import time
import tqdm
import ConfigParser

config=ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))

uniprot_sprot_data=config.get('Download','UniProtKB_sprot')
uniprot_sprot=config.get('Convert','UniProtKB_sprot')


#def getUniprotKB():
    
    #with open(uniprot_sprot_data, 'r') as infile,\
    #open(uniprot_sprot, 'w') as output:
        #UniprotID=""
        #GeneID=""
        #Accession=[]
        #for line in tqdm.tqdm(infile,"Time for loop of Swissprot"):
            #if(re.match(r"^[I][D]",line)):
             #   UniprotID=line[5:].split(" ")[0]
            #if(re.match(r"[G][e][n][e][I][D]",line[5:])):
               # GeneID=line[5:].split("; ")[1]


            #if(re.match(r"^[A][C]",line)):
                #tempAccessionList = re.sub(" ","",line[5:])
                ##tempAccessionList = re.sub("\n","", tempAccessionList)
                #tempAccessionList = tempAccessionList.split(";")
                ##print tempAccessionList
                #for AccessionID in tempAccessionList:
                    #Accession.append(AccessionID)
            #if(re.match(r'^//',line)):
                #for accessionID in Accession:
                    #if(accessionID != "\n"):
                       # output.write(str(GeneID) + "\t" + str(accessionID) + "\n")
                    ##print UniprotID
                #Accession=[]

def getSwissprot():
    with open(uniprot_sprot_data,'r') as info,\
    open(uniprot_sprot, 'w') as output:
        ID=""
        AC=[]
        for line in tqdm.tqdm(info, "Time for loop of SwissProt : "):
            if("AC" in line[:2]):
                newLine=line[5:].split("; ")
                for ac in newLine:
                    AC.append(ac)
            if("GeneID" in line and "DR" in line):
                newLine=line[5:].split("; ")
                ID=newLine[1]
            if("//" in line):
                if (ID != ""):
                    for ac in AC:
                        output.write(str(ID) + "\t" + str(ac.split(";")[0]) + "\n")
                ID=""
                AC=[]
t0=time.time()
getSwissprot()
#getUniprotKB()
print time.time() - t0, "seconds wall time"
 
