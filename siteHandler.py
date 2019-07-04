import os
import subprocess
from classify import classify
import time
import projectProperties

projectProperties.checkFiles()

UPLOAD_FOLDER = projectProperties.details['upload_folder']
ALLOWED_EXTENSIONS = projectProperties.details['allowed_extensions'].split(",")
FEEDBACK_TEXT_FILE = projectProperties.details['feedback_file']

UPLOAD_FOLDER_ABSOLUTE = os.getcwd()+"/"+UPLOAD_FOLDER
while '\\' in UPLOAD_FOLDER_ABSOLUTE:
    UPLOAD_FOLDER_ABSOLUTE = UPLOAD_FOLDER_ABSOLUTE.replace('\\','/')

def getUploadFolder():
    return UPLOAD_FOLDER_ABSOLUTE

def getExtension(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
	return '.' in filename and getExtension(filename) in ALLOWED_EXTENSIONS

def classifyImage(file):
    return classify(file)

def getClassifyHTML(predicitions):
    output = ""
    for prediction in predicitions:
        output+="<li>"+prediction+"</li>\n"
    return output

def getFeedbackHTML(predicitions, imageName):
    output = "<input type='hidden' name='image' value='"+imageName+"'>"
    output += "<select name='select' id='select' onchange='selectChange()' required>\n"
    for prediction in predicitions:
        prediction = prediction.split(":")[0]
        output+="<option value='"+prediction+"'>"+prediction+"</option>\n"
    return output+"<option value='other'>Other</option></select>"

def writeFeedbackToFile(label, image):
    f = open(FEEDBACK_TEXT_FILE, "a+")
    f.write(image+","+label+"\n")
    f.close()