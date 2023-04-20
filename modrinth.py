import requests
import util


MODRINTH_API = "https://api.modrinth.com/v2/"


def getModFiles(modName):
    params = {
        "game_versions": '["' + util.getFromConfig("version") + '"]',
        "loaders": '["fabric"]',
    }

    request = requests.get(
        MODRINTH_API + "project/" + modName + "/version", params=params
    )

    if request.status_code != 200:
        return None

    request = request.json()

    if not (isinstance(request, list) and len(request) > 0):
        return None

    RELEASE_ORDER = {
        "release": 0,
        "beta": 1,
        "alpha": 2,
    }
    files = sorted(request, key=lambda file: file["date_published"], reverse=True)
    files = sorted(files, key=lambda file: RELEASE_ORDER[file["version_type"]])
    return files


def getModFile(modName):
    files = getModFiles(modName)
    if files is None:
        return None, None

    file = files[0]
    if not (
        file.get("files") and isinstance(file["files"], list) and len(file["files"]) > 0
    ):
        return None, None

    file = file["files"][0]

    return file["filename"], file["url"]
