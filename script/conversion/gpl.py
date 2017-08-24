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
        
        
        self.platform=str
        self.platform_title=str
        self.platform_organism=str
        
        
        self.header_platform="!Annotation_platform ="  
        self.header_platform_title="!Annotation_platform_title ="
        self.header_platform_organism="!Annotation_platform_organism ="    
        self.gpl_header_start = ('!','#','^')
                
        
        self.header_range=int
        
        
        self.size=1000000 #panda will read by chunksize here 1 million line by 1 million line

        # Store column index we need
        self.index_entrez = None
        self.index_probe_number = None


        self.dataframe = list        
        
        self.logger=None
        self.formatter=None
        self.file_handler=None
        

        self.path_exist()
        self.remove_finale_file()
        self.init_log()
        self.create_list_path_files()
        #self.create_index()
    
    def __str__(self):
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
    
    def afficher(self):
        print "{} : {} : {}".format(self.platform, self.platform_title, self.platform_organism)
        print "{} : {}" .format(self.index_entrez,self.index_probe_number)
        print "\n"

    def path_exist(self):
        """ Check if dir exist if not we create the path

        string = dir/subdir/subsubdir 
        string.rsplit('/',1)[0] 
        ==> return dir/subdir/ """
        
        if not os.path.isdir(self.gpl.rsplit('/',1)[0]):
            os.makedirs(self.gpl.rsplit('/', 1)[0])

    def remove_finale_file(self):
        
        if os.path.isfile(self.gpl):
            os.remove(self.gpl)
            
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
        
    def create_index(self, one_gpl_File):

        with open(one_gpl_File , 'r') as infile:
            
            header_line = next(infile)
            number_range=0
            organism = []
            while header_line.startswith(self.gpl_header_start, 0, 1):
                #print header_line.startswith(self.header_platform_organism) , " : ",header_line
                #print header_line.startswith(self.header_platform_title)
                #print "\n"
                if header_line.startswith(self.header_platform):
                    self.platform=str(header_line.split("= ")[1].split("\n")[0])
                    
                elif header_line.startswith(self.header_platform_title):
                    self.platform_title=str(header_line.split("= ")[1].split("\n")[0])
                
                elif header_line.startswith(self.header_platform_organism):
                    organism.append(str(header_line.split("= ")[1].split("\n")[0]))
                

                number_range += 1
                header_line=next(infile)
                
            self.platform_organism = ";".join(organism) 
            self.header_range = number_range
            
            header_line = header_line.split('\t')
            self.index_entrez = header_line.index('Gene ID')
            self.index_probe_number = header_line.index('ID')
        

    def getDataFromOneFile(self, fileToOpen, headerRange):
        
        try :
            self.dataframe =[]
            for df in pandas.read_csv(fileToOpen,skiprows=headerRange, header=0, sep="\t", usecols=[self.index_entrez, self.index_probe_number], dtype='str', chunksize=self.size):
                
                df.columns = ['EGID','BDID']
                
                
                """We can have 
                              EGID                                   BDID
                   0    1769308_at                                 853878
                   1    1769309_at                                2539804
                   2    1769310_at                                2539380
                   3    1769311_at                                 851398
                   4    1769312_at                                 856787
                   5    1769313_at                                 852821
                   6    1769314_at                                 852092
                   7    1769315_at                                2540239
                   8  1769316_s_at  2543353///2541576///2541564///2541343
                   
                   We want to split line 8 to obtain :
                   
                               EGID     BDID
                   0     1769308_at   853878
                   1     1769309_at  2539804
                   2     1769310_at  2539380
                   3     1769311_at   851398
                   4     1769312_at   856787
                   5     1769313_at   852821
                   6     1769314_at   852092
                   7     1769315_at  2540239
                   8   1769316_s_at  2543353
                   9   1769316_s_at  2541576
                   10  1769316_s_at  2541564
                   11  1769316_s_at  2541343
                  
                   So : 
                   
                   
                   df =df.set_index(df.columns.drop('BDID',2).tolist())\ 
                       #on supprime la colonne "BDID" dont l'axe est 2 et on la met dans une lsite
                   
                            .BDID.str.split('///', expand=True)\
                            .stack()\
                            .reset_index()\
                            .rename(columns={0:'BDID'})\
                            .loc[:, df.columns]
                  
                
                """
                
                df = df.set_index(df.columns.drop('BDID',2).tolist())\
                                 .BDID.str.split('///', expand=True)\
                                 .stack()\
                                 .reset_index()\
                                 .rename(columns={0:'BDID'})\
                                 .loc[:, df.columns]
    
                df["Platform"]=pandas.Series([self.platform for x in range(len(df.index))])
                df["Platform_title"]=pandas.Series([self.platform_title for x in range(len(df.index))])  
                df["Platform_organism"]=pandas.Series([self.platform_organism for x in range(len(df.index))])  
                               
                
                self.dataframe.append(df)
                
        except:
            
            self.logger.warning("Error - gpl.py - getDataFromOneFile" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
                #self.platform=str
        #self.platform_title=str
        #self.platform_organism=str
    
    def writeFile(self):
        
        try:
            
            pandas.concat(self.dataframe).drop_duplicates(['EGID', 'BDID', "Platform", "Platform_title", "Platform_organism"], keep='first').to_csv(self.filename_gpl, header=None, index=None, sep='\t', mode='a')
        
        except:
            
            self.logger.warning("Error - gpl.py - writeFile" )
            self.logger.warning("Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno))
            self.logger.warning(sys.exc_info())
            
    def getGPL(self):
        
        for pathFile in self.list_path_files:
            self.create_index(pathFile)
            self.getDataFromOneFile(pathFile, self.header_range)
            self.writeFile()
            

                    

test = GPL()
test.getGPL()


