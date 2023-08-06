from pythontools.core import tools
from pythontools.dev import crypthography
import os, json

cfg = None

class Config(object):

    def __init__(self, path="", default_config={}):
        self.path = path
        self.default_config = default_config
        if "%APPDATA%" in self.path:
            self.path = self.path.replace("%APPDATA%", str(os.getenv("APPDATA")))
        if not tools.existDirectory(self.path):
            tools.createDirectory(self.path)
        self.reloadConfig()

    def reloadConfig(self):
        if not tools.existFile(self.path + "config.json"):
            tools.createFile(self.path + "config.json")
            tools.saveJson(self.path + "config.json", self.default_config, indent=4)
        self.config = tools.loadJson(self.path + "config.json")
        global cfg
        cfg = self

    def getConfig(self):
        return self.config

    def saveConfig(self):
        tools.saveJson(self.path + "config.json", self.config, indent=4)

class EncryptedConfig(object):

    def __init__(self, secret_key, path="", default_config={}):
        self.secret_key = secret_key
        self.path = path
        self.default_config = default_config
        if "%APPDATA%" in self.path:
            self.path = self.path.replace("%APPDATA%", str(os.getenv("APPDATA")))
        if not tools.existDirectory(self.path):
            tools.createDirectory(self.path)
        self.reloadConfig()

    def reloadConfig(self):
        if not tools.existFile(self.path + "config.cfg"):
            tools.createFile(self.path + "config.cfg")
            encrypted = crypthography.encrypt(self.secret_key, json.dumps(self.default_config))
            tools.writeToFile(self.path + "config.cfg", encrypted)
        decrypted = crypthography.decrypt(self.secret_key, tools.getFileContent(self.path + "config.cfg", asBytes=True))
        self.config = json.loads(decrypted.decode("utf-8"))
        global cfg
        cfg = self

    def getConfig(self):
        return self.config

    def saveConfig(self):
        encrypted = crypthography.encrypt(self.secret_key, json.dumps(self.config))
        tools.writeToFile(self.path + "config.cfg", encrypted)

def setConfig(config):
    global cfg
    cfg = config

def getConfig():
    global cfg
    return cfg