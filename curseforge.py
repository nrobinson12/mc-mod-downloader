import os
import requests
import util
from variables import *


CURSEFORGE_API = "https://api.curseforge.com/v1/"
CURSEFORGE_HEADERS = {
    "Accept": "application/json",
    "x-api-key": os.environ["ETERNAL_API_KEY"],
}
MINECRAFT_ID = 432
FABRIC_MOD_LOADER_ID = 4


# function that gets a mod by its name
def getMod(modName):
    params = {"gameId": MINECRAFT_ID, "slug": modName}

    request = requests.get(
        CURSEFORGE_API + "mods/search", params=params, headers=CURSEFORGE_HEADERS
    )

    if request.status_code != 200:
        return None

    request = request.json()

    if not (
        request.get("data")
        and isinstance(request["data"], list)
        and len(request["data"]) > 0
    ):
        return None

    return request["data"][0]


# function that gets the files of a mod by its id
def getModFiles(modId):
    params = {
        "gameVersion": util.getFromConfig("version"),
        "modLoaderType": FABRIC_MOD_LOADER_ID,
    }

    request = requests.get(
        CURSEFORGE_API + "mods/" + str(modId) + "/files",
        params=params,
        headers=CURSEFORGE_HEADERS,
    )

    if request.status_code != 200:
        return None

    request = request.json()

    if not (
        request.get("data")
        and isinstance(request["data"], list)
        and len(request["data"]) > 0
    ):
        return None

    files = sorted(request["data"], key=lambda file: file["fileDate"], reverse=True)
    files = sorted(files, key=lambda file: file["releaseType"])
    return files


def getModFile(modName):
    mod = getMod(modName)
    if mod is None:
        return None, None

    files = getModFiles(mod["id"])
    if files is None:
        return None, None

    return files[0]["fileName"], files[0]["downloadUrl"]
