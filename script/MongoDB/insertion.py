# -*- coding: utf-8 -*-
"""
Created on Mon July 28 13:44:19 2017

@author: clancien
"""

try:

	import ConfigParser

except ImportError:

	import configparser as ConfigParser


import os 
import subprocess

import logging
from logging.handlers import RotatingFileHandler
import sys

class Insertion():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')        

        self.Ensembl_gene=config.get('Convert','Ensembl_gene')
        self.Ensembl_transcript=config.get('Convert','Ensembl_transcript')
        self.Ensembl_protein=config.get('Convert','Ensembl_protein')
        
        self.UniGene=config.get('Convert','UniGene')

        self.GenBank_transcript=config.get('Convert','GenBank_transcript')
        self.RefSeq_transcript=config.get('Convert','RefSeq_transcript')
        self.GenBank_protein=config.get('Convert','GenBank_protein')
        self.RefSeq_protein=config.get('Convert','RefSeq_protein')
        self.GI_transcript=config.get('Convert','GI_transcript')
        self.GI_protein=config.get('Convert','GI_protein')

        self.Info=config.get('Convert', 'Info')

        self.GPL=config.get('Convert','GPL')

        self.Homologene=config.get('Convert','Homologene')

        self.Vega_gene=config.get('Convert','Vega_gene')
        self.Vega_transcript=config.get('Convert','Vega_transcript')
        self.Vega_protein=config.get('Convert','Vega_protein')


        self.History=config.get('Convert','History')

        self.Swissprot=config.get('Convert', 'Swissprot')
        self.trEMBL=config.get('Convert', 'trEMBL')

        self.size=100000

        self.logger=None
        self.formatter=None
        self.file_handler=None

        self.init_log()

    def file_exist(self, filepath):
        return os.path.isfile(filepath)
            
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

    def push_Ensembl_gene(self):
        
        if self.file_exist(self.Ensembl_gene):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Ensembl_gene --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Ensembl_gene ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Ensembl_gene")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - Ensembl_gene")
            self.logger.warning("Ensembl_gene file has not been found")

    def push_Ensembl_transcript(self):
        
        if self.file_exist(self.Ensembl_transcript):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Ensembl_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Ensembl_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Ensembl_transcript")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - Ensembl_transcript")
            self.logger.warning("Ensembl_transcript file has not been found")
            
    def push_Ensembl_protein(self):
        
        if self.file_exist(self.Ensembl_transcript):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Ensembl_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Ensembl_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Ensembl_protein")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - Ensembl_protein")
            self.logger.warning("Ensembl_protein file has not been found")

    def push_UniGene(self):
        
        if self.file_exist(self.UniGene):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c UniGene --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.UniGene ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - UniGene")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - UniGene")
            self.logger.warning("UniGene file has not been found")


    def push_GenBank_transcript(self):
        
        if self.file_exist(self.GenBank_transcript):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GenBank_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GenBank_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GenBank_transcript")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - GenBank_transcript")
            self.logger.warning("GenBank_transcript file has not been found")


    def push_RefSeq_transcript(self):
        
        if self.file_exist(self.RefSeq_transcript):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c RefSeq_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.RefSeq_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - RefSeq_transcript")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - GenBank_transcript")
            self.logger.warning("RefSeq_transcript file has not been found")

    def push_GenBank_protein(self):
        
        if self.file_exist(self.GenBank_protein):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GenBank_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GenBank_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GenBank_protein")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - GenBank_transcript")
            self.logger.warning("GenBank_protein file has not been found")

    def push_RefSeq_protein(self):
        
        if self.file_exist(self.RefSeq_protein):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c RefSeq_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.RefSeq_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - RefSeq_protein")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - RefSeq_protein")
            self.logger.warning("RefSeq_protein file has not been found")

    def push_GI_transcript(self):
        
        if self.file_exist(self.GI_transcript):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GI_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GI_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GI_transcript")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - RefSeq_protein")
            self.logger.warning("GI_transcript file has not been found")

    def push_GI_protein(self):
        
        if self.file_exist(self.GI_protein):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GI_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GI_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GI_protein")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - RefSeq_protein")
            self.logger.warning("GI_protein file has not been found")

    def push_Info(self):
        
        if self.file_exist(self.Info):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GeneInfo --type tsv --fields EGID.string\(\),TAXID.string\(\),SYMBOL.string\(\),DESCRIPTION.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Info ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GeneInfo")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - GeneInfo")
            self.logger.warning("GeneInfo file has not been found")
    
    def push_Homologene(self):
        
        if self.file_exist(self.Homologene):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c HomoloGene --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Homologene ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - HomoloGene")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - HomoloGene")
            self.logger.warning("HomoloGene file has not been found")

    def push_Vega_gene(self):
        
        if self.file_exist(self.Vega_gene):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Vega_gene --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Vega_gene ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Vega_gene")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - Vega_gene")
            self.logger.warning("Vega_gene file has not been found")
        
    def push_Vega_transcript(self):
        
        if self.file_exist(self.Vega_transcript):
            
            try:
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Vega_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Vega_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Vega_transcript")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - Vega_transcript")
            self.logger.warning("Vega_transcript file has not been found")

    def push_Vega_protein(self):
        
        if self.file_exist(self.Vega_protein):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Vega_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Vega_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Vega_protein")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - Vega_protein")
            self.logger.warning("Vega_protein file has not been found")            

insert = Insertion()

insert.push_Ensembl_gene()
insert.push_Ensembl_transcript()
insert.push_Ensembl_protein
insert.push_UniGene()
insert.push_GenBank_transcript()
insert.push_RefSeq_transcript()
insert.push_GenBank_protein()
insert.push_RefSeq_protein()
insert.push_GI_transcript()
insert.push_GI_protein()
insert.push_Info()
insert.push_GPL()
insert.push_Homologene()
insert.push_Vega_gene()
insert.push_Vega_transcript()
insert.push_Vega_protein()
insert.push_History()
insert.push_Swissprot()
insert.push_trEMBL()