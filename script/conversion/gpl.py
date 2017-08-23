# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:32:07 2017

@author: clancien
"""

import ConfigParser
import os
import pandas
import glob
import logging
from logging.handlers import RotatingFileHandler
import sys

class GPL():
    
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))
        
        self.logFile = config.get('Error', 'logFile')
        
        self.path= config.get('Download', 'gene2gpl')
        self.gpl=config.get('Convert', 'GPL')
        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string
        
        self.filepath= str(self.path)
        self.filename_gpl=str(self.gpl)
        
        self.list_path_files=list
        self.platform_name=str
        
        self.header_range=int
        
        self.header_platform="!Annotation_platform"        
        self.gpl_header_start = ('!','#','^')
        
        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line

        # Store column index we need
        self.index_entrez = None
        self.index_gene = None
        self.index_transcript = None
        self.index_protein = None

        self.dataframe = list        
        
        self.logger=None
        self.formatter=None
        self.file_handler=None
        

        self.path_exist()
        self.init_log()
        self.create_list_path_files()
        #self.create_index()
    
    def __repr__(self):
        #0336
        #02EA
        _list= [
                    #"{}".format("list_path_files"),
                    #"\n".join([u'\t\u02EA '+ "{}".format(path) for path in self.list_path_files]).encode('utf-8'),
                    "{}\n{}".format("list_path_files", "\n".join([u'\t\u02EA '+ "{}".format(path) for path in self.list_path_files]).encode('utf-8')),
                    "{} : {}".format("filename_gpl", self.filename_gpl),
                    "{} : {}".format("platform", self.platform),
                    "{} : {}".format("size", self.size),
                    "{} : {}".format("index_entrez", self.index_entrez),
                    "{} : {}".format("index_entrez", self.index_entrez),
                    "{} : {}".format("index_entrez", self.index_entrez),
                    "{} : {}".format("index_entrez", self.index_entrez),



               ]
        return "\n\n".join(_list)
        #return "\n".join([u'\t\u02EA '+ "{}".format(path) for path in self.list_path_files[1:]]).encode('utf-8')
        #return "{:^10}".format(*self.list_path_files)
        
    def path_exist(self):
        """ Check if dir exist if not we create the path

        string = dir/subdir/subsubdir 
        string.rsplit('/',1)[0] 
        ==> return dir/subdir/ """
        
        if not os.path.isdir(self.gpl.rsplit('/',1)[0]):
            os.makedirs(self.gpl.rsplit('/', 1)[0])

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
        
    def create_list_path_files(self):
        
        self.list_path_files = glob.glob(self.filepath + '*.annot' )
        #print self.list_path_files
        
    def create_index(self):

        with open(self.filename_ensembl , 'r') as infile:
            
            header_line = next(infile)
            number_range=0
            while header_line.startwith(self.gpl_header_start, 0, 1):
                if header_line.startwith(self.header_platform, 0, len(self.gpl_header_start)):
                    self.platform=str(header_line.split("= ")[1].split("\n")[0])
                number_range += 1
                header_line=next(infile)
                
            self.header_range = number_range
            
            header_line = header_line.split('\t')
            
            self.index_entrez = header_line.index('GeneID')
            self.index_gene = header_line.index('Ensembl_gene_identifier')
            self.index_transcript = header_line.index('Ensembl_rna_identifier')
            self.index_protein = header_line.index('Ensembl_protein_identifier\n')
        
        self.header_range
        self.platform
        
    def getGPL(self, filename_one_gpl):

        try:
            
            self.dataframe=[]
            header_range, self.platform = self.create_index(filename_one_gpl)
           
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
            print "toto"
    
#print GPL()
_str = "!Annotation_platform = GPL1225"
print len("!Annotation_platform")
print _str.startswith( "!Annotation_platform", 0, 20  )
print _str.startswith( ('!','#','^'), 0, 1 )

#print u'\u02EA' +'\t'+ 'a'


