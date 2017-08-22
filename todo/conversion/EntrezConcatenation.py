# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 13:21:42 2017

@author: clancien
"""


import time
import ConfigParser
import shutil
import tqdm
config = ConfigParser.ConfigParser()
config.readfp(open("../../../conf.ini",'r'))

Ensembl_gene=config.get('Convert','Ensembl_gene')
Ensembl_transcript=config.get('Convert','Ensembl_transcript')
Ensembl_protein=config.get('Convert','Ensembl_protein')
UniGene=config.get('Convert','UniGene')
vega_gene=config.get('Convert','vega_gene')
vega_transcript=config.get('Convert','vega_transcript')
vega_protein=config.get('Convert','vega_protein')
gene2gene=config.get('Convert','gene2gene')
GenBank_transcript=config.get('Convert','GenBank_transcript')
RefSeq_transcript=config.get('Convert','RefSeq_transcript')
GenBank_protein=config.get('Convert','GenBank_protein')
RefSeq_protein=config.get('Convert','RefSeq_protein')
GI_transcript=config.get('Convert','GI_transcript')
GI_protein=config.get('Convert','GI_protein')

Gene_TaxID=config.get('Convert','Gene_TaxID')
Gene_Symbol=config.get('Convert','Gene_Symbol')
HomoloGene=config.get('Convert','HomoloGene')

Concatenation_Entrez=config.get('Convert','Concatenation_Entrez')

fileList = [Ensembl_gene, Ensembl_transcript, Ensembl_protein,\
        UniGene, vega_gene, vega_transcript, vega_protein,\
        gene2gene, GenBank_transcript, RefSeq_transcript,\
        GenBank_protein, GI_transcript, GI_protein, Gene_TaxID,\
        Gene_Symbol, HomoloGene]
        
def getConcatenate():
    
    with open(Concatenation_Entrez, 'wb') as output:
        for file_ in tqdm.tqdm(fileList, "Time for loop of EntrezConcatenation"):
            with open(file_ , 'rb' ) as readfile:
             shutil.copyfileobj(readfile, output)
t0 = time.time()
getConcatenate()
print time.time() - t0, "seconds wall time"