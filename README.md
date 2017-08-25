EntrezGene : Download - Extract Column from Biological Database files
================================================

[comment]: <> (https://rozaxe.github.io/factory/)
[![Stable v0.1.0](https://img.shields.io/badge/Stable-v0.1.0-blue.svg)](https://github.com/ClementLancien/convertToEntrezGeneID)
[![Release v0.1.0](https://img.shields.io/badge/Release-v0.1.0-blue.svg)](https://github.com/ClementLancien/convertToEntrezGeneID)
[![Python v2.7.0](https://img.shields.io/badge/Python-v2.7.0-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Status
======

Completed

Table of contents
=================

1. [What is EntrezGene?](#what-is-entrezgene?)
2. [Data File Structure](#data-file-structure)
3. [Tree Structure Data Folder](#tree-structure-data-folder)
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

Requirements
============

Panda==0.17.1


