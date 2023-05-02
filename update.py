import shutil
from github import Github
import urllib.request
import urllib.error
import zipfile
import configparser
import subprocess
import os
from rich.console import Console

class Updater:
    def __init__(self,console:Console) -> None:
        self.console = console
        self.savePath = "./tmp.zip"
        g = Github()
        user = g.get_user("Kazuryu0907")
        repo = user.get_repo("GBC-S2Ws")

        self.latestRele = repo.get_releases()[0]
        self.latestVersion = self.latestRele.tag_name
        self.currentVersion = self.getCurrentVersion()

    def getIntVersion(self,version:str):
        return int(version[1:].replace(".",""))
    
    def getLatestVersion(self):
        return self.latestVersion
    
    def getCurrentVersion(self):
        configIni = configparser.ConfigParser()
        configIni.read("./config.ini",encoding="utf-8")
        return configIni["DEFAULT"]["Version"]

    def downloadZip(self,url,savePath):
        try:
            with urllib.request.urlopen(url) as df:
                data = df.read()
                with open(savePath,mode="wb") as f:
                    f.write(data)
        except urllib.error.URLError as e:
            print(e)

    def writeVersion2ini(self,version):
        configIni = configparser.ConfigParser()
        configIni.read("./config.ini",encoding="utf-8")
        configIni.set("DEFAULT","Version",version)
        with open("./config.ini","w") as f:
            configIni.write(f)

    def deleteTempFile(self):
        shutil.rmtree("./temp")
        os.remove("tmp.zip")

    def update(self):
        self.console.print(f"[cyan][+]Current Version: {self.currentVersion}")
        self.console.print(f"[cyan][+]Latest Version: {self.latestVersion}")
        if not self.latestVersion == self.currentVersion:
            self.console.print("[cyan][+]Avable Update")
            # assetsのzipファイルのurl
            downloadUrl = self.latestRele.assets[0].browser_download_url
            # DL file
            self.console.print("[cyan][+]Downloading new Files...")
            self.downloadZip(downloadUrl,self.savePath)
            # 解凍
            self.console.print("[cyan][+]Unpacking Files...")
            with zipfile.ZipFile(self.savePath) as z:
                z.extract("GBC-S2Ws/GBC-S2Ws.exe","./temp/")
                z.extract("GBC-S2Ws/ReleaseNote.txt","./temp/")
            self.console.print("[red][-]Removing Temp Files...")
            shutil.move("temp/GBC-S2Ws/GBC-S2Ws.exe","./GBC-S2Ws.exe")
            shutil.move("temp/GBC-S2Ws/ReleaseNote.txt","./ReleaseNote.txt")
            #Run ReleaseNote
            subprocess.Popen(["notepad.exe","ReleaseNote.txt"])
            #Write new Version
            self.writeVersion2ini(self.latestVersion)
            self.deleteTempFile()


if __name__ == "__main__":
    u = Updater(Console())
    u.update()