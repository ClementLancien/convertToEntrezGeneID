# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 16:42:44 2017

@author: clancien
"""

try:
	import ConfigParser

except ImportError:

	import configparser as ConfigParser

import os
import pandas

import logging
from logging.handlers import RotatingFileHandler
import sys

class Info():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')
        
        self.gene2info = config.get('Download', 'gene2info')
        self.info = config.get('Convert', 'Info')
        
        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string
        
        self.filename_gene2info = str(self.gene2info)
        self.filename_info = str(self.info)
        
        
        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line
        
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
        
        if not os.path.isdir(self.filename_info.rsplit('/',1)[0]):
            os.makedirs(self.filename_info.rsplit('/', 1)[0])

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

        with open(self.filename_gene2info , 'r') as infile:

            header_line = next(infile)

            header_line = header_line.split('\t')

            self.index_entrez = header_line.index('GeneID')
            self.index_tax_id = header_line.index('#tax_id')
            self.index_symbol = header_line.index('Symbol')
            self.index_description = header_line.index('description')
            
    def get_Info(self):
        
        # ~False = true
        try:
            
            self.dataframe=[]
           
            for df in pandas.read_csv(self.filename_gene2info ,header=0, sep="\t", usecols=[self.index_entrez, self.index_tax_id, self.index_symbol, self.index_description], dtype='str', chunksize=self.size):
                               
                df.columns = ['TAXID', 'EGID', 'SYMBOL', 'DESCRIPTION']
                
                df = df[['EGID','TAXID', 'SYMBOL', 'DESCRIPTION']]
                #df['EGID'] = df['EGID'].astype(str)
                #df['TAXID'] = df['TAXID'].astype(str)
                #df['SYMBOL'] = df['SYMBOL'].astype(str)
                #df['DESCRIPTION'] = df['DESCRIPTION'].astype(str)
                
                self.dataframe.append(df)
                
        except:
            
            self.logger.warning("Error - info.py - getInfo - loop over file" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID','TAXID', 'SYMBOL', 'DESCRIPTION'], keep='first').to_csv(self.filename_info, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - info.py - getInfo - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info())       

if __name__ == '__main__':
    
    Info().get_Info()
