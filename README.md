EntrezGene
==========

[comment]: <> (https://rozaxe.github.io/factory/)
[![Stable v0.1.0](https://img.shields.io/badge/Stable-v0.1.0-green.svg)](https://github.com/ClementLancien/convertToEntrezGeneID)
[![Release v0.1.0](https://img.shields.io/badge/Release-v0.1.0-blue.svg)](https://github.com/ClementLancien/convertToEntrezGeneID)
[![Python v>=2.7.0](https://img.shields.io/badge/Python-v>=2.7.0-0077ea.svg)](https://www.python.org/)
[![Dependencies pandas](https://img.shields.io/badge/Dependencies-pandas-cc9900.svg)](https://pandas.pydata.org/)
[![Dependencies pymongo](https://img.shields.io/badge/Dependencies-pymongo-cc9900.svg)](https://docs.mongodb.com/getting-started/python/insert/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

These scripts are used to create the GeneULike DataBase. They download then extract different biological database files to get the identifier of the database associated with unique Entre Gene identiifier.

Status
======

Completed

Table of contents
=================

1. [What is EntrezGene?](#what-is-entrezgene)
2. [Data File Structure](#data-file-structure)
3. [Tree Structure Data Folder](#tree-structure-data-folder)
4. [Code informations](#code-informations)
4. [Requirements](#requirements)

What is EntrezGene?
====================

EntrezGene is a script which allow you to download database file like Ensembl, UniGene, Accession, GeneInfo, GPL (GEO), HomoloGene, Vega, History, SwissProt, trEMBL.

Each File as its own structure multiple column with header or not. The goal is to extract the column named Entrez Gene ID and Gene ID


From these files, Entrez Gene extract and create the following files :

- Entrez_GeneToGenBank_protein

- Entrez_GeneToGenBank_transcript

- Entrez_GeneToGI_protein

- Entrez_GeneToGI_transcript

- Entrez_GeneToRefSeq_protein

- Entrez_GeneToRefSeq_transcript

- Entrez_GeneToEnsembl_gene

- Entrez_GeneToEnsembl_transcript

- Entrez_GeneToEnsembl_protein

- Entrez_GeneToGPL (merge all GPL Files)

- Entrez_GeneToHistory

- Entrez_GeneToHomoloGene

- Entrez_GeneToInfo

- Entrez_GeneToSwissProt

- Entrez_GeneTotrEMBL

- Entrez_GeneToUniGene

- Entrez_GeneToVega_gene

- Entrez_GeneToVega_transcript

- Entrez_GeneToVega_protein

Data File Structure
===================

All files are tab separated.

|             Files		|      Entrez Gene ID      |      DataBase ID      |        Tax ID        |      Description     |       Platform       |       Platform Title       |       Organism       |
|:------------------------------|:------------------------:|:---------------------:|:--------------------:|:--------------------:|:--------------------:|:--------------------------:|:--------------------:|
|Entrez_GeneToGenBank_protein	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToGenBank_transcript|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToGI_protein	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToGI_transcript	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToRefSeq_protein	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToRefSeq_transcript	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToEnsembl_gene	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToEnsembl_transcript|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToEnsembl_protein	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToGPL		|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |  :white_check_mark:  |     :white_check_mark:     |  :white_check_mark:  |
|Entrez_GeneToHistory		|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToHomoloGene	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToInfo		|    :white_check_mark:    |   :white_check_mark:  |  :white_check_mark:  |  :white_check_mark:  |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToSwissProt		|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneTotrEMBL		|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToUniGene		|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToVega_gene		|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToVega_transcript	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |
|Entrez_GeneToVega_protein	|    :white_check_mark:    |   :white_check_mark:  |   :no_entry_sign:    |   :no_entry_sign:    |   :no_entry_sign:    |      :no_entry_sign:       |   :no_entry_sign:    |


Tree Structure Data Folder 
==========================

Path to where files are downloaded and where information from these files are extracted.


```
Data
├──accession
|   ├──convert
|   |  └──accession .(tsv)
|   └──raw
|      ├──Entrez_GeneToGenBank_protein (.tsv)
|      ├──Entrez_GeneToGenBank_transcript (.tsv)
|      ├──Entrez_GeneToGI_protein (.tsv)
|      ├──Entrez_GeneToGI_transcript (.tsv)
|      ├──Entrez_GeneToRefSeq_protein (.tsv)
|      └──Entrez_GeneToRefSeq_transcript (.tsv)
|
├──ensembl
|   ├──convert
|   |  └──ensembl (.tsv)
|   └──raw
|      ├──Entrez_GeneToEnsembl_gene (.tsv)
|      ├──Entrez_GeneToEnsembl_protein (.tsv)
|      └──Entrez_GeneToEnsembl_transcript (.tsv)
|
├──gpl
|   ├──convert
|   |  └──all gpl files
|   └──raw
|      └──Entrez_GeneToGPL (.tsv)
|
├──history
|   ├──convert
|   |  └──history (.tsv)
|   └──raw
|      └──Entrez_GeneToHistory (.tsv)
|
├──homologene
|   ├──convert
|   |  └──homologene (.tsv)
|   └──raw
|      └──Entrez_GeneToHomoloGene (.tsv)
|
├──info
|   ├──convert
|   |  └──info (.tsv)
|   └──raw
|      └──Entrez_GeneToInfo (.tsv)
|
├──swissprot
|   ├──convert
|   |  └──swissprot
|   └──raw
|      └──Entrez_GeneToSwissProt (.tsv)
|
├──trembl
|   ├──convert
|   |  └──trembl
|   └──raw
|      └──Entrez_GeneTotrEMBL (.tsv)
|
├──unigene
|   ├──convert
|   |  └──unigene (.tsv)
|   └──raw
|      └──Entrez_GeneToUniGene (.tsv)
|
└──vega
    ├──convert
    |  └──vega (.tsv)
    └──raw
       ├──Entrez_GeneToVega_gene (.tsv)
       ├──Entrez_GeneToVega_transcript (.tsv)
       └──Entrez_GeneToVega_protein (.tsv)
```
Code Informations
=================

```python

dataframe=[]

# We open the file named Filename, which have a header's row at the first line of the file (0). The file is
# tab separated.
# dtype = 'str' ==> We told to pandas to read each columns has str
# Have to be precise, if you precise in the loop. Pandas is going to guess the type of each column (slow)
# chunksize=size ==> pandas is going to read the file by chunk. The chunksize can be precise.
# Example : if we have a dimension table equals to 10 (square matix) and a chunksize of 5
# pandas takes the 5 first row in a table then at each loop take the other 5 etc...
# usecols =[int,int] is used to select the column by index we want to extract from the files

for df in pandas.read_csv(Filename, header=0, sep="\t", usecols=[int ,int], dtype='str', chunksize=size):

	# rename the column's names
	df.columns = ['EGID','BDID'] 

	#reorder coloumn order BDID, EGID to EGID, BDID
        df = df[['EGID', 'BDID']]
	
	# In some column the database identifier can been versionning
	"""We can have 
                              EGID                  BDID
                   0        145035              853878.1
                   1       5478012             2539804.1
                   2       8759258             2539380.1
                   3       2335981              851398.1
                   4        362589              856787.1
                   5      23568987              852821.1
                   6      23568797              852092.1
                   7      78935468             2540239.1

                   
           We want to remove each versionning :
                   
                              EGID                  BDID
                   0        145035                853878
                   1       5478012               2539804
                   2       8759258               2539380
                   3       2335981                851398
                   4        362589                856787
                   5      23568987                852821
                   6      23568797                852092
                   7      78935468               2540239
	"""

	df['BDID'] = df['BDID'].str.replace('[.][0-9]+','')
	

	""""
	   We can have in some file separator inside a column 

                                                         EGID           BDID
                   0                                   853878     1769308_at
                   1                                  2539804     1769309_at
                   2                                  2539380     1769310_at                                
                   3                                   851398     1769311_at
                   4                                   856787     1769312_at
                   5                                   852821     1769313_at                                 
                   6                                   852092     1769314_at 
                   7                                  2540239     1769315_at
                   8    2543353///2541576///2541564///2541343   1769316_s_at
                   
                   We want to split line 8 to obtain :
                   
                               EGID         BDID
                   0         853878     1769308_at   
                   1        2539804     1769309_at
                   2        2539380     1769310_at  
                   3         851398     1769311_at   
                   4         856787     1769312_at   
                   5         852821     1769313_at   
                   6         852092     1769314_at   
                   7        2540239     1769315_at  
                   8        2543353   1769316_s_at  
                   9        2541576   1769316_s_at  
                   10       2541564   1769316_s_at  
                   11       2541343   1769316_s_at  
                  
                   So : 
                   
   	"""

	df = df.set_index(df.columns.drop('EGID',2).tolist())\
                         .EGID.str.split('///', expand=True)\
                         .stack()\
                         .reset_index()\
                         .rename(columns={0:'EGID'})\
                         .loc[:, df.columns]

	# When df is correctly defined and each separator or versionning has been remove
	# We add df to our list dataframe
	# We add only the lines in df where df['EGID'] is equal to a regex, same for df['BDID]' and df['BDID'] != '-'
	# flags=re.IGNORECASE ignore the case sensitivity. (DO NOT FORGET TO IMPORT re)
	# Rennes != rennes with re.IGNORECASE Rennes == rennes
	# When we do not want that a cell value match a regex we add tild (~) before
	# ~False == True ==> True

	dataframe.append(df[
                              (df['EGID'].str.match('^[0-9]+$', flags=re.IGNORECASE))  &
                              (df['BDID'] != '-') &
                              (~df['BDID'].str.match('^[A-Z]{2}[_][0-9]+$', flags=re.IGNORECASE))           
                           ])

# After we read all the files
# we concatenate each dataframe then
# we drop_duplicates : we don not want to have 2 identicals lines (keep = 'first' keep the first occurence) then
# we write the concatenata dataframe without duplicates in a new file, named here FileToSave
# in the file we have :
#	- no header (header=None)
# 	- no index (index=None)
# The file is tab separated

pandas.concat(dataframe).drop_duplicates(['EGID', 'BDID'], keep='first').to_csv(FileToSave, header=None, index=None, sep='\t', mode='w')


```
Requirements
============

pandas==0.17.1
pymongo==2.7.2

