# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:24:30 2017

@author: clancien
"""
import pandas
import re
import time
import ConfigParser
import tqdm
import collections
import pprint
import os 
config = ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))

gene2accession = config.get('Download', 'gene2accession')
GenBank_transcript = config.get('Convert', 'GenBank_transcript')
RefSeq_transcript = str(config.get('Convert', 'RefSeq_transcript'))
GenBank_protein = config.get('Convert', 'GenBank_protein')
RefSeq_protein = config.get('Convert', 'RefSeq_protein')
GI_transcript = config.get('Convert', 'GI_transcript')
GI_protein = config.get('Convert', 'GI_protein')

_GenBank_transcript=str(GenBank_transcript)
_RefSeq_transcript=str(RefSeq_transcript)
_GenBank_protein=str(GenBank_protein)
_RefSeq_protein=str(RefSeq_protein)
_GI_transcript=str(GI_transcript)
_GI_protein=str(GI_protein)
print "'"+RefSeq_transcript+"'"

readFile=gene2accession
size=1000000 #loop : number lines by lines

EGIDcolumn = 1
BDIDColumn = {
                      'GenBank_transcript': 3,
                      'RefSeq_transcript':3,
                      'GenBank_protein':5,
                      'RefSeq_protein':5,
                      'GI_transcript':4,
                      'GI_protein':6
                     }

def RefSeq_transcript():
    
    #size=1000000 #loop : number lines by lines
    dataframe=[]
    for df in pandas.read_csv(readFile,header=0,sep="\t",usecols=[EGIDcolumn,BDIDColumn['RefSeq_transcript']],chunksize=size):

        df.columns = ['EGID','BDID']
        df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
        #df = df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=True, na=False)]# & df['BDID'].str.contains('-')==False]
        dataframe.append(df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=True, na=False)])
        #self.dataframe.append(((df[df['GRT'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull() & (df['GRT'] != "-") & (df['GRT'] != "NA") & df['GRT'].notnull()]).drop_duplicates(['EGID', 'GRT'], keep='first')))#.to_csv('EntrezGeneToRefSeq_transcript.txt', header=None, index=None, sep='\t', mode='w')
        #if len(dataframe) == 8:
            #print df[df['BDID'] != '-']
        #    print df['EGID']
            #print df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=True, na=False) ] & df[(df['EGID'] != '-') ]
        #    return
        #    break
    
    pandas.concat(dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(_RefSeq_transcript, header=None, index=None, sep='\t', mode='w')

def GenBank_transcript():
    #size=1000000 #loop : number lines by lines
    dataframe=[]
    for df in pandas.read_csv(readFile,header=0,sep="\t",usecols=[EGIDcolumn,BDIDColumn['GenBank_transcript']],chunksize=size):

        df.columns = ['EGID','BDID']
        df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
        df = df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+[.][0-9]+$', flags=re.IGNORECASE, regex=False, na=False)]
        dataframe.append(df[df['BDID'] != '-'])
        
       # dataframe.append(df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+[.][0-9]+$', flags=re.IGNORECASE, regex=False, na=False) & df['EGID'].notnull() & df['BDID'] != '-'])
        
    #pandas.concat(dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(_GenBank_transcript, header=None, index=None, sep='\t', mode='w')
    pandas.concat(dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv("test", header=None, index=None, sep='\t', mode='w')


def RefSeq_protein():
    #size=1000000 #loop : number lines by lines
    dataframe=[]
    for df in pandas.read_csv(readFile,header=0,sep="\t",usecols=[EGIDcolumn,BDIDColumn['RefSeq_protein']],chunksize=size):

        df.columns = ['EGID','BDID']
        df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
        #df =df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=True, na=False)]
        dataframe.append(df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=True, na=False)])
        #dataframe.append(df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull()])

    pandas.concat(dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(_RefSeq_protein, header=None, index=None, sep='\t', mode='w')

def GenBank_protein():
    #size=1000000 #loop : number lines by lines
    dataframe=[]
    for df in pandas.read_csv(readFile,header=0,sep="\t",usecols=[EGIDcolumn,BDIDColumn['GenBank_protein']],chunksize=size):

        df.columns = ['EGID','BDID']
        df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
        df =df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=False, na=False)]
        dataframe.append(df[df['BDID'] != '-'])
        #dataframe.append(df[df['BDID'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=False, na=False) & df['EGID'].notnull() & df['BDID'] !='-'])

    pandas.concat(dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(_GenBank_protein, header=None, index=None, sep='\t', mode='w')

def GI_transcript():
    #size=1000000 #loop : number lines by lines
    dataframe=[]
    for df in pandas.read_csv(readFile,header=0,sep="\t",usecols=[EGIDcolumn,BDIDColumn['GI_transcript']],chunksize=size):

        df.columns = ['EGID','BDID']
        df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
        #df =df[df['BDID'].str.contains('^[0-9]+$', flags=re.IGNORECASE, regex=True, na=False)]
        dataframe.append(df[df['BDID'].str.contains('^[0-9]+$', flags=re.IGNORECASE, regex=True, na=False)])
        #dataframe.append(df[df['BDID'].str.contains('^[0-9]+$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull()])

    pandas.concat(dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(_GI_transcript, header=None, index=None, sep='\t', mode='w')

def GI_protein():
    #size=1000000 #loop : number lines by lines
    dataframe=[]
    for df in pandas.read_csv(readFile,header=0,sep="\t",usecols=[EGIDcolumn,BDIDColumn['GI_protein']],chunksize=size):

        df.columns = ['EGID','BDID']
        df['BDID'] = df['BDID'].astype(str)
        df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
        #df =df[df['BDID'].str.contains('^[0-9]+$', flags=re.IGNORECASE, regex=True, na=False)]
        dataframe.append(df[df['BDID'].str.contains('^[0-9]+$', flags=re.IGNORECASE, regex=True, na=False)])
        #dataframe.append(df[df['BDID'].str.contains('^[0-9]+$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull()])
    
    pandas.concat(dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(_GI_protein, header=None, index=None, sep='\t', mode='w')

t0=time.time()

t1=time.time()
#RefSeq_transcript()
print (time.time() - t1), "seconds RefSeq_transcript"

t1=time.time()
#GenBank_transcript()
print (time.time() - t1), "seconds GenBank_transcript"

t1=time.time()
#RefSeq_protein()
print (time.time() - t1), "seconds RefSeq_protein"

t1=time.time()
#GenBank_protein()
print (time.time() - t1), "seconds GenBank_protein"

t1=time.time()
#GI_transcript()
print (time.time() - t1), "seconds GI_transcript"

t1=time.time()
#GI_protein()
print (time.time() - t1), "seconds GI_protein"

print (time.time() - t0), "seconds total"