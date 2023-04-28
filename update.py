import shutil
from github import Github,GitRelease
import urllib.request
import urllib.error
import zipfile
import configparser
import subprocess
import os

def getCurrentVersion():
    configIni = configparser.ConfigParser()
    configIni.read("./config.ini",encoding="utf-8")
    return configIni["DEFAULT"]["Version"]

def downloadZip(url,savePath):
    try:
        with urllib.request.urlopen(url) as df:
            data = df.read()
            with open(savePath,mode="wb") as f:
                f.write(data)
    except urllib.error.URLError as e:
        print(e)

def writeVersion2ini(version):
    configIni = configparser.ConfigParser()
    configIni.read("./config.ini",encoding="utf-8")
    configIni.set("DEFAULT","Version",version)
    with open("./config.ini","w") as f:
        configIni.write(f)

def deleteTempFile():
    shutil.rmtree("./temp")
    os.remove("tmp.zip")


savePath = "./tmp.zip"

g = Github()
user = g.get_user("Kazuryu0907")
repo = user.get_repo("GBC-S2Ws")

latestRele = repo.get_releases()[0]
latestVersion = latestRele.tag_name
currentVersion = getCurrentVersion()

print(f"[+]Current Version: {currentVersion}")
print(f"[+]Latest Version: {latestVersion}")
if not latestVersion == currentVersion:
    print("[+]Avable Update")
    # assetsのzipファイルのurl
    downloadUrl = latestRele.assets[0].browser_download_url
    print(downloadUrl)
    # DL file
    downloadZip(downloadUrl,savePath)
    # 解凍
    with zipfile.ZipFile(savePath) as z:
        z.extract("GBC-S2Ws/main.exe","./temp/")
        z.extract("GBC-S2Ws/ReleaseNote.txt","./temp/")

    shutil.move("temp/GBC-S2Ws/main.exe","./main.exe")
    shutil.move("temp/GBC-S2Ws/ReleaseNote.txt","./ReleaseNote.txt")
    #Run ReleaseNote
    subprocess.Popen(["notepad.exe","ReleaseNote.txt"])
    #Write new Version
    writeVersion2ini(latestVersion)
    deleteTempFile()

