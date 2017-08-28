# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:48:42 2017

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

class Ensembl():

    def __init__(self):

        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))

        self.logFile = config.get('Error', 'logFile')
        self.ensembl = config.get('Download', 'gene2ensembl')
        self.gene = config.get('Convert', 'Ensembl_gene')
        self.transcript = config.get('Convert', 'Ensembl_transcript')
        self.protein = config.get('Convert', 'Ensembl_protein')

        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string

        self.filename_ensembl = str(self.ensembl)
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

        with open(self.filename_ensembl , 'r') as infile:

            header_line = next(infile)
            header_line = header_line.split('\t')

            self.index_entrez = header_line.index('GeneID')
            self.index_gene = header_line.index('Ensembl_gene_identifier')
            self.index_transcript = header_line.index('Ensembl_rna_identifier')
            self.index_protein = header_line.index('Ensembl_protein_identifier\n')
            
    def getColByIndex(self, index_column):
        
        if self.index_gene == index_column:
            return 'Ensembl_gene'
            
        elif self.index_transcript == index_column:
            return 'Ensembl_transcript'
        
        else:
            return 'Ensembl_protein'
            
    def getData(self, index_column):

        try:

            self.dataFrame=[]

            for df in pandas.read_csv(self.filename_ensembl, header=0, sep="\t", usecols=[self.index_entrez, index_column], dtype='str', chunksize=self.size):
                #df.to_string()
                df.columns = ['EGID','BDID']
                
                #df["EGID"]= df["EGID"].astype(str)
                df['BDID'] = df['BDID'].str.replace('[.][0-9]+','') #del versionning

                self.dataFrame.append(
                    df[
                        (df['EGID'] != '-') &
                        (df['BDID'] != '-')
                    ]
                    )
                #OR 
                #    self.dataFrame.append(
                #         df[
                #               (df['EGID'].str.contains('[0-9]+$', flags=re.IGNORECASE, regex=True, na=False)) & 
                #               (df['BDID'].str.contains('^[A-Z]', flags=re.IGNORECASE, regex=True, na=False))
                #           ]
                #
        except:
            
            self.logger.warning("Error - ensembl.py - getData - " + self.getColByIndex(index_column))
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def delDoublonInDataframe(self, index_column):

        try:

            self.finalDataFrame = pandas.concat(self.dataFrame).drop_duplicates(['EGID', 'BDID'], keep='first')

        except:
            
            self.logger.warning("Error - ensembl.py - delDoublonInDataframe - " + self.getColByIndex(index_column))
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def writeFile(self, filename):

        try:
            self.finalDataFrame.to_csv(filename, header=None, index=None, sep='\t', mode='w')

        except:
            
            self.logger.warning("Error - ensembl.py - writeFile - " + filename)
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())

    def convertToGene(self):

        self.getData(self.index_gene)
        self.delDoublonInDataframe(self.index_gene)
        self.writeFile(self.filename_gene)

    def convertToTranscript(self):

        self.getData(self.index_transcript)
        self.delDoublonInDataframe(self.index_transcript)
        self.writeFile(self.filename_transcript)

    def convertToProtein(self):

        self.getData(self.index_protein)
        self.delDoublonInDataframe(self.index_protein)
        self.writeFile(self.filename_protein)

ensembl_file= Ensembl()
ensembl_file.convertToGene()
ensembl_file.convertToTranscript()
ensembl_file.convertToProtein()
