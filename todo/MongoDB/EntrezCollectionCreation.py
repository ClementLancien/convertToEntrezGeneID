# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 13:44:19 2017

@author: clancien
"""
import time
import tqdm
from pymongo import MongoClient
import ConfigParser

config= ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))


#Concatenation_Entrez=config.get('Convert','Concatenation_Entrez')

Ensembl_gene=config.get('Convert','Ensembl_gene')
Ensembl_transcript=config.get('Convert','Ensembl_transcript')
Ensembl_protein=config.get('Convert','Ensembl_protein')
UniGene=config.get('Convert','UniGene')

vega_gene=config.get('Convert','vega_gene')
vega_transcript=config.get('Convert','vega_transcript')
vega_protein=config.get('Convert','vega_protein')

gene2gene=config.get('Convert','gene2gene')

GenBank_transcript=config.get('Convert','GenBank_transcript')
RefSeq_transcript=config.get('Convert','RefSeq_transcript')
GenBank_protein=config.get('Convert','GenBank_protein')
RefSeq_protein=config.get('Convert','RefSeq_protein')

GI_transcript=config.get('Convert','GI_transcript')
GI_protein=config.get('Convert','GI_protein')
Gene_TaxID=config.get('Convert','Gene_TaxID')
Gene_Symbol=config.get('Convert','Gene_Symbol')

HomoloGene=config.get('Convert','HomoloGene')

Swissprot=config.get('Convert', 'UniProtKB_sprot')
trEMBL=config.get('Convert', 'trEmblID')

GPL=config.get('Convert','GPL_all')

def pushEnsembl_gene():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(Ensembl_gene , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.Ensembl_gene.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushEnsembl_transcript():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(Ensembl_transcript , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.Ensembl_transcript.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line                


def pushEnsembl_protein():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(Ensembl_protein , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.Ensembl_protein.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line 
                
def pushUniGene():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(UniGene , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.UniGene.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line 
                
def pushvega_gene():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(vega_gene , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.Vega_gene.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushvega_transcript():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(vega_transcript , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.Vega_transcript.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line
                

def pushvega_protein():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(vega_protein , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.Vega_protein.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushgene2gene():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(gene2gene , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.gene2gene.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushGenBank_transcript():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(GenBank_transcript , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            print line
            try:
                lineList=line.split("\t")            
                #print line
                db.GenBank_transcript.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[1].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushRefSeq_transcript():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(RefSeq_transcript , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.RefSeq_transcript.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[1].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line
                
def pushGenBank_protein():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(GenBank_protein , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.GenBank_protein.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushRefSeq_protein():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(RefSeq_protein , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.RefSeq_protein.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[1].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushGI_transcript():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(GI_transcript , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.GI_transcript.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushGI_protein():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(GI_protein , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.GI_protein.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushGene_TaxID():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(Gene_TaxID , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.Gene_TaxID.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushGene_Symbol():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(Gene_Symbol , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.Gene_Symbol.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushHomoloGene():
    client = MongoClient()
    db=client["geneulike"]
    #for file_ in tqdm.tqdm(fileList, 'Time for loop of EntrezCollectionCreation'):
    with open(HomoloGene , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            try:
                lineList=line.split("\t")            
                #print line
                db.HomoloGene.insert(
                            {
                             "GeneID" : str(lineList[0]),
                             #"BD" : str(lineList[1]),
                             "BDID" : str(lineList[2].split("\n")[0])
                             })
            except:
                #print file_
                print "lastline is : ", line

def pushSwissprot():
    client=MongoClient()
    db=client['geneulike']
    
    with open(Swissprot, 'r') as infile:
        for line in tqdm.tqdm(infile, "Time for loop of Swissprot"):
            try:
                lineList=line.split("\t")
                db.SwissProt.insert(
                {
                    "GeneID" : str(lineList[0]),
                    "BDID": str(lineList[1].split("\n")[0])
                
                })
            except:
                print "lastline is : ", line
                
def pushtrEMBL():
    client=MongoClient()
    db=client['geneulike']
    
    with open(trEMBL, 'r') as infile:
        for line in tqdm.tqdm(infile, "Time for loop of trEMBL" ):
            try:
                lineList = line.split("\t")
                db.trEMBL.insert(
                    {
                        "GeneID" : str(lineList[0]),
                        "BDID": str(lineList[1].split("\n")[0])
                    })
            except:
                print "Lastline is : ", line
                
def pushGPL():
    client=MongoClient()
    db=client['geneulike']
    
    with open(GPL, 'r') as infile:

        for line in tqdm.tqdm(infile, "Time for loop of GPL" ):
            try:
                lineList = line.split("\t")
                db.GPL.insert(
                   {
                        "GeneID" : str(lineList[0]),
                        "BDID": str(lineList[2]),
                        "BD": str(lineList[3].split("\n")[0])
                    })
            except:
                print "Lastline is : ", line   
def pushEntrez():
    #pushEnsembl_gene()
    #pushEnsembl_transcript()
    #pushEnsembl_protein()
    #pushUniGene()
    #pushvega_gene()
    #pushvega_transcript()
    #pushvega_protein()
    #pushgene2gene()
    #pushGenBank_transcript()
    #pushRefSeq_transcript()
    #pushGenBank_protein()
    #pushRefSeq_protein()
    #pushGI_transcript()
    #pushGI_protein()
    #pushGene_TaxID()
    #pushGene_Symbol()
    #pushHomoloGene()
    #pushSwissprot()
    #pushtrEMBL()
    pushGPL()

         
t0 = time.time()
pushEntrez()
print time.time() - t0, "seconds wall time"