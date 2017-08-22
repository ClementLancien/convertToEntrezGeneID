# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:37:36 2017

@author: clancien
"""


import re
import time
import ConfigParser
import tqdm

config= ConfigParser.ConfigParser()

config.readfp(open('../../../conf.ini', 'r'))

gene_info = config.get('Download', 'gene_info')
Entrez_GeneInfo = config.get('Convert', 'Entrez_GeneInfo')


def getFileGeneInfo():
    
    """Create a new File :
    columns : GeneID TaxID Symbol (Symbol+Locus Tag + Synonyms) Description TypeOfGenes"""
    
    with open(gene_info, 'r') as infile,\
    open(Entrez_GeneInfo, 'w') as output:
        
        header_line = next(infile)
        header_line = header_line.split("\t")
        print header_line
        GeneID_index = header_line.index('GeneID')
        TaxID_index = header_line.index('#tax_id')
        Symbol_index = header_line.index('Symbol')
        LocusTag_index = header_line.index('LocusTag')
        Synonyms_index = header_line.index('Synonyms')
        Description_index = header_line.index('description')
        TypeOfGene_index = header_line.index('type_of_gene')
        
        for line in tqdm.tqdm(infile, 'Time for loop of geneInfoConversion'):
            lineList = line.split("\t")
            newStr=""
            if(re.match(r"^([0-9]*)$", lineList[GeneID_index])):
                newStr += str(lineList[GeneID_index]) +"\t"
            if(re.match(r"^([0-9]*)$", lineList[TaxID_index])):
                newStr += str(lineList[TaxID_index]) + "\t"
            if (lineList[Symbol_index] == '-'):
                newStr += str(lineList[GeneID_index]) + "\t" + str(lineList[GeneID_index])
            else:
                newStr += str(lineList[Symbol_index]) + "\t" + str(lineList[Symbol_index])
            if(lineList[LocusTag_index] != '-'):
                newStr += "|" + str(lineList[LocusTag_index])
            if(lineList[Synonyms_index] != '-'):
                newStr += str(lineList[Synonyms_index])
            newStr+="\t"
            for letter in lineList[Description_index]:
                if (re.match(r"^[a-zA-Z0-9]", letter) or letter =='-' or letter == '_' or letter =='+'):
                    newStr += str(letter)
                else:
                    newStr += " "
            if (lineList[TypeOfGene_index] != '-'):
                newStr += "\t" + str(lineList[TypeOfGene_index])
            else:
                newStr += "\tNA"
            
            output.write(newStr + "\n")
            
            #print lineList
        
t0=time.time()
getFileGeneInfo()
print time.time() - t0 , "seconds wall time"
