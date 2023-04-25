import glob
import os
from rapidfuzz.process import extract

class SimilaryFile:
    def __init__(self,path:str) -> None:
        files = glob.glob(path)
        self.fileNames = list(map(lambda f:os.path.basename(f).split(".")[0],files))
        self.nameFileTable = {f"{n}":f for (f,n) in list(zip(files,self.fileNames))}
        self.fileNamesEx = list(map(lambda f:os.path.basename(f),files))

    def getSimilaryPath(self,query:str):
        similary = extract(query,self.fileNames,limit=10)
        mostSimilaryName = list(similary[0])[0]
        self.sims = similary
        return self.nameFileTable[mostSimilaryName]
