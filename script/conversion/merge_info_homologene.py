# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 13:35:08 2017

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

__all__ = ['InfoWithHomologene']


class InfoWithHomologene():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')
        
        self.info=config.get('Convert', 'Info')
        self.homologene=config.get('Convert', 'Homologene')
        self.info_with_homologene=config.get('Convert','InfoWithHomologene')
        
        
        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string
        
        self.filename_info = str(self.info)
        self.filename_homologene = str(self.homologene)
        self.filename_info_with_homologene = str(self.info_with_homologene)
        
        
        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line
        
        self.dataframe_homologene=None
        self.dataframe=None
        
        self.logger=None
        self.formatter=None
        self.file_handler=None
        
        self.init_log()
        
    def files_exist(self):
        
        if not os.path.isfile(self.info):
            self.logger.warning("Error - merge_Info_With_Homologene.py - files_exist - loop over file" )
            self.logger.warning("Can't find "+ self.filename_info)
            return False
        
        if not os.path.isfile(self.homologene):
            self.logger.warning("Error - merge_Info_With_Homologene.py - files_exist - loop over file" )
            self.logger.warning("Can't find "+ self.filename_homologene)
            return False

        return True
    
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
    
    def get_detaframe_homologene(self):
        
        if self.files_exist():
            
            try:
                
                homologene=[]
                
                for df in pandas.read_csv(self.filename_homologene, header=None, usecols=[0,1], sep="\t", dtype='str', chunksize=self.size):

                    df.columns = ['EGID','BDID']
                    homologene.append(df)
                    
                self.dataframe_homologene =  pandas.concat(homologene)
                
            except:
                
                self.logger.warning("Error - merge_Info_With_Homologene.py - get_detaframe_homologene")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info())
    
    def merge_info_homologene(self):
        
        if self.files_exist():
            
            try:
                self.dataframe=[]
                for df in pandas.read_csv(self.filename_info, header=None, usecols=[0,1,2,3], sep="\t", dtype='str', chunksize=self.size):
                    
                    df.columns = ['EGID','TAXID','SYMBOL','DESCRIPTION']

                    self.dataframe.append(df.merge(self.dataframe_homologene, how ='left', left_on='EGID', right_on='EGID').fillna('-'))
            
            except:
                
                self.logger.warning("Error - merge_Info_With_Homologene.py - merge_info_homologene - merge function")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info())
            
            else:
                
                try:
            
                    pandas.concat(self.dataframe).to_csv(self.filename_info_with_homologene, header=None, index=None, sep='\t', mode='w')
        
                except:
            
                    self.logger.warning("Error - accession.py - merge_info_homologene - write File")
                    self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                    self.logger.warning(sys.exc_info()) 
                    
    def get_Info_With_Homologene(self):
        
        self.get_detaframe_homologene()
        self.merge_info_homologene()
        
if __name__ == '__main__':        

    InfoWithHomologene().get_Info_With_Homologene()
              