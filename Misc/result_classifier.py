import os
import shutil
import string

path = "../Results/glue_stuff/raw/"
for root, dirs, files in os.walk(path):
    for file in files:
        #print(file)z
        if(root == path): #if files are in the immediate directory, not subdirectories.
            #(if '-data' in )
            fileInfo , _ = file.split("-data")
            fileInfo = fileInfo.rstrip(string.digits) #removing the random code
            fileInfo = fileInfo[:-1] #removing the space
            _ , pdata = fileInfo.split(".txt ")
            cooperation = ''
            
            if('non-coop' in pdata):
                cooperation = 'non-coop '
                _, pdata = pdata.split('non-coop ')
            pdata = float(pdata)
            print(fileInfo)
            pdata = "{0:.4f}".format(pdata)
            print(pdata)
            if not os.path.exists(root+cooperation+pdata): #creating the subirectory if doesn't exits.
                os.makedirs(root+cooperation+pdata)
            
            shutil.move(path + file, path + cooperation + pdata +'/'+ file) #moving the file to it's
                                                              #relevant subdir