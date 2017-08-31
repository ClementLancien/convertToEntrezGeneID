# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 17:51:26 2017

@author: clancien
"""

try:
	import ConfigParser

except ImportError:

	import configparser as ConfigParser

import os


import logging
from logging.handlers import RotatingFileHandler
import sys

__all__ = ['TREMBL']

class TREMBL():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')
        
        self.trembl = config.get('Download', 'gene2trembl')
        self.protein = config.get('Convert', 'trEMBL')        
        
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
        
        if not os.path.isdir(self.protein.rsplit('/',1)[0]):
            os.makedirs(self.protein.rsplit('/', 1)[0])

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
        
    def get_trEMBL(self):
        
        try:
            
            with open(self.trembl,'r') as inputFile,\
            open(self.protein, 'w') as outputFile:
                
                ID=""
                AC=[]
                
                for line in inputFile:
                    
                    if("AC" in line[:2]):
                        newLine=line[5:].split("; ")
                        for ac in newLine:
                            AC.append(ac)
                            
                    if("GeneID" in line and "DR" in line):
                        newLine=line[5:].split("; ")
                        ID=newLine[1]
                        
                    if("//" in line):
                        
                        if (ID != ""):
                            
                            for ac in AC:
                                outputFile.write(str(ID) + "\t" + str(ac.split(";")[0]) + "\n")
                        ID=""
                        AC=[]

        except:
            
            self.logger.warning("Error - trembl.py - gettrEMBL ")
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())



if __name__ == '__main__': 
       
    TREMBL().get_trEMBL()
