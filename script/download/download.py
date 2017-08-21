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

        self.path_exist()
        
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
        
    def writeError(self, message):
        with open(self.logFile,'a') as log:
            log.write(message+'\n')
            
    def getEnsembl(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2ensembl.gz --append-output=" + self.logFile + " --output-document=" + self.ensembl])

        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getEnsembl - Error")
            self.writeError(str(e))
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.ensembl])

        except subprocess.CalledProcessError as e:
            
            self.writeError("download.py - getEnsembl - Error")
            self.writeError(str(e))
            return

    def getUnigene(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2unigene --append-output=" + self.logFile + " --output-document=" + self.unigene])

        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getUnigene - Error")
            self.writeError(str(e))
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.unigene])

        except subprocess.CalledProcessError as e:
            
            self.writeError("download.py - getUnigene - Error")
            self.writeError(str(e))
            return

    def getAccession(self):
        
        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2accession.gz --append-output=" + self.logFile + " --output-document=" + self.accession]) 
        
        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getAccession - Error")
            self.writeError(str(e))
            return
            
        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.accession])
            
        except subprocess.CalledProcessError as e:
            
            self.writeError("download.py - getAccession - Error")
            self.writeError(str(e))
            return

    def getInfo(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz --append-output=" + self.logFile + " --output-document=" + self.info])

        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getInfo - Error")
            self.writeError(str(e))
            return

        try:
            subprocess.check_output(['bash','-c', "gunzip -f " + self.info])

        except subprocess.CalledProcessError as e:
            
            self.writeError("download.py - getInfo - Error")
            self.writeError(str(e))
            return

    def getGPL(self):
        """This function allows you to connect to the NCBI FTP server"""
        

        host = "ftp.ncbi.nlm.nih.gov" # adresse du serveur FTP
        connect = ftplib.FTP(host, 'anonymous', 'anonymous') 
        connect.cwd("/geo/platforms")
        for _dir in connect.nlst():  
            #print dir
            for subdir in connect.nlst(str(_dir)):
                if ((str(subdir) + "/annot") in connect.nlst(str(subdir))):
                    response = urllib2.urlopen('ftp://'+host+"/geo/platforms/"+str(subdir) + "/annot/" + (str(subdir.split("/")[1])) + ".annot.gz")
                    compressedFile = StringIO.StringIO()
                    compressedFile.write(response.read())
                    compressedFile.seek(0)
                    decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
        
                    with open(os.path.join(self.gpl ,(str(subdir.split("/")[1])) +'.annot'), 'w') as outfile:
                        outfile.write(decompressedFile.read())

        connect.quit()

    def getHomoloGene(self):
        """Already in flat file """

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/pub/HomoloGene/current/homologene.data --append-output=" + self.logFile + " --output-document=" + self.homologene])

        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getHomoloGene - Error")
            self.writeError(str(e))
            return

    def getVega(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2vega.gz --append-output=" + self.logFile + " --output-document=" + self.vega])

        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getVega - Error")
            self.writeError(str(e))
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.vega])

        except subprocess.CalledProcessError as e:
            
            self.writeError("download.py - getVega - Error")
            self.writeError(str(e))
            return

    def getHistory(self):
        """ gene2gene"""

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_history.gz --append-output=" + self.logFile + " --output-document=" + self.history])

        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getHistory - Error")
            self.writeError(str(e))
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.history])

        except subprocess.CalledProcessError as e:
            
            self.writeError("download.py - getHistory - Error")
            self.writeError(str(e))
            return

    def getSwissprot(self):

        try:

            subprocess.check_output(['bash','-c', "wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz --append-output=" + self.logFile + " --output-document=" + self.swissprot])

        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getSwissprot - Error")
            self.writeError(str(e))
            return

        try:

            subprocess.check_output(['bash','-c', "gunzip -f " + self.swissprot + " | egrep \"^ID   | ^AC  | ^DP | ^//"])

        except subprocess.CalledProcessError as e:
            
            self.writeError("download.py - getSwissprot - Error")
            self.writeError(str(e))
            return

    def getTrembl(self):

        try:
            subprocess.check_output(['bash','-c', "wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.dat.gz --append-output=" + self.logFile + " --output-document=" + self.trembl])

        except subprocess.CalledProcessError as e:

            self.writeError("download.py - getTrembl - Error")
            self.writeError(str(e))
            return

        try:
            subprocess.check_output(['bash','-c', "gunzip -f " + self.trembl + " | egrep \"^ID   | ^AC  | ^DP | ^//"])

        except subprocess.CalledProcessError as e:
            
            self.writeError("download.py - getTrembl - Error")
            self.writeError(str(e))
            return

fileDownload = Download()

fileDownload.getEnsembl()
#fileDownload.getUnigene()
#fileDownload.getAccession()
#fileDownload.getInfo()
#fileDownload.getGPL()
#fileDownload.getHomoloGene()
#fileDownload.getVega()
#fileDownload.getHistory()
#fileDownload.getSwissprot()
#fileDownload.getTrembl()