# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 09:44:59 2017

@author: clancien
"""
import time
import ConfigParser
import glob
import tqdm
import re


config=ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))
GPL_path=config.get('Download','GPL')
GPL_all=config.get('Convert','GPL_all')


def getAllGPL():

    files = glob.glob( GPL_path + '*.annot' )
    i=0
    with open( GPL_all, 'w' ) as output:
        for file_ in tqdm.tqdm(files,"Time for loop of GPL files"):
            filename= file_.split(".")[4].split("/")[2]
            name=""
            for line in open( file_, 'r' ):
                if("!Annotation_platform_title" in line):
                    name = str(line.split("= ")[1].split("\n")[0])
                if(re.match(r"^[0-9]",line)):
                    lineList = line.split("\t")
                    #print i
                    GeneID=lineList[3]
                    #['853878', '', '1769308_at\n']
                    #print file_                    
                    if(re.match(r'([0-9]*)[/][/][/]',GeneID)):
                        GeneID=list(set(GeneID.split("///")))
                        for gID in GeneID:
                            output.write(str(gID)  + "\t" +str(filename) + "\t" + lineList[0] + "\t" + str(name) + "\n")
                    elif(str(GeneID) != '-'):
                        output.write(str(GeneID)  + "\t" +str(filename) + "\t" + lineList[0] + "\t" + str(name) + "\n")
                    #else:
                    #    i+=1
                    #    if(GeneID == ""):
                    #        GeneID="NA"
                    #    output.write(lineList[3]  + "\t" + str(filename) + "\t" + lineList[0] + "\t" + str(name) + "\n")
                #i=i+1
    print "absent : ", i                        

t0 = time.time()
getAllGPL()
print time.time() - t0, "seconds wall time"


