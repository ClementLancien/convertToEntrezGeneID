# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:15:47 2017

@author: clancien
"""

import re
import time
import ConfigParser
import tqdm

config = ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))

gene2accession = config.get('Download', 'gene2accession')
GenBank_transcript = config.get('Convert', 'GenBank_transcript')
RefSeq_transcript = config.get('Convert', 'RefSeq_transcript')
GenBank_protein = config.get('Convert', 'GenBank_protein')
RefSeq_protein = config.get('Convert', 'RefSeq_protein')
GI_transcript = config.get('Convert', 'GI_transcript')
GI_protein = config.get('Convert', 'GI_protein')

def filesAccession():
    
    """Create 6 files from gene2Accession :
            - Entrez_GeneToGenBank_transcript
            - Entrez_GeneToGenBank_protein
            - Entrez_GeneToRefSeq_transcript
            - Entrez_GeneToRefSeq_protein
            - Entrez_GeneToGI_transcript
            - Entrez_GeneToGI_protein
    
       For each file :
            
               _____________________ _____________________
              |                     |                     |
              |      Column_1       |      Column_2       |
              |_____________________|_____________________|
              |                     |                     |
              |   Entrez_Gene_IDs   |        BDID         |
              |_____________________|_____________________|
              
           
    """
    
    with open(gene2accession , 'r') as accession,\
    open(GenBank_transcript, 'w') as gtranscript,\
    open(RefSeq_transcript, 'w') as rtranscript,\
    open(GenBank_protein, 'w') as gprotein,\
    open(RefSeq_protein, 'w') as rprotein,\
    open(GI_transcript, 'w') as GItranscript,\
    open(GI_protein, 'w') as GIprotein:

###################################################################################
#                                                                                 #
#                                                                                 #
#                       Index Value of columns we need                            #  
#                                                                                 # 
#                                                                                 #
###################################################################################

        header_line=next(accession)
        header_line= header_line.split("\t")
        GeneID_index = header_line.index('GeneID')
        RefSeq_transcript_index = header_line.index('RNA_nucleotide_accession.version')
        RefSeq_protein_index = header_line.index('protein_accession.version')
        GItranscript_index = header_line.index('RNA_nucleotide_gi')
        GIprotein_index = header_line.index('protein_gi')

#################################################################################################################################################################################
#
#
#
#Pour GenBank_transcript 4 identifiants ne sont pas rangés à la suite (Peut etre pareil pour refseq etc) :
#
#       - X69913
#       - X68289
#       - X69154
#       - X58564
#
# ==> Du coup on utilise des listes de 3 identifiants (previous max=3)
#               ==> Perte de ?10000? iteration/sec 
#
#Pour checker doublon (apres indexation bien sur) dans MongoDB utiliser la commande suivante :
#
#   db.collection.aggregate([{
#       "$group":{
#                   "_id": {"GeneID":"$GeneID", "BDID":"$BDID"},
#                   "uniqueIds":{"$addToSet":"$_id"},
#                   "count":{"$sum":1}}},{
#       "$match":{
#                   "count":{"$gt":1}}
#       }],
#   {allowDiskUse :true}) # permet de creer des fichier temporaires pour effectuer la requete (necessaire pour des collections tres volumineuses)
#
# sur 1 ligne : db.GenBank_transcript.aggregate([{"$group" : { "_id": {"GeneID":"$GeneID", "BDID":"$BDID"},"uniqueIds":{"$addToSet":"$_id"},"count":{"$sum":1}}},{"$match":{"count":{"$gt":1}}}],{allowDiskUse :true})
#
#   collection =[
#               "GenBank_transcript",
#               "GenBank_protein",
#               "RefSeq_transcript",
#               "RefSeq_protein",
#               "GI_transcript",
#               "GI_protein"]
#
#
#




        

        previous_refseqt=[]
        previous_refseqp=[]
        previous_git=[]
        previous_gip=[]
             
        for line in tqdm.tqdm(accession, 'Time for loop of accessionConversion'):
            lineList= line.split("\t")
            gid=str(lineList[GeneID_index])

            
            
            if(gid != "-"  ):
                refseqt= str(lineList[RefSeq_transcript_index].split(".")[0])
                refseqp= str(lineList[RefSeq_protein_index].split(".")[0])
                gip=str(lineList[GIprotein_index])
                git=str(lineList[GItranscript_index])
                if refseqt != '-' and refseqt not in previous_refseqt:
                    
                    if(re.match(r"^[A-Z]{2}[_]([0-9]*)$",refseqt) ):
                        rtranscript.write(gid + "\t" + refseqt + "\n")
                    else:
                        gtranscript.write(gid + "\t" + refseqt + "\n")
                
                
                if refseqp != '-' and refseqp not in previous_refseqp:
                    if(re.match(r"^[A-Z]{2}[_]([0-9]*)$",refseqp)):
                        rprotein.write(gid + "\t" + refseqp + "\n")
                    else:
                        gprotein.write(gid + "\t" + refseqp + "\n")
            
                if(re.match(r"(^[0-9]*)$",git) and git not in previous_git):
                    GItranscript.write(gid + "\t" + git + "\n")
                    
                if(re.match(r"(^[0-9]*)$",gip) and gip not in previous_gip):
                    GIprotein.write(gid + "\t" + gip + "\n")
                    
                if len(previous_refseqt) < 3:
                    previous_refseqt.append(refseqt)
                    previous_refseqp.append(refseqp)
                    previous_git.append(git)
                    previous_gip.append(gip)
                else:
                    del previous_refseqt[0]
                    del previous_refseqp[0]
                    del previous_git[0]
                    del previous_gip[0]
                    previous_refseqt.append(refseqt)
                    previous_refseqp.append(refseqp)
                    previous_git.append(git)
                    previous_gip.append(gip)
                    

            ##    previous_Symbol = symbol

t0 = time.time()
filesAccession()

print time.time() - t0, "seconds wall time"
