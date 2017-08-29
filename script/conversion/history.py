# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:25:48 2017

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

__all__ = ['History']


class History():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')        
        
        self.history = config.get('Download', 'gene2history')
        self.gene = config.get('Convert', 'History')
        
        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string
        
        self.filename_history = str(self.history)
        self.filename_gene = str(self.gene)
        
        
        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line
        
        #No header in homologene file (raw data)
        self.index_entrez = None
        self.index_history = None

        
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

        with open(self.filename_history , 'r') as infile:

            header_line = next(infile)

            header_line = header_line.split('\t')
            
            self.index_entrez = header_line.index('GeneID')
            self.index_history = header_line.index('Discontinued_GeneID')

    def getData(self):
        
        try:
            
            self.dataframe=[]
            print self.index_entrez
            for df in pandas.read_csv(self.filename_history, header=0, sep="\t", usecols=[self.index_entrez, self.index_history], dtype='str', chunksize=self.size):
                #df.to_string()
                print df
                return 
                df.columns = ['EGID','BDID']
                
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$'))  &
                                            (df['BDID'].str.match('^[0-9]+$'))
                                            
                                        ])

        except:
            
            self.logger.warning("Error - history.py - getData")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
    
    def writeFile(self):
        
        try:
            
            pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_gene, header=None, index=None, sep='\t', mode='w')

        except:
            
            self.logger.warning("Error - history.py - writeFile ")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
    def get_History(self):
        
        self.getData()
        self.writeFile()           

#if __name__ == '__main__':

#    History().get_History()
