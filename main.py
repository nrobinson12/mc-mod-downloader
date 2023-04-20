import curseforge
import modrinth
import util
from variables import *


def getModFile(modName):
    fileName, downloadUrl = curseforge.getModFile(modName)
    if fileName != None and downloadUrl != None:
        return fileName, downloadUrl

    util.log(modName + " not found on curseforge, trying modrinth")

    fileName, downloadUrl = modrinth.getModFile(modName)
    if fileName != None and downloadUrl != None:
        return fileName, downloadUrl

    util.log(modName + " not found on curseforge or modrinth")
    return None, None


def main():
    util.eraseFile(LOG_FILE)

    # backup mods
    modFolder = util.getFromConfig("modFolder")
    util.moveFiles(modFolder, modFolder + "backup/")

    # download all mods
    for modName in util.getFromConfig("mods"):
        fileName, downloadUrl = getModFile(modName)
        if fileName is None or downloadUrl is None:
            continue

        util.downloadFile(downloadUrl, "mods/" + fileName)

    # copy mods to mods folder
    util.copyFiles("mods/", modFolder)


if __name__ == "__main__":
    main()
