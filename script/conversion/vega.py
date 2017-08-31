# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:31:03 2017

@author: clancien
"""

try:
	import ConfigParser

except ImportError:

	import configparser as ConfigParser

import os
import pandas
import re

import logging
from logging.handlers import RotatingFileHandler
import sys

__all__=['Vega']

class Vega():

    def __init__(self):

        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))

        self.logFile = config.get('Error', 'logFile')
        self.vega = config.get('Download', 'gene2vega')
        self.gene = config.get('Convert', 'Vega_gene')
        self.transcript = config.get('Convert', 'Vega_transcript')
        self.protein = config.get('Convert', 'Vega_protein')

        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string

        self.filename_vega = str(self.vega)
        self.filename_gene = str(self.gene)
        self.filename_transcript = str(self.transcript)
        self.filename_protein = str(self.protein)

        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line

        # Store column index we need
        self.index_entrez = None
        self.index_gene = None
        self.index_transcript = None
        self.index_protein = None

        self.dataframe = list
        self.finalDataFrame=None
        
        
        self.logger=None
        self.formatter=None
        self.file_handler=None
        
        
        self.path_exist()
        self.init_log()
        self.create_index()


    def path_exist(self):
        """ Check if dir exist if not we create the path

        string = dir/subdir/subsubdir 
        string.rsplit('/',1)[0] 
        ==> return dir/subdir/ """
        
        if not os.path.isdir(self.gene.rsplit('/',1)[0]):
            os.makedirs(self.gene.rsplit('/', 1)[0])

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

        with open(self.filename_vega , 'r') as infile:

            header_line = next(infile)
            header_line = header_line.split('\t')

            self.index_entrez = header_line.index('GeneID')
            self.index_gene = header_line.index('Vega_gene_identifier')
            self.index_transcript = header_line.index('Vega_rna_identifier')
            self.index_protein = header_line.index('Vega_protein_identifier\n')
                 
    def get_Gene(self):

        try:

            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_vega, header=0, sep="\t", usecols=[self.index_entrez, self.index_gene], dtype='str', chunksize=self.size):

                df.columns = ['EGID','BDID']
            
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE))  &
                                            (df['BDID'].str.match('^[O][T][T][D][A][R][G]([0-9]+)$', flags=re.IGNORECASE))
                                            
                                        ])                                 
        except:
            
            self.logger.warning("Error - vega.py - getVega_gene - loop over file")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_gene, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - vega.py - getVega_gene - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))

    def get_Transcript(self):

        try:

            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_vega, header=0, sep="\t", usecols=[self.index_entrez, self.index_transcript], dtype='str', chunksize=self.size):

                df.columns = ['EGID','BDID']
            
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE))  &
                                            (df['BDID'].str.match('^[O][T][T][D][A][R][T]([0-9]+)$', flags=re.IGNORECASE))
                                            
                                        ])
                                        
        except:
            
            self.logger.warning("Error - vega.py - getVega_transcript - loop over file")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_transcript, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - vega.py - getVega_transcript - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))

    def get_Protein(self):

        try:

            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_vega, header=0, sep="\t", usecols=[self.index_entrez, self.index_protein], dtype='str', chunksize=self.size):

                df.columns = ['EGID','BDID']
            
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE))  &
                                            (df['BDID'].str.match('^[O][T][T][D][A][R][P]([0-9]+)$', flags=re.IGNORECASE))
                                            
                                        ])                
        except:
            
            self.logger.warning("Error - vega.py - getVega_protein - loop over file")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_protein, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - vega.py - getVega_protein - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))

if __name__ == '__main__':
    
    Vega().get_Gene()
    Vega().get_Transcript()
    Vega().get_Protein

