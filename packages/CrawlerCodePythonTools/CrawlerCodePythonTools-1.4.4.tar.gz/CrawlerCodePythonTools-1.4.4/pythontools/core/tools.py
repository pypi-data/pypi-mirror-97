import random, json, os, shutil

def getFileContent(path, asBytes=False, asLines=True):
    if asBytes is True:
        with open(path, 'rb') as file:
            content = file.read()
        return content
    else:
        with open(path, 'r', encoding='utf-8') as file:
            if asLines is True:
                content = file.readlines()
            else:
                content = file.read()
        if asLines is True:
            return [line.replace("\n", "").replace("\r", "") for line in content]
        else:
            return content

def getLineFromFile(path, line):
    content = getFileContent(path)
    if len(content) > line:
        return content[line]
    return None

def getRandomLineFromFile(path):
    content = getFileContent(path)
    return content[random.randint(0, len(content) - 1)]

def appendToFile(path, text, nextLine=True):
    with open(path, 'a', encoding='utf-8') as file:
        file.write(text + ("\n" if nextLine else ""))

def writeToFile(path, content):
    if type(content) is bytes:
        with open(path, 'wb') as file:
            file.write(content)
    else:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

def createFile(path):
    file = open(path, "w", encoding='utf-8')
    file.close()

def createDirectory(path):
    try: os.makedirs(path)
    except:pass

def clearFile(path):
    file = open(path, "w", encoding='utf-8')
    file.close()

def existFile(path):
    return os.path.isfile(path)

def existDirectory(path):
    return os.path.isdir(path)

def copyFile(file, dir_path):
    if os.path.isdir(file):
        createDirectory(dir_path + "\\" + os.path.basename(file))
        for f in os.listdir(file):
            copyFile(file + "\\" + f, dir_path + "\\" + os.path.basename(file))
    else:
        shutil.copyfile(file, dir_path + "\\" + os.path.basename(file))

def removeFile(path):
    os.remove(path)

def removeDirectory(path):
    os.removedirs(path)

def clearDirectory(path):
    for f in os.listdir(path):
        if os.path.isdir(path + "\\" + f):
            clearDirectory(path + "\\" + os.path.basename(f))
        else:
            removeFile(path + "\\" + f)

def loadJson(path):
    with open(path, "r", encoding='utf-8') as json_data:
        data = json.load(json_data)
        json_data.close()
        return data

def saveJson(path, data, indent=None):
    with open(path, "w", encoding='utf-8') as json_data:
        json.dump(data, json_data, indent=indent)
        json_data.close()

def convertTime(seconds, millis=False, millisDecimalPlaces=10):
    sec = seconds
    min = 0
    h = 0
    days = 0
    while sec >= 60:
        min += 1
        sec -= 60
    while min >= 60:
        h += 1
        min -= 60
    while h >= 24:
        days += 1
        h -= 24
    if days > 0:
        return str(days) + "d " + str(h) + "h"
    if h > 0:
        return str(h) + "h " + str(min) + "m"
    if min > 0:
        if millis:
            return str(min) + "m " + str(round(sec, millisDecimalPlaces)) + "s"
        return str(min) + "m " + str(int(sec)) + "s"
    if millis:
        return str(round(sec, millisDecimalPlaces)) + "s"
    return str(int(sec)) + "s"

round_robin_indices = {}

def getRoundRobinValue(list):
    if id(list) not in round_robin_indices:
        round_robin_indices[id(list)] = 0
    if len(list) >= 0:
        if round_robin_indices[id(list)] >= len(list):
            round_robin_indices[id(list)] = 0
        round_robin_indices[id(list)] += 1
        return list[round_robin_indices[id(list)]-1]
    return None