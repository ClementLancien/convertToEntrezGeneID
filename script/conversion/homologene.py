# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 14:54:46 2017

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

class Homologene():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')        
        
        self.homologene = config.get('Download', 'gene2homologene')
        self.gene = config.get('Convert', 'Homologene')
        
        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string
        
        self.filename_homologene = str(self.homologene)
        self.filename_gene = str(self.gene)
        
        
        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line
        
        #No header in homologene file (raw data)
        self.index_entrez = 2
        self.index_homologene = 0

        
        self.dataframe = list
        
        self.logger=None
        self.formatter=None
        self.file_handler=None
        #GeneID UniGene_cluster
        
        self.path_exist()
        self.init_log()

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


    def getData(self):
        
        try:
            
            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_homologene, header=0, sep="\t", usecols=[self.index_entrez, self.index_homologene], dtype='str', chunksize=self.size):
                #df.to_string()
                df.columns = ['BDID', 'EGID']
                df = df[['EGID', 'BDID']]
                
                #df["EGID"]= df["EGID"].astype(str)

                self.dataframe.append(
                    df[
                        (df['EGID'] != '-') &
                        (df['BDID'] != '-')
                    ]
                    )

        except:
            
            self.logger.warning("Error - homologene.py - getData")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
    
    def writeFile(self):
        
        try:
            
            pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_gene, header=None, index=None, sep='\t', mode='w')

        except:
            
            self.logger.warning("Error - homologene.py - writeFile")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
    def get_Homologene(self):
        
        self.getData()
        self.writeFile()
        
if __name__ == '__main__':
    
    Homologene().get_Homologene()
