# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 16:42:44 2017

@author: clancien
"""

import ConfigParser
import os
import pandas
import re

import logging
from logging.handlers import RotatingFileHandler
import sys

class Info():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')
        
        self.gene2info = config.get('Download', 'gene2accession')
        self.info = config.get('Convert', 'Info')
        
        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string
        
        self.filename_gene2info = str(self.gene2info)
        self.filename_info = str(self.info)
        
        
        self.size=1000000 #panda will read by chunsize here 1 million line by 1 million line
        
        self.index_entrez = None
        self.index_tax_id = None
        self.index_symbol = None
        self.index_description = None
        
        self.dataframe = list
        
        self.logger=None
        self.formatter=None
        self.file_handler=None
        #GeneID UniGene_cluster
        
        self.path_exist()
        self.init_log()
        self.create_index()
        
    def path_exist(self):
        
        """ Check if dir exist if not we create the path

        string = dir/subdir/subsubdir 
        string.rsplit('/',1)[0] 
        ==> return dir/subdir/ """
        
        if not os.path.isdir(self.info.rsplit('/',1)[0]):
            os.makedirs(self.info.rsplit('/', 1)[0])

    def init_log(self):
        
        # création de l'objet logger qui va nous servir à écrire dans les logs
        self.logger = logging.getLogger()
        # on met le niveau du logger à DEBUG, comme ça il écrit tout
        self.logger.setLevel(logging.DEBUG)
         
        # création d'un formateur qui va ajouter le temps, le niveau
        # de chaque message quand on écrira un message dans le log
        self.formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        # création d'un handler qui va rediriger une écriture du log vers
        # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
        
        self.file_handler = RotatingFileHandler(self.logFile, 'a', 1000000, 1)
        # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
        # créé précédement et on ajoute ce handler au logger
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        

    def create_index(self):

        with open(self.filename_accession , 'r') as infile:

            header_line = next(infile)
            header_line = header_line.split('\t')
                
            self.index_entrez = header_line.index('GeneID')
            self.index_tax_id = header_line.index('#tax_id')
            self.index_symbol = header_line.index('S')
            self.index_description = header_line.index('#tax_id')
            


#tax_id GeneID  Symbol  LocusTag        Synonyms        dbXrefs chromosome      map_location    description     type_of_gene    Symbol_from_nomenclature_authority      Full_name_from_nomenclature_authority   Nomenclature_status     Other_designations      Modification_date       Feature_type

def fileInfo():
    """ tax_ID GeneID Status Symbol"""
    with open('gene_info/gene_info' , 'r') as infile:
        with open('gene_info/gene_info_convert', 'w') as newFile:
            for line in infile:
                lineList= line.split("\t")
                newStr = str(lineList[0]) + "\t" + str(lineList[1]) + "\t" + str(lineList[2]) + "\t" + str(lineList[4]) + "\t" + str(lineList[8])
                newFile.write(newStr)
t0 = time.time()
fileInfo()
print time.time() - t0, "seconds wall time"