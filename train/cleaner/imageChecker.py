import subprocess
import concurrent.futures
import os

#min accuracy in %
minAccuracy = 20
#max similatenous threads for multithreading
max_similtaneous_threads = 1
#text recording to be deleted list 
toBeDeleted = dict()
#log of classifications for vertification
log = list()

#classify log
logFile = "../log.txt"
#ToBeDeleted text file path
toBeDeletedFile = "../ToBeDeleted.txt"
#dataSet path
dataSetPath = "../../dataset"
#class were checking for
classToBeChecked = "dog"
#yolo model
yoloModel = "yolov3.weights"
#yolo config
yoloConfig = "cfg/yolov3.cfg"

def checkImage(folder, image):
        command = ["./darknet","detect",yoloConfig,yoloModel,dataSetPath+"/"+folder+"/"+image]
        print(command)
        check = subprocess.check_output(command)
        outputtedLines = check.decode("utf-8").split("\n")
        del outputtedLines[0]
        del outputtedLines[len(outputtedLines)-1]
        log.append(folder+"/"+image+": "+str(outputtedLines))
        for line in outputtedLines:
                if classToBeChecked in line:
                        accuracy = line.split(':')[1]
                        accuracy = int(accuracy[0:len(accuracy)-1])
                        if(accuracy > minAccuracy):
                                return True
        return False

def checkImagesInFolder(folder):
        filesToDeletedInThisFolder = list()
        for image in os.listdir(dataSetPath+"/"+folder):
                imageValid = checkImage(folder, image)
                if not imageValid:
                        filesToDeletedInThisFolder.append(image)
        toBeDeleted[folder] = filesToDeletedInThisFolder

def writeToBeDeletedTextFile():
        f = open(toBeDeletedFile,"w")
        for folder in toBeDeleted:
                if len(toBeDeleted[folder]) > 0:
                        #f.write(folder+";\n\n")
                        for image in toBeDeleted[folder]:
                                f.write(image+"\n")
                        #f.write("\n")
        f.close()

def writeLog():
        f = open(logFile,"w") 
        for msg in log:
                f.write(msg+"\n")
        f.close()
        
folders = os.listdir(dataSetPath)[2:3]
print(folders)

if __name__ == "__main__":
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_similtaneous_threads) as executor:
                executor.map(checkImagesInFolder, folders)

print("TOTAL TO BE DELETED;")
for folder in toBeDeleted:
        print(folder+": "+str(len(toBeDeleted[folder])))

writeToBeDeletedTextFile()
writeLog()