# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:48:42 2017

@author: clancien
"""

import time
import re
import ConfigParser
import tqdm 

config = ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini', 'r'))

gene2ensembl = config.get('Download','gene2ensembl')
Ensembl_gene = config.get('Convert', 'Ensembl_gene')
Ensembl_transcript = config.get('Convert', 'Ensembl_transcript')
Ensembl_protein = config.get('Convert', 'Ensembl_protein')


def filesEnsembl():
    """ Create 3 files from gene2ensembl :
        Ensembl_gene : GeneID Ensembl_gene Ensembl_gene_identifier
        Ensembl_transcript : GeneID Ensemble_transcript Ensembl_rna_identifier 
        Ensembl_proteine : GeneID Ensembl_protein Ensembl_protein_identifier """
        
    with open(gene2ensembl , 'r') as infile,\
        open(Ensembl_gene, 'w') as gene, \
        open(Ensembl_transcript, 'w') as transcript, \
        open(Ensembl_protein, 'w') as protein :
            
            header_line = next(infile)
            header_line = header_line.split('\t')
            
            
###################################################################################
#                                                                                 #
#                                                                                 #
#                       Index Value of columns we need                            #  
#                                                                                 # 
#                                                                                 #
###################################################################################

            
            GeneID_index = header_line.index('GeneID')
            Ensembl_gene_index = header_line.index('Ensembl_gene_identifier')
            Ensembl_transcript_index = header_line.index('Ensembl_rna_identifier')
            Ensembl_protein_index = header_line.index('Ensembl_protein_identifier\n')

            
            previous_Ensembl_gene=None
            previous_Ensembl_transcript=None
            for line in tqdm.tqdm(infile, 'Time for loop of ensemblConversion'):
                lineList= line.split("\t")
                if str(lineList[GeneID_index]) != '-':
                    if(str(lineList[Ensembl_gene_index]) != previous_Ensembl_gene and str(lineList[Ensembl_gene_index]) != '-'):
                        gene.write(str(lineList[GeneID_index]) + "\t" + str(lineList[Ensembl_gene_index]) + "\n")                    
                    
                    if(str(lineList[Ensembl_transcript_index]) != "-" and str(lineList[Ensembl_transcript_index]) != previous_Ensembl_transcript):
                        transcript.write(str(lineList[GeneID_index]) + "\t" + str(lineList[Ensembl_transcript_index]) + "\n")
                    if(str(lineList[Ensembl_protein_index]) != "-\n"):
                        protein.write(str(lineList[GeneID_index]) + "\t" + str(lineList[Ensembl_protein_index].split("\n")[0]) + "\n")
                    
                previous_Ensembl_gene = str(lineList[Ensembl_gene_index])
                previous_Ensembl_transcript = str(lineList[Ensembl_gene_index])
                



t0 = time.time()
filesEnsembl()
print time.time() - t0, "seconds wall time"
