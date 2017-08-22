# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 16:07:57 2017

@author: clancien
"""

import time
import tqdm
from pymongo import MongoClient



import ConfigParser
import pymongo
config= ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))


#Concatenation_Entrez=config.get('Convert','Concatenation_Entrez')

Ensembl_gene=config.get('Convert','Ensembl_gene')#
Ensembl_transcript=config.get('Convert','Ensembl_transcript')#
Ensembl_protein=config.get('Convert','Ensembl_protein')#
UniGene=config.get('Convert','UniGene')#

vega_gene=config.get('Convert','vega_gene')#
vega_transcript=config.get('Convert','vega_transcript')#
vega_protein=config.get('Convert','vega_protein')#

gene2gene=config.get('Convert','gene2gene')

GenBank_transcript=config.get('Convert','GenBank_transcript')#
RefSeq_transcript=config.get('Convert','RefSeq_transcript')#
GenBank_protein=config.get('Convert','GenBank_protein')#
RefSeq_protein=config.get('Convert','RefSeq_protein')#

GI_transcript=config.get('Convert','GI_transcript')#
GI_protein=config.get('Convert','GI_protein')#


HomoloGene=config.get('Convert','HomoloGene')#

Swissprot=config.get('Convert', 'UniProtKB_sprot')#
trEMBL=config.get('Convert', 'trEmblID')#

GPL=config.get('Convert','GPL_all')#
Entrez_GeneInfo=config.get('Convert','Entrez_GeneInfo')#

#client = MongoClient()
#db=client["geneulike"]   
#db['GeneInfo'].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
#my_collection.create_index([("type", pymongo.ASCENDING),("amount", pymongo.ASCENDING),("loss", pymongo.ASCENDING),("price", pymongo.ASCENDING),("create_date", pymongo.ASCENDING)], unique=True)
collection={
            'Ensembl_gene' : Ensembl_gene,
            'Ensembl_transcript' : Ensembl_transcript,
            'Ensembl_protein': Ensembl_protein,
            'UniGene' : UniGene,
            'Vega_gene' :vega_gene,
            'Vega_transcript': vega_transcript,
            'Vega_protein' : vega_protein,
            'GenBank_transcript' : GenBank_transcript,
            'RefSeq_transcript' : RefSeq_transcript,
            'GenBank_protein' : GenBank_protein,
            'RefSeq_protein' :RefSeq_protein,
            'GI_transcript' : GI_transcript,
            'GI_protein' : GI_protein,
            'UniProt' : 'toto',
            'GPL' : GPL
            }
            
def GeneInfo():
    #t0=time.time()
    client = MongoClient()
    db=client["geneulike"]    


    _list={}
    
    _range=0
    with open(Entrez_GeneInfo , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
            _range+=1
            
            newList=line.split("\t")
            _list[newList[0]]=[newList[1],newList[2], newList[4]]
            if _range == 100000:


                result=db.HomoloGene.find({'GeneID': {"$in" :_list.keys()}})
                eltToInsert=[]
                notfound=[]
                for elt in result:
                    notfound.append(elt['GeneID'])
                    eltToInsert.append({
                    'GeneID':elt['GeneID'],
                    'GeneName':_list[elt['GeneID']][1],
                    'GeneDescription':_list[elt['GeneID']][2],
                    'TaxID':_list[elt['GeneID']][0],
                    'HomoloGene':elt['BDID']
                    
                    })
                notfound=list(set(_list.keys()).symmetric_difference(set(notfound)))               
                for elt in notfound:
                    eltToInsert.append({
                    'GeneID':elt,
                    'GeneName':_list[elt][1],
                    'GeneDescription':_list[elt][2],
                    'TaxID':_list[elt][0],
                    'HomoloGene':'-'
                    
                    })
                db['GeneInfo'].insert(eltToInsert)

                _list={}
                _range=0
                
        result=db.HomoloGene.find({'GeneID': {"$in" :_list.keys()}})
        eltToInsert=[]
        notfound=[]
        for elt in result:
            notfound.append(elt['GeneID'])
            eltToInsert.append({
                    'GeneID':elt['GeneID'],
                    'GeneName':_list[elt['GeneID']][1],
                    'GeneDescription':_list[elt['GeneID']][2],
                    'TaxID':_list[elt['GeneID']][0],
                    'HomoloGene':elt['BDID']
                    
                    })
        notfound=list(set(_list.keys()).symmetric_difference(set(notfound)))               
        for elt in notfound:
            eltToInsert.append({
                    'GeneID':elt,
                    'GeneName':_list[elt][1],
                    'GeneDescription':_list[elt][2],
                    'TaxID':_list[elt][0],
                    'HomoloGene':'-'
                    
                    })
        db['GeneInfo'].insert(eltToInsert)

        _list={}
        _range=0
        db['GeneInfo'].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
t1=time.time()        
t0=time.time()
#GeneInfo()
print time.time() - t0, "seconds wall time"
def pushGPL():

    client = MongoClient()
    db=client["geneulike"]    
    _list=[]
    _range=0
    with open(GPL , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of GPL "):
            _range+=1
            
            newList=line.split("\t")
            _list.append([newList[0],newList[1],newList[2],newList[3].split("\n")[0]])
        
            if _range == 100000:
                insert=[]
                for elt in _list:
                    insert.append({
                    'GeneID':elt[0],
                    'GPLcode':elt[1],
                    'BDID':elt[2],
                    'GPLname':elt[3],
                    })
                db['GPL'].insert(insert)
                _range=0
                _list=[]
                
                
                
        insert=[]        
        for elt in _list:
            insert.append({
                    'GeneID':elt[0],
                    'GPLcode':elt[1],
                    'BDID':elt[2],
                    'GPLname':elt[3],
                    })
        db['GPL'].insert(insert)
        _range=0
        _list=[]
               
    #db['GPL'].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
                
t0=time.time()
#pushGPL()
print time.time() - t0, "seconds wall time"
#db.GI_protein.aggregate({"$group" : { "_id": "$BDID", "count": { "$sum": 1 } } },{"$match": {"_id" :{ "$ne" : null } , "count" : {"$gt": 1} } }, {"$project": {"BDID" : "$_id", "_id" : 0} },{"$sort": {"count" : -1} })

#db.GI_protein.aggregate([{$group : { _id: "$BDID", count: { $sum: 1 } } },{$match: {_id:{ $ne : null } , count : {$gt: 1} } }, {$project: {"BDID" : $_id, "_id" : 0} },{$sort: {count : -1} }])

#db.Wall.aggregate([{$group : { _id: "$event_time" ,  count : { $sum: 1}}},{$match : { count : { $gt : 1 } }} ])

def push(_file,collection):

    client = MongoClient()
    db=client["geneulike"]    
    _list=[]
    _range=0
    with open(_file , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of "+collection+" "):
            _range+=1
            
            newList=line.split("\t")
            _list.append([newList[0],newList[2].split("\n")[0]])
            if _range == 100000:
                insert=[]
                for elt in _list:
                    insert.append({
                    'GeneID':elt[0],
                    'BDID':elt[1],
                    })  

                db[collection].insert(insert)
                _range=0
                _list=[]
                
        insert=[]
        for elt in _list:
            insert.append({
                    'GeneID':elt[0],
                    'BDID':elt[1],
                    })  

        db[collection].insert(insert)
        _range=0
        _list=[]
    #db[collection].create_index([("GeneID",pymongo.ASCENDING)],unique=True)   
                

t0=time.time()

#push(vega_gene,'Vega_gene')
#push(vega_protein,'Vega_protein')
#push(vega_transcript,'Vega_transcript')

#push(UniGene,'UniGene')
print time.time() - t0, "seconds wall time"

#db.Ensembl_gene.aggregate({"$group" : { "_id": "$BDID", "count": { "$sum": 1 }}},{"$match":{"count":{"$gt":1}}})

def _push(_file,collection):

    client = MongoClient()
    db=client["geneulike"]    
    _list=[]
    _range=0
    with open(_file , 'r') as infile:
        for line in tqdm.tqdm(infile,"Time for loop of "+collection+" "):
            _range+=1
            
            newList=line.split("\t")
            _list.append([newList[0],newList[1].split("\n")[0]])
            if _range == 100000:
                insert=[]
                for elt in _list:
                    insert.append({
                    'GeneID':elt[0],
                    'BDID':elt[1],

                    })  

                db[collection].insert(insert)
                _range=0
                _list=[]
        insert=[]
        for elt in _list:
            insert.append({
                    'GeneID':elt[0],
                    'BDID':elt[1],
                    })  

        db[collection].insert(insert)
        _range=0
        _list=[]
    #db[collection].create_index([("GeneID",pymongo.ASCENDING)],unique=True)   


t0=time.time()
#_push(Ensembl_gene,'Ensembl_gene')
#_push(Ensembl_transcript,'Ensembl_transcript')
#_push(Ensembl_protein,'Ensembl_protein')
#_push(GenBank_transcript,'GenBank_transcript')
_push(RefSeq_transcript,'RefSeq_transcript')
#_push(RefSeq_protein,'RefSeq_protein')
#_push(GenBank_protein,'GenBank_protein')
#_push(GI_transcript,'GI_transcript')
#_push(GI_protein,'GI_protein')
#_push(Swissprot,'Uniprot')
#_push(trEMBL,'Uniprot')
print time.time() - t0, "seconds wall time"
print "FINAL TIME : ", time.time() - t1, "seconds wall time"









# def pushGPL():

#     client = MongoClient()
#     db=client["geneulike"]    
#     _list=[]
#     _listGene=[]
#     _range=0
#     with open(GPL , 'r') as infile:
#         for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
#             _range+=1
            
#             newList=line.split("\t")
#             _list.append([newList[0],newList[1],newList[2],newList[3].split("\n")[0]])
#             _listGene.append(newList[0])
#             if _range == 100000:
#                 resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#                 homologene={}
#                 for elt in resultH:
#                     homologene[elt['GeneID']] = elt['BDID']
            
#                 resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#                 info={}
#                 for elt in resultI:
#                     info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#                 eltToInsert=[]
#                 for elt in _list:
#                     try:
#                         _homologene=homologene[elt[0]]
#                     except:
#                         _homologene='-'
#                     try:
#                         _info=info[elt[0]]
#                         genename=_info[0]
#                         genedescription=_info[1]
#                         taxid=_info[2]
#                     except:
#                         genename='-'
#                         genedescription='-'
#                         taxid='-'
#                     eltToInsert.append({
#                     'GeneID':elt[0],
#                     'GPLcode':elt[1],
#                     'BDID':elt[2],
#                     'GPLname':elt[3],
#                     'Homologene':_homologene,
#                     'GeneName':genename,
#                     'GeneDescription':genedescription,
#                     'TaxID':taxid
#                     })  
#                 #print '100000 : ', len(eltToInsert)
#                 #return
#                 db['GPL'].insert(eltToInsert)
#                 _range=0
#                 _list=[]
#                 _listGene=[]
                
                
#         resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#         homologene={}
#         for elt in resultH:
#             homologene[elt['GeneID']] = elt['BDID']
            
#         resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#         info={}
#         for elt in resultI:
#             info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#         eltToInsert=[]
#         for elt in _list:
#             try:
#                 _homologene=homologene[elt[0]]
#             except:
#                 _homologene='-'
#             try:
#                 _info=info[elt[0]]
#                 genename=_info[0]
#                 genedescription=_info[1]
#                 taxid=_info[2]
#             except:
#                 genename='-'
#                 genedescription='-'
#                 taxid='-'
#             eltToInsert.append({
#             'GeneID':elt[0],
#             'GPLcode':elt[1],
#             'BDID':elt[2],
#             'GPLname':elt[3],
#             'Homologene':_homologene,
#             'GeneName':genename,
#             'GeneDescription':genedescription,
#             'TaxID':taxid
#             })  

#         db['GPL'].insert(eltToInsert)
#         _range=0
#         _list=[]
#         _listGene=[]
#         db['GPL'].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
                
# t0=time.time()
# pushGPL()
# print time.time() - t0, "seconds wall time"

# def pushEnsembl_gene():

#     client = MongoClient()
#     db=client["geneulike"]    
#     _list=[]
#     _listGene=[]
#     _range=0
#     with open(Ensembl_gene , 'r') as infile:
#         for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
#             _range+=1
            
#             newList=line.split("\t")
#             _list.append([newList[0],newList[2].split("\n")[0]])
#             _listGene.append(newList[0])
#             if _range == 100000:
#                 resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#                 homologene={}
#                 for elt in resultH:
#                     homologene[elt['GeneID']] = elt['BDID']
            
#                 resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#                 info={}
#                 for elt in resultI:
#                     info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#                 eltToInsert=[]
#                 for elt in _list:
#                     try:
#                         _homologene=homologene[elt[0]]
#                     except:
#                         _homologene='-'
#                     try:
#                         _info=info[elt[0]]
#                         genename=_info[0]
#                         genedescription=_info[1]
#                         taxid=_info[2]
#                     except:
#                         genename='-'
#                         genedescription='-'
#                         taxid='-'
#                     eltToInsert.append({
#                     'GeneID':elt[0],
#                     'BDID':elt[1],
#                     'Homologene':_homologene,
#                     'GeneName':genename,
#                     'GeneDescription':genedescription,
#                     'TaxID':taxid
#                     })  
#                 #print '100000 : ', len(eltToInsert)
#                 #return
#                 db['Ensembl_gene'].insert(eltToInsert)
#                 _range=0
#                 _list=[]
#                 _listGene=[]
                
                
#         resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#         homologene={}
#         for elt in resultH:
#             homologene[elt['GeneID']] = elt['BDID']
            
#         resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#         info={}
#         for elt in resultI:
#             info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#         eltToInsert=[]
#         for elt in _list:
#             try:
#                 _homologene=homologene[elt[0]]
#             except:
#                 _homologene='-'
#             try:
#                 _info=info[elt[0]]
#                 genename=_info[0]
#                 genedescription=_info[1]
#                 taxid=_info[2]
#             except:
#                 genename='-'
#                 genedescription='-'
#                 taxid='-'
#             eltToInsert.append({
#             'GeneID':elt[0],
#             'BDID':elt[1],
#             'Homologene':_homologene,
#             'GeneName':genename,
#             'GeneDescription':genedescription,
#             'TaxID':taxid
#             })  

#         db['Ensembl_gene'].insert(eltToInsert)
#         _range=0
#         _list=[]
#         _listGene=[]
#         db['Ensembl_gene'].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
                
# t0=time.time()
# pushEnsembl_gene()
# print time.time() - t0, "seconds wall time"


# def pushEnsembl_protein():

#     client = MongoClient()
#     db=client["geneulike"]    
#     _list=[]
#     _listGene=[]
#     _range=0
#     with open(Ensembl_protein , 'r') as infile:
#         for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
#             _range+=1
            
#             newList=line.split("\t")
#             _list.append([newList[0],newList[2].split("\n")[0]])
#             _listGene.append(newList[0])
#             if _range == 100000:
#                 resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#                 homologene={}
#                 for elt in resultH:
#                     homologene[elt['GeneID']] = elt['BDID']
            
#                 resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#                 info={}
#                 for elt in resultI:
#                     info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#                 eltToInsert=[]
#                 for elt in _list:
#                     try:
#                         _homologene=homologene[elt[0]]
#                     except:
#                         _homologene='-'
#                     try:
#                         _info=info[elt[0]]
#                         genename=_info[0]
#                         genedescription=_info[1]
#                         taxid=_info[2]
#                     except:
#                         genename='-'
#                         genedescription='-'
#                         taxid='-'
#                     eltToInsert.append({
#                     'GeneID':elt[0],
#                     'BDID':elt[1],
#                     'Homologene':_homologene,
#                     'GeneName':genename,
#                     'GeneDescription':genedescription,
#                     'TaxID':taxid
#                     })  
#                 #print '100000 : ', len(eltToInsert)
#                 #return
#                 db['Ensembl_protein'].insert(eltToInsert)
#                 _range=0
#                 _list=[]
#                 _listGene=[]
                
                
#         resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#         homologene={}
#         for elt in resultH:
#             homologene[elt['GeneID']] = elt['BDID']
            
#         resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#         info={}
#         for elt in resultI:
#             info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#         eltToInsert=[]
#         for elt in _list:
#             try:
#                 _homologene=homologene[elt[0]]
#             except:
#                 _homologene='-'
#             try:
#                 _info=info[elt[0]]
#                 genename=_info[0]
#                 genedescription=_info[1]
#                 taxid=_info[2]
#             except:
#                 genename='-'
#                 genedescription='-'
#                 taxid='-'
#             eltToInsert.append({
#             'GeneID':elt[0],
#             'BDID':elt[1],
#             'Homologene':_homologene,
#             'GeneName':genename,
#             'GeneDescription':genedescription,
#             'TaxID':taxid
#             })  

#         db['Ensembl_protein'].insert(eltToInsert)
#         _range=0
#         _list=[]
#         _listGene=[]
#         db['Ensembl_protein'].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
                
# t0=time.time()
# pushEnsembl_protein()
# print time.time() - t0, "seconds wall time"

# def pushEnsembl_transcript():

#     client = MongoClient()
#     db=client["geneulike"]    
#     _list=[]
#     _listGene=[]
#     _range=0
#     with open(Ensembl_transcript , 'r') as infile:
#         for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
#             _range+=1
            
#             newList=line.split("\t")
#             _list.append([newList[0],newList[2].split("\n")[0]])
#             _listGene.append(newList[0])
#             if _range == 100000:
#                 resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#                 homologene={}
#                 for elt in resultH:
#                     homologene[elt['GeneID']] = elt['BDID']
            
#                 resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#                 info={}
#                 for elt in resultI:
#                     info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#                 eltToInsert=[]
#                 for elt in _list:
#                     try:
#                         _homologene=homologene[elt[0]]
#                     except:
#                         _homologene='-'
#                     try:
#                         _info=info[elt[0]]
#                         genename=_info[0]
#                         genedescription=_info[1]
#                         taxid=_info[2]
#                     except:
#                         genename='-'
#                         genedescription='-'
#                         taxid='-'
#                     eltToInsert.append({
#                     'GeneID':elt[0],
#                     'BDID':elt[1],
#                     'Homologene':_homologene,
#                     'GeneName':genename,
#                     'GeneDescription':genedescription,
#                     'TaxID':taxid
#                     })  
#                 #print '100000 : ', len(eltToInsert)
#                 #return
#                 db['Ensembl_transcript'].insert(eltToInsert)
#                 _range=0
#                 _list=[]
#                 _listGene=[]
                
                
#         resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#         homologene={}
#         for elt in resultH:
#             homologene[elt['GeneID']] = elt['BDID']
            
#         resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#         info={}
#         for elt in resultI:
#             info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#         eltToInsert=[]
#         for elt in _list:
#             try:
#                 _homologene=homologene[elt[0]]
#             except:
#                 _homologene='-'
#             try:
#                 _info=info[elt[0]]
#                 genename=_info[0]
#                 genedescription=_info[1]
#                 taxid=_info[2]
#             except:
#                 genename='-'
#                 genedescription='-'
#                 taxid='-'
#             eltToInsert.append({
#             'GeneID':elt[0],
#             'BDID':elt[1],
#             'Homologene':_homologene,
#             'GeneName':genename,
#             'GeneDescription':genedescription,
#             'TaxID':taxid
#             })  

#         db['Ensembl_transcript'].insert(eltToInsert)
#         _range=0
#         _list=[]
#         _listGene=[]
#         db['Ensembl_transcript'].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
# t0=time.time()
# pushEnsembl_transcript()
# print time.time() - t0, "seconds wall time"

# def pushVega(_file,collection):

#     client = MongoClient()
#     db=client["geneulike"]    
#     _list=[]
#     _listGene=[]
#     _range=0
#     with open(_file , 'r') as infile:
#         for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
#             _range+=1
            
#             newList=line.split("\t")
#             _list.append([newList[0],newList[2].split("\n")[0]])
#             _listGene.append(newList[0])
#             if _range == 100000:
#                 resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#                 homologene={}
#                 for elt in resultH:
#                     homologene[elt['GeneID']] = elt['BDID']
            
#                 resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#                 info={}
#                 for elt in resultI:
#                     info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#                 eltToInsert=[]
#                 for elt in _list:
#                     try:
#                         _homologene=homologene[elt[0]]
#                     except:
#                         _homologene='-'
#                     try:
#                         _info=info[elt[0]]
#                         genename=_info[0]
#                         genedescription=_info[1]
#                         taxid=_info[2]
#                     except:
#                         genename='-'
#                         genedescription='-'
#                         taxid='-'
#                     eltToInsert.append({
#                     'GeneID':elt[0],
#                     'BDID':elt[1],
#                     'Homologene':_homologene,
#                     'GeneName':genename,
#                     'GeneDescription':genedescription,
#                     'TaxID':taxid
#                     })  
#                 #print '100000 : ', len(eltToInsert)
#                 #return
#                 db[collection].insert(eltToInsert)
#                 _range=0
#                 _list=[]
#                 _listGene=[]
                
                
#         resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#         homologene={}
#         for elt in resultH:
#             homologene[elt['GeneID']] = elt['BDID']
            
#         resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#         info={}
#         for elt in resultI:
#             info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#         eltToInsert=[]
#         for elt in _list:
#             try:
#                 _homologene=homologene[elt[0]]
#             except:
#                 _homologene='-'
#             try:
#                 _info=info[elt[0]]
#                 genename=_info[0]
#                 genedescription=_info[1]
#                 taxid=_info[2]
#             except:
#                 genename='-'
#                 genedescription='-'
#                 taxid='-'
#             eltToInsert.append({
#             'GeneID':elt[0],
#             'BDID':elt[1],
#             'Homologene':_homologene,
#             'GeneName':genename,
#             'GeneDescription':genedescription,
#             'TaxID':taxid
#             })  

#         db[collection].insert(eltToInsert)
#         _range=0
#         _list=[]
#         _listGene=[]
#         db[collection].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
# t0=time.time()
# pushVega(vega_gene,'Vega_gene')
# pushVega(vega_transcript,'Vega_transcript')
# pushVega(vega_protein,'Vega_protein')

# pushVega(GenBank_protein,'GenBank_protein')
# pushVega(GI_transcript,'GI_transcript')
# pushVega(GI_protein,'GI_protein')
# pushVega(UniGene,'UniGene')
# print time.time() - t0, "seconds wall time"

# def push(_file,collection):

#     client = MongoClient()
#     db=client["geneulike"]    
#     _list=[]
#     _listGene=[]
#     _range=0
#     with open(_file , 'r') as infile:
#         for line in tqdm.tqdm(infile,"Time for loop of EntrezCollectionCreation"):
#             _range+=1
            
#             newList=line.split("\t")
#             _list.append([newList[0],newList[1].split("\n")[0]])
#             _listGene.append(newList[0])
#             if _range == 100000:
#                 resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#                 homologene={}
#                 for elt in resultH:
#                     homologene[elt['GeneID']] = elt['BDID']
            
#                 resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#                 info={}
#                 for elt in resultI:
#                     info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#                 eltToInsert=[]
#                 for elt in _list:
#                     try:
#                         _homologene=homologene[elt[0]]
#                     except:
#                         _homologene='-'
#                     try:
#                         _info=info[elt[0]]
#                         genename=_info[0]
#                         genedescription=_info[1]
#                         taxid=_info[2]
#                     except:
#                         genename='-'
#                         genedescription='-'
#                         taxid='-'
#                     eltToInsert.append({
#                     'GeneID':elt[0],
#                     'BDID':elt[1],
#                     'Homologene':_homologene,
#                     'GeneName':genename,
#                     'GeneDescription':genedescription,
#                     'TaxID':taxid
#                     })  
#                 #print '100000 : ', len(eltToInsert)
#                 #return
#                 db[collection].insert(eltToInsert)
#                 _range=0
#                 _list=[]
#                 _listGene=[]
                
                
#         resultH=db.HomoloGene.find({'GeneID': {"$in" :_listGene}})
#         homologene={}
#         for elt in resultH:
#             homologene[elt['GeneID']] = elt['BDID']
            
#         resultI=db.GeneInfo.find({'GeneID': {"$in" :_listGene}})
#         info={}
#         for elt in resultI:
#             info[elt['GeneID']] = [elt['GeneName'],elt['GeneDescription'],elt['TaxID']]
#         eltToInsert=[]
#         for elt in _list:
#             try:
#                 _homologene=homologene[elt[0]]
#             except:
#                 _homologene='-'
#             try:
#                 _info=info[elt[0]]
#                 genename=_info[0]
#                 genedescription=_info[1]
#                 taxid=_info[2]
#             except:
#                 genename='-'
#                 genedescription='-'
#                 taxid='-'
#             eltToInsert.append({
#             'GeneID':elt[0],
#             'BDID':elt[1],
#             'Homologene':_homologene,
#             'GeneName':genename,
#             'GeneDescription':genedescription,
#             'TaxID':taxid
#             })  

#         db[collection].insert(eltToInsert)
#         _range=0
#         _list=[]
#         _listGene=[]
#         db[collection].create_index([("GeneID",pymongo.ASCENDING)],unique=True)
# t0=time.time()
# push(GenBank_transcript,'GenBank_transcript')
# push(RefSeq_transcript,'RefSeq_transcript')
# push(RefSeq_protein,'RefSeq_protein')
# push(Swissprot,'Uniprot')
# push(trEMBL,'Uniprot')
# print time.time() - t0, "seconds wall time"
# print "FINAL TIME : ", time.time() - t0, "seconds wall time"