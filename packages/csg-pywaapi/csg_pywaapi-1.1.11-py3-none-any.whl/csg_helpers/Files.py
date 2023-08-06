import os
import fnmatch

def setupSourceFileList(path,pattern='*.wav'):
    """From a path find and return all files matching the pattern"""
    filelist = []
    for root, dirs, files in os.walk(path):
        # for file in os.listdir(path):
        for filename in fnmatch.filter(files, pattern):
            absFilePath = os.path.abspath(os.path.join(root, filename))
            filelist.append(absFilePath)
    return filelist


def filterSourceFileList(sourcefilelist, filterTerms):
    filteredFileList = []
    for file in sourcefilelist:
        addFile = True
        fileString = str(file)
        for filter in filterTerms:
            if filter.lower() in fileString.lower():
                addFile = False
        if addFile:
            filteredFileList.append(os.path.basename(file))
            # print(file)
    return filteredFileList