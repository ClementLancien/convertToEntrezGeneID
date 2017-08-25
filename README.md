EntrezGene : Download - Extract Column from Biological Database files
================================================

Status
======

Completed

Table of contents
=================

1. [What is EntrezGene ?](#what-is-entrezgene-?)
2. [Tree Structure Data Folder](#tree-structure-data-folder)



























1. What is EntrezGene ?
===================

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

  ​

Tree Structure Data Folder
=====================

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


