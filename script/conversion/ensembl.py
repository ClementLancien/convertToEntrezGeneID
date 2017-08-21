# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:48:42 2017

@author: clancien
"""

import ConfigParser
import os
import pandas
import re

class Ensembl():

    def __init__(self):

        config = ConfigParser.ConfigParser()
        config.readfp(open('../../configuration.ini','r'))

        self._ensembl = config.get('Download', 'gene2ensembl')
        self._gene = config.get('Convert', 'Ensembl_gene')
        self._transcript = config.get('Convert', 'Ensembl_transcript')
        self._protein = config.get('Convert', 'Ensembl_protein')

        ##Panda read _protein(same for all) as function and not as string so raise error
        ##To bypass this error we create for each file a new variable to store the path as string

        self.filename_ensembl = str(self._ensembl)
        self.filename_gene = str(self._gene)
        self.filename_transcript = str(self._transcript)
        self.filename_protein = str(self._protein)

        self.size=1000000 #panda will read by chunsize here 1 million line 1 million line

        # Store column index we need
        self.index_entrez = None
        self.index_gene = None
        self.index_transcript = None
        self.index_protein = None

        self.dataframe = []
        self.finalDataFrame=None
        self.logFile = config.get('Error', 'logFile')

        self.path_exist()
        self.createIndex()


    def path_exist(self):
        print self._gene.rsplit('/',1)[0]
        if not os.path.isdir(self._gene.rsplit('/',1)[0]):
            os.makedirs(self._gene.rsplit('/', 1)[0])

    def writeError(self, message):

        with open(self.logFile,'a') as log:
            log.write(message+'\n')

    def createIndex(self):

        with open(self.filename_ensembl , 'r') as infile:

            header_line = next(infile)
            header_line = header_line.split('\t')

            self.index_entrez = header_line.index('GeneID')
            self.index_gene = header_line.index('Ensembl_gene_identifier')
            self.index_transcript = header_line.index('Ensembl_rna_identifier')
            self.index_protein = header_line.index('Ensembl_protein_identifier\n')

    # def getGene(self):

    #     try:

    #         self.dataFrame=[]

    #         for df in pandas.read_csv(self._ensembl, header=0, sep="\t", usecols=[self.index_entrez,self.index_gene], chunksize=size):
    #             df.columns = ['EGID','BDID']
                
    #             self.dataframe.append(
    #                 df[
    #                     df['BDID'].str.contains('^[⁻]', flags=re.IGNORECASE, regex=False, na=False) & 
    #                     df['EGID'].str.contains('^[-]', flags=re.IGNORECASE, regex=False, na=False)
    #                 ]
    #                 )

    #     except IOError as error:
    
    #         self.writeError("ensembl.py - convertToGene - Error")
    #         self.writeError(str(error.errno))
    #         self.writeError(str(error.strerror))

    # def getTranscript(self):

    #     try:

    #         self.dataFrame=[]

    #         for df in pandas.read_csv(self._ensembl, header=0, sep="\t", usecols=[self.index_entrez,self.index_transcript], chunksize=size):
    #             df.columns = ['EGID','BDID']
                
    #             self.dataframe.append(
    #                 df[
    #                     df['BDID'].str.contains('^[⁻]', flags=re.IGNORECASE, regex=False, na=False) & 
    #                     df['EGID'].str.contains('^[-]', flags=re.IGNORECASE, regex=False, na=False)
    #                 ]
    #                 )

    #     except IOError as error:
    
    #         self.writeError("ensembl.py - convertToGene - Error")
    #         self.writeError(str(error.errno))
    #         self.writeError(str(error.strerror))

    # def getProtein(self):

    #     try:

    #         self.dataFrame=[]

    #         for df in pandas.read_csv(self._ensembl, header=0, sep="\t", usecols=[self.index_entrez,self.index_transcript], chunksize=size):
    #             df.columns = ['EGID','BDID']
                
    #             self.dataframe.append(
    #                 df[
    #                     df['BDID'].str.contains('^[⁻]', flags=re.IGNORECASE, regex=False, na=False) & 
    #                     df['EGID'].str.contains('^[-]', flags=re.IGNORECASE, regex=False, na=False)
    #                 ]
    #                 )

    #     except IOError as error:
    
    #         self.writeError("ensembl.py - convertToGene - Error")
    #         self.writeError(str(error.errno))
    #         self.writeError(str(error.strerror))



    def getData(self, index_column):

        try:

            self.dataFrame=[]

            for df in pandas.read_csv(self._ensembl, header=0, sep="\t", usecols=[self.index_entrez, index_column], chunksize=self.size):
                #df.to_string()
                df.columns = ['EGID','BDID']
                
                df["EGID"]= df["EGID"].astype(str)
                #return df.info()
                #print df[df['EGID'].notnull()]
                        #df['EGID'].str.contains('^[-]', flags=re.IGNORECASE, regex=False, na=False)
                   # ]
                self.dataFrame.append(
                    df[
                        df['BDID'].notnull() &
                        #df['BDID'].str.contains('^[-]', flags=re.IGNORECASE, regex=False, na=False) & 
                        df['EGID'].notnull()
                        #df['EGID'].str.contains('^[-]', flags=re.IGNORECASE, regex=False, na=False)
                    ]
                    )
            print len(self.dataFrame)
        except IOError as error:
    
            self.writeError("ensembl.py - convertToGene - Error")
            self.writeError(str(error.errno))
            self.writeError(str(error.strerror))

    def delDoublonInDataframe(self):

        try:
            print self.dataFrame
            print pandas.concat(self.dataFrame).drop_duplicates(['EGID', 'BDID'], keep='first')
            self.finalDataFrame = pandas.concat(self.dataFrame).drop_duplicates(['EGID', 'BDID'], keep='first')
            #self.dataFrame.drop_duplicates(['EGID', 'BDID'], keep='first')

        except IOError as error:

            self.writeError("ensembl.py - writeGene - Error")
            self.writeError(str(error.errno))
            self.writeError(str(error.strerror))

    def writeFile(self, file):

        try:
            print self.finalDataFrame
            self.finalDataFrame.to_csv(file, header=None, index=None, sep='\t', mode='w')

        except IOError as error:
    
            self.writeError("ensembl.py - writeGene - Error")
            self.writeError(str(error.errno))
            self.writeError(str(error.strerror))


    def convertToGene(self):

        #self.getGene()
        self.getData(self.index_gene)
        self.delDoublonInDataframe()
        self.writeFile(self.filename_gene)

    def convertToTranscript(self):

        #self.getTranscript()
        self.getData(self.index_transcript)
        self.delDoublonInDataframe()
        self.writeFile(self.filename_transcript)

    def convertToProtein(self):

        #self.getTranscript()
        self.getData(self.index_protein)
        self.delDoublonInDataframe()
        self.writeFile(self.filename_protein)

ensembl_file= Ensembl()
ensembl_file.convertToGene()
ensembl_file.convertToTranscript()
ensembl_file.convertToProtein()