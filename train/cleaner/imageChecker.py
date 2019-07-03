import subprocess
import concurrent.futures
import os

#min accuracy in %
minAccuracy = 20
#max similatenous threads for multithreading
max_similtaneous_threads = 12
#text recording to be deleted list 
toBeDeleted = dict()

#ToBeDeleted text file path
toBeDeletedFile = "ToBeDeleted.txt"
#dataSet path
dataSetPath = "../dataset"
#class were checking for
classToBeChecked = "dog"

def checkImage(folder, image):
        command = "./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights "+dataSetPath+"/"+folder+"/"+image
        check = subprocess.check_output(command.split(" "))
        outputtedLines = check.decode("utf-8").split("\n")
        del outputtedLines[0]
        del outputtedLines[len(outputtedLines)-1]
        for line in outputtedLines:
                if classToBeChecked in line:
                        accuracy = line.split(':')[1]
                        accuracy = int(accuracy[0:len(accuracy)-1])
                        if(accuracy > minAccuracy):
                                return True
        print(outputtedLines)
        return False

def checkImagesInFolder(folder):
        filesToDeletedInThisFolder = list()
        for image in os.listdir("../data/"+folder):
                imageValid = checkImage(folder, image)
                if not imageValid:
                        filesToDeletedInThisFolder.append(image)
        toBeDeleted[folder] = filesToDeletedInThisFolder

def writeToBeDeletedTextFile():
        f = open(toBeDeletedFile,"w")
        for folder in toBeDeleted:
                if len(toBeDeleted[folder]) > 0:
                        f.write(folder+";\n\n")
                        for image in toBeDeleted[folder]:
                                f.write(image+"\n")
                        f.write("\n")
        f.close()
        
folders = os.listdir(dataSetPath)
for i in range(0, len(folders)):
        while " " in folders[i]:
                folders[i] = folders[i].replace(" ","$")  
        while "$" in folders[i]:
                folders[i] = folders[i].replace("$","\ ")

if __name__ == "__main__":
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_similtaneous_threads) as executor:
                executor.map(checkImagesInFolder, folders)

print("TOTAL TO BE DELETED;")
for folder in toBeDeleted:
        print(folder+": "+str(len(toBeDeleted[folder])))

writeToBeDeletedTextFile()