# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:54:13 2017

@author: clancien
"""

import re
import time
import ConfigParser
import tqdm
import collections
import pprint
config = ConfigParser.ConfigParser()
config.readfp(open('../../../../conf.ini','r'))



gene2accession = config.get('Download', 'gene2accession')
GenBank_transcript = config.get('Convert', 'GenBank_transcript')
RefSeq_transcript = config.get('Convert', 'RefSeq_transcript')
GenBank_protein = config.get('Convert', 'GenBank_protein')
RefSeq_protein = config.get('Convert', 'RefSeq_protein')
GI_transcript = config.get('Convert', 'GI_transcript')
GI_protein = config.get('Convert', 'GI_protein')



class gene2accession:

    def __init__(self, writeFile):
        self.readFile = '../'+config.get('Download', 'gene2accession')
        self.writeFile = writeFile
        self.EGIDColumn = 1
        self.BDIDColumn = None
        #we dont want doublon in our values so with initialize the dico has a set. By default dico['key'] =set()
        self.dico = collections.defaultdict(set) 
        self.collection=None
        
        self.initCollection()
        self.initBDID()
    
    def setEGID(self,EGID):
        self.EGID=EGID
        
    def setBDID(self,BDID):
        self.BDIDColumn = BDID
    
    def initCollection(self):
        collection = {
                      GenBank_transcript:'GenBank_transcript',
                      GenBank_protein:'GenBank_protein',
                      RefSeq_transcript:'RefSeq_transcript',
                      RefSeq_protein:'RefSeq_protein',
                      GI_transcript:'GI_transcript',
                      GI_protein:'GI_protein'
                     }
        self.collection=collection[self.writeFile]
        
    def initBDID(self):
        
        BDIDColumn = {
                      'GenBank_transcript': 3,
                      'RefSeq_transcript':3,
                      'GenBank_protein':5,
                      'RefSeq_protein':5,
                      'GI_transcript':4,
                      'GI_protein':6
                     }
        #print "self.collection " ,self.collection
        #print BDIDColumn[self.collection]
        #print "en"
        self.BDIDColumn=BDIDColumn[self.collection]
    
        
    def printall(self):
        print str(self.BDIDColumn)
    
    def RefSeq_transcript_condition(self,egid, bdid):

        if egid != '-':
            if (re.match(r"^[A-Z]{2}[_]([0-9]*)$", bdid) != None and bdid != "NA"):
                return True
            else:
                return False
        else:
            return False
            
    def GenBank_transcript_condition(self, newLine):
        if newLine[self.EGIDColumn] != '-':
            if re.match(r"^[A-Z]{2}[_]([0-9]*)$", newLine[self.BDIDColumn]):
                return False
            else:
                return True
        else:
            return False
    
    def RefSeq_protein_condition(self, newLine):
        if newLine[self.EGIDColumn] != '-':
            if re.match(r"^[A-Z]{2}[_]([0-9]*)$", newLine[self.BDIDColumn]):
                return True
            else:
                return False
        else:
            return False
    
    def GenBank_protein_condition(self, newLine):
        if newLine[self.EGIDColumn] != '-':
            if re.match(r"^[A-Z]{2}[_]([0-9]*)$", newLine[self.BDIDColumn]):
                return False
            else:
                return True
        else:
            return False
    
    def GI_condition(self, newLine):
        if newLine[self.EGIDColumn] != '-':
            if re.match(r"(^[0-9]*)$", newLine[self.BDIDColumn]):
                return True
            else:
                return False
        else:
            return False
    
            
    def RefSeq_transcript_reading(self):
        with open(self.readFile, 'r') as infile:
            next(infile)
            for line in tqdm.tqdm(infile, 'Time for loop of '):
                newLine=line.split("\t")
                egid=newLine[self.EGIDColumn]
                bdid=newLine[self.BDIDColumn].split(".")[0]
                if(self.RefSeq_transcript_condition(egid, bdid)):
                    self.dico[egid].add(bdid)
    
    def GenBank_transcript_reading(self):
         with open(self.readFile, 'r') as infile:
            for line in infile:
                newLine=str(line.split("\t"))
                
                if(self.GenBank_transcript_condition(newLine)):
                    self.dico[newLine[self.EGIDColumn]].add(newLine[self.BDIDColumn])
                    
    def RefSeq_protein_reading(self):
        with open(self.readFile, 'r') as infile:
            for line in infile:
                newLine=str(line.split("\t"))
                self.RefSeq_protein_condition(newLine)
                return
                if(self.RefSeq_protein_condition(newLine)):
                    
                    self.dico[newLine[self.EGIDColumn]].add(newLine[self.BDIDColumn])
    
    def GenBank_protein_reading(self):
        with open(self.readFile, 'r') as infile:
            for line in infile:
                newLine=str(line.split("\t"))
                if(self.GenBank_protein_condition(newLine)):
                    self.dico[newLine[self.EGIDColumn]].add(newLine[self.BDIDColumn])
                    
    def GI_reading(self):
        with open(self.readFile, 'r') as infile:
            for line in infile:
                newLine=str(line.split("\t"))
                if(self.GI_condition(newLine)):
                    self.dico[newLine[self.EGIDColumn]].add(newLine[self.BDIDColumn])
                    
    def write(self):
        with open('RefSeq_transcript', 'w') as output:
            for key, value in self.dico.iteritems(): #iteritems ==> Generator Do not use dict.items() which return all at once            
                for val in value:
                    output.write(key + "\t" + value + "\n")
        print "done"       
    
    
    def process(self):

        if self.collection == 'RefSeq_transcript':
            self.RefSeq_transcript_reading()
        elif self.collection == 'GenBank_transcript':
            self.GenBank_transcript_reading
        elif self.collection == 'RefSeq_protein':
            self.RefSeq_protein_reading
        elif self.collection == 'GenBank_protein':
            self.GenBank_protein_reading
        elif self.collection == 'GI_protein' or self.writeFile == 'GI_transcript':
            self.GI_reading
        else:
            print 'Error your writeFile is not recognize'
            print 'Choose between :\
                  GenBank_transcript\n \
                  RefSeq_transcript\n \
                  GenBank_protein\n \
                  RefSeq_protein\n \
                  GI_transcript\n \
                  GI_protein\n'
            return
        print "dans la place"
        self.write()
        
gene2accession(RefSeq_transcript).process()
