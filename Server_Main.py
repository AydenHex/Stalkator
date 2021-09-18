import pandas as pd
from datetime import date
import threading
import socket
import os
import time

from FileLib import *
import Interface

def CompileReports(reportName):
        tabTmp = ParseFile('MainReport.txt')
        tab_abon1 = tabTmp[0]; tab_abon2 = tabTmp[1]
        tabTmp = ParseFile(reportName)
        tab_abon12 = tabTmp[0]; tab_abon22 = tabTmp[1]

        for i in range(len(tab_abon12)):
            if(tab_abon12[i] not in tab_abon1):
                tab_abon1.append(tab_abon12[i])

        for i in range(len(tab_abon22)):
            if(tab_abon22[i] not in tab_abon2):
                tab_abon2.append(tab_abon22[i])

        MakeFile('MainReport.txt', tab_abon1, tab_abon2)

        follow = {'Followers': tab_abon2, 'Following': tab_abon1}
        df = pd.DataFrame.from_dict(follow, orient='index').transpose()
        df.to_csv(str(date.today())+'.csv')

        os.remove(reportName)

def DownloadFile(self, dirPath):
        fileSize = int(self.clientsocket.recv(2048).decode())
        dataSize = 0
        with open(dirPath+'Report'+self.ip+'.txt', 'wb') as file:
            while dataSize < fileSize:
                data = self.clientsocket.recv(4096)
                dataSize += len(data)
                file.write(data)
            file.close()
            print("[%s]: Report received !" % (self.ip))

class ClientThread(threading.Thread):
    
        def __init__(self, ip, port, clientsocket):
            threading.Thread.__init__(self)
            self.ip = ip
            self.port = port
            self.clientsocket = clientsocket
            self.scrapeBool = False
            self.scrapeType = 0
            self.running = True
            print("\n[+] Connection of %s %s" % (self.ip, self.port))

        def run(self):
            while(self.running):
                if(self.scrapeBool):
                    self.clientsocket.sendall((str('StartScraping_')+str(self.scrapeType)+interface.targetUsername).encode())
                    DownloadFile(self, os.getcwd()+'\\')
                    while(interface.IsWorking): time.sleep(1)
                    CompileReports('Report'+self.ip+'.txt')
                    print("[%s]: Reports compiled" % (self.ip))
                    self.scrapeBool = False
            self.clientsocket.sendall(str('Quit').encode())
            print("[%s]: Client disconnected..." % (self.ip))
        
class ServerThread(threading.Thread):
    
        def __init__(self, port):
            threading.Thread.__init__(self)
            self.running = True
            self.port = port

        def run(self):
            tcpSvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM = TCP/SOCK_DGRAM = UDP #AF_INET = IPv4/AF_INET6 = IPv6
            tcpSvr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcpSvr.bind(("", self.port)) #Associe le port 1111 au programme (Socket)
            while(self.running):
                tcpSvr.listen(10)
                print( "\nServer: Listening...")
                (clientsocket, (ip, port)) = tcpSvr.accept()
                newthread = ClientThread(ip, port, clientsocket)
                interface.tab_Client.append(newthread)
                newthread.daemon = True
                newthread.start()
            print('Server: Shutdown sucessfull !')

 # Main
interface = Interface.Interface()
interface.serverThread = ServerThread(1111)
interface.serverThread.start()
interface.mainloop()
