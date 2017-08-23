# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:01:06 2017

@author: clancien
"""

import os # nééd to use to make a path 
import ftplib 
import gzip
import StringIO
import urllib2
import subprocess
import ConfigParser
import logging
from logging.handlers import RotatingFileHandler
import sys

class Download():

    def __init__(self):

        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))

        ##### Path variable (to store document) 
        self.ensembl=config.get('DownloadRAW', 'gene2ensembl')
        self.unigene=config.get('DownloadRAW', 'gene2unigene')

        self.accession=config.get('DownloadRAW', 'gene2accession')
        self.info=config.get('DownloadRAW', 'gene2info')
        self.gpl=config.get('DownloadRAW', 'gene2gpl')
        self.homologene =config.get('DownloadRAW', 'gene2homologene')
        self.vega=config.get('DownloadRAW', 'gene2vega')
        self.history =config.get('DownloadRAW', 'gene2history') #gene2gene
        self.swissprot=config.get('DownloadRAW', 'gene2swissprot')
        self.trembl=config.get('DownloadRAW', 'gene2trembl')
        self.logFile = config.get('Error', 'logFile')


        self.logger=None
        self.formatter=None
        self.file_handler=None

        
        self.path_exist()
        self.init_log()
        
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
        
    def path_exist(self):
        """ Check if dir exist if not we create the path

        string = dir/subdir/subsubdir 
        string.rsplit('/',1)[0] 
        ==> return dir/subdir/ """
        
        if not os.path.isdir(self.ensembl.rsplit('/',1)[0]):
            os.makedirs(self.ensembl.rsplit('/', 1)[0])
        
        if not os.path.isdir(self.unigene.rsplit('/',1)[0]):
            os.makedirs(self.unigene.rsplit('/', 1)[0])
            
        if not os.path.isdir(self.accession.rsplit('/',1)[0]):
            os.makedirs(self.accession.rsplit('/', 1)[0])
        
        if not os.path.isdir(self.info.rsplit('/',1)[0]):
            os.makedirs(self.info.rsplit('/', 1)[0])
        
        if not os.path.isdir(self.gpl.rsplit('/',1)[0]):
            os.makedirs(self.gpl.rsplit('/', 1)[0])
              
        if not os.path.isdir(self.homologene.rsplit('/',1)[0]):
            os.makedirs(self.homologene.rsplit('/', 1)[0])
            
        if not os.path.isdir(self.vega.rsplit('/',1)[0]):
            os.makedirs(self.vega.rsplit('/', 1)[0])
            
        if not os.path.isdir(self.history.rsplit('/',1)[0]):
            os.makedirs(self.history.rsplit('/', 1)[0])
            
        if not os.path.isdir(self.swissprot.rsplit('/',1)[0]):
            os.makedirs(self.swissprot.rsplit('/', 1)[0])
            
        if not os.path.isdir(self.trembl.rsplit('/',1)[0]):
            os.makedirs(self.trembl.rsplit('/', 1)[0])
            
    def getEnsembl(self):
        #--append-output=" + self.logFile + "
        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2ensembl.gz --output-document=" + self.ensembl + " &>/dev/null" ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getEnsembl - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.ensembl])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getAccession - Extract File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)

    def getUnigene(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2unigene --output-document=" + self.unigene + " &>/dev/null" ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getUnigene - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)

    def getAccession(self):
        
        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2accession.gz --output-document=" + self.accession + " &>/dev/null" ]) 
        
        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getAccession - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)
            return
            
        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.accession])
            
        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getAccession - Extract File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)

    def getInfo(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz --output-document=" + self.info + " &>/dev/null" ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getInfo - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)
            return

        try:
            subprocess.check_output(['bash','-c', "gunzip -f " + self.info])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getInfo - Extract File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)

    def getGPL(self):
        """This function allows you to connect to the NCBI FTP server"""
        
        a=0
        host = "ftp.ncbi.nlm.nih.gov" # adresse du serveur FTP
        connect = ftplib.FTP(host, 'anonymous', 'anonymous') 
        connect.cwd("/geo/platforms")
        for _dir in connect.nlst():  
 

            for subdir in connect.nlst(str(_dir)):
                if ((str(subdir) + "/annot") in connect.nlst(str(subdir))):
                    response = urllib2.urlopen('ftp://'+host+"/geo/platforms/"+str(subdir) + "/annot/" + (str(subdir.split("/")[1])) + ".annot.gz")
                    compressedFile = StringIO.StringIO()
                    compressedFile.write(response.read())
                    compressedFile.seek(0)
                    decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
        
                    with open(os.path.join(self.gpl ,(str(subdir.split("/")[1])) +'.annot'), 'w') as outfile:
                        outfile.write(decompressedFile.read())
                else:
                    print a
                    a=a+1
        connect.quit()

    def getHomoloGene(self):
        """Already in flat file """

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/pub/HomoloGene/current/homologene.data --output-document=" + self.homologene + " &>/dev/null" ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getHomoloGene - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)

    def getVega(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2vega.gz --output-document=" + self.vega + " &>/dev/null" ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getVega - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.vega + " &>/dev/null" ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getVega - Extract File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)

    def getHistory(self):
        """ gene2gene"""

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_history.gz --output-document=" + self.history + " &>/dev/null" ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getHistory - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.history])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getHistory - Extract File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)

    def getSwissprot(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz --output-document=" + self.swissprot + " &>/dev/null" ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getSwissprot - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.swissprot + " | egrep \"^ID   | ^AC  | ^DP | ^// \" "])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getSwissprot - Extract File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)


    def getTrembl(self):

        try:
            subprocess.check_output(['bash','-c', "wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.dat.gz --output-document=" + self.trembl + " &>/dev/null"])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getTrembl - Download File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)
            return
            
        try:
            subprocess.check_output(['bash','-c', "gunzip -f " + self.trembl + " | egrep \"^ID   | ^AC  | ^DP | ^// \" " ])

        except subprocess.CalledProcessError as error:
            
            self.logger.warning("Error - download.py - getTrembl - Extract File")
            self.logger.warning(sys.exc_info())
            self.logger.warning(error)

fileDownload = Download()

#fileDownload.getEnsembl()
#fileDownload.getUnigene()
#fileDownload.getAccession()
#fileDownload.getInfo()
fileDownload.getGPL()
#fileDownload.getHomoloGene()
#fileDownload.getVega()
#fileDownload.getHistory()
#fileDownload.getSwissprot()
#fileDownload.getTrembl()