from pythontools.core import events
from pythontools.sockets import server, client
from threading import Thread

class Relay:

    def __init__(self, password):
        self.password = password
        self.relayServer = server.Server(password=self.password)
        self.clients = []
        self.relayServerEncrypt = False
        self.serverClientEncrypt = False
        self.relayServer_secret_key = b''
        self.serverClient_secret_key = b''

    def enableRelayServerEncrypt(self, secret_key):
        self.relayServerEncrypt = True
        if type(secret_key) == str: secret_key = bytes(secret_key, "utf-8")
        if type(secret_key) != bytes: secret_key = b''
        self.relayServer_secret_key = secret_key

    def enableServerClientEncrypt(self, secret_key):
        self.serverClientEncrypt = True
        if type(secret_key) == str: secret_key = bytes(secret_key, "utf-8")
        if type(secret_key) != bytes: secret_key = b''
        self.serverClient_secret_key = secret_key

    def start(self, relayHost, relayPort, serverHost, serverPort):
        def ON_CLIENT_CONNECT(relayClient):
            serverClient = client.Client(password=self.password, clientID=relayClient["clientID"], clientType=relayClient["clientType"])
            serverClient.eventScope = relayClient["clientID"]

            def ON_RECEIVE(data):
                self.relayServer.sendTo(relayClient["clientSocket"], data)

            events.registerEvent(events.Event("ON_RECEIVE", ON_RECEIVE, scope=serverClient.eventScope))

            if self.serverClientEncrypt is True: serverClient.enableEncrypt(self.serverClient_secret_key)
            serverClient.printUnsignedData = False
            Thread(target=serverClient.connect, args=[serverHost, serverPort]).start()
            self.clients.append({"relayClient": relayClient, "serverClient": serverClient})

        def ON_CLIENT_DISCONNECT(client):
            for c in self.clients:
                if c["relayClient"] == client:
                    c["serverClient"].disconnect()
                    self.clients.remove(c)
            for event in events.events:
                if event.name == "ON_RECEIVE" and event.scope == client["clientID"]:
                    events.unregisterEvent(event)

        def ON_RECEIVE(client, data):
            for c in self.clients:
                if c["relayClient"] == client:
                    c["serverClient"].send(data)

        events.registerEvent(events.Event("ON_CLIENT_CONNECT", ON_CLIENT_CONNECT))
        events.registerEvent(events.Event("ON_CLIENT_DISCONNECT", ON_CLIENT_DISCONNECT))
        events.registerEvent(events.Event("ON_RECEIVE", ON_RECEIVE))
        if self.relayServerEncrypt is True: self.relayServer.enableEncrypt(self.relayServer_secret_key)
        self.relayServer.printUnsignedData = False
        Thread(target=self.relayServer.start, args=[relayHost, relayPort]).start()