import os
import urllib.request
import configparser

config = configparser.ConfigParser()
configName = "modelDetails.ini"
config.read(configName)

details = dict()
for key in config:
    for prop in config[key]:
        details[prop] = config[key][prop]

def downloadModel():
    print("Downloading model")
    urllib.request.urlretrieve(details['modelurl'], details['model'])
    print("Downloaded model")

def downloadLabels():
    print("Downloading labels")
    urllib.request.urlretrieve(details['labelsurl'], details['labels'])
    print("Downloaded labels")

def checkFiles():
    if details['model'] not in os.listdir('./'):
        downloadModel()
    else:
        print("Model found")

    if details['labels'] not in os.listdir('./'):
        downloadLabels()
    else:
        print("Labels found")