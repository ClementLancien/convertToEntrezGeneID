# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:31:08 2017

@author: clancien
"""

import ftplib 

import time
import subprocess
GPL_path = '/home/clancien/Desktop/Fichier_Convert/GPL'
import gzip
import StringIO
import urllib2
import os
import tqdm
import ConfigParser
config=ConfigParser.ConfigParser()
config.readfp(open('../../../conf.ini','r'))
GPL_path=config.get('Download', 'GPL')

t0 = time.time()


def download(directory):
    host = "ftp.ncbi.nlm.nih.gov" # adresse du serveur FTP
    connect = ftplib.FTP(host, 'anonymous', 'anonymous') 
    connect.cwd("/geo/platforms")
    subdirectories_ = connect.nlst(directory)
    connect.quit()
    #connect.quit()
    i=0
    for sub in tqdm.tqdm(range(i,len(subdirectories_),i+35), "Time for loop of " + str(directory)):
        #print subdirectory,"\t", str(subdirectory.split("/")[1])
        host = "ftp.ncbi.nlm.nih.gov" # adresse du serveur FTP
        connect = ftplib.FTP(host, 'anonymous', 'anonymous') 
        connect.cwd("/geo/platforms")
        subdirectories = subdirectories_[i:i+35]
        for subdirectory in subdirectories:
            try:
               #connect.voidcmd("NOOP")
               command = "MLST "+ str(subdirectory) + "/annot/" #+ (str(subdirectory.split("/")[1])) + ".annot.gz"
               #print connect.sendcmd(command)
               if(connect.sendcmd(command)):
                   #print subdirectory, "\tOK"
                   command = "wget ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/"+ str(subdirectory) + "/annot/" + (str(subdirectory.split("/")[1])) + ".annot.gz"
                   subprocess.check_output(['bash','-c',command])
                   command = "mv " +  (str(subdirectory.split("/")[1])) + ".annot.gz ../../GPL/"
                   subprocess.check_output(['bash','-c',command])
                   command = " gunzip -f ../../GPL/"+ (str(subdirectory.split("/")[1])) + ".annot.gz"
                   subprocess.check_output(['bash','-c',command])
            except ftplib.all_errors:
                #print subdirectory, "\tfail"#, str(connect.connect())[1:3]
                #print connect.connect()
                #print connect.sendcmd(command)
                #pass
                continue
        connect.quit()
        i+=35
        #print str(connect.connect())[:3]
            
            #if( connect.nlst((subdirectory) + "/annot/")):
            #    print subdirectory, "OK"
            #else:
            #    print subdirectory, "NA"
            #liste=connect.nlst(str(subdirectory)
            #if(str(subdirectory) + "/annot") in liste):
       
        
        #if(connect.sendcmd(command)):
        #    print subdirectory, "\tOK"
        #    command = "wget ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/"+ str(subdirectory) + "/annot/" + (str(subdirectory.split("/")[1])) + ".annot.gz"
        #    subprocess.check_output(['bash','-c',command])
        #    command = "mv " +  (str(subdirectory.split("/")[1])) + ".annot.gz GPL/"
        #    subprocess.check_output(['bash','-c',command])
        #    command = " gunzip -f GPL/"+ (str(subdirectory.split("/")[1])) + ".annot.gz"
        #    subprocess.check_output(['bash','-c',command])
                #response = urllib2.urlopen('ftp://'+host+"/geo/platforms/"+str(subdirectory) + "/annot/" + (str(subdirectory.split("/")[1])) + ".annot.gz")
                #compressedFile = StringIO.StringIO()
                #compressedFile.write(response.read())
                #compressedFile.seek(0)
                #decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
    
                #with open(os.path.join('/home/clancien/Desktop/Fichier_Convert/GPL',(str(subdirectory.split("/")[1])) +'.annot'), 'w') as outfile:
                 #   outfile.write(decompressedFile.read())
        #except ftplib.all_errors:
            #print subdirectory, "\tfail"#, str(connect.connect())[1:3]
            #print connect.sendcmd(command)
            #pass

def getSubdir():
    host = "ftp.ncbi.nlm.nih.gov" # adresse du serveur FTP
    connect = ftplib.FTP(host, 'anonymous', 'anonymous') 
    connect.cwd("/geo/platforms")
    listdir=connect.nlst()
    connect.quit()
    return listdir

def loop():
    listdir=getSubdir()#getSubdir()

     #print listdir
    #i=0
    for directory in listdir:
        print directory
        download(directory)
        #i+=1
   # print i
loop()
#response = urllib2.urlopen('ftp://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL10nnn/GPL10239/annot/GPL10239.annot.gz')
#print response
#try:
 #   connect.sendcmd("MLST GPL10nnn/GPL10239/annot/GPL10240.annot.gz")
        #print "ok"
#except ftplib.all_errors,e:
#     print("Do no find file")

#for dir in connect.nlst():
 #   for subdir in connect.nlst(str(dir)):
 #       if ((str(subdir) + "/annot") in connect.nlst(str(subdir))):
 #           response = urllib2.urlopen('ftp://'+host+"/geo/platforms/"+str(subdir) + "/annot/" + (str(subdir.split("/")[1])) + ".annot.gz")
 #           compressedFile = StringIO.StringIO()
 #           compressedFile.write(response.read())
 #           compressedFile.seek(0)
 #           decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

 #           with open(os.path.join('/home/clancien/Desktop/Fichier_Convert/GPL',(str(subdir.split("/")[1])) +'.annot'), 'w') as outfile:
 #               outfile.write(decompressedFile.read())

#connect.quit()
print time.time() - t0, "seconds wall time"
#print connect.nlst()


 #   host = "ftp.ncbi.nlm.nih.gov" # adresse du serveur FTP
 #   connect = ftplib.FTP(host, 'anonymous', 'anonymous') 
 #   connect.cwd("/geo/platforms")
 #   files=[]
 #   connect.retrlines("NLST",files.append)
 #   print len(files)
 #   i=0
 #   print i
    #print files
 #   for file in range(0,len(files)):
        #print files[file]
        #connect.cwd("/geo/platforms/"+str(files[file]))
 #       filesDirectory=[]
 #       connect.retrlines("NLST" + str(files[file]) ,filesDirectory.append)
        #connect.retrlines("NLST",filesDirectory.append)
        #print filesDirectory
 #       for rep in range(0,len(filesDirectory)):
            #connect.cwd("/geo/platforms/"+str(files[file])+"/"+str(filesDirectory[rep]))
 #           filesInDirectory=[]
 #           connect.retrlines("NLST" + str(files[file])+"/"+str(filesDirectory[rep]) ,filesInDirectory.append)
            #print files[file] + "/" + filesDirectory[rep]
 #           if "annot" in filesInDirectory:
               # print "ok"
               # print host+"/geo/platforms/"+str(files[file])+"/"+str(filesDirectory[rep])+ "/" +"annot/" + str(filesDirectory[rep]) + ".annot.gz"
 #               response = urllib2.urlopen('ftp://'+host+"/geo/platforms/"+str(files[file])+"/"+str(filesDirectory[rep])+ "/" +"annot/" + str(filesDirectory[rep]) + ".annot.gz")
 #               compressedFile = StringIO.StringIO()
 #               compressedFile.write(response.read())
 #               compressedFile.seek(0)
 #               decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

 #               with open(os.path.join(GPL_path,(str(filesDirectory[rep]) +'.annot')), 'w') as outfile:
 #                   outfile.write(decompressedFile.read())
 #       i+=1
 #       print i
 #   connect.quit()