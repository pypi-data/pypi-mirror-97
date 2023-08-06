from colorama import init
from colorama import Fore, Back, Style
import time, os, stdiomask
from pythontools.core import tools

init()

logs = []
logPath = ""
logFile = ""
timeFormat = "%H:%M:%S"

def initLogDirectory(path):
    global logFile, logPath
    logPath = path
    logFile = path + "/" + time.strftime("log_%Y_%m_%d_%H_%M_%S", time.localtime()) + ".txt"
    tools.createDirectory(path)
    tools.createFile(logFile)

def setTimeFormat(date, time):
    global timeFormat
    if date and time:
        timeFormat = "%Y/%m/%d %H:%M:%S"
    elif not date and time:
        timeFormat = "%H:%M:%S"
    elif date and not time:
        timeFormat = "%Y/%m/%d"

def getLogByDisplayname(displayname):
    return tools.getFileContent(logPath + "/log_" + displayname.replace("/", "_").replace(":", "_").replace(" ", "_") + ".txt")

def getDisplayname(filename):
    pices = filename.replace("log_", "").replace(".txt", "").split("_")
    return pices[0] + "/" + pices[1] + "/" + pices[2] + " " + pices[3] + ":" + pices[4] + ":" + pices[5]

def getAllLogs():
    list = []
    for filename in os.listdir(logPath):
        list.append(getDisplayname(filename))
    return list

def writeToLogFile(message):
    outLog = "§f" + "[" + time.strftime(timeFormat, time.localtime()) + "] §r" + message
    try: tools.appendToFile(logFile, outLog)
    except: pass

def _replaceColors(message):
    if "§r" in message:
        message = message.replace("§r", Fore.RESET)
    if "§1" in message:
        message = message.replace("§1", Fore.BLUE)
    if "§9" in message:
        message = message.replace("§9", Fore.LIGHTBLUE_EX)
    if "§b" in message:
        message = message.replace("§b", Fore.LIGHTCYAN_EX)
    if "§3" in message:
        message = message.replace("§3", Fore.CYAN)
    if "§4" in message:
        message = message.replace("§4", Fore.RED)
    if "§c" in message:
        message = message.replace("§c", Fore.LIGHTRED_EX)
    if "§6" in message:
        message = message.replace("§6", Fore.YELLOW)
    if "§e" in message:
        message = message.replace("§e", Fore.LIGHTYELLOW_EX)
    if "§a" in message:
        message = message.replace("§a", Fore.LIGHTGREEN_EX)
    if "§2" in message:
        message = message.replace("§2", Fore.GREEN)
    if "§5" in message:
        message = message.replace("§5", Fore.MAGENTA)
    if "§d" in message:
        message = message.replace("§d", Fore.LIGHTMAGENTA_EX)
    if "§f" in message:
        message = message.replace("§f", Fore.WHITE)
    if "§7" in message:
        message = message.replace("§7", Fore.LIGHTWHITE_EX)
    if "§8" in message:
        message = message.replace("§8", Fore.LIGHTBLACK_EX)
    if "§0" in message:
        message = message.replace("§0", Fore.BLACK)
    if "§&" in message:
        if "§&r" in message:
            message = message.replace("§&r", Back.RESET)
        if "§&1" in message:
            message = message.replace("§&1", Back.BLUE)
        if "§&9" in message:
            message = message.replace("§&9", Back.LIGHTBLUE_EX)
        if "§&b" in message:
            message = message.replace("§&b", Back.LIGHTCYAN_EX)
        if "§&3" in message:
            message = message.replace("§&3", Back.CYAN)
        if "§&4" in message:
            message = message.replace("§&4", Back.RED)
        if "§&c" in message:
            message = message.replace("§&c", Back.LIGHTRED_EX)
        if "§&6" in message:
            message = message.replace("§&6", Back.YELLOW)
        if "§&e" in message:
            message = message.replace("§&e", Back.LIGHTYELLOW_EX)
        if "§&a" in message:
            message = message.replace("§&a", Back.LIGHTGREEN_EX)
        if "§&2" in message:
            message = message.replace("§&2", Back.GREEN)
        if "§&5" in message:
            message = message.replace("§&5", Back.MAGENTA)
        if "§&d" in message:
            message = message.replace("§&d", Back.LIGHTMAGENTA_EX)
        if "§&f" in message:
            message = message.replace("§&f", Back.WHITE)
        if "§&7" in message:
            message = message.replace("§&7", Back.LIGHTWHITE_EX)
        if "§&8" in message:
            message = message.replace("§&8", Back.LIGHTBLACK_EX)
        if "§&0" in message:
            message = message.replace("§&0", Back.BLACK)
    if "§!r" in message:
        message = message.replace("§!r", Style.RESET_ALL)
    if "§!b" in message:
        message = message.replace("§!b", Style.BRIGHT)
    return message

def log(message):
    message = "§!r§f[" + time.strftime(timeFormat, time.localtime()) + "] §!r" + message + "§!r"
    logs.append(message)
    try: tools.appendToFile(logFile, message)
    except: pass
    message = _replaceColors(message)
    print(message)

def userInput(message, password=False, strip=True):
    message = "§!r§f[" + time.strftime(timeFormat, time.localtime()) + "] §!r" + message + "§!r"
    message = _replaceColors(message)
    if password is True:
        response = str(stdiomask.getpass(prompt=message))
        return response.strip() if strip is True else response
    else:
        print(message, end="")
        return input().strip() if strip is True else input()