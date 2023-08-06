CrawlerCodePythonTools - Documentation
======================================

Tools for python by CrawlerCode.

    - Source Code: https://github.com/CrawlerCode/PythonTools
    - PyPi: https://pypi.org/project/CrawlerCodePythonTools

Installation
============

::

    pip install CrawlerCodePythonTools

Config
======

.. code:: python

    from pythontools.core import config

    cfg = config.Config(path="", default_config={"config_data_1": "value_123"})
    cfgData = cfg.getConfig()

    # get config value
    print(cfgData["config_data_1"])

    # chang value and save config
    cfgData["config_data_1"] = "value_456"
    cfg.saveConfig()

Logger
======

.. code:: python

    from pythontools.core import logger

    # path to logs directory (optional)
    logger.initLogDirectory("logs")

    # set time format (optional)
    logger.setTimeFormat(date=True, time=True)

    # print color test
    logger.log("§1Blue §9Light-Blue §3Cyan §bLight-Cyan §4Red §cLight-Red §6Yellow §eLight-Yellow §2Green §aLight-Green §5Magenta §dLight-Magenta §fWhite §7Light-Gray §8Gray §0Black")



Server and Client (sockets)
===========================

    Server

.. code:: python

    from pythontools.sockets import server
    from threading import Thread

    SERVER = server.Server(password="PASSWORD")

    def ON_CLIENT_CONNECT(client):
        # send a message to client on connect by clientSocket
        SERVER.sendTo(client["clientSocket"], {"METHOD": "HELLO"})

    def ON_CLIENT_DISCONNECT(client):
        pass

    def ON_RECEIVE(client, data):
        METHOD = data["METHOD"]

    SERVER.ON_CLIENT_CONNECT(ON_CLIENT_CONNECT)
    SERVER.ON_CLIENT_DISCONNECT(ON_CLIENT_DISCONNECT)
    SERVER.ON_RECEIVE(ON_RECEIVE)

    Thread(target=SERVER.start, args=["HOST-IP", 15749]).start()

    # send a message to client by clientID
    SERVER.sendToClient("MY_CLIENT_ID", {"METHOD": "TEST", "mydata": "123"})
..

    Client

.. code:: python

    from pythontools.sockets import client
    from threading import Thread

    CLIENT = client.Client(password="PASSWORD", clientID="MY_CLIENT_ID", clientType="CLIENT")

    def ON_CONNECT():
        pass

    def ON_RECEIVE(data):
        METHOD = data["METHOD"]
        # recipe the test message
        if METHOD == "TEST":
            print("test:", data["mydata"])

    CLIENT.ON_CONNECT(ON_CONNECT)
    CLIENT.ON_RECEIVE(ON_RECEIVE)

    Thread(target=CLIENT.connect, args=["HOST-IP", 15749]).start()


WebBot
===========

    Download chromedriver or geckodriver
        - https://chromedriver.chromium.org/downloads
        - https://github.com/mozilla/geckodriver/releases

.. code:: python

    from pythontools.webbot import webbot

    # Google Chrome
    browser = webbot.WebBot().Chrome(chromedriver="chromedriver.exe")
    # Firefox
    browser = webbot.WebBot().Firefox(geckodriver="geckodriver.exe")
    browser.get("https://www.google.com/")

    browser.input('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input', "what is python?")
    browser.click('//*[@id="tsf"]/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]')

    time.sleep(10)

    browser.close()
