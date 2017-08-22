# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 11:43:10 2017

@author: clancien
"""
#mongoimport -d geneulike -c test --type tsv Entrez_GeneToEnsembl_gene -f GeneID.string\(\),BDID.string\(\) --columnsHaveTypes
#mongoimport -d geneulike -c test --type tsv GPL_all -f GeneID.string\(\),GPLcode.string\(\),BDID.string\(\),GPLname.string\(\) --columnsHaveTypes

import pandas
from itertools import (takewhile,repeat)
import re
import time
import ConfigParser
import tqdm
import collections
import pprint
config = ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))

gene2accession = config.get('Download', 'gene2accession')
GenBank_transcript = config.get('Convert', 'GenBank_transcript')
RefSeq_transcript = config.get('Convert', 'RefSeq_transcript')
GenBank_protein = config.get('Convert', 'GenBank_protein')
RefSeq_protein = config.get('Convert', 'RefSeq_protein')
GI_transcript = config.get('Convert', 'GI_transcript')
GI_protein = config.get('Convert', 'GI_protein')


#def test():
#    _list=[]
#    with open(gene2accession,'r') as infile:
#        dico={}
#        geneidlist=[]
#        bdifidlist=[]
#        _index=[]
#        i=0
#        for line in tqdm.tqdm(infile):
#            newLine=line.split("\t")
#            if len(_index) ==1000:
#                dico['EGID']=geneidlist
#                dico['BDID']=bdifidlist
#                _list.append(pd.DataFrame(dico,index=_index))
#                dico={}
#                geneidlist=[]
#                bdifidlist=[]
#                _index=[]
#
#            if newLine[1] != '-':
#                if (re.match(r"^[A-Z]{2}[_]([0-9]*)$", newLine[3].split(".")[0]) != None and newLine[3] != "NA"):
#                    
#                    geneidlist.append(newLine[1])
#                    bdifidlist.append(newLine[3].split(".")[0])
#                    _index.append(i)
#                    i+=1
#        dico['EGID']=geneidlist
#        dico['BDID']=bdifidlist
#        _list.append(pd.DataFrame(dico,index=_index))
#        dico={}
#        geneidlist=[]
#        bdifidlist=[]
#        _index=[]
#        print i            
#        print len(_list)        
#        return _list
              

#t0=time.time()
##new=pd.concat(test()).drop_duplicates(['EGID', 'BDID'], keep='first')
##np.savetxt(r'c:\data\np.txt', new.values, fmt='%d')
#new.to_csv('EntrezGeneToRefSeq_transcript.txt', header=None, index=None, sep='\t', mode='w')
#print (len(new))
#print time.time() - t0, "seconds wall time"




class convert:
    
    def __init__(self,readFile,writeFile,EGIDColumn,BDIDColumn, header):
        self.readFile=readFile
        self.writeFile=writeFile
        self.EGIDColumn=EGIDColumn
        self.BDIDColumn=BDIDColumn
        #self.listComparaisonEquall=listComparaisonEquall
        #self.listComparaisonDIfference=listComparaisonDIfference
        self.header=header
        self.number=None
        self.dataframe=[]
        self.check()
        
    def check(self):
        if not isinstance(self.readFile,str):
            raise ValueError('The File which is use for reading information is not found. Please check your file or use quote')
            
        if not isinstance(self.writeFile,str):
            raise ValueError('The File which is use for writing the new information is not valid. Please use quote')
            
        if not isinstance(self.EGIDColumn,int):
            raise ValueError('The column number for Entrez Gene ID is not an integer')
            
        if not isinstance(self.BDIDColumn,int):
            raise ValueError('The column number you which to exctract is not an integer')
        
        #if not isinstance(self.listComparaisonDIfference, list):
        #    raise ValueError('The element you which to mismatch are not in a list. Please use []')
        
        #if not isinstance(self.listComparaisonEquall, list):
        #    raise ValueError('The element you which to match are not in a list. Please use []')
            
        if not isinstance(self.header,bool):
            raise ValueError('The header is use to determine if the first line of your reading file has Tag. Use \'True\' or \'False\' ')
            
    def append(self,EGIDList, BDIDList, _index):
        dico={}
        dico['EGID']=EGIDList
        dico['BDID']=BDIDList

        self.dataframe.append(pandas.DataFrame(dico, index=_index))   
        #(pandas.DataFrame(dico, index=_index)).to_csv('EntrezGeneToRefSeq_transcript.txt', header=None, index=None, sep='\t', mode='a')
    def concatenate(self):
        pandas.concat(self.dataframe)
    #def count(self):
        #46 secondes
        #i=0
        #with open (self.readFile, 'r') as infile:
        #    for line in infile:
        #        i+=1
        #self.number=i
        
        #40secondes
        #def _make_gen(reader):
            #b = reader(1024 * 1024)
            #while b:
                #yield b
                #b = reader(1024*1024)

        #def rawpycount(filename):
            #f = open(filename, 'rb')
            #f_gen = _make_gen(f.read)
            #return sum( buf.count(b'\n') for buf in f_gen )
        
        #44seconde
        #def rawbigcount(filename):
        #    f = open(filename, 'rb')
        #    bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
        #    return sum( buf.count(b'\n') for buf in bufgen if buf )

        #self.number=rawbigcount(self.readFile)
    def reading(self):
        
        size=1000000 #loop : number lines by lines
        for df in pandas.read_csv(self.readFile,header=0,sep="\t",usecols=[1,3],chunksize=size):
            t0=time.time()
            df.columns = ['EGID','GRT']
            df['GRT'] = df['GRT'].str.replace('[.][0-9]+','')#r'[.]([0-9]*)', '')
            self.dataframe.append(df[df['GRT'].str.contains('^[A-Z]{2}[_][0-9]+[.][0-9]+$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull()])
            #self.dataframe.append(((df[df['GRT'].str.contains('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull() & (df['GRT'] != "-") & (df['GRT'] != "NA") & df['GRT'].notnull()]).drop_duplicates(['EGID', 'GRT'], keep='first')))#.to_csv('EntrezGeneToRefSeq_transcript.txt', header=None, index=None, sep='\t', mode='w')
            print (time.time() - t0),  "seconds"  
        return
        #a=range(16)
        #print a
        #with open(self.readFile, 'r')as infile:
        #    next(infile)
        #    a=next(infile)
        #    a=a.split("\t")
        #    b=[a[1],a[3],a[4],a[5],a[6]]
        #    print b
        
        #t1=time.time()
        #t0=time.time()
        step=8000000
        for i in range (0,self.number,step):
            df= pandas.read_csv(self.readFile,
                             header=0,
                             sep="\t",
                             #index_col=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
                             usecols=[1,3],#,4,5,6],
                             skiprow=i,
                             #index_col=[1,3,4,5,6],
                             nrows=i+step)#61668701)
        #print time.time() - t0, "seconds read time"
        
        #t0=time.time()
            df.columns = ['EGID','GRT']#,'GIT','GRP','GIP']
        #print time.time() - t0, "seconds name time"
        #'EGID' = Entrez gene Ids
        #'GRT' = GenBank et Refseq trranscript
        #'GIT' = GI_transcript
        #'GRT' = GenBank et RefSeq protein
        #'GIT' = GI_protein
        
        
        #t0=time.time()
            df['GRT'] = df['GRT'].str.replace()#r'[.]([0-9]*)', '')
        #print time.time() - t0, "seconds replace time"
        #print df[df['GRT'].str.contains('^[A-Z]{2}[_]([0-9]*)$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull() & (df['GRT'] != "-") & (df['GRT'] != "NA")].drop_duplicates(['EGID', 'GRT'], keep='first')
        #return
        #df[df['genre'].str.contains('IC')]
        #t0=time.time()
            self.dataframe.append(((df[df['GRT'].str.contains('^[A-Z]{2}[_]([0-9]*)$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull() & (df['GRT'] != "-") & (df['GRT'] != "NA") & df['GRT'].notnull()]).drop_duplicates(['EGID', 'GRT'], keep='first')))#.to_csv('EntrezGeneToRefSeq_transcript.txt', header=None, index=None, sep='\t', mode='w')
         
        df= pandas.read_csv(self.readFile,
                             header=0,
                             sep="\t",
                             #index_col=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
                             usecols=[1,3],#,4,5,6],
                             skiprow=(self.number-(self.number%step))-10,
                             #index_col=[1,3,4,5,6],
                             nrows=self.number%step)#61668701)
        df.columns = ['EGID','GRT']
        df['GRT'] = df['GRT'].str.replace(r'[.]([0-9]*)', '')
        self.dataframe.append(((df[df['GRT'].str.contains('^[A-Z]{2}[_]([0-9]*)$', flags=re.IGNORECASE, regex=True, na=False) & df['EGID'].notnull() & (df['GRT'] != "-") & (df['GRT'] != "NA") & df['GRT'].notnull()]).drop_duplicates(['EGID', 'GRT'], keep='first')))#.to_csv('EntrezGeneToRefSeq_transcript.txt', header=None, index=None, sep='\t', mode='w')
        #print time.time() - t0, "seconds select, del doublon and write time"  
        
        #print time.time() - t1, "seconds process time" 
        #ab= df[df['EGID'].notnull() & (df['GRT'] != "-") & (df['GRT'] != "NA") & df['GRT'].notnull()]
        #_list=[]
        #_list.append(ab)
        #print _list
        #df.to_csv('EntrezGeneToRefSeq_transcript.txt', header=None, index=None, sep='\t', mode='w')
        #df['GRP'] = df['GRP'].str.replace(r'[.]([0-9]*)', '')            
        #print df
        #print df[4]
        #df['GRT'] = df['GRT'].str.replace(r'[.]([0-9]*)', '')
        #print df[4]
        #print df
       # i=0
       # geneidlist=[]
       # bdidlist=[]
       # _index=[]

       # with open(self.readFile, 'r')as infile:
       #     if self.header:
       #         next(infile)
                
       #     for line in tqdm.tqdm(infile):
       #         i+=1
       #     print i
                #newLine=line.split("\t")
                #if len(_index) == 1000000:
                #    self.append(geneidlist, bdidlist, _index )
                #    geneidlist=[]
                #    bdidlist=[]
                #    _index=[]

                #if newLine[self.EGIDColumn] != '-' and re.match(r"^[A-Z]{2}[_]([0-9]*)$", newLine[self.BDIDColumn].split(".")[0]) != None and newLine[self.BDIDColumn] != "NA": 
                #    geneidlist.append(newLine[self.EGIDColumn])
                #    bdidlist.append(newLine[self.BDIDColumn].split(".")[0])
                #    _index.append(i)
        #self.append(geneidlist, bdidlist, _index )
    
    def delDoublon(self):
        self.dataframe.drop_duplicates(['EGID', 'BDID'], keep='first')
        
    def write(self):
        self.dataframe.to_csv('EntrezGeneToRefSeq_transcript.txt', header=None, index=None, sep='\t', mode='w')
        
    
        
    def process(self):
        #t0=time.time()
        #self.count()
        #print self.number
        #print (time.time() - t0), "seconds row count times"
        
        self.reading()
        t0=time.time()
        pandas.concat(self.dataframe).drop_duplicates(['EGID', 'GRT'], keep='first').to_csv('testttt', header=None, index=None, sep='\t', mode='w')
        print (time.time() - t0), "seconds row count times"    
        #self.concatenate()
        #self.delDoublon()
        #self.write()
        


t0=time.time()

convert(gene2accession,RefSeq_transcript,1,3,False).process()
print (time.time() - t0), "seconds 100 times"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    