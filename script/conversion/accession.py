# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:15:47 2017

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

__all__ = ['Accession']
            
class Accession():
    
    
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')        
        
        self.accession = config.get('Download', 'gene2accession')
        self.GenBank_transcript = config.get('Convert', 'GenBank_transcript')
        self.GenBank_protein = config.get('Convert', 'GenBank_protein')
        self.RefSeq_transcript = config.get('Convert', 'RefSeq_transcript')
        self.RefSeq_protein = config.get('Convert', 'RefSeq_protein')
        self.GI_transcript = config.get('Convert', 'GI_transcript')
        self.GI_protein = config.get('Convert', 'GI_protein')
        
        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string
        
        self.filename_accession = str(self.accession)
        self.filename_GenBank_transcript = str(self.GenBank_transcript)
        self.filename_GenBank_protein = str(self.GenBank_protein)
        self.filename_RefSeq_transcript = str(self.RefSeq_transcript)
        self.filename_RefSeq_protein = str(self.RefSeq_protein)
        self.filename_GI_transcript = str(self.GI_transcript)
        self.filename_GI_protein = str(self.GI_protein)
        
        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line
        
        self.index_entrez = None
        self.index_GenBank_transcript = None
        self.index_GenBank_protein = None
        self.index_RefSeq_transcript = None
        self.index_RefSeq_protein = None
        self.index_GI_transcript = None
        self.index_GI_protein = None
        
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
        
        if not os.path.isdir(self.GenBank_transcript.rsplit('/',1)[0]):
            os.makedirs(self.GenBank_transcript.rsplit('/', 1)[0])

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

        with open(self.filename_accession , 'r') as infile:

            header_line = next(infile)
            header_line = header_line.split('\t')
                
            self.index_entrez = header_line.index('GeneID')
            self.index_GenBank_transcript = header_line.index('RNA_nucleotide_accession.version')
            self.index_GenBank_protein = header_line.index('protein_accession.version')
            self.index_RefSeq_transcript = header_line.index('RNA_nucleotide_accession.version')
            self.index_RefSeq_protein = header_line.index('protein_accession.version')
            self.index_GI_transcript = header_line.index('RNA_nucleotide_gi')
            self.index_GI_protein = header_line.index('protein_gi')
    
    
    def get_GenBank_transcript(self):
        
        # ~False = true
        try:
            
            self.dataframe=[]
           
            for df in pandas.read_csv(self.filename_accession, header=0, sep="\t", usecols=[self.index_entrez,self.index_GenBank_transcript], dtype='str', chunksize=self.size):

                df.columns = ['EGID','BDID']
                #df['EGID'] = df['EGID'].astype(str)
                #df['BDID'] = df['BDID'].astype(str)
                df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
               
                
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE))  &
                                            (df['BDID'] != '-') &
                                            (~df['BDID'].str.match('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE))
                                            
                                        ])
        except:
            
            self.logger.warning("Error - accession.py - GenBank_transcript - loop over file" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_GenBank_transcript, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - accession.py - GenBank_transcript - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info())
            
    def get_GenBank_protein(self):
        
        # ~False = true
        try:
            
            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_accession, header=0,sep="\t", usecols=[self.index_entrez,self.index_GenBank_protein], dtype='str', chunksize=self.size):

                df.columns = ['EGID','BDID']
                #df['EGID'] = df['EGID'].astype(str)
               # df['BDID'] = df['BDID'].astype(str)
                df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
                #df =df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=False, na=False)]
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE)) &
                                            (df['BDID'] != '-') &
                                            (~df['BDID'].str.match('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE))
                                            
                                        ])
        
        except:
            
            self.logger.warning("Error - accession.py - GenBank_protein - loop over file" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_GenBank_protein, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - accession.py - GenBank_protein - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info()) 
         
    def get_RefSeq_transcript(self):
        
        try:
            
            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_accession, header=0, sep="\t", usecols=[self.index_entrez,self.index_RefSeq_transcript], dtype='str', chunksize=self.size):

                df.columns = ['EGID','BDID']
                #df['EGID'] = df['EGID'].astype(str)
                #df['BDID'] = df['BDID'].astype(str)
                df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE)) &
                                            (df['BDID'].str.match('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE))
                                            
                                        ])
        
        except:
            
            self.logger.warning("Error - accession.py - RefSeq_transcript - loop over file" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else: 
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_RefSeq_transcript, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - accession.py - RefSeq_transcript - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info())    
  
    def get_RefSeq_protein(self):
        
        try:
            
            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_accession, header=0,sep="\t", usecols=[self.index_entrez,self.index_RefSeq_protein], dtype='str', chunksize=self.size):

                 df.columns = ['EGID','BDID']
                 #df['EGID'] = df['EGID'].astype(str)
                 #df['BDID'] = df['BDID'].astype(str)
                 df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
                 self.dataframe.append(df[
                                             (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE)) &
                                             (df['BDID'].str.match('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE))
                                             
                                        ])
        
        except:
            
            self.logger.warning("Error - accession.py - RefSeq_protein - loop over file" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_RefSeq_protein, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - accession.py - RefSeq_protein - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info())  

    def get_GI_transcript(self):
        
        try:
            
            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_accession, header=0, sep="\t", usecols=[self.index_entrez,self.index_GI_transcript], dtype='str', chunksize=self.size):
                
                df.columns = ['EGID','BDID']# ~False = true
                #df['EGID'] = df['EGID'].astype(str)
                #df['BDID'] = df['BDID'].astype(str)
                df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE))  &
                                            (df['BDID'].str.match('^[0-9]+$', flags=re.IGNORECASE))
                                            
                                        ])
        except:
            
            self.logger.warning("Error - accession.py - GI_transcript - loop over file" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_GI_transcript, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - accession.py - GI_transcript - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info())  

    def get_GI_protein(self):
        
        try:
            
            self.dataframe=[]
            
            for df in pandas.read_csv(self.filename_accession, header=0, sep="\t", usecols=[self.index_entrez,self.index_GI_protein], dtype='str', chunksize=self.size):
                
                df.columns = ['EGID','BDID']
                #df['EGID'] = df['EGID'].astype(str)
                #df['BDID'] = df['BDID'].astype(str)
                df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')
                self.dataframe.append(df[
                                            (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE)) &
                                            (df['BDID'].str.match('^[0-9]+$', flags=re.IGNORECASE))
                                            
                                        ])
        
        except:
            
            self.logger.warning("Error - accession.py - GI_protein - loop over file" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
            
        else:
            
            try:
            
                pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(self.filename_GI_protein, header=None, index=None, sep='\t', mode='w')
        
            except:
            
                self.logger.warning("Error - accession.py - GI_protein - write File")
                self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
                self.logger.warning(sys.exc_info())  




if __name__ == '__main__':
    
    Accession().get_GenBank_transcript()
    Accession().get_GenBank_protein()
    Accession().get_RefSeq_transcript()
    Accession().get_RefSeq_protein()
    Accession().get_GI_transcript()
    Accession().get_GI_protein()
        
#accession = Accession()
#print "getGenBank_transcript"
#accession.get_GenBank_transcript()
#print "getGenBank_protein"
#Accession().get_GenBank_protein()
#print "getRefSeq_transcript"
#Accession().get_RefSeq_transcript()
#print "getRefSeq_protein"
#
#print "getGI_transcript"
#Accession().get_GI_transcript()
#print "getGI_protein"
#Accession().get_GI_protein()
