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

from pymongo import MongoClient, ASCENDING

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

        self.Info=config.get('Convert', 'InfoWithHomologene')

        self.GPL=config.get('Convert','GPL')

        self.Homologene=config.get('Convert','Homologene')

        self.Vega_gene=config.get('Convert','Vega_gene')
        self.Vega_transcript=config.get('Convert','Vega_transcript')
        self.Vega_protein=config.get('Convert','Vega_protein')


        self.History=config.get('Convert','History')

        self.Swissprot=config.get('Convert', 'Swissprot')
        self.trEMBL=config.get('Convert', 'trEMBL')

        self.client = MongoClient()
        self.db = self.client["geneulike"]

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
                
                self.logger.warning("Error - insert.py - Ensembl_gene - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - Ensembl_gene - File not found")
            self.logger.warning("Ensembl_gene file has not been found")
        
        try:
            
            self.db['Ensembl_gene'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - Ensembl_gene - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())


    def push_Ensembl_transcript(self):
        
        if self.file_exist(self.Ensembl_transcript):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Ensembl_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Ensembl_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Ensembl_transcript - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - Ensembl_transcript - File not found")
            self.logger.warning("Ensembl_transcript file has not been found")
            
        try:
            
            self.db['Ensembl_transcript'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - Ensembl_transcript - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
        
    def push_Ensembl_protein(self):
        
        if self.file_exist(self.Ensembl_transcript):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Ensembl_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Ensembl_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Ensembl_protein - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - Ensembl_protein - File not found")
            self.logger.warning("Ensembl_protein file has not been found")

        try:
            
            self.db['Ensembl_protein'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - Ensembl_protein - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def push_UniGene(self):
        
        if self.file_exist(self.UniGene):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c UniGene --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.UniGene ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - UniGene - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - UniGene - File not found")
            self.logger.warning("UniGene file has not been found")

        try:
            
            self.db['UniGene'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - UniGene - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def push_GenBank_transcript(self):
        
        if self.file_exist(self.GenBank_transcript):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GenBank_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GenBank_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GenBank_transcript - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            self.logger.warning("Error - insertion.py - GenBank_transcript - File not found")
            self.logger.warning("GenBank_transcript file has not been found")

        try:
            
            self.db['GenBank_transcript'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - GenBank_transcript - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())


    def push_RefSeq_transcript(self):
        
        if self.file_exist(self.RefSeq_transcript):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c RefSeq_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.RefSeq_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - RefSeq_transcript - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - RefSeq_transcript - File not found")
            self.logger.warning("RefSeq_transcript file has not been found")
        
        try:
            
            self.db['RefSeq_transcript'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - RefSeq_transcript - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
            
    def push_GenBank_protein(self):
        
        if self.file_exist(self.GenBank_protein):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GenBank_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GenBank_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GenBank_protein - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - GenBank_transcript - File not found")
            self.logger.warning("GenBank_protein file has not been found")

        try:
            
            self.db['GenBank_protein'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - GenBank_protein - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def push_RefSeq_protein(self):
        
        if self.file_exist(self.RefSeq_protein):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c RefSeq_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.RefSeq_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - RefSeq_protein - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - RefSeq_protein - File not found")
            self.logger.warning("RefSeq_protein file has not been found")

        try:
            
            self.db['RefSeq_protein'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - RefSeq_protein - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
    def push_GI_transcript(self):
        
        if self.file_exist(self.GI_transcript):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GI_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GI_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GI_transcript - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - RefSeq_protein - File not found")
            self.logger.warning("GI_transcript file has not been found")

        try:
            
            self.db['GI_transcript'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - GI_transcript - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
    def push_GI_protein(self):
        
        if self.file_exist(self.GI_protein):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GI_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GI_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GI_protein - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - GI_protein - File not found")
            self.logger.warning("GI_protein file has not been found")
            
        try:
            
            self.db['GI_protein'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - GI_protein - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def push_Info(self):
        
        if self.file_exist(self.Info):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GeneInfo --type tsv --fields EGID.string\(\),TAXID.string\(\),SYMBOL.string\(\),DESCRIPTION.string\(\),HOMOLOGENE.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Info ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GeneInfo - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - GeneInfo - File not found")
            self.logger.warning("GeneInfo file has not been found")
        
        try:
            
            self.db['GeneInfo'].create_index([('EGID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - GeneInfo - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
    
    def push_GPL(self):
        
        if self.file_exist(self.GPL):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c GPL --type tsv --fields EGID.string\(\),BDID.string\(\),TAXID.string\(\),PLATFORM.string\(\),TITLE.string\(\),ORGANISM.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.GPL ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - GPL - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - GPL - File not found")
            self.logger.warning("GPL file has not been found")
        
        try:
            
            self.db['GPL'].create_index([('BDID', ASCENDING), ('PLATFORM', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - GPL - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
                
    
    def push_Homologene(self):
        
        if self.file_exist(self.Homologene):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c HomoloGene --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Homologene ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - HomoloGene - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - HomoloGene - File not found")
            self.logger.warning("HomoloGene file has not been found")
            
        try:
            
            self.db['HomoloGene'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - HomoloGene - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def push_Vega_gene(self):
        
        if self.file_exist(self.Vega_gene):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Vega_gene --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Vega_gene ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Vega_gene - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - Vega_gene - File not found")
            self.logger.warning("Vega_gene file has not been found")
        
        try:
            
            self.db['Vega_gene'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - Vega_gene - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
        
    def push_Vega_transcript(self):
        
        if self.file_exist(self.Vega_transcript):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Vega_transcript --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Vega_transcript ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Vega_transcript - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - Vega_transcript - File not found")
            self.logger.warning("Vega_transcript file has not been found")
        
        try:
            
            self.db['Vega_transcript'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - Vega_transcript - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def push_Vega_protein(self):
        
        if self.file_exist(self.Vega_protein):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c Vega_protein --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Vega_protein ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Vega_protein - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - Vega_protein File not found")
            self.logger.warning("Vega_protein file has not been found")
        
        try:
            
            self.db['Vega_protein'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - Vega_protein - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
    
    def push_History(self):
        
        if self.file_exist(self.History):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c History --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.History ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - History - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - History File not found")
            self.logger.warning("History file has not been found")
        
        try:
            
            self.db['History'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - History - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def push_Swissprot(self):
        
        if self.file_exist(self.History):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c UniProt --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.Swissprot ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - Swissprot - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - Swissprot - File not found")
            self.logger.warning("Swissprot file has not been found")
        
        try:
            
            self.db['UniProt'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - Swissprot - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
    
    def push_trEMBL(self):
        
        if self.file_exist(self.trEMBL):
            
            try:
                
                subprocess.check_output(['bash','-c',"mongoimport -d geneulike -c UniProt --type tsv --fields EGID.string\(\),BDID.string\(\) --columnsHaveTypes --numInsertionWorkers 8 --file " + self.trEMBL ])
            
            except subprocess.CalledProcessError as error:
                
                self.logger.warning("Error - insert.py - trEMBL - insertion")
            	self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            	self.logger.warning(sys.exc_info())
            	self.logger.warning(error)
             
        else:
            
            self.logger.warning("Error - insertion.py - trEMBL - File not found")
            self.logger.warning("Swissprot file has not been found")
        
        try:
            
            self.db['UniProt'].create_index([('BDID', ASCENDING)])
        
        except:
            
            self.logger.warning("Error - insert.py - trEMBL - createIndex")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
insert = Insertion()

#insert.push_Ensembl_gene()
#insert.push_Ensembl_transcript()
#insert.push_Ensembl_protein
#insert.push_UniGene()
#insert.push_GenBank_transcript()
#insert.push_RefSeq_transcript()
#insert.push_GenBank_protein()
#insert.push_RefSeq_protein()
#insert.push_GI_transcript()
#insert.push_GI_protein()
insert.push_Info()
#insert.push_GPL()
#insert.push_Homologene()
#insert.push_Vega_gene()
#insert.push_Vega_transcript()
#insert.push_Vega_protein()
#insert.push_History()
#insert.push_Swissprot()
#insert.push_trEMBL()
