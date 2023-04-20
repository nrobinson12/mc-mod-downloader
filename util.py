import json
import os
import shutil
import urllib.request
from variables import *


# function to print a json variable to a file in a pretty format
def printJsonToFile(jsonVar, fileName):
    with open(fileName, "w") as f:
        f.write(json.dumps(jsonVar, indent=4, sort_keys=True))


# function to get a json variable from a file, and return the value of a key parameter
def getFromConfig(key):
    with open("config.json", "r") as f:
        return json.load(f)[key]


# append string to log
def log(string):
    with open(LOG_FILE, "a") as f:
        f.write(string + "\n")


# erase contents of file
def eraseFile(fileName):
    with open(fileName, "w") as f:
        f.write("")


# function to download file from url
def downloadFile(url, fileName):
    if DEBUG:
        log("downloading " + url + " to " + fileName)
        return

    # check if file already exists
    try:
        with open(fileName, "r") as f:
            return
    except FileNotFoundError:
        pass

    urllib.request.urlretrieve(url, fileName)


# move all files from one directory to another
def moveFiles(fromDir, toDir):
    doToFiles(fromDir, toDir, shutil.move)


# copy all files from one directory to another
def copyFiles(fromDir, toDir):
    doToFiles(fromDir, toDir, shutil.copy)


def doToFiles(fromDir, toDir, func):
    for file in os.listdir(fromDir):
        # make sure file is not a directory
        if os.path.isdir(fromDir + file):
            continue

        # check if dir exists
        if not os.path.exists(toDir):
            os.makedirs(toDir)

        if DEBUG:
            log(func.__name__ + " " + file + " to " + toDir)
            continue

        func(fromDir + file, toDir + file)
