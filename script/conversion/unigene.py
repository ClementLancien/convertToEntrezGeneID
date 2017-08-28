# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:20:41 2017

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

class Unigene():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')
        self.unigene = config.get('Download', 'gene2unigene')
        self.gene = config.get('Convert', 'UniGene')
        
        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string
        
        self.filename_unigene = str(self.unigene)
        self.filename_gene = str(self.gene)
        
        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line
        
        self.index_entrez = None
        self.index_gene = None
        
        self.dataframe = list
        self.finalDataFrame=None
        
        
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

        with open(self.unigene , 'r') as infile:

            header_line = next(infile)
            header_line = header_line.split('\t')
            
            self.index_entrez = header_line.index('#GeneID')
            self.index_gene = header_line.index('UniGene_cluster\n')

    def getData(self):

        try:

            self.dataframe=[]

            for df in pandas.read_csv(self.filename_unigene, header=0, sep="\t", usecols=[self.index_entrez, self.index_gene], dtype='str', chunksize=self.size):
                #df.to_string()
                df.columns = ['EGID','BDID']
                
                #df["EGID"]= df["EGID"].astype(str)

                self.dataframe.append(
                    df[
                        (df['EGID'] != '-') &
                        (df['BDID'] != '-')
                    ]
                    )
                #OR 
                #    self.dataFrame.append(
                #         df[
                #               (df['EGID'].str.contains('[0-9]+$', flags=re.IGNORECASE, regex=True, na=False)) & 
                #               (df['BDID'].str.contains('^[a-zA-Z]{2,3}[.]([0-9]*)$', flags=re.IGNORECASE, regex=True, na=False))
                #           ]
                #better to use str.match()
        except:
            
            self.logger.warning("Error - unigene.py - getData")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())           

    
    def delDoublonInDataframe(self):

        try:

            self.finalDataFrame = pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first')

        except:
            
            self.logger.warning("Error - unigene.py - delDoublonInDataframe - UniGene_cluster")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def writeFile(self):

        try:
            self.finalDataFrame.to_csv(self.filename_gene, header=None, index=None, sep='\t', mode='w')

        except:
            
            self.logger.warning("Error - unigene.py - writeFile")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())


    def convertToGene(self):

        self.getData()
        self.delDoublonInDataframe()
        self.writeFile()
        

Unigene().convertToGene()
