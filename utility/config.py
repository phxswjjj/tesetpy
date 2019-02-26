import os.path as opath

def readFirstLine(filename):
    resDir = 'res'
    filepath = opath.join(resDir, filename)
    if opath.isfile(filepath):
        with open(filepath, 'r') as reader:
            while True:
                content = reader.readline()
                if not content:
                    break
                content = content.strip()
                if len(content) > 0:
                    return content.strip()