# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:40:27 2017

@author: clancien
"""

import re
import time
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini', 'r'))

gene2vega = config.get('Download', 'gene2vega')
vega_gene = config.get('Convert', 'vega_gene')
vega_transcript = config.get('Convert', 'vega_transcript')
vega_protein = config.get('Convert', 'vega_protein')

def fileVega():
    
    with open(gene2vega, 'r') as vega,\
    open(vega_gene, 'w') as gene,\
    open(vega_transcript, 'w') as transcript,\
    open(vega_protein, 'w') as protein:
        
        header_line = next(vega)
        header_line= header_line.split("\t")
        
        
###################################################################################
#                                                                                 #
#                                                                                 #
#                       Index Value of columns we need                            #  
#                                                                                 # 
#                                                                                 #
###################################################################################                
        
        GeneID_index = header_line.index('GeneID')
        Vega_gene_index = header_line.index('Vega_gene_identifier')
        Vega_transcript_index = header_line.index('Vega_rna_identifier')
        Vega_protein_index = header_line.index('Vega_protein_identifier\n')

        
        previous_GeneID=None
        for line in vega:
            lineList= line.split("\t")
            if(re.match(r"^[O][T][T][D][A][R][G]([0-9]*)$", lineList[Vega_gene_index])):
               if(str(lineList[Vega_gene_index]) != previous_GeneID):
                   gene.write(lineList[GeneID_index] + "\tVega_gene\t" + str(lineList[Vega_gene_index])+"\n")
            if(re.match(r"^[O][T][T][D][A][R][T]([0-9]*)$", lineList[Vega_transcript_index])):
                transcript.write(lineList[GeneID_index] + "\tVega_gene\t" + str(lineList[Vega_transcript_index]) +"\n")
            if(re.match(r"^[O][T][T][D][A][R][P]([0-9]*)$", lineList[Vega_protein_index])):
                protein.write(lineList[GeneID_index] + "\tVega_gene\t" + str(lineList[Vega_protein_index]))
            previous_GeneID=str(lineList[Vega_gene_index])
t0 = time.time()
fileVega()
print time.time() - t0, "seconds wall time"