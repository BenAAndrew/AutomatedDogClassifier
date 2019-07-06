import concurrent.futures
import os

#get elevated directory
from ... import projectProperties 

#ToBeDeleted text file path
toBeDeletedFile = "ToBeDeleted.txt"
#dataSet path
dataSetPath = "../"+projectProperties.details['dataset_name']
#max similatenous threads for multithreading
max_similtaneous_threads = 12

toBeDeleted = [line.rstrip('\n') for line in open(toBeDeletedFile)]

def deleteImage(fileName):
        os.remove(dataSetPath+"/"+fileName)
        print(image+" deleted!")

print("Have you run imageChecker.py successfully to build the toBeDeleted file before running this? (y/n)")

if(input().lower() == "y"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_similtaneous_threads) as executor:
                executor.map(deleteImage, toBeDeleted)