from pythontools.core import logger, events
import socket, json, base64, traceback, math
from threading import Thread
from pythontools.dev import crypthography, dev

class Server:

    def __init__(self, password):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.password = password
        self.clientSocks = []
        self.clients = []
        self.seq = base64.b64encode(self.password.encode('ascii')).decode("utf-8")
        self.packagePrintBlacklist = []
        self.packagePrintBlacklist.append("ALIVE")
        self.packagePrintBlacklist.append("ALIVE_OK")
        self.maxClients = 10
        self.printUnsignedData = True
        self.uploadError = False
        self.eventScope = "global"
        self.enabled_encrypt = False
        self.secret_key = b''
        self.enabled_whitelist_mac = False
        self.enabled_whitelist_ip = False
        self.whitelisted_ips = []
        self.whitelisted_macs = []

    def enableEncrypt(self, secret_key):
        self.enabled_encrypt = True
        if type(secret_key) == str: secret_key = bytes(secret_key, "utf-8")
        if type(secret_key) != bytes: secret_key = b''
        self.secret_key = secret_key

    def enableWhitelistIp(self, ips:list):
        self.enabled_whitelist_ip = True
        self.whitelisted_ips = ips

    def enableWhitelistMac(self, macs:list):
        self.enabled_whitelist_mac = True
        self.whitelisted_macs = macs

    def start(self, host, port):
        if self.enabled_encrypt is True:
            if self.secret_key == b'':
                self.secret_key = crypthography.generateSecretKey()
                logger.log("§8[§eSERVER§8] §aSecret-Key generated: " + self.secret_key.decode("utf-8"))
                return
        logger.log("§8[§eSERVER§8] §6Starting...")
        try:
            self.serverSocket.bind((host, port))
            self.serverSocket.listen(self.maxClients)
            logger.log("§8[§eSERVER§8] §aListening on §6" + str((host, port)))
        except Exception as e:
            logger.log("§8[§eSERVER§8] §8[§cERROR§8] §cFailed: " + str(e))
            return
        def clientTask(clientSocket, address):
            logger.log("§8[§eSERVER§8] §aClient connected from §6" + str(address))
            error = False
            if self.enabled_whitelist_ip is True:
                if address[0] not in self.whitelisted_ips:
                    error = True
                    logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cIp-Address §6'" + str(address[0]) + "'§c not whitelisted!")
            lastData = ""
            while error is False:
                try:
                    recvData = clientSocket.recv(32768)
                    recvData = str(recvData, "utf-8")
                    if recvData != "":
                        if not recvData.startswith("{") and (recvData.endswith("}" + self.seq) or (lastData + recvData).endswith("}" + self.seq)):
                            if lastData != "":
                                recvData = lastData + recvData
                                if self.printUnsignedData:
                                    logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cUnsigned data repaired")
                        elif not recvData.endswith("}" + self.seq):
                            lastData += recvData
                            if self.printUnsignedData:
                                logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cReceiving unsigned data: §r" + recvData)
                            continue
                        if "}" + self.seq + "{" in recvData:
                            recvDataList = recvData.split("}" + self.seq + "{")
                            recvData = "["
                            for i in range(len(recvDataList)):
                                if self.enabled_encrypt is True:
                                    recvData += crypthography.decrypt(self.secret_key, base64.b64decode((recvDataList[i][1:] if i == 0 else recvDataList[i]).replace("}" + self.seq, "").encode('ascii'))).decode("utf-8")
                                    if i + 1 < len(recvDataList):
                                        recvData += ", "
                                else:
                                    recvData += recvDataList[i].replace(self.seq, "")
                                    if i + 1 < len(recvDataList):
                                        recvData += "}, {"
                            recvData += "]"
                            lastData = ""
                        elif "}" + self.seq in recvData:
                            if self.enabled_encrypt is True:
                                recvData = "[" + crypthography.decrypt(self.secret_key, base64.b64decode(recvData.replace("}" + self.seq, "")[1:].encode('ascii'))).decode("utf-8") + "]"
                            else:
                                recvData = "[" + recvData.replace(self.seq, "") + "]"
                            lastData = ""
                        try:
                            recvData = json.loads(recvData)
                        except:
                            logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cReceiving broken data: §r" + str(recvData))
                            continue
                        for data in recvData:
                            if data["METHOD"] == "ALIVE":
                                self.sendTo(clientSocket, {"METHOD": "ALIVE_OK"})
                            elif data["METHOD"] == "AUTHENTICATION":
                                logger.log("§8[§eSERVER§8] §r[IN] " + data["METHOD"])
                                if data["PASSWORD"] == self.password:
                                    if self.enabled_whitelist_mac is True:
                                        if "MAC" not in data:
                                            error = True
                                            self.sendTo(clientSocket, {"METHOD": "AUTHENTICATION_FAILED"})
                                            logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cNo MAC are given!")
                                        elif data["MAC"] not in self.whitelisted_macs:
                                            error = True
                                            self.sendTo(clientSocket, {"METHOD": "AUTHENTICATION_FAILED"})
                                            logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cMAC §6'" + str(data["MAC"]) + "'§c not whitelisted!")
                                    if error is False:
                                        for c in self.clients:
                                            if c["clientID"] == data["CLIENT_ID"]:
                                                self.sendTo(clientSocket, {"METHOD": "AUTHENTICATION_FAILED"})
                                                error = True
                                                break
                                    if error is False:
                                        client = {"clientSocket": clientSocket, "clientID": data["CLIENT_ID"], "clientType": data["CLIENT_TYPE"]}
                                        self.clients.append(client)
                                        self.sendTo(clientSocket, {"METHOD": "AUTHENTICATION_OK"})
                                        logger.log("§8[§eSERVER§8] §aClient '" + data["CLIENT_ID"] + "' authenticated §6('" + data["MAC"] + "')")
                                        events.call("ON_CLIENT_CONNECT", client, scope=self.eventScope)
                                else:
                                    self.sendTo(clientSocket, {"METHOD": "AUTHENTICATION_FAILED"})
                                    error = True
                                    break
                            else:
                                client = self.getClient(clientSocket)
                                if client is not None:
                                    if data["METHOD"] not in self.packagePrintBlacklist:
                                        logger.log("§8[§eSERVER§8] §r[IN] " + data["METHOD"])
                                    events.call("ON_RECEIVE", client, data, scope=self.eventScope)
                                else:
                                    logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cReceiving not authenticated package: §r" + data["METHOD"])
                except Exception as e:
                    if "Connection reset by peer" in str(e) or "Connection timed out" in str(e) or "Bad file descriptor" in str(e): break
                    if self.uploadError is True:
                        try:
                            link = dev.uploadToHastebin(traceback.format_exc())
                            logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cException: §4" + str(e) + " §r" + str(link))
                        except: logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cException: §4" + str(e))
                    else: logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cException: §4" + str(e))
                    break
            p = True
            for client in self.clients:
                if client["clientSocket"] == clientSocket:
                    events.call("ON_CLIENT_DISCONNECT", client, scope=self.eventScope)
                    logger.log("§8[§eSERVER§8] §6Client '" + client["clientID"] + "' disconnected")
                    self.clients.remove(client)
                    p = False
            try: self.clientSocks.remove(clientSocket)
            except: pass
            try: clientSocket.close()
            except: pass
            if p is True: logger.log("§8[§eSERVER§8] §6Client " + str(address) + " disconnected")

        while True:
            (client, clientAddress) = self.serverSocket.accept()
            client.settimeout(120)
            self.clientSocks.append(client)
            Thread(target=clientTask, args=[client, clientAddress]).start()

    def ON_CLIENT_CONNECT(self, function):
        events.registerEvent(events.Event("ON_CLIENT_CONNECT", function, scope=self.eventScope))

    def ON_CLIENT_DISCONNECT(self, function):
        events.registerEvent(events.Event("ON_CLIENT_DISCONNECT", function, scope=self.eventScope))

    def ON_RECEIVE(self, function):
        events.registerEvent(events.Event("ON_RECEIVE", function, scope=self.eventScope))

    def addPackageToPrintBlacklist(self, package):
        self.packagePrintBlacklist.append(package)

    def getClient(self, clientSocket):
        for client in self.clients:
            if client["clientSocket"] == clientSocket:
                return client
        return None

    def sendToAll(self, message):
        for sSock in self.clientSocks:
            self.sendTo(sSock, message)

    def sendTo(self, sock, data):
        try:
            send_data = json.dumps(data)
            if self.enabled_encrypt is True:
                send_data = "{" + base64.b64encode(crypthography.encrypt(self.secret_key, send_data)).decode('utf-8') + "}"
            send_data = bytes(send_data + self.seq, "utf-8")
            #if len(send_data) > 65536:
            #    for i in range(math.ceil(len(send_data)/65536)):
            #        sock.send(send_data[65536*i:][:65536])
            #else:
            #    sock.send(send_data)
            sock.send(send_data)
            if data["METHOD"] not in self.packagePrintBlacklist:
                logger.log("§8[§eSERVER§8] §r[OUT] " + data["METHOD"])
        except Exception as e:
            logger.log("§8[§eSERVER§8] §8[§cWARNING§8] §cFailed to send data: " + str(e))
            if e == BrokenPipeError or "Broken pipe" in str(e):
                p = True
                for client in self.clients:
                    if client["clientSocket"] == sock:
                        events.call("ON_CLIENT_DISCONNECT", client, scope=self.eventScope)
                        logger.log("§8[§eSERVER§8] §6Client '" + client["clientID"] + "' disconnected")
                        self.clients.remove(client)
                        p = False
                try: self.clientSocks.remove(sock)
                except: pass
                try: sock.close()
                except: pass
                if p is True: logger.log("§8[§eSERVER§8] §6Client disconnected")

    def sendToClientID(self, clientID, data):
        for client in self.clients:
            if client["clientID"] == clientID:
                self.sendTo(clientID["clientSocket"], data)

    def close(self):
        self.serverSocket.close()
        logger.log("§8[§eSERVER§8] §6Closed")

