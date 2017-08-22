# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 09:55:18 2017

@author: clancien
"""


import re
import time
import ConfigParser
#from progressbar import ProgressBar
import tqdm


config = ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini', 'r'))

data = config.get('Download','homologene_data')
Homologene = config.get ('Convert', 'HomoloGene')


#pbar = ProgressBar()

def fileHomologene():

        
    with open(data , 'r') as infile,\
    open(Homologene, 'w') as output:


###################################################################################
#                                                                                 #
#                                                                                 #
#                       Index Value of columns we need                            #  
#                                                                                 # 
#                                                                                 #
###################################################################################

# No header so by default:

        GeneID_index = 2
        HomologeneID = 0
     
        for line in tqdm.tqdm(infile, 'Time for loop of homologeneCovnerison'):
            lineList= line.split("\t")
            if(re.match(r"^([0-9]*)$", lineList[HomologeneID])):
                output.write( str(lineList[GeneID_index]) + "\tHomoloGene_ID\t" + str(lineList[HomologeneID]) + "\n" )
            

t0= time.time()
fileHomologene()
print time.time() - t0, "seconds wall time"