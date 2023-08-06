import requests, time
from pythontools.core import logger, tools

def uploadToHastebin(content):
    url = 'https://hastebin.com'
    data = ""
    if type(content) == str:
        data = content
    elif type(content) == list:
        for i in content:
            data += str(i) + "\n"
    else:
        logger.log("§cError: Please insert string or list!")
        return
    response = requests.post(url + '/documents', data=data.encode('utf-8'))
    return url + '/' + response.json()['key']

logTimes = {}

def startLogTime(name):
    logTimes[name] = time.time()

def endLogTime(name, log=True):
    if name in logTimes:
        convertedTime = convertTime(time.time() - logTimes[name], millis=True)
        if log:
            logger.log("§8[§bTIME§8] §e" + str(name) + " finished in §6" + convertedTime)
        logTimes.pop(name)
        return convertedTime
    else:
        logger.log("§cError: " + str(name) + " not exist!")

convertTime = tools.convertTime  # will be removed in future
getRoundRobinValue = tools.getRoundRobinValue  # will be removed in future