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
import time
import subprocess

gene2accesion_path = '/home/clancien/Desktop/Fichier_Convert/gene2accession'
gene2ensembl_path = '/home/clancien/Desktop/Fichier_Convert/gene2ensembl'
gene2go_path = '/home/clancien/Desktop/Fichier_Convert/gene2go'
gene2unigene_path = '/home/clancien/Desktop/Fichier_Convert/gene2unigene'
gene_info_path =  '/home/clancien/Desktop/Fichier_Convert/gene_info'
gene_refseq_unitprotkb_collab_path = '/home/clancien/Desktop/Fichier_Convert/gene_refseq_unitprotkb_collab'
gene2refseq_path = '/home/clancien/Desktop/Fichier_Convert/gene2refseq'
GPL_path = '/home/clancien/Desktop/Data_ressource/Fichier_Convert/GPL'



def download():
    getGPL()
    #getGeneInfo()
    #getRefSeq()
    #getGeneEnsembl()
    #getGeneAccession()
    #getGeneUnigene()
    #getGeneRefseqUnitprotkb()
    #getGeneGo()
    #getHomoloGene()
    
def getGPL():
    """This function allows you to connect to the NCBI FTP server"""
    

    host = "ftp.ncbi.nlm.nih.gov" # adresse du serveur FTP
    connect = ftplib.FTP(host, 'anonymous', 'anonymous') 
    connect.cwd("/geo/platforms")
    for dir in connect.nlst():  
        #print dir
        for subdir in connect.nlst(str(dir)):
            if ((str(subdir) + "/annot") in connect.nlst(str(subdir))):
                response = urllib2.urlopen('ftp://'+host+"/geo/platforms/"+str(subdir) + "/annot/" + (str(subdir.split("/")[1])) + ".annot.gz")
                compressedFile = StringIO.StringIO()
                compressedFile.write(response.read())
                compressedFile.seek(0)
                decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
    
                with open(os.path.join('/home/clancien/Desktop/Data_ressource/Fichier_Convert/GPL',(str(subdir.split("/")[1])) +'.annot'), 'w') as outfile:
                    outfile.write(decompressedFile.read())

    connect.quit()
                
def getGeneInfo():
    subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz "])
    subprocess.check_output(['bash','-c', "mv gene_info.gz gene_info/"])
    subprocess.check_output(['bash','-c', "gunzip -f gene_info/gene_info.gz"]) 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

def getRefSeq():
    subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2refseq.gz "])
    subprocess.check_output(['bash','-c', "mv gene2refseq.gz gene2refseq/"])
    subprocess.check_output(['bash','-c', "gunzip -f gene2refseq/gene2refseq.gz"]) 
    
    
def getGeneEnsembl():
    subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2ensembl.gz"])
    subprocess.check_output(['bash','-c', "mv gene2ensembl.gz gene2ensembl/"])
    subprocess.check_output(['bash','-c', "gunzip -f gene2ensembl/gene2ensembl.gz"]) 

def getGeneAccession():
    subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2accession.gz"])
    subprocess.check_output(['bash','-c', "mv gene2accession.gz gene2accession/"])
    subprocess.check_output(['bash','-c', "gunzip -f gene2accession/gene2accession.gz"]) 

def getGeneUnigene():
    subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2unigene -P gene2unigene/"])
    #subprocess.check_output(['bash','-c', "mv gene2unigene gene2unigene/"])
    #subprocess.check_output(['bash','-c', "gunzip -f gene2unigene/gene2unigene.gz"]) 
    
def getGeneRefseqUnitprotkb():
    subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_refseq_uniprotkb_collab.gz"])
    subprocess.check_output(['bash','-c', "mv gene_refseq_uniprotkb_collab.gz gene_refseq_uniprotkb_collab/"])
    subprocess.check_output(['bash','-c', "gunzip -f gene_refseq_uniprotkb_collab/gene_refseq_uniprotkb_collab.gz"]) 

    
def getGeneGo():
    subprocess.check_output(['bash','-c', "wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz"])
    subprocess.check_output(['bash','-c', "mv gene2go.gz gene2go/"])
    subprocess.check_output(['bash','-c', "gunzip -f gene2go/gene2go.gz"]) 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
def getHomoloGene():
    subprocess.check_output(['bash', '-c', "wget ftp://ftp.ncbi.nlm.nih.gov/pub/HomoloGene/current/homologene.data"])
    #subprocess.check_output(['bash', '-c', "mv homologene.data homologene/"])
    
def getUniprot_sprot():
    subprocess.check_output(['bash', '-c', "wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz"])
    subprocess.check_output(['bash','-c', "mv uniprot_sprot.dat.gz gene2go/"])
    subprocess.check_output(['bash','-c', "gunzip uniprot_sprot.dat.gz | egrep \"^ID   | ^AC  | ^DP | ^//"])
    
t0 = time.time()
download()
print time.time() - t0, "seconds wall time"                                                                                                                                                                                                                                    