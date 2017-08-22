# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:25:29 2017

@author: clancien
"""

import time
import ConfigParser
import glob
import tqdm
import re


config=ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))

Ensembl_gene= config.get('Convert','Ensembl_gene')
Ensembl_transcript= config.get('Convert','Ensembl_transcript')
Ensembl_protein= config.get('Convert','Ensembl_protein')

HomoloGene= config.get('Convert','HomoloGene')

GPL_all=config.get('Convert','GPL_all')

GenBank_transcript=config.get('Convert','GenBank_transcript')
GenBank_protein=config.get('Convert','GenBank_protein')

GI_transcript=config.get('Convert','GI_transcript')
GI_protein=config.get('Convert','GI_protein')
UniGene=config.get('Convert','UniGene')

RefSeq_transcript=config.get('Convert','RefSeq_transcript')
RefSeq_protein=config.get('Convert','RefSeq_protein')

SwissProt=config.get('Convert','UniProtKB_sprot')
trEmblID=config.get('Convert','trEmblID')


vega_gene=config.get('Convert','vega_gene')
vega_transcript=config.get('Convert','vega_transcript')
vega_protein=config.get('Convert','vega_protein')
    
                
def create(base,string):
    print str(string)
    with open(str(string), 'w') as output,\
    open(Ensembl_gene, 'r') as infile:
        for line in infile:
            output.write(str(line.split("\t")[0]) + "\n")



create(Ensembl_gene,0)
create(Ensembl_transcript,1)
create(Ensembl_protein,2)

create(HomoloGene,3)

create(GPL_all,4)

create(GenBank_transcript,5)
create(GenBank_protein,6)

create(GI_transcript,7)
create(GI_protein,8)
create(UniGene,9)

create(RefSeq_transcript,10)
create(RefSeq_protein,11)

create(SwissProt,12)
create(trEmblID,13)

create(vega_gene,14)
create(vega_transcript,15)
create(vega_protein,16)

def getnumberEGID():
    with open("42",'r') as infile:
        i=0
        for line in infile:
            i=i+1
    print i
          
def isRedondant():
    with open("42",'r') as output:
        i=0
        for line in output:
            i=i+1
            newline=line.split("\n")
            for _line in output:
                _newline=_line.split("\n")
                if newline == _newline:
                    print "is redondant : ", i
                    return
#getEGID()
getnumberEGID()
isRedondant()
                    
